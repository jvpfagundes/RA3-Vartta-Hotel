from datetime import datetime
import state.database as db
from models import Guest
from ui.helpers import obter_string, obter_inteiro

def realizar_checkin() -> bool:
    """
    Função/Classe: realizar_checkin
    Params:
    Descrição: Orquestra o fluxo de check-in de um hóspede em um quarto vago.
    Returns: bool se o processo de checkin foi concluído
    """
    print("\n--- NOVO CHECK-IN ---")
    
    if not db.quartos:
        print("Erro: Não há quartos configurados no hotel no momento.")
        return False

    nome = obter_string("Digite o nome completo do hóspede: ", min_len=2, max_len=80)
    dias = obter_inteiro("Digite a quantidade de diárias reservadas: ", min_val=1)

    print("\nCategorias disponíveis:")
    categorias_lista = list(db.categorias.keys())
    for idx, cat_nome in enumerate(categorias_lista, 1):
        cat = db.categorias[cat_nome]
        print(f" [{idx}] {cat.name} - Diária: R$ {cat.daily_rate:.2f}")
    
    escolha_idx = obter_inteiro("Escolha o número da categoria desejada: ", min_val=1, max_val=len(categorias_lista))
    categoria_escolhida = db.categorias[categorias_lista[escolha_idx - 1]]

    quarto_vago = None
    for n_quarto, qto in db.quartos.items():
        if qto.category.name == categoria_escolhida.name and not qto.is_occupied:
            quarto_vago = qto
            break

    if not quarto_vago:
        print(f"\nDesculpe, não há quartos vagos da categoria '{categoria_escolhida.name}' no momento.")
        return False

    novo_hospede = Guest(name=nome, days=dias)
    quarto_vago.is_occupied = True
    quarto_vago.guest = novo_hospede

    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print("\n" + "=" * 50)
    print("           COMPROVANTE DE CHECK-IN ")
    print("=" * 50)
    print(f" Nome do Hóspede:  {novo_hospede.name}")
    print(f" Quarto Alocado:   Nº {quarto_vago.number} ({categoria_escolhida.name})")
    print(f" Diárias:          {novo_hospede.days} dia(s)")
    print(f" Valor da Diária:  R$ {categoria_escolhida.daily_rate:.2f}")
    print(f" Data/Hora Entrada: {data_hora_atual}")
    print("=" * 50)
    print("Check-in realizado com sucesso!")
    return True
