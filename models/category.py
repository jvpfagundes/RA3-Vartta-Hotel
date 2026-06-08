from pydantic import BaseModel, Field

class Category(BaseModel):
    """
    Função/Classe: Category
    Params: 
    Descrição: Classe pydantic utilizada para a categoria. Cria objetos tipados para cada categoria.
    Returns:
    """
    name: str = Field(..., min_length=2, max_length=50, description="Nome da categoria de quarto")
    daily_rate: float = Field(..., gt=0, description="Preço cobrado pela diária nesta categoria")
