# ------------------------------- Importación de librerías necesarias
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
# -------------------------------------------------------------------

gen_1 = pd.read_csv('gen_1.csv')
lista_buscar = gen_1[76:151]

def scrapeo_que_te_veo (lista):
    
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
        
        datos = sopa_poke.find_all("td" , {'class' : 'roundy' , 'colspan' : '2'}) 
        
        lista_limpia = []
        
        for dato in datos:
            
            dato = dato.getText().split('\n')
            lista_limpia.extend(dato)
        
        lista_limpia = [dato for dato in datos if dato != '']
        
        # ¿Probar mejor a coger todos los elementos en negrita?
        datos2 = sopa_poke.find_all("b") 
        
        # Comparación de ambos métodos:
        print(lista_limpia)
        print(datos2)
        
        break
    
scrapeo_que_te_veo (lista_buscar)