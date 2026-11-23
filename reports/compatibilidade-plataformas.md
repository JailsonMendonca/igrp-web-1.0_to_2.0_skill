# Relatório de compatibilidade entre plataformas — skill `igrp-web-v1-v2`

Verificado em 2026-11-20 e revisto em 2026-11-21 (cobertura de todas as builds 1.x e 2.x) contra as especificações oficiais:
Agent Skills (`agentskills.io/specification`), Claude Code (`code.claude.com/docs/en/skills`) e Codex/ChatGPT
(`learn.chatgpt.com/docs/build-skills`, destino do antigo `developers.openai.com/codex/skills`).

## 1. Resultado

| Verificação | Resultado |
|---|---|
| Validador oficial `skills-ref` 0.1.1 (`agentskills validate igrp-web-v1-v2`) | **Valid skill** |
| Validador do skill-creator (`scripts/quick_validate.py`) | **Skill is valid!** |
| Validador do workspace `tools/validar_skill.py` (spec + portabilidade + rastreabilidade) | 0 erros, 0 avisos |
| `name` = `igrp-web-v1-v2` (minúsculas, dígitos e hífenes; ≤ 64; igual ao nome da pasta) | Conforme |
| `description` 912 caracteres, sem `<` nem `>` (≤ 1024 Agent Skills; ≤ 1536 na listagem do Claude Code) | Conforme |
| Frontmatter só com campos portáveis (`name`, `description`, `metadata` string→string) | Conforme |
| `SKILL.md` 120 linhas (< 500), corpo ≈ 2 450 tokens (< 5 000) | Conforme |
| Referências ligadas diretamente pelo `SKILL.md`, um nível, caminhos relativos | 19/19 |
| Codificação UTF-8 sem BOM, fins de linha LF | Conforme |
| Rastreabilidade: p_id citados existem no inventário; 169/169 documentos citados | Conforme |
| Teste de ativação da `description` (skill-creator `run_eval`, modelo `claude-opus-5-5`, 1 execução por consulta) | **47/47**: 27/27 positivas ativam (código colado, DAO `BaseActiveRecord`, CRUD Generator, criação de páginas, RULES, Report Designer, acessos, domínios), 20/20 quase-acertos negativos não ativam (DAO/CRUD/páginas em Spring, Hibernate puro, React, Laravel, WordPress, JSF). 7 casos-limite repetidos 3 vezes: estáveis |

## 2. Por plataforma

### Agent Skills (padrão aberto)
- Estrutura `igrp-web-v1-v2/SKILL.md` + `references/` + `agents/openai.yaml` (diretórios adicionais são permitidos).
- *Progressive disclosure*: metadados sempre carregados, `SKILL.md` ao ativar, referências a pedido, conforme a tabela "Mapa de referências".

### Claude Code
- Localizações: pessoal `~/.claude/skills/igrp-web-v1-v2/`, projeto `.claude/skills/igrp-web-v1-v2/` (carregado a partir da pasta de
  arranque e das pastas-pai até à raiz do repositório), ou plugin `<plugin>/skills/igrp-web-v1-v2/`.
- Invocação: automática pela `description`, ou `/igrp-web-v1-v2`.
- Campos específicos do Claude Code (`when_to_use`, `allowed-tools`, `paths`, `context`…) **não** foram usados, porque nos uploads do
  claude.ai e na Skills API só são aceites `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools` (os
  restantes dão erro).
- `agents/openai.yaml` é ignorado pelo Claude.

### Codex (CLI e extensão IDE)
- Localizações: `.agents/skills/` em cada pasta desde a pasta de trabalho até à raiz do repositório, `$HOME/.agents/skills/`, `/etc/codex/skills/`.
- Requisitos: `name` e `description` (cumpridos). `agents/openai.yaml` com `interface.display_name`, `short_description`,
  `default_prompt` (`$igrp-web-v1-v2`) e `policy.allow_implicit_invocation: true`.
- Orçamento da lista de skills: ~2% do contexto ou 8 000 caracteres. Com muitos skills instalados o Codex encurta as descrições.
  Por isso a descrição tem os gatilhos no início (IGRP 1.0/2.0, igrpweb, Horizon).
- Invocação: `$igrp-web-v1-v2`, `/skills`, ou implícita.

### ChatGPT
- Skills autónomos disponíveis no ChatGPT desktop (barra Skills), no Codex CLI e na extensão IDE. Skills incluídos em plugins ficam
  disponíveis também no web, desktop e mobile. Invocação explícita com `@`.
- Não foi possível testar a instalação no ChatGPT neste ambiente (ver §4).

### Instalação com o CLI do skills.sh (`npx skills` 1.9.0), validada em 2026-11-21

Testes feitos numa pasta temporária, com `DISABLE_TELEMETRY=1` e sem tocar nas pastas do utilizador:

