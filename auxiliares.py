import pandas as pd
from pypdf import PdfReader


def consultar_politica(num_paginas:list[int]):
    
    reader = PdfReader('./data/políticas_da_loja.pdf')
    system_file = reader.pages[0].extract_text() + '\n'

    for i in num_paginas:
        system_file += reader.pages[i].extract_text() + '\n'
    
    return system_file

def consultar_pedidos(numero_pedido:int):
    
    pedidos = pd.read_csv('data/desafio_tecnico_ai_eng - orders.csv')
    
    
    return pedidos[pedidos['order_id'] == numero_pedido].to_json(orient="records")

def consultar_produtos():
    return pd.read_csv('data/desafio_tecnico_ai_eng - products.csv').to_json(orient="records")
    

def consultar_categorias():
   return pd.read_csv('data/desafio_tecnico_ai_eng - categories.csv').to_json(orient="records")


def consultar_clientes():
    return pd.read_csv('data/desafio_tecnico_ai_eng - customers.csv').to_json(orient="records")


def consultar_itens():
    return pd.read_csv('data/desafio_tecnico_ai_eng - order_items.csv').to_json(orient="records")


def consultar_promocoes():
    return pd.read_csv('data/desafio_tecnico_ai_eng - promotions.csv').to_json(orient="records")

