- **ID-06** - Atualiza changelog e remove comentários.
- **ID-05** - Remova bloco de texto do README.
- **ID-04** - Documente o script AI Git Helper.
- **ID-02** - Este diff reorganiza e atualiza uma entrada NO-ID no CHANGELOG.md. A descrição sobre a inserção de itens é realocada, e a referência
- **ID-03** - Refatora IA commit, remove ajuda e extrai IDs.
 é simplificada para Unreleased, com um ajuste de espaçamento na linha seguinte.
- **ID-01** - Este diff refatora o script ai_commit.py, otimizando funções auxiliares (ajuda, obtenção de diff e geração AI) ao remover funções dedicadas e inline-las. A principal mudança é a implementação de um sistema de fallback para o ID da tarefa, que agora gera um ID sequencial (ID-XX) quando nenhum ID explícito é encontrado ou fornecido, e a função update_changelog_file foi atualizada para gerenciar essa nova lógica e a formatação de links Jira. Prompts de usuário e mensagens de erro também foram simplificados.
  ou no topo.
- **NO-ID** - CHG: Insere entrada no CHANGELOG abaixo de Unreleased
- **NO-ID** - Adiciona script Python para helper de commit Git com IA e Changelog automático.
