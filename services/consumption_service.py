import state.database as db
from ui.helpers import obter_inteiro

def registrar_consumo_frigobar() -> bool:
    """
    Função/Classe: registrar_consumo_frigobar
    Params:
    Descrição: Registra a compra de um item físico do frigobar pelo hóspede de um quarto.
    Returns: bool se a operação funcionou ou não.
    """
    print("\n--- CONSUMO DE FRIGOBAR ---")
    
    n_quarto = obter_inteiro("Digite o número do quarto: ")
    if n_quarto not in db.quartos:
        print("Erro: Quarto não cadastrado.")
        return False
        
    quarto = db.quartos[n_quarto]
    if not quarto.is_occupied or not quarto.guest:
        print("Erro: Este quarto está desocupado no momento.")
        return False

    itens_fisicos = {
        idx: item
        for idx, item in enumerate(db.estoque_produtos.values(), 1)
        if item.is_physical
    }

    if not itens_fisicos:
        print("Não há itens físicos cadastrados no estoque do frigobar.")
        return False

    print("\nProdutos disponíveis no Frigobar:")
    for idx, item in itens_fisicos.items():
        print(f" [{idx}] {item.name} - R$ {item.price:.2f} (Estoque: {item.stock} un)")

    escolha_idx = obter_inteiro("Escolha o número do produto desejado: ", min_val=1, max_val=len(itens_fisicos))
    item_escolhido = itens_fisicos[escolha_idx]

    quantidade = obter_inteiro(f"Digite a quantidade de '{item_escolhido.name}' consumida: ", min_val=1)
    
    if item_escolhido.stock < quantidade:
        print(f"Estoque insuficiente! Há apenas {item_escolhido.stock} unidades de '{item_escolhido.name}' no frigobar.")
        return False

    item_escolhido.stock -= quantidade
    custo_total_item = item_escolhido.price * quantidade
    quarto.guest.extra_costs += custo_total_item

    print(f"\nLançado com sucesso! R$ {custo_total_item:.2f} adicionados à conta do quarto {quarto.number}.")
    print(f"Estoque atualizado de '{item_escolhido.name}': {item_escolhido.stock} unidades.")
    return True

def registrar_consumo_lazer() -> bool:
    """
    Função/Classe: registrar_consumo_lazer
    Params:
    Descrição: Registra um serviço de lazer (SPA, massagem, lavanderia) na conta do hóspede.
    Returns: bool se a operação funcionou ou não
    """
    print("\n--- CONSUMO DE LAZER E SERVIÇOS ---")
    
    n_quarto = obter_inteiro("Digite o número do quarto: ")
    if n_quarto not in db.quartos:
        print("Erro: Quarto não cadastrado.")
        return False
        
    quarto = db.quartos[n_quarto]
    if not quarto.is_occupied or not quarto.guest:
        print("Erro: Este quarto está desocupado no momento.")
        return False

    servicos = {nome: item for nome, item in db.estoque_produtos.items() if not item.is_physical}
    if not servicos:
        print("Não há serviços de lazer cadastrados no sistema.")
        return False

    print("\nServiços de Lazer Disponíveis:")
    lista_nomes = list(servicos.keys())
    for idx, nome in enumerate(lista_nomes, 1):
        servico = servicos[nome]
        print(f" [{idx}] {servico.name} - R$ {servico.price:.2f}")

    escolha_idx = obter_inteiro("Escolha o número do serviço prestado: ", min_val=1, max_val=len(lista_nomes))
    servico_escolhido = servicos[lista_nomes[escolha_idx - 1]]

    quarto.guest.extra_costs += servico_escolhido.price

    print(f"\nServiço '{servico_escolhido.name}' registrado com sucesso! R$ {servico_escolhido.price:.2f} adicionados à conta do quarto {quarto.number}.")
    return True
