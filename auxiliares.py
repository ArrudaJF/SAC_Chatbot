import pandas as pd
import os
from dotenv import load_dotenv


def consultar_pedidos(numero_pedido:int):
    
    pedidos = pd.read_csv('data/desafio_tecnico_ai_eng - orders.csv')
    
    # Retorna o status ou uma mensagem de erro em formato de string (ou JSON)
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

