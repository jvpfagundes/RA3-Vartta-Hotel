# Vartta Hotel

### Project: Vartta Hotel
**Description**: Robust terminal-mode (CLI) system for daily operational management of a hotel. The software orchestrates check-in flows, consumption control (physical minibar and leisure/room services), checkout with automated fee/discount calculation, inventory management, and data persistence for daily closure.

**Students/Class**: João Victor Pontes de Oliveira Fagundes, Tales Augusto Tavares, João Flávio Sobral Dorea Correa. Software Engineering Class 1ºU

## How to Use?
- To use the system, first we need to initialize a venv, download the requirements, and then run it.

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

## System Architecture

The project adopts a modular structure focused on separation of concerns (Single Responsibility Principle) and type-safe design:

```
root/
│
├── main.py              # Entry point and system loop orchestration
├── config.py            # Definition of constants and default initial data
│
├── models/              # Pydantic data models (Validation and Structure)
│   ├── category.py
│   ├── guest.py
│   ├── item.py
│   └── room.py
│
├── services/            # Business logic and rules
│   ├── admin_service.py
│   ├── checkin_service.py
│   ├── checkout_service.py
│   ├── consumption_service.py
│   └── file_service.py
│
├── state/               # Global in-memory state (Simulated Database)
│   └── database.py
│
└── ui/                  # Interface components and input helpers
    ├── helpers.py
    └── screens.py
```

### Module: `state` (In-Memory Database)
- **Description**: Stores the in-memory state of application entities during runtime, simulating database tables.
- **Tables (Variables)**:
  - `quartos`: Dictionary containing [Room](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/room.py) instances indexed by number.
  - `categorias`: Dictionary with [Category](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/category.py) of rooms.
  - `estoque_produtos`: Dictionary of registered products and services ([Item](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/item.py)).
  - `historico_hospedes`: Detailed history of guests who have already checked out.
  - `faturamento_diario`: Gross billing accumulated on the current day.

### Module: `models` (Pydantic Models)
- **Description**: Defines strict typing and validation of input data.
- **Classes**:
  - [Guest](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/guest.py): Representation of active guests and their accumulated consumptions/extra services.
  - [Category](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/category.py): Room category (Standard, Luxury, Suite) with associated daily rate.
  - [Room](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/room.py): Hotel room containing number, category, occupancy status, and guest reference.
  - [Item](file:///Users/jfagundes/Documents/pessoal/puc/TCC/models/item.py): Physical inventory item or leisure/room service with price, quantity control, and type.

### Module: `services` (Business Logic)
- **Description**: Contains operational logic isolated by domain of operation.
- **Services**:
  - [admin_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/admin_service.py): Hotel initialization, category creation, inventory viewing, and occupancy map.
  - [checkin_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/checkin_service.py): Check-in orchestration, validating available categories and allocating guests.
  - [consumption_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/consumption_service.py): Record of minibar item consumption and provision of additional leisure services.
  - [checkout_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/checkout_service.py): Closure of stays, application of discounts for long stays, charging management fees.
  - [file_service.py](file:///Users/jfagundes/Documents/pessoal/puc/TCC/services/file_service.py): Export of daily financial reports in TXT and persistence of global backup in JSON.

### Module: `ui` (User Interface)
- **Description**: Interactive visual presentation in the terminal, including aesthetic effects and robust input handling to prevent crashes.

---

## Global Parameters (`config.py`)
- **Description**: Editable configurations that define the operational constraints of the hotel.
- **Configurations**:
  - `LIMITE_QUARTOS`: Limit of total room capacity.
  - `CATEGORIAS_PADRAO`: Name and value of default daily rates for each category.
  - `PRODUTOS_PADRAO`: Initial registration of physical consumption items and initial stock quantity.
  - `SERVICOS_PADRAO`: Registration of hotel services (laundry, massages, SPA).
  - `ARQUIVO_RELATORIO_TXT`: Location and name of the generated report.
  - `ARQUIVO_ESTADO_JSON`: Output file for state persistence and backup.

---

## Main Execution Flow (`main.py`)
- **Function/Class**: `main`
- **Description**: Entry point that initializes the hotel (with default quick loading or manual room configuration by the administrator) and manages the dynamic menu of 8 options.
- **Return/Results**:
  - Generation of detailed billing report `relatorio_fechamento.txt`.
  - Structured persistence in `estado_hotel.json`.

## Third-party Libraries Used:
- **Pydantic**: Used for robust data typing.
- **Reason**:
  - Creation of our database simulation. Using Pydantic's BaseModel, we can have custom and typed objects to create "tables" to save our data in memory.
