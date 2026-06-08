import json
import os
from datetime import datetime
import state.database as db
from config import ARQUIVO_RELATORIO_TXT, ARQUIVO_ESTADO_JSON
from models import Room, Category, Item, Guest

def salvar_relatorio_fechamento_txt() -> bool:
    """
    Função/Classe: salvar_relatorio_fechamento_txt
    Params:
    Descrição: Gera um relatório financeiro completo em arquivo txt de fechamento diário.
    Returns: bool se a operação funcionou ou não
    """
    try:
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        with open(ARQUIVO_RELATORIO_TXT, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("          VARTTA HOTEL - RELATÓRIO DE FECHAMENTO\n")
            f.write("=" * 60 + "\n")
            f.write(f"Data de Emissão: {data_atual}\n")
            f.write(f"Faturamento Total do Dia: R$ {db.faturamento_diario:.2f}\n")
            f.write(f"Quantidade de Estadias Finalizadas: {len(db.historico_hospedes)}\n")
            f.write("=" * 60 + "\n\n")

            f.write("1. HISTÓRICO DE ESTADIAS ENCERRADAS HOJE:\n")
            f.write("-" * 60 + "\n")
            if not db.historico_hospedes:
                f.write("Nenhuma estadia finalizada hoje.\n")
            else:
                for idx, t in enumerate(db.historico_hospedes, 1):
                    f.write(f"Hóspede {idx}: {t['hospede']}\n")
                    f.write(f"  - Quarto: {t['quarto']} ({t['categoria']}) | Diárias: {t['dias']} dia(s)\n")
                    f.write(f"  - Subtotal Diárias: R$ {t['total_diarias']:.2f}\n")
                    f.write(f"  - Subtotal Consumos: R$ {t['total_extras']:.2f}\n")
                    f.write(f"  - Desconto Concedido: -R$ {t['desconto']:.2f}\n")
                    f.write(f"  - Taxa Municipal ISS: R$ {t['iss']:.2f}\n")
                    f.write(f"  - Total Pago pelo Cliente: R$ {t['total_pago']:.2f}\n")
                    f.write(f"  - Hora de Saída: {t['data_saida']}\n")
                    f.write("-" * 40 + "\n")
            f.write("\n")

            f.write("2. MAPA DE OCUPAÇÃO DE QUARTOS (STATUS ATUAL):\n")
            f.write("-" * 60 + "\n")
            for num, quarto in sorted(db.quartos.items()):
                status = "OCUPADO" if quarto.is_occupied else "LIVRE"
                hospede_nome = quarto.guest.name if quarto.guest else "N/A"
                f.write(f"Quarto {num:03d} | Tipo: {quarto.category.name:<10} | Status: {status:<8} | Hóspede: {hospede_nome}\n")
            f.write("\n")

            f.write("3. STATUS ATUAL DO ESTOQUE DO FRIGOBAR:\n")
            f.write("-" * 60 + "\n")
            for nome, item in db.estoque_produtos.items():
                if item.is_physical:
                    f.write(f"Item: {nome:<25} | Preço: R$ {item.price:<6.2f} | Em Estoque: {item.stock} un\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Fim do relatório de fechamento de expediente.\n")
            f.write("=" * 60 + "\n")

        print(f"Relatório txt exportado com sucesso para: '{ARQUIVO_RELATORIO_TXT}'")
        return True
    except IOError as e:
        print(f"Erro ao gravar o arquivo de relatório: {e}")
        return False

def salvar_backup_estado_json() -> bool:
    """
    Função/Classe: salvar_backup_estado_json
    Params:
    Descrição: Exporta o estado atual do hotel em formato json (backup).
    Returns: bool se a operação funcionou ou não
    """
    try:
        dados_backup = {
            "faturamento_diario": db.faturamento_diario,
            "historico_hospedes": db.historico_hospedes,
            "categorias": {nome: cat.model_dump() for nome, cat in db.categorias.items()},
            "estoque_produtos": {nome: item.model_dump() for nome, item in db.estoque_produtos.items()},
            "quartos": {str(num): quarto.model_dump() for num, quarto in db.quartos.items()}
        }

        with open(ARQUIVO_ESTADO_JSON, "w", encoding="utf-8") as f:
            json.dump(dados_backup, f, indent=4, ensure_ascii=False)
            
        print(f"Backup do banco de dados em memória exportado para: '{ARQUIVO_ESTADO_JSON}'")
        return True
    except (TypeError, IOError) as e:
        print(f"Erro ao realizar o backup em json: {e}")
        return False

def carregar_backup_estado_json() -> bool:
    """
    Função/Classe: carregar_backup_estado_json
    Params:
    Descrição: Importa o estado do hotel a partir do arquivo json.
    Returns: bool se a operação funcionou ou não
    """
    try:
        if not os.path.exists(ARQUIVO_ESTADO_JSON):
            print(f"Erro: Arquivo de backup '{ARQUIVO_ESTADO_JSON}' não encontrado.")
            return False
            
        with open(ARQUIVO_ESTADO_JSON, "r", encoding="utf-8") as f:
            dados = json.load(f)

        db.categorias.clear()
        db.estoque_produtos.clear()
        db.quartos.clear()
        db.historico_hospedes.clear()
        
        db.faturamento_diario = float(dados.get("faturamento_diario", 0.0))
        db.historico_hospedes = dados.get("historico_hospedes", [])
        
        for nome, dados_cat in dados.get("categorias", {}).items():
            db.categorias[nome] = Category(**dados_cat)
            
        for nome, dados_item in dados.get("estoque_produtos", {}).items():
            db.estoque_produtos[nome] = Item(**dados_item)
            
        for num_str, dados_quarto in dados.get("quartos", {}).items():
            num = int(num_str)
            
            dados_guest = dados_quarto.get("guest")
            guest_obj = Guest(**dados_guest) if dados_guest else None
            
            dados_cat = dados_quarto.get("category")
            category_obj = Category(**dados_cat) if dados_cat else None
            
            db.quartos[num] = Room(
                number=num,
                category=category_obj,
                is_occupied=dados_quarto.get("is_occupied", False),
                guest=guest_obj
            )
            
        print(f"Backup carregado com sucesso de '{ARQUIVO_ESTADO_JSON}'!")
        return True
    except Exception as e:
        print(f"Erro ao carregar o estado do JSON: {e}")
        return False
