# Skill `igrp-web-v1-v2` — especialista em IGRP 1.x e 2.x

Agent Skill (pt-PT) para desenvolver, rever, auditar e migrar aplicações **IGRP v1** (igrpweb "legacy") e **IGRP v2** ("Horizon")
da NOSi. As regras vêm da documentação oficial [docs.igrp.cv](https://docs.igrp.cv) e foram confirmadas no código do
[IGRP-Framework](https://github.com/NOSiCode-CV/IGRP-Framework). Funciona no Claude Code, no Codex e em qualquer agente compatível
com o padrão [Agent Skills](https://agentskills.io).

| Versão | Faixa coberta | Exemplos |
|---|---|---|
| v1 — igrpweb "legacy" | `1.0.0` ≤ versão < `2.0.0`, e os formatos antigos só com data (`211115`, `V200403`) | 1.7.4, 1.8.3.240913, 1.9.0.261013, 1.9.1.261027 |
| v2 — IGRP "Horizon" | `2.0.0` ≤ versão < `3.0.0` | 2.0.0.250518-GA, 2.1.0.261013, 2.1.1.261027; futuras 2.2.0 a 2.9.9 com a indicação "não verificado" |
| Fora de âmbito | IGRP v0 (PL/SQL) e IGRP 3.x / New Horizon | — |

## Conteúdo do repositório

```
igrp-web-v1-v2/          o skill (a única pasta que se instala)
  SKILL.md               comportamento, Passo 0 (versão e build), modos de trabalho, mapa de referências
  agents/openai.yaml     metadados de interface para Codex/ChatGPT (ignorado pelo Claude)
  references/            19 referências carregadas a pedido (versões, builds, temas, checklists)
tools/                   manutenção: extrair o portal, gerar relatórios, validar o skill e as versões
audit/                   inventário do portal, análise por documento, consultas de teste de ativação
reports/                 validação documental, compatibilidade entre plataformas, estrutura e necessidade
skills-lock.json         ferramentas de autoria do workspace instaladas com `npx skills` (não fazem parte do skill)
```

## Instalação

### Com o CLI do skills.sh (recomendado)

Requer Node.js 22.20 ou superior. O CLI copia o skill para `.agents/skills/` e cria um symlink para cada agente escolhido.
Para desligar a telemetria anónima do CLI, define `DISABLE_TELEMETRY=1` (ou `DO_NOT_TRACK=1`).

```bash
# A partir do GitHub (aponta diretamente para a pasta do skill):
npx skills add https://github.com/JailsonMendonca/igrp-web-1.0_to_2.0_skill/tree/main/igrp-web-v1-v2 -a claude-code -a codex

# Ou pelo repositório, escolhendo o skill:
npx skills add JailsonMendonca/igrp-web-1.0_to_2.0_skill --skill igrp-web-v1-v2 -a claude-code -a codex

# A partir de uma cópia local:
npx skills add ./igrp-web-v1-v2 -a claude-code -a codex
```

Sem mais opções, o CLI pergunta tudo no terminal (validado com o CLI 1.9.0 em 2026-11-21):

1. **Source** — clona o repositório e encontra `igrp-web-v1-v2`.
2. **Agentes** — `Universal (.agents/skills)` vem sempre incluído e serve Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode,
   Amp e outros. Em *Additional agents* marca **Claude Code** (`.claude/skills`).
3. **Installation scope** — *Project* (pasta atual, para versionar com o projeto IGRP) ou *Global* (todos os projetos).
4. **Installation method** — *Symlink (Recommended)*: uma cópia em `.agents/skills/` e um symlink em `.claude/skills/`. *Copy to
   all agents*: uma cópia real em cada pasta.
5. **Proceed with installation** — confirma.

Equivalente sem perguntas: `-a claude-code` (agentes), `-g` (Global), `--copy` (Copy) e `-y` (confirmar). Se o comando correr
dentro de um agente (variáveis `CLAUDECODE` ou `AI_AGENT` definidas), o CLI não mostra os ecrãs e instala para os agentes que
encontrar na máquina. Para escolher, corre-o num terminal normal ou passa as opções.

| Agente | Projeto | Utilizador (`-g`) |
|---|---|---|
| Claude Code | `.claude/skills/igrp-web-v1-v2` (symlink para `.agents/skills/…`) | `~/.claude/skills/igrp-web-v1-v2` |
| Codex | `.agents/skills/igrp-web-v1-v2` | `~/.agents/skills/igrp-web-v1-v2` |

Gestão: `npx skills list`, `npx skills update`, `npx skills remove igrp-web-v1-v2`. Uma instalação no projeto fica registada
em `skills-lock.json`.

### Manual

Copia a pasta `igrp-web-v1-v2/` inteira para um destes sítios:

- Claude Code: `~/.claude/skills/` (pessoal) ou `<projeto>/.claude/skills/` (projeto).
- Codex: `~/.agents/skills/` (pessoal) ou `<projeto>/.agents/skills/` (projeto).
- claude.ai ou ChatGPT: comprime a pasta em ZIP e carrega-a na área de Skills da conta, se o plano o permitir.

### Confirmar

- Claude Code: `/skills` lista `igrp-web-v1-v2`. Também se pode invocar com `/igrp-web-v1-v2`.
- Codex: `/skills` lista o skill. Também se pode invocar com `$igrp-web-v1-v2`.
- O skill ativa-se sozinho quando a conversa refere IGRP, igrpweb, IGRP Studio ou cola código com marcas do IGRP
  (`#start-code`, `Core.query`, `nosi.webapps`, `cv.igrp:igrp-core`, `ResultSet.Record`), mesmo sem escrever "IGRP".

## Exemplos de pedidos

- "Que versão do IGRP é este projeto e que build está a usar? Faz uma auditoria de segurança." → identifica v1/v2 e a build
  (`overlays/`, `WEB-INF/lib/igrp-core-<build>.jar`) e aplica `checklist-auditoria.md`.
- "No IGRP 2.1 tenho um botão que devolve um PDF; onde ponho o código para o Studio não o apagar?" → áreas `start-code` e
  Custom Return.
- "Quero passar este projeto igrpweb 1.8.3 para Horizon." → `comparacao-e-migracao.md` e `variantes-e-builds.md`.

Cada regra indica a fonte: `[DOC n.n #p_id]` (portal), `[REPO]`, `[CÓD-v1|v2]` (código oficial), `[MVN]` (repositórios Maven),
`[PROJ]` (projeto real confirmado no código) ou `[ENG]` (engenharia geral, não é regra oficial).

## Manutenção

```bash
python -I tools/extrair_portal.py audit/portal     # volta a descarregar o portal (menu, 169 documentos, inventário)
python -I tools/gerar_relatorio.py                 # regenera o inventário do skill e reports/validacao-documental.md
python -I tools/validar_skill.py igrp-web-v1-v2    # especificação, portabilidade, ligações, citações e cobertura
python -I tools/validar_versoes.py                 # builds publicadas e intervalos Maven (precisa de Java e Maven)
agentskills validate igrp-web-v1-v2                # validador oficial (pip install skills-ref)
```

Quando sair uma build nova (por exemplo 2.2.0), corre `tools/validar_versoes.py`, revê `references/variantes-e-builds.md` com o
histórico de `Config.VERSION` e do `pom.xml` do framework, e volta a correr `tools/validar_skill.py`.

## Estado da validação (2026-11-21)

| Verificação | Resultado |
|---|---|
| `agentskills validate`, skill-creator `quick_validate`, `tools/validar_skill.py` | Válido; 0 erros, 0 avisos |
| Teste de ativação da `description` (31 consultas, 4 delas só com código IGRP colado, sem a palavra "IGRP") | 31/31 |
| Versões: 424 builds publicadas (Maven Central e Nexus NOSi) e casos 1.10, 2.2.0, 2.9.9, 2.10 | Todas classificadas na linha certa; nenhuma 2.2+ publicada |
| Instalação com `npx skills` 1.9.0, modo interativo (clonar → Universal + Claude Code → Project → Symlink ou Copy) | 21/21 ficheiros idênticos nos dois métodos; o Claude Code lista o skill no arranque; `npx skills list` mostra-o |
| Carregamento no Codex (Codex CLI 0.171.0, `codex debug prompt-input`) | O skill instalado em `.agents/skills/` aparece na lista de skills do modelo, com a `description` completa e o caminho do `SKILL.md` |
| Java no Studio: compilação com o ECJ que o TomEE carrega e as opções do `Compiler.java` | v2 (ECJ 4.27, `-16`): até Java 16. v1: Java 8 em JDK 8; + `var`/`List.of` em JDK 11; até Java 16 em JDK 17 (ECJ 4.20). Fora do TomEE, o ECJ 3.19 da v1 rejeita `-16` |
| Estrutura MVC gerada (87 páginas em cada ramo oficial) | Model/View/Controller, `actionIndex` + `action<Tag>`, áreas `packages_import`/`index`/botão/`custom_actions`; nenhuma área em Model/View |

Detalhes em `reports/`.
