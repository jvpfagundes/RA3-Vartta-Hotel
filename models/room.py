from typing import Optional
from pydantic import BaseModel, Field
from .category import Category
from .guest import Guest

class Room(BaseModel):
    """
    Função/Classe: Room
    Params:
    Descrição: Modelo representando um quarto de hotel e seu status de ocupação atual.
    Returns:
    """
    number: int = Field(..., gt=0, description="Número identificador do quarto")
    category: Category = Field(..., description="Categoria associada a este quarto")
    is_occupied: bool = Field(default=False, description="Status de ocupação do quarto")
    guest: Optional[Guest] = Field(default=None, description="Hóspede atualmente alocado no quarto")
