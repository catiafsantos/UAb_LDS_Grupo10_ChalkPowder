# CSVGraphExporter - ChalkPowder
Programa do grupo 10 "ChalkPowder" na UC de Laboratório de Desenvolvimento de Software do ano 2024-2025

![image](https://github.com/user-attachments/assets/7654ffa6-867a-43ff-b47d-02d488302c71)

## Ponto de entrada:

No terminal com a working directory na localização de run.py (na pasta graficos).

1. Dois passos necessários para utilizar com o uv:

1.1 : Setup inicial:

```sh
machine:~/.../graficos % uv venv                                        
machine:~/.../graficos % source .venv/bin/activate
machine:~/.../graficos % uv sync 
```

1.2 : Correr o programa:
```sh
machine:~/.../graficos$ python run.py
```

Listagem de directorias:
```sh
UAb_LDS_Grupo10_ChalkPowder/
├── Diagramas
│   (diagramas de componentes e sequências do projeto)
│
├── FicheirosTeste
│   (ficheiros de teste para a aplicação)
│
├── graficos
│   ├── src
│   │   └── graficos
│   │       ├── controller
│   │       │   ├── controllerConsoleLogger.py
│   │       │   ├── controllerEvent.py
│   │       │   ├── controller.py
│   │       │   └── __init__.py
│   │       ├── guiview.py
│   │       ├── ILogger.py
│   │       ├── __init__.py
│   │       ├── IUserView.py
│   │       ├── model.py
│   │       └── view.py
│   ├── run.py
│   ├── README.md
│   ├── pyproject.toml
│   ├── uv.lock
└── README.md
```