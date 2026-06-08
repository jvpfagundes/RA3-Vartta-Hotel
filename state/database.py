"""
este arquivo é utilizado como nosso banco de dados.
cada variável aqui representa uma "tabela". Os itens são salvos de maneira tipada
em seus objetos correspondentes.
"""

from typing import Dict, List, Any
from models import Room, Category, Item



quartos: Dict[int, Room] = {}

categorias: Dict[str, Category] = {}

estoque_produtos: Dict[str, Item] = {}

historico_hospedes: List[Dict[str, Any]] = []

faturamento_diario: float = 0.0
