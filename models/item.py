from pydantic import BaseModel, Field

class Item(BaseModel):
    """
    Função/Classe: Item
    Params:
    Descrição: Classe pydantic utilizada para o item. Cria objetos tipados para cada item.
    Returns:
    """
    name: str = Field(..., min_length=2, description="Nome do produto ou serviço")
    price: float = Field(..., gt=0, description="Preço unitário")
    stock: int = Field(default=0, ge=0, description="Quantidade em estoque (usado se for físico)")
    is_physical: bool = Field(default=True, description="Indica se é um produto físico com estoque limitado")
