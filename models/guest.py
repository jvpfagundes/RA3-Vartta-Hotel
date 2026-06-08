from pydantic import BaseModel, Field

class Guest(BaseModel):
    """
    Função/Classe: Guest
    Params:
    Descrição: Modelo representando os dados do hóspede alocado em um quarto.
    Returns:
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do hóspede")
    days: int = Field(..., ge=1, description="Quantidade de dias que permanecerá hospedado")
    extra_costs: float = Field(default=0.0, ge=0, description="Gastos extras acumulados (Frigobar e Lazer)")