| Teste | Resultado |
|---|---|
| `npx skills add <workspace> --list` | Encontra 1 skill: `igrp-web-v1-v2` (description completa) |
| `npx skills add ./igrp-web-v1-v2 --list` | Encontra `igrp-web-v1-v2` |
| Clone de um repositório com o `.gitignore` novo (34 ficheiros versionados) | Encontra só `igrp-web-v1-v2` |
| Repositório com um skill válido em `.agents/skills/` e o `igrp-web-v1-v2` na raiz (estrutura real, sem o `.gitignore`) | Encontra os dois: o `skill-builder` de terceiros seria oferecido ao lado do `igrp-web-v1-v2` |
| O mesmo, mas com o `igrp-web-v1-v2` dois níveis abaixo (`sub/igrp-web-v1-v2`) | Encontra só o outro skill (a pesquisa fora das pastas padrão só acontece quando não há nenhum skill nelas) |
| Outro skill em `skills/` + `igrp-web-v1-v2` na raiz; ou os dois em `skills/<nome>/` | Encontra os dois nos dois casos |
| `skills.sh.json` com `"paths"` | Os caminhos são pastas que contêm skills; um caminho para a própria pasta do skill não funciona, e a raiz é ignorada. Não serve para este repositório |
| `npx skills add <clone> --skill igrp-web-v1-v2 -a claude-code -a codex -y` (projeto) | Cópia em `.agents/skills/igrp-web-v1-v2` (Codex, "universal") e symlink em `.claude/skills/igrp-web-v1-v2` (Claude Code); 21/21 ficheiros idênticos ao original; `skills-lock.json` criado |
| Arranque do Claude Code nesse projeto (evento `init`) | `igrp-web-v1-v2` listado nos skills e como `/igrp-web-v1-v2` |
| Modo interativo, como num terminal normal (fonte git clonada; ecrãs *Universal (.agents/skills)* + *Claude Code*, *Installation scope: Project*, *Installation method*) | **Symlink**: pasta real em `.agents/skills/` + symlink em `.claude/skills/`. **Copy to all agents**: pasta real nos dois sítios, `installMode: "copy"` no lock. Nos dois casos: 21/21 ficheiros idênticos, lock `sourceType: git` com o commit, e o Claude Code lista o skill no arranque |
| CLI chamado dentro de um agente (`CLAUDECODE`/`AI_AGENT` definidas) | Não mostra os ecrãs e instala para os agentes encontrados na máquina (Antigravity, Claude Code, Cursor, Gemini CLI, GitHub Copilot, Junie, Windsurf neste PC) |
| Codex (CLI 0.171.0 via `npx @openai/codex`, `CODEX_HOME` isolado, `codex debug prompt-input` no projeto instalado do GitHub) | O skill aparece na lista de skills que o modelo recebe, com a `description` completa e o caminho `.agents/skills/igrp-web-v1-v2/SKILL.md`. Os campos `interface` do `openai.yaml` não entram no prompt (são só para a interface) |

Comando recomendado, sem opções, para o utilizador escolher agentes, âmbito e método:
`npx skills add https://github.com/JailsonMendonca/igrp-web-1.0_to_2.0_skill/tree/main/igrp-web-v1-v2`.

Perguntas mostradas por opção (teste de 2026-11-23 a partir do GitHub, cancelado na confirmação): sem opções → agentes, âmbito,
método, confirmação; `-a claude-code -a codex` → âmbito, método, confirmação (os agentes ficam pré-escolhidos, que foi o
que aconteceu na instalação no projeto `teste`); `--copy` → agentes, âmbito, confirmação; `-g` → agentes, método, confirmação.
(aponta diretamente para a pasta e não depende da descoberta). Instruções completas no `README.md`.

## 3. Decisões de portabilidade

- **Sem scripts no pacote.** A identificação de versão e as auditorias são procedimentos em Markdown, o que evita depender de Python ou
  shell no ambiente de execução. Os scripts de manutenção (`tools/`) ficam fora do pacote.
- **Sem dependência de ferramentas específicas** (MCP, subagentes, `${CLAUDE_SKILL_DIR}`): o skill só pede leitura de ficheiros do projeto.
- **Língua**: pt-PT, como o portal e as equipas. Os termos técnicos e identificadores ficam no original.
- **Instalação** (copiar a pasta `igrp-web-v1-v2` inteira):
  - Claude Code: `%USERPROFILE%\.claude\skills\igrp-web-v1-v2` (pessoal) ou `<repo>\.claude\skills\igrp-web-v1-v2` (projeto);
  - Codex: `<repo>\.agents\skills\igrp-web-v1-v2` ou `%USERPROFILE%\.agents\skills\igrp-web-v1-v2`;
  - claude.ai / ChatGPT: carregar a pasta em ZIP na área de Skills da conta (se o plano o permitir).

## 4. Limitações

- O carregamento foi testado no Claude Code e no Codex, com instalações de projeto em pastas temporárias. Não foi testada a
  instalação pessoal (`~/.claude/skills`, `~/.agents/skills`), nem o claude.ai ou o ChatGPT, nem a ativação implícita no Codex
  (exigiria login e chamadas ao modelo).
- O teste de ativação usa a `description` como comando de projeto do Claude Code (método do skill-creator), não o skill instalado.
  Com 25/25 não foi preciso o ciclo de otimização `run_loop`. As 25 consultas estão em `audit/trigger-evals.json`.
- O `run_eval.py` do skill-creator não corre no Windows sem adaptação: usa `select()` sobre pipes e, em paralelo, cada execução vê
  os ficheiros de comando das outras (todas com a mesma descrição), o que contou como falha 9 ativações corretas na 1.ª execução
  (11/20). Foi usada uma cópia adaptada fora do workspace (leitura por thread e um projeto temporário por consulta).
- As especificações das plataformas mudam: voltar a correr `agentskills validate` e `tools/validar_skill.py` após alterações.
