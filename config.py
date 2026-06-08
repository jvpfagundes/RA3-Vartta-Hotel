"""
este arquivo é utilizado para salvar as constantes do sistema na memória global
"""


LIMITE_QUARTOS = 20

CATEGORIAS_PADRAO = {
    "Standard": 150.00,
    "Luxo": 280.00,
    "Suíte": 500.00
}

QTD_PADRAO_CATEGORIAS = {
    "Standard": 5,
    "Luxo": 3,
    "Suíte": 2
}

PRODUTOS_PADRAO = {
    "Água Mineral": {"preco": 6.00, "estoque": 50, "is_fisico": True},
    "Refrigerante": {"preco": 8.00, "estoque": 30, "is_fisico": True},
    "Cerveja Artesanal": {"preco": 14.00, "estoque": 20, "is_fisico": True},
    "Batata Chips": {"preco": 10.00, "estoque": 25, "is_fisico": True}
}

SERVICOS_PADRAO = {
    "Lavanderia Expressa": {"preco": 35.00, "estoque": 0, "is_fisico": False},
    "Massagem Terapêutica": {"preco": 120.00, "estoque": 0, "is_fisico": False},
    "Jantar Gourmet Quarto": {"preco": 85.00, "estoque": 0, "is_fisico": False},
    "Acesso SPA Completo": {"preco": 60.00, "estoque": 0, "is_fisico": False}
}

ARQUIVO_RELATORIO_TXT = "relatorio_fechamento.txt"
ARQUIVO_ESTADO_JSON = "estado_hotel.json"
