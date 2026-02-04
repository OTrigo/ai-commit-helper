# 🤖 AI Git Helper

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