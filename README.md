# 🤖 AI Git Helper

Automate your Git workflow with AI. This script handles the "dirty work": adding files, detecting task IDs from your branch, generating smart commit messages, and keeping your `CHANGELOG.md` updated and linked to Jira.

---

## 🚀 Key Features

* **Auto-Add:** Runs `git add .` automatically before analyzing changes.
* **Branch Intelligence:** Automatically detects task IDs (e.g., `ID-123`) from the branch name.
* **AI-Powered Commits:** Generates technical descriptions via Gemini (following Conventional Commits standards).
* **Dynamic Changelog:** Updates the top of your `CHANGELOG.md` with clickable Jira links.
* **Atomic Commits:** Code changes and Changelog updates are bundled into a single commit.
* **Turbo Mode (`-y`):** Prompt-free execution for maximum speed.

---

## 🛠️ Environment Setup

The script uses the following environment variables. Add them to your `~/.zshrc`, `~/.bashrc`, or PowerShell Profile:

| Variable | Description | Default / Example |
| --- | --- | --- |
| `GOOGLE_API_KEY` | **(Required)** Google AI Studio API Key | `AIzaSy...` |
| `GEMINI_MODEL_ID` | Gemini model to be used | `gemini-2.5-flash` |
| `JIRA_BASE_URL` | Your Jira/Atlassian base URL | `https://company.atlassian.net/browse/` |

---

## 📦 Quick Installation (Linux/macOS)

1. **Prepare the environment:**

```bash
mkdir -p ~/scripts && cd ~/scripts
python3 -m venv venv
source venv/bin/activate
pip install google-genai

```

2. **Create a shell alias:**

```bash
# Example for .zshrc or .bashrc
alias gcommit="~/scripts/venv/bin/python ~/scripts/ai_commit.py"

```

---

## ⌨️ How to Use

### Interactive Mode (Default)

The script will ask for confirmation regarding the Task ID, Jira linking, and the generated message.

```bash
gcommit

```

### Turbo Mode (Automatic)

Assumes "Yes" for all prompts and extracts all possible info from the branch.

```bash
gcommit -y

```

### Built-in Help

```bash
gcommit --help

```

---

## 📂 Changelog Output Example

The script formats the `CHANGELOG.md` as follows:

* [ID-1678](https://www.google.com/search?q=https://%5Byourorganization%5D.atlassian.net/browse/ID-1678) - Refactor login logic and add session validation
* **ID-01** - Update README with technical documentation
* [ID-1550](https://www.google.com/search?q=https://%5Byourorganization%5D.atlassian.net/browse/ID-1550) - Fix bug in payment gateway integration

---

## ⚖️ License

Distributed under the MIT License. Feel free to use and modify it.

---

# 🤖 AI Git Helper - PT

Automatize seu fluxo de trabalho Git com IA. Este script faz o "trabalho sujo": adiciona arquivos, detecta IDs de tarefas da branch, gera mensagens de commit inteligentes e mantém seu `CHANGELOG.md` atualizado e linkado ao Jira.

---

## 🚀 Funcionalidades Principais

* **Auto-Add:** Executa `git add .` automaticamente antes de analisar as mudanças.
* **Branch Intelligence:** Detecta IDs de tarefas (ex: `ID-123`) automaticamente do nome da branch.
* **IA-Powered Commits:** Gera descrições técnicas via Gemini (padrão Conventional Commits).
* **Changelog Dinâmico:** Atualiza o topo do seu `CHANGELOG.md` com links clicáveis para o Jira.
* **Atomic Commits:** O código e a atualização do Changelog vão no mesmo commit.
* **Modo Turbo (`-y`):** Execução sem perguntas para máxima velocidade.

---

## 🛠️ Configuração de Ambiente

O script utiliza as seguintes variáveis de ambiente. Adicione-as ao seu `~/.zshrc`, `~/.bashrc` ou Profile do PowerShell:

| Variável | Descrição | Default / Exemplo |
| --- | --- | --- |
| `GOOGLE_API_KEY` | **(Obrigatório)** Chave do Google AI Studio | `AIzaSy...` |
| `GEMINI_MODEL_ID` | Modelo do Gemini a ser utilizado | `gemini-2.5-flash` |
| `JIRA_BASE_URL` | URL base do seu Jira/Atlassian | `https://empresa.atlassian.net/browse/` |

---

## 📦 Instalação Rápida (Linux/macOS)

1. **Prepare o ambiente:**

```bash
mkdir -p ~/scripts && cd ~/scripts
python3 -m venv venv
source venv/bin/activate
pip install google-genai

```

2. **Crie o alias no seu shell:**

```bash
# Exemplo para .zshrc ou .bashrc
alias gcommit="~/scripts/venv/bin/python ~/scripts/ai_commit.py"

```

---

## ⌨️ Como Usar

### Modo Interativo (Padrão)

O script solicita confirmação para o Task ID, uso de links e a mensagem gerada.

```bash
gcommit

```

### Modo Turbo (Automático)

Assume "Sim" para todas as perguntas e extrai tudo o que pode da branch.

```bash
gcommit -y

```

### Ajuda Integrada

```bash
gcommit --help

```

---

## 📂 Exemplo de Output no Changelog

O script formata o `CHANGELOG.md` da seguinte forma:

* [ID-1678](https://[yourorganization].atlassian.net/browse/ID-XXXX) - Refactor login logic and add session validation
* **NO-ID** - Update README with technical documentation
* [ID-1550] - Fix bug in payment gateway integration

---

## ⚖️ Licença

Distribuído sob a licença MIT. Sinta-se à vontade para usar e modificar.

---