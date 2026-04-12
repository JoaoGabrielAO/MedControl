# 💊 MedControl

<p align="center">
  <img src="https://img.shields.io/badge/versão-1.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/python-3.10%2B-yellow?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/testes-pytest-green?style=for-the-badge&logo=pytest" alt="Pytest">
  <img src="https://img.shields.io/badge/linting-flake8-orange?style=for-the-badge" alt="Flake8">
  <img src="https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions" alt="CI">
  <img src="https://img.shields.io/badge/licença-MIT-lightgrey?style=for-the-badge" alt="MIT License">
</p>

> **Controle de Medicamentos e Horários para Idosos** — Uma ferramenta CLI simples, robusta e acessível para que idosos e seus cuidadores não percam nenhuma dose.

---

## 📋 Índice

- [O Problema](#-o-problema)
- [A Solução](#-a-solução)
- [Público-Alvo](#-público-alvo)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Como Executar](#-como-executar)
- [Testes Automatizados](#-testes-automatizados)
- [Linting Estático](#-linting-estático)
- [CI/CD — GitHub Actions](#-cicd--github-actions)
- [Versionamento](#-versionamento)
- [Autor](#-autor)
- [Repositório](#-repositório)

---

## 🩺 O Problema

No Brasil, mais de **32 milhões de pessoas** têm 60 anos ou mais (IBGE, 2022), e grande parte delas utiliza múltiplos medicamentos de uso contínuo — uma condição chamada **polifarmácia**. O esquecimento de doses ou a confusão entre remédios com nomes e dosagens parecidas é uma das principais causas de internações hospitalares evitáveis nessa faixa etária.

Muitos idosos não têm acesso a smartphones ou aplicativos complexos, e os cuidadores frequentemente gerenciam a rotina de medicação **manualmente**, em papéis ou cadernos que se perdem com facilidade.

---

## 💡 A Solução

O **MedControl** é uma aplicação de linha de comando (CLI) desenvolvida em Python que permite:

- Cadastrar medicamentos com nome, dosagem e horários de administração.
- Listar todos os medicamentos de forma organizada.
- Consultar os detalhes de cada medicamento individualmente.
- Atualizar observações importantes (ex.: "tomar com leite", "monitorar pressão").
- Remover medicamentos que não são mais utilizados.
- Persistir todos os dados localmente em um arquivo **JSON**, sem necessidade de internet ou servidores externos.

A interface é **deliberadamente simples** — apenas números e texto — para ser acessível a qualquer perfil de usuário ou cuidador, inclusive em computadores antigos ou terminais de baixo recurso.

---

## 👥 Público-Alvo

| Perfil | Como usa o MedControl |
|---|---|
| **Idosos independentes** | Consultam a lista de medicamentos diariamente |
| **Cuidadores e familiares** | Cadastram e atualizam a rotina de medicamentos |
| **Enfermeiros domiciliares** | Gerenciam múltiplos pacientes via terminal |
| **Clínicas e postos de saúde** | Usam como ferramenta leve em computadores simples |

---

## ✅ Funcionalidades

- [x] **Cadastrar medicamento** — nome, dosagem, horários (múltiplos) e observações opcionais
- [x] **Listar medicamentos** — visão geral de todos os cadastros em formato tabular
- [x] **Ver detalhes** — informações completas de um medicamento específico por ID
- [x] **Remover medicamento** — exclusão com confirmação obrigatória para evitar acidentes
- [x] **Atualizar observações** — editar notas de um medicamento sem recadastrar
- [x] **Persistência em JSON** — dados salvos automaticamente em `data/medications.json`
- [x] **Validação de entradas** — campos obrigatórios validados com mensagens claras de erro
- [x] **IDs únicos** — cada medicamento recebe um identificador incremental e permanente

---

## 🛠 Tecnologias

| Tecnologia | Versão | Finalidade |
|---|---|---|
| **Python** | 3.10+ | Linguagem principal |
| **pytest** | 8.2.2 | Framework de testes automatizados |
| **pytest-cov** | 5.0.0 | Relatório de cobertura de testes |
| **flake8** | 7.1.0 | Linting e análise estática de código |
| **GitHub Actions** | — | Integração contínua (CI) |
| **JSON** | (stdlib) | Formato de persistência de dados |

> O projeto utiliza **apenas a biblioteca padrão do Python** em runtime — sem dependências externas pesadas.

---

## 📁 Estrutura do Projeto

```
medcontrol/
│
├── .github/
│   └── workflows/
│       └── ci.yml           
│
├── src/
│   ├── __init__.py
│   ├── main.py              
│   ├── cli.py              
│   ├── models.py            
│   └── storage.py           
│
├── tests/
│   ├── __init__.py
│   └── test_medcontrol.py   
│
├── data/                    
│   └── medications.json
│
├── .flake8                  
├── .gitignore
├── README.md
├── requirements.txt
└── VERSION                  # Versionamento semântico: 1.0.0
```

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10 ou superior instalado
- Git instalado

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/JoaoGabrielAO/medcontrol.git
cd medcontrol

# 2. Crie e ative o ambiente virtual
python -m venv .venv

# No Linux/macOS:
source .venv/bin/activate

# No Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Como Executar

Com o ambiente virtual ativado, a partir da **raiz do projeto**:

```bash
python -m src.main
```

Você verá o menu interativo:

```
────────────────────────────────────────────────────────────
  💊  MedControl — Controle de Medicamentos para Idosos  💊
────────────────────────────────────────────────────────────

  Bem-vindo ao MedControl!
  Gerencie os medicamentos e horários de forma simples e segura.

  MENU PRINCIPAL
  1. Cadastrar novo medicamento
  2. Listar todos os medicamentos
  3. Ver detalhes de um medicamento
  4. Remover medicamento
  5. Atualizar observações
  0. Sair
```

> 💡 **Dica:** Os dados são salvos automaticamente em `data/medications.json` a cada operação.

---

## 🧪 Testes Automatizados

O projeto possui **24 testes** organizados em três categorias:

| Categoria | Descrição | Exemplo |
|---|---|---|
| **Caminho Feliz** | Fluxos normais e esperados | Adicionar, listar, remover medicamentos |
| **Entrada Inválida** | Dados incorretos devem ser rejeitados | Nome vazio, dosagem vazia, lista de horários vazia |
| **Casos Limite** | Situações de borda | Storage vazio, 50 medicamentos, reutilização de ID |

### Executar todos os testes

```bash
pytest tests/ -v
```

### Executar com relatório de cobertura

```bash
pytest tests/ --cov=src --cov-report=term-missing -v
```

### Saída esperada

```
tests/test_medcontrol.py::TestCaminhoFeliz::test_adicionar_medicamento_retorna_objeto_correto PASSED
tests/test_medcontrol.py::TestCaminhoFeliz::test_listar_todos_retorna_lista_com_medicamentos  PASSED
...
========================= 24 passed in 0.42s ============================
```

---

## 🔍 Linting Estático

O projeto usa **flake8** para garantir qualidade e padronização do código (PEP 8).

```bash
# Verificar todo o código-fonte e os testes
flake8 src/ tests/
```

A ausência de saída indica que **nenhum problema foi encontrado**.

Configuração em `.flake8`:
- Comprimento máximo de linha: **100 caracteres**
- Diretórios excluídos: `.venv`, `__pycache__`, `build`, `dist`

---

## ⚙️ CI/CD — GitHub Actions

O pipeline de CI é definido em `.github/workflows/ci.yml` e é acionado automaticamente a cada `push` ou `pull_request` para as branches `main` e `develop`.

### Etapas do pipeline

```
📥 Checkout  →  🐍 Setup Python  →  📦 Cache pip
→  ⚙️ Instalar deps  →  🔍 flake8  →  🧪 pytest + cobertura
```

### Matriz de versões

O pipeline testa nas versões **Python 3.10, 3.11 e 3.12** simultaneamente.

Para verificar o status da última execução, acesse:
**`https://github.com/SEU_USUARIO/medcontrol/actions`**

---

## 🔖 Versionamento

Este projeto segue o padrão [**Versionamento Semântico (SemVer)**](https://semver.org/lang/pt-BR/):

```
MAJOR.MINOR.PATCH
  │      │     └── Correções de bugs (sem quebra de compatibilidade)
  │      └──────── Novas funcionalidades (sem quebra de compatibilidade)
  └─────────────── Mudanças que quebram compatibilidade
```

**Versão atual: `1.0.0`**

---

## 👤 Autor

**JoaoGabrielAO**

Desenvolvido como projeto acadêmico de programação, aplicando boas práticas de engenharia de software: estrutura modular, testes automatizados, linting, CI/CD e versionamento semântico.

---

## 🔗 Repositório

> 📌 Link do repositório: **[https://github.com/JoaoGabrielAO/medcontrol](https://github.com/JoaoGabrielAO/medcontrol)**
>
> 

---

<p align="center">
  Feito com ❤️ para cuidar de quem a gente ama.
</p>
