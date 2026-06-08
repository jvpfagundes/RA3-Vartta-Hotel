import random
import math
from datetime import datetime
import state.database as db
from ui.helpers import obter_inteiro, obter_confirmacao

def realizar_checkout() -> bool:
    """
    Função/Classe: realizar_checkout
    Params:
    Descrição: Orquestra o fechamento da conta de um hóspede e liberação do quarto.
    Returns: bool se a operação funcionou ou não
    """
    print("\n--- CHECK-OUT E FECHAMENTO DE CONTA ---")
    
    n_quarto = obter_inteiro("Digite o número do quarto para check-out: ")
    if n_quarto not in db.quartos:
        print("Erro: Quarto não cadastrado.")
        return False
        
    quarto = db.quartos[n_quarto]
    if not quarto.is_occupied or not quarto.guest:
        print("Erro: Este quarto já está desocupado.")
        return False

    hospede = quarto.guest
    categoria = quarto.category

    subtotal_diarias = categoria.daily_rate * hospede.days
    subtotal_extras = hospede.extra_costs
    subtotal_geral = subtotal_diarias + subtotal_extras

    percentual_desconto = 0.0
    if random.random() < 0.20:
        percentual_desconto = random.choice([0.05, 0.10, 0.15])
        print(f"\nPARABÉNS! Hóspede contemplado no Sorteio de Fidelidade!")
        print(f"Ganhou {percentual_desconto * 100:.0f}% de desconto sobre o valor das diárias!")
    
    desconto_calculado = subtotal_diarias * percentual_desconto
    valor_com_desconto = subtotal_geral - desconto_calculado

    taxa_iss = valor_com_desconto * 0.05
    taxa_iss_final = math.ceil(taxa_iss * 100) / 100

    total_a_pagar = valor_com_desconto + taxa_iss_final

    data_hora_saida = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print("\n" + "=" * 50)
    print("             NOTA FISCAL DE SAÍDA ")
    print("=" * 50)
    print(f" Hóspede:           {hospede.name}")
    print(f" Quarto Ocupado:     Nº {quarto.number} ({categoria.name})")
    print(f" Estadia Efetiva:    {hospede.days} dia(s)")
    print(f" Valor Diária:       R$ {categoria.daily_rate:.2f}")
    print("-" * 50)
    print(f" Subtotal Diárias:   R$ {subtotal_diarias:.2f}")
    print(f" Consumos Extras:    R$ {subtotal_extras:.2f}")
    print(f" Desconto Sorteio:  -R$ {desconto_calculado:.2f} ({percentual_desconto*100:.0f}%)")
    print(f" Taxa ISS (5%):      R$ {taxa_iss_final:.2f} (arredondado)")
    print("-" * 50)
    print(f" VALOR TOTAL A PAGAR: R$ {total_a_pagar:.2f}")
    print(f" Data/Hora Saída:    {data_hora_saida}")
    print("=" * 50)

    if not obter_confirmacao("Confirmar recebimento do pagamento e check-out? (S/N): "):
        print("Operação de check-out cancelada. Quarto permanece ocupado.")
        return False

    db.faturamento_diario += total_a_pagar
    
    transacao = {
        "quarto": quarto.number,
        "hospede": hospede.name,
        "dias": hospede.days,
        "categoria": categoria.name,
        "total_diarias": subtotal_diarias,
        "total_extras": subtotal_extras,
        "desconto": desconto_calculado,
        "iss": taxa_iss_final,
        "total_pago": total_a_pagar,
        "data_saida": data_hora_saida
    }
    db.historico_hospedes.append(transacao)

    quarto.is_occupied = False
    quarto.guest = None

    print(f"\nCheck-out finalizado! Quarto {quarto.number} liberado e disponível para novos hóspedes.")
    return True
