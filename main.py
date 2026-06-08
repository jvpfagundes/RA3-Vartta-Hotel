import sys
import state.database as db
from services.admin_service import (
    inicializar_hotel,
    adicionar_nova_categoria,
    mostrar_mapa_quartos,
    visualizar_estoque
)
from services.checkin_service import realizar_checkin
from services.consumption_service import registrar_consumo_frigobar, registrar_consumo_lazer
from services.checkout_service import realizar_checkout
from services.file_service import salvar_relatorio_fechamento_txt, salvar_backup_estado_json
from ui.screens import exibir_introducao, exibir_menu_principal, exibir_fim_expediente
from ui.helpers import obter_inteiro, obter_confirmacao

def main():
    """
    Função/Classe: main
    Params:
    Descrição: Função principal do sistema. Orquestra submódulos e funções.
    Returns:
    """
    exibir_introducao()
    inicializar_hotel()
    sistema_aberto = True
    
    while sistema_aberto:
        try:
            exibir_menu_principal()
            opcao = obter_inteiro("Selecione a ação desejada (1 a 8): ", min_val=1, max_val=8)
            
            if opcao == 1:
                realizar_checkin()
            elif opcao == 2:
                registrar_consumo_frigobar()
            elif opcao == 3:
                registrar_consumo_lazer()
            elif opcao == 4:
                realizar_checkout()
            elif opcao == 5:
                mostrar_mapa_quartos()
            elif opcao == 6:
                visualizar_estoque()
            elif opcao == 7:
                adicionar_nova_categoria()
            elif opcao == 8:
                print("\nSolicitação de fechamento do hotel recebida.")
                if obter_confirmacao("Tem certeza que deseja encerrar o expediente de hoje? (S/N): "):
                    print("\nEncerrando as operações...")
                    salvar_relatorio_fechamento_txt()
                    salvar_backup_estado_json()
                    
                    exibir_fim_expediente(db.faturamento_diario, len(db.historico_hospedes))
                    
                    sistema_aberto = False
                else:
                    print("Retornando ao painel principal do hotel...")
            
            if sistema_aberto:
                print("\nPressione [ENTER] para continuar...")
                input()
                
        except KeyboardInterrupt:
            print("\n\nSalvando dados antes de forçar o fechamento...")
            salvar_relatorio_fechamento_txt()
            salvar_backup_estado_json()
            sys.exit(0)

if __name__ == "__main__":
    main()
