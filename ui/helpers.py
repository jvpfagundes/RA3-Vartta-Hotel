import sys
import time
from typing import Optional

def efeito_digitacao(texto: str, delay: float = 0.02):
    """
    Função/Classe: efeito_digitacao
    Params: texto: string que será printada
            delay: float do tamanho do delay em segundos
    Descrição: Exibe um texto com um efeito elegante de digitação simulada.
    Returns:
    """
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def obter_string(prompt: str, min_len: int = 1, max_len: int = 100) -> str:
    """
    Função/Classe: obter_string
    Params: prompt: string com o que será printado no input.
            min_len: int de número minímo de caracteres
            max_len: int de número máximo de caracteres
    Descrição: Garante que a entrada do usuário seja uma string limpa e não vazia.
    Returns: string tratada
    """
    while True:
        entrada = input(prompt).strip()
        if min_len <= len(entrada) <= max_len:
            return entrada
        print(f"Entrada inválida! Digite um texto contendo entre {min_len} e {max_len} caracteres.")

def obter_inteiro(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Função/Classe: obter_inteiro
    Params: prompt: string com o que será printado no input.
            min_val: int do valor mínimo que o usuário pode digitar
            max_val: int do valor máximo que o usuário pode digitar.
    Descrição: Garante que o usuário digite um inteiro válido dentro dos limites definidos.
    Returns: int tratado do input.
    """
    while True:
        try:
            valor = int(input(prompt).strip())
            if min_val is not None and valor < min_val:
                print(f"O número deve ser maior ou igual a {min_val}.")
                continue
            if max_val is not None and valor > max_val:
                print(f"O número deve ser menor ou igual a {max_val}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida! Por favor, digite um número inteiro válido.")

def obter_float(prompt: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """
    Função/Classe: obter_float
    Params: prompt: string com o que será printado no input.
            min_val: float do valor mínimo que o usuário pode digitar
            max_val: float do valor mínimo que o usuário pode digitar
    Descrição: Garante que o usuário digite um número float válido dentro dos limites.
    Returns: float tratado do input
    """
    while True:
        try:
            valor = float(input(prompt).strip().replace(",", "."))
            if min_val is not None and valor < min_val:
                print(f"O valor deve ser maior ou igual a {min_val:.2f}.")
                continue
            if max_val is not None and valor > max_val:
                print(f"O valor deve ser menor ou igual a {max_val:.2f}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida! Por favor, digite um valor monetário/decimal válido (ex: 150.50).")

def obter_confirmacao(prompt: str) -> bool:
    """
    Função/Classe: obter_confirmacao
    Params: prompt: string com o que será printado no input.
    Descrição: Solicita uma confirmação de Sim ou Não do usuário.
    Returns: bool correspondente a entrada do usuário
    """
    while True:
        entrada = input(prompt).strip().lower()
        if entrada in ['s', 'sim', 'y', 'yes']:
            return True
        if entrada in ['n', 'nao', 'não', 'no']:
            return False
        print("Por favor, responda com [S] para Sim ou [N] para Não.")
