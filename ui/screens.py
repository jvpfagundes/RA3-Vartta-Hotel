import os
import time

def limpar_tela():
    """
    Função/Classe: limpar_tela
    Params:
    Descrição: Limpa a tela do console de forma compatível com Windows e Linux/Mac.
    Returns:
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_introducao():
    """
    Função/Classe: exibir_introducao
    Params:
    Descrição: Função utilizada para exibir a introdução do projeto no terminal.
    Returns:
    """
    limpar_tela()
    print("=" * 60)
    print("        BEM-VINDO AO VARTTA HOTEL SIMULATOR")
    print("=" * 60)
    print("Este é o sistema inteligente de gestão de expediente do hotel.")
    print("Como administrador, você será responsável por:")
    print("  1. Configurar os quartos e tarifas do dia.")
    print("  2. Controlar a entrada e saída de hóspedes (Check-in / Check-out).")
    print("  3. Gerenciar o frigobar de cada quarto.")
    print("  4. Lançar o consumo de serviços de lazer (SPA, Lavanderia, etc.).")
    print("  5. Encerrar o dia de forma segura exportando relatórios fiscais.")
    print("-" * 60)
    print("O sistema foi projetado com blindagem contra erros de digitação.")
    print("Pressione [ENTER] para iniciar o processo de configuração inicial...")
    input()

def exibir_menu_principal():
    """
    Função/Classe: exibir_menu_principal
    Params:
    Descrição: Exibe as opções do painel de desenvolvimento no terminal.
    Returns:
    """
    print("\n" + "=" * 60)
    print("                   PAINEL DE CONTROLE CLI ")
    print("=" * 60)
    print(" [1] Efetuar Check-in (Hospedar Cliente)")
    print(" [2] Lançar Consumo de Frigobar (Produtos Físicos)")
    print(" [3] Lançar Consumo de Lazer (Serviços Adicionais)")
    print(" [4] Efetuar Check-out (Faturamento e Recibo)")
    print(" [5] Mostrar Mapa de Ocupação dos Quartos")
    print(" [6] Visualizar Estoque do Frigobar")
    print(" [7] Adicionar Nova Categoria de Quarto")
    print(" [8] Encerrar Expediente e Fechar Hotel (Fim)")
    print("-" * 60)

def exibir_fim_expediente(total_faturado: float, num_atendimentos: int):
    """
    Função/Classe: exibir_fim_expediente
    Params: total_faturado: float, representa quanto foi faturado no dia
            num_atendimentos: int, representa quantos atendimentos foram realizados no dia
    Descrição: Exibe a tela de fechamento de caixa e encerramento do expediente.
    Returns:
    """
    limpar_tela()
    print("=" * 60)
    print("         FECHANDO HOTEL - ENCERRANDO EXPEDIENTE ")
    print("=" * 60)
    print("Gerando o relatório financeiro...")
    time.sleep(1)
    print("Salvando movimentações diárias no arquivo 'relatorio_fechamento.txt'...")
    time.sleep(1)
    print("-" * 60)
    print(f"Receita Total Bruta Gerada: R$ {total_faturado:.2f}")
    print(f"Total de Estadias Encerradas com Sucesso: {num_atendimentos}")
    print("-" * 60)
    print("Sistema encerrado com segurança. Obrigado por utilizar nosso software!")
    print("=" * 60)
