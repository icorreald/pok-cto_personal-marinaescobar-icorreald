# ------------------------------- Importación de librerías necesarias
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
# -------------------------------------------------------------------

gen_1 = pd.read_csv('gen_1.csv')
lista_buscar = gen_1[75:151]

def scrapeo_que_te_veo (lista):
    
    generacion = {'I' : 1,
                  'II' : 2,
                  'III' : 3,
                  'IV' : 4,
                  'V' : 5,
                  'VI' : 6,
                  'VII' : 7,
                  'VIII' : 8,
                  'IX' : 9}
    
    pokedex_2 = {'pokedex' : [], 
                 'nombre': [],
                 'generacion': [], 
                 'tipo1': [], 
                 'tipo2': [], 
                 'habilidad-especial1': [], 
                 'habilidad-especial2': [], 
                 'egg-group1': [], 
                 'egg-group2': [], 
                 'nivel-de-evolucion': [], 
                 'forma-regional': [], 
                 'legendario': []}
    
    
    for poke in lista['Poke_Name']:
        
        url_poke = f'https://bulbapedia.bulbagarden.net/wiki/{poke}_(Pokémon)'
        
        res_poke = requests.get(url_poke)
        
        if res_poke.status_code != 200:
            print(f"Ha habido un error del tipo {res_poke.status_code}")
        
        sopa_poke = BeautifulSoup(res_poke.content, 'html.parser')
        
        # Captura el número de registro en la Pokédex
        poke_num = sopa_poke.find_all("td" , style='text-align: left')
        poke_num = [dato.text for dato in poke_num]
        poke_num = re.search(r'0*(\d+)', poke_num[0])
        poke_num = int(poke_num[1])-1
        
        # Guarda el registro en el diccionario
        pokedex_2['pokedex'].append(poke_num)
        
        # Captura la generación, el nombre del Pokémon y si es legendario
        nombre_gen = sopa_poke.find('p')
        nombre_gen = [dato.text for dato in nombre_gen]
        nombre = nombre_gen[0]

        gen = [dato for i, dato in enumerate(nombre_gen) if 'introduced' in nombre_gen[i-1]]
        gen = gen[0].replace('Generation ', '')
        gen = generacion[gen]
        
        legendario = [dato for dato in nombre_gen if 'mythical' in dato.lower() or 'legendary' in dato.lower()]
        
        # Guarda los registros en el diccionario
        pokedex_2['nombre'].append(nombre.lower())
        pokedex_2['generacion'].append(gen)
        if legendario:
            pokedex_2['legendario'].append(True)
        else:
            pokedex_2['legendario'].append(False)
        
        # Captura los datos generales del Pokémon
        datos_poke = sopa_poke.find_all("td" , {'class' : 'roundy'}) 
        
        # Limpia los datos
        datos_poke = [dato.text for dato in datos_poke]
        lista_datos = []
        for dato in datos_poke:
            dato = dato.split("\n")
            lista_datos.extend(dato)
        lista_datos = [dato for dato in lista_datos if dato != '']
        
        # Itera por cada uno de los elementos y guarda aquellos que son relevantes en el diccionario
        for i , dato in enumerate(lista_datos):
            
            # Encuentra el tipo o tipos del pokémon
            if re.search('^types$', dato.lower()) or re.search('^type$' , dato.lower()):
                pokedex_2['tipo1'].append(lista_datos[i+1].lower())
                
                if lista_datos[i+2].lower() == 'unknown':
                    pokedex_2['tipo2'].append(np.nan)
                
                else:
                    pokedex_2['tipo2'].append(lista_datos[i+2].lower())
            
            # Encuentra las abilidades del pokémon
            if re.search('^abilities$' , dato.lower()) or re.search('^ability$' , dato.lower()):
                
                if 'or' in lista_datos[i+1]:
                    abilidades = lista_datos[i+1].split('or ')
                   
                    if len(abilidades) > 1:
                        pokedex_2['habilidad-especial1'].append(abilidades[0].replace('\xa0' , '').lower().strip())
                        pokedex_2['habilidad-especial2'].append(abilidades[1].rstrip(nombre).strip().lower())
                    else:
                        pokedex_2['habilidad-especial1'].append(abilidades[0].replace('\xa0' , '').rstrip(nombre).lower().strip())
                        pokedex_2['habilidad-especial2'].append(np.nan)
                else: 
                    pokedex_2['habilidad-especial1'].append(lista_datos[i+1].rstrip(nombre).lower().strip())
                    pokedex_2['habilidad-especial2'].append(np.nan)
            
            # Encuentra el grupo-huevo del pokémon        
            if 'egg group' in dato.lower():
                
                if 'and' in lista_datos[i+1]:
                    grupos = lista_datos[i+1].split('and')
                    pokedex_2['egg-group1'].append(grupos[0].replace('\xa0' , '').lower().strip())
                    pokedex_2['egg-group2'].append(grupos[1].lower().strip())
                    
                else:
                    pokedex_2['egg-group1'].append(lista_datos[i+1].lower())
                    pokedex_2['egg-group2'].append(np.nan)
        
        # Comprueba si el pokémon tiene forma regional
        regional = [dato for dato in lista_datos if 'galarian' in dato.lower() or 'alolan' in dato.lower()]       
        if regional:
            pokedex_2['forma-regional'].append(True)
        else:
            pokedex_2['forma-regional'].append(False)
            
        # Captura los datos de la evolución del pokémon
        datos_evolucion = sopa_poke.find_all("div", style='max-width:100%; text-align:center;') 
        datos_evolucion = [dato.text for dato in datos_evolucion]
        
        # Limpieza datos evolución
        lista_evo = []
        for dato in datos_evolucion:
            dato = dato.split("\n")
            lista_evo.extend(dato)
        lista_evo = [dato for dato in lista_evo if dato != '']
        
        # Comprueba el nivel de evolución del pokémon
        first = [dato for dato in lista_evo if 'first' in dato.lower()]
        second = [dato for dato in lista_evo if 'second' in dato.lower()]
        
        if second:
            pokedex_2['nivel-de-evolucion'].append(2)
        elif first:
            pokedex_2['nivel-de-evolucion'].append(1)
        else:
            pokedex_2['nivel-de-evolucion'].append(0)
    
    return pokedex_2
    
pokedex = scrapeo_que_te_veo (lista_buscar)

pokedex_df = pd.DataFrame(pokedex)

pokedex_df.to_csv('pokedex_gen_1-2.csv' , index = False)


