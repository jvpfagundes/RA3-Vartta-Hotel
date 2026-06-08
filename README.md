# Vartta Hotel

### Projeto: Vartta Hotel
**Descrição**: Sistema em modo de terminal (CLI) robusto para administração operacional diária de um hotel. O software orquestra fluxos de check-in, controle de consumo (frigobar físico e serviços de lazer/quarto), checkout com cálculo automatizado de taxas/descontos, gestão de estoque e persistência de dados de fechamento diário.

**Alunos/Turma**: João Victor Pontes de Oliveira Fagundes, Tales Augusto Tavares, João Flávio Sobral Dorea Correa. Turma de Engenharia de Software 1ºU

## Como utilizar?
- Para utilizar o sistema, primeiro precisamos iniciar uma venv, baixar os requisitos e então rodar.

**Windows**:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Linux/Mac**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
---

## Arquitetura do Sistema

O projeto adota uma estrutura modular focada na separação de responsabilidades (Single Responsibility Principle) e tipagem segura:

```
root/
│
├── main.py              # Ponto de entrada e orquestração do loop do sistema
├── config.py            # Definição de constantes e dados iniciais padrão
│
├── models/              # Modelos de dados Pydantic (Validação e Estrutura)
│   ├── category.py
│   ├── guest.py
│   ├── item.py
│   └── room.py
│
├── services/            # Lógicas e regras de negócio
│   ├── admin_service.py
│   ├── checkin_service.py
│   ├── checkout_service.py
│   ├── consumption_service.py
│   └── file_service.py
│
├── state/               # Estado global em memória (Banco de Dados simulado)
│   └── database.py
│
└── ui/                  # Componentes de interface e helpers de entrada
    ├── helpers.py
    └── screens.py
```

### Módulo: `state` (Banco de Dados em Memória)
- **Descrição**: Armazena o estado em memória das entidades da aplicação durante o tempo de execução, simulando tabelas de banco de dados.
- **Tabelas (Variáveis)**:
  - `quartos`: Dicionário contendo instâncias de [Room](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/room.py) indexados por número.
  - `categorias`: Dicionário com [Category](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/category.py) de quartos.
  - `estoque_produtos`: Dicionário de produtos e serviços cadastrados ([Item](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/item.py)).
  - `historico_hospedes`: Histórico detalhado de hóspedes que já realizaram o checkout.
  - `faturamento_diario`: Faturamento bruto acumulado no dia atual.

### Módulo: `models` (Modelos Pydantic)
- **Descrição**: Define a tipagem estrita e validação dos dados de entrada.
- **Classes**:
  - [Guest](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/guest.py): Representação de hóspedes ativos e seus consumos/serviços extras acumulados.
  - [Category](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/category.py): Categoria de quarto (Standard, Luxo, Suíte) com valor da diária associado.
  - [Room](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/room.py): Quarto do hotel contendo número, categoria, status de ocupação e referência ao hóspede.
  - [Item](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/item.py): Item físico do estoque ou serviço de lazer/quarto com preço, controle de quantidade e tipo.

### Módulo: `services` (Lógica de Negócios)
- **Descrição**: Contém a lógica operacional isolada por domínio de atuação.
- **Serviços**:
  - [admin_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/admin_service.py): Inicialização do hotel, criação de categorias, visualização de estoque e mapa de ocupação gráfica dos quartos.
  - [checkin_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/checkin_service.py): Orquestração de check-in, validando categorias disponíveis e alocando hóspedes.
  - [consumption_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/consumption_service.py): Registro de consumo de itens do frigobar e prestação de serviços adicionais de lazer/SPA.
  - [checkout_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/checkout_service.py): Fechamento de estadias, aplicação de desconto para estadias longas, cobrança de taxa municipal de ISS e desocupação.
  - [file_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/file_service.py): Exportação de relatórios financeiros diários em TXT e persistência do backup global em JSON.

### Módulo: `ui` (Interface do Usuário)
- **Descrição**: Apresentação visual interativa no terminal, incluindo efeitos estéticos e tratamentos de inputs robustos para evitar crashes.

---

## Parâmetros Globais (`config.py`)
- **Descrição**: Configurações editáveis que definem as restrições operacionais do hotel.
- **Configurações**:
  - `LIMITE_QUARTOS`: Limite de capacidade total de quartos.
  - `CATEGORIAS_PADRAO`: Nome e valor das diárias padrão de cada categoria.
  - `PRODUTOS_PADRAO`: Cadastro inicial de itens físicos de consumo e quantidade inicial em estoque.
  - `SERVICOS_PADRAO`: Cadastro de serviços do hotel (lavanderia, massagens, SPA).
  - `ARQUIVO_RELATORIO_TXT`: Localização e nome do relatório gerado.
  - `ARQUIVO_ESTADO_JSON`: Arquivo de saída para persistência do estado e backup.

---

## Fluxo Principal de Execução (`main.py`)
- **Função/Classe**: `main`
- **Descrição**: Ponto de entrada que inicializa o hotel (com carregamento rápido padrão ou configuração manual de quartos pelo administrador) e gerencia o menu dinâmico de 8 opções. Adicionalmente, escuta interrupções forçadas (como Ctrl+C) para garantir o salvamento de segurança do estado em disco.
- **Retorno/Resultados**:
  - Geração de relatório de faturamento detalhado `relatorio_fechamento.txt`.
  - Persistência estruturada em `estado_hotel.json`.


## Bibliotecas não built in usadas:
- **Pydantic**: Utilizado para tipagem robusta dos dados.
- **Motivo**:
  - Criação da nossa simulação de banco de dados. Usando BaseModel do pydantic conseguimos ter objetos personalizados e tipados, para criar "tabelas" para salvarmos nossos dados na memória local, persistindo por todo o projeto.

