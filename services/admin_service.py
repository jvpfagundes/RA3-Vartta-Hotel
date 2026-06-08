import os
import sys
import state.database as db
from models import Category, Room, Item
from config import (CATEGORIAS_PADRAO, PRODUTOS_PADRAO, SERVICOS_PADRAO, LIMITE_QUARTOS, QTD_PADRAO_CATEGORIAS,
                    ARQUIVO_ESTADO_JSON)
from ui.helpers import obter_string, obter_float, obter_inteiro, obter_confirmacao
from services.file_service import carregar_backup_estado_json

def inicializar_hotel():
    """
    Função/Classe: inicializar_hotel
    Params:
    Descrição: Função utilizada para inicializar as variáveis do hotel (como os produtos, categorias, etc).
    Returns:
    """


    if os.path.exists(ARQUIVO_ESTADO_JSON):
        while True:
            print("\n" + "=" * 60)
            print("             CONFIGURAÇÃO DE INICIALIZAÇÃO")
            print("=" * 60)
            print(" Detectamos um estado anterior salvo em JSON.")
            print(" Como deseja prosseguir?")
            print("\n [1] Retornar de onde paramos (Carregar JSON)")
            print(" [2] Iniciar um novo expediente (Configuração Inicial)")
            print(" [3] Sair do sistema")
            print("-" * 60)
            
            opcao = obter_inteiro("Selecione a ação desejada (1 a 3): ", min_val=1, max_val=3)
            
            if opcao == 1:
                if carregar_backup_estado_json():
                    print("\nInicialização concluída! Pressione [ENTER] para entrar no painel administrativo...")
                    input()
                    return
                else:
                    print("\nErro ao carregar o backup. Retornando ao menu de inicialização...")
            elif opcao == 2:
                if obter_confirmacao("Atenção: Iniciar um novo expediente apagará o estado anterior. Continuar? (S/N): "):
                    break
                else:
                    print("\nRetornando ao menu de inicialização...")
            elif opcao == 3:
                print("\nEncerrando o sistema...")
                sys.exit(0)
    
    for nome, rate in CATEGORIAS_PADRAO.items():
        db.categorias[nome] = Category(name=nome, daily_rate=rate)

    for nome, dados in PRODUTOS_PADRAO.items():
        db.estoque_produtos[nome] = Item(name=nome, price=dados["preco"], stock=dados["estoque"], is_physical=dados["is_fisico"])

    for nome, dados in SERVICOS_PADRAO.items():
        db.estoque_produtos[nome] = Item(name=nome, price=dados["preco"], stock=0, is_physical=dados["is_fisico"])

    print("\n--- INICIALIZAÇÃO E CONFIGURAÇÃO OPERACIONAL ---")
    print(f"O hotel suporta um limite de até {LIMITE_QUARTOS} quartos no total.")
    
    inicializar_quartos()
    
    print("\nInicialização concluída! Pressione [ENTER] para entrar no painel administrativo...")
    input()


def inicializar_quartos():
    """
    Função/Classe: inicializar_quartos
    Params:
    Descrição: Realiza a inicialização dos quartos (configuração personalizada ou padrão).
    Returns:
    """
    if obter_confirmacao("Deseja realizar a configuração personalizada de quartos hoje? (S/N): "):
        print("\nDefina a quantidade de quartos para cada categoria cadastrada:")
        total_quartos_adicionados = 0
        quarto_n = 101

        for cat_nome, cat_obj in db.categorias.items():
            max_permitido = LIMITE_QUARTOS - total_quartos_adicionados
            if max_permitido <= 0:
                print("Limite máximo de quartos atingido!")
                break
                
            qtd = obter_inteiro(
                f"Quantos quartos da categoria '{cat_nome}' (Máx {max_permitido}): ", 
                min_val=0, 
                max_val=max_permitido
            )
            
            for _ in range(qtd):
                db.quartos[quarto_n] = Room(number=quarto_n, category=cat_obj)
                quarto_n += 1
            total_quartos_adicionados += qtd
            
        print(f"\nConfiguração salva! {total_quartos_adicionados} quartos ativados.")
    else:
        print("\nAplicando configuração padrão do hotel (10 quartos ativados):")

        contador = 101
        for cat_nome, cat_obj in db.categorias.items():
            qtd = QTD_PADRAO_CATEGORIAS[cat_nome]
            for _ in range(qtd):
                db.quartos[contador] = Room(number=contador, category=cat_obj)
                contador += 1
                
        print("Configuração rápida carregada: 5 Standard, 3 Luxo, 2 Suítes.")


def adicionar_nova_categoria() -> bool:
    """
    Função/Classe: adicionar_nova_categoria
    Params:
    Descrição: Permite ao administrador criar uma nova categoria de quarto dinamicamente.
    Returns: booleano representando se a operação foi bem suceedida ou não.
    """
    print("\n--- CADASTRAR NOVA CATEGORIA ---")
    nome = obter_string("Digite o nome da nova categoria (ex: Presidencial): ", min_len=2, max_len=30)
    
    if nome.lower() in [c.lower() for c in db.categorias.keys()]:
        print("Erro: Já existe uma categoria com este nome.")
        return False
        
    diaria = obter_float("Digite o valor da diária para esta categoria (R$): ", min_val=1.0)

    nova_cat = Category(name=nome, daily_rate=diaria)
    db.categorias[nome] = nova_cat
    
    print(f"\nCategoria '{nome}' com diária de R$ {diaria:.2f} cadastrada com sucesso!")
    return True

def mostrar_mapa_quartos():
    """
    Função/Classe: mostrar_mapa_quartos
    Params:
    Descrição: Exibe um mapa visual de ocupação de todos os quartos no terminal.
    Returns:
    """
    print("\n" + "=" * 55)
    print("             MAPA DE OCUPAÇÃO DO HOTEL")
    print("=" * 55)
    
    if not db.quartos:
        print("Nenhum quarto configurado.")
        print("=" * 55)
        return

    print(f"{'QUARTO':<8} | {'CATEGORIA':<12} | {'STATUS':<9} | {'HÓSPEDE ATIVO':<20}")
    print("-" * 55)
    
    for num, qto in sorted(db.quartos.items()):
        status_texto = "OCUPADO" if qto.is_occupied else "LIVRE"
        hospede_nome = qto.guest.name if qto.guest else "-"
        print(f"Quarto {num:03d} | {qto.category.name:<12} | {status_texto:<9} | {hospede_nome:<20}")
        
    print("=" * 55)

def visualizar_estoque():
    """
    Função/Classe: visualizar_estoque
    Params:
    Descrição: Exibe uma tabela com o estoque de frigobar e catálogo de serviços.
    Returns:
    """
    print("\n" + "=" * 55)
    print("           CATÁLOGO E ESTOQUE DE PRODUTOS ")
    print("=" * 55)
    print(f"{'PRODUTO/SERVIÇO':<25} | {'PREÇO':<10} | {'ESTOQUE':<12}")
    print("-" * 55)
    
    for nome, item in db.estoque_produtos.items():
        tipo_texto = f"{item.stock} un" if item.is_physical else "Lazer (Ilimitado)"
        print(f"{item.name:<25} | R$ {item.price:<7.2f} | {tipo_texto:<12}")
        
    print("=" * 55)
