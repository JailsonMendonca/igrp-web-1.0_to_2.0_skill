# Relatório de estrutura e necessidade de ficheiros e diretórios

Data: 2026-11-20 (revisto em 2026-11-21: referência de variantes e builds). Parte 1: o skill e o workspace. Parte 2: ensaio do skill (identificação de versão e avaliação de ficheiros) nos
dois projetos de referência, só em leitura.

## Parte 1 — Skill e workspace

### 1.1 Estado inicial e remoções (autorizadas pelo utilizador)

| Elemento | Estado | Ação | Justificação |
|---|---|---|---|
| `SKILL.md` (raiz) | 0 bytes | Removido | Vazio; a raiz não pode ser a pasta do skill (`igrp-web-1.0_and_2.0_skill` é um `name` inválido) |
| `references/` (11 ficheiros) | 0 bytes cada | Removidos | Vazios; estrutura plana misturava versões (ex.: `igrp-web2-environment-setup.md` ao lado de `java.md`) |
| `examples/` (3) e `workflows/` (3) | 0 bytes cada | Removidos | Vazios; os exemplos oficiais passaram para as referências temáticas e os fluxos para "Modos de trabalho" do `SKILL.md` e para as checklists |
| pastas `references/`, `examples/`, `workflows/` | vazias após remoção | Removidas | — |
| `.agents/skills/skill-builder/`, `.claude/skills/skill-builder`, `skills-lock.json` | ferramenta de terceiros (ruvnet/ruflo) | **Mantidos**, fora do pacote | Ferramentas de autoria do utilizador; não fazem parte do skill |

Correspondência entre os placeholders antigos e os ficheiros novos: architecture → `v1-legacy.md`/`v2-horizon.md`; components/forms/tables →
`componentes.md`/`campos.md`; api-integration → `webservices.md` + `remote-javascript-css.md`; database → `dados-dao-hibernate.md`;
best-practices → `boas-praticas.md`; igrp-web2-environment-setup/project-execution → `v2-horizon.md`/`v1-legacy.md`;
development-guidelines/java → `gerador-de-codigo-e-mvc.md`.

### 1.2 Pacote do skill (`igrp-web-v1-v2/`, 21 ficheiros, ~173 KB)

| Ficheiro | Necessidade |
|---|---|
| `SKILL.md` | Obrigatório (comportamento, Passo 0, modos de trabalho, mapa de referências) |
| `agents/openai.yaml` | Opcional; metadados de interface do Codex/ChatGPT (ignorado pelo Claude). Mantido por compatibilidade |
| `references/identificacao-de-versao.md` | Necessário: passo obrigatório em todas as tarefas |
| `references/variantes-e-builds.md` | Necessário: cobre todas as builds 1.x e 2.x (ex.: 1.8.3, 1.9.0, 2.0.0 GA, 2.1.1) e a regra para variantes ainda não verificadas (ex.: 2.2.0); lido só quando a resposta depende da build |
| `references/fontes-e-inventario.md` | Necessário: rastreabilidade (etiquetas, inventário dos 169 docs, correções) |
| `references/v1-legacy.md`, `v2-horizon.md` | Necessários: documentação independente por versão (entregáveis 4 e 5) |
| `references/comparacao-e-migracao.md` | Necessário: entregável 6 |
| 10 referências temáticas (gerador, componentes, campos, dados, remote/JS/CSS, studio, BPMN/relatórios, acessos/segurança, webservices, colaboração) | Necessárias: conhecimento comum v1+v2 com aplicabilidade por regra, carregado só quando a tarefa o exige |
| `references/boas-praticas.md`, `checklist-auditoria.md`, `checklist-conformidade.md` | Necessários: entregáveis 7, 8 e 9 |

Simplificações avaliadas e rejeitadas: juntar `webservices.md` a `remote-javascript-css.md` (são áreas distintas: integração vs UI);
juntar as duas checklists (são usos distintos e entregáveis separados). Simplificação adotada: comparação e migração num só ficheiro.

### 1.3 Workspace (fora do pacote)

| Elemento | Papel | Necessidade |
|---|---|---|
| `tools/extrair_portal.py` | Extrai menu, documentos e inventário do portal | Manutenção (repetir quando o portal mudar) |
| `tools/gerar_relatorio.py` | Gera o inventário do skill e o relatório de validação | Manutenção |
| `tools/validar_skill.py` | Valida a spec, a portabilidade e a rastreabilidade | Manutenção / CI |
| `tools/validar_versoes.py` | Classifica as builds publicadas e os casos-limite (1.10, 2.2.0, 2.9.9…) e testa os intervalos com o motor do Maven | Manutenção (repetir quando sair uma build nova) |
| `README.md` | Descrição, instalação (skills.sh, manual, claude.ai), manutenção, publicação e estado da validação | Necessário para publicar |
| `.gitignore` | Exclui as ferramentas de autoria (`.agents/skills/`, `.claude/skills/`), que esconderiam o skill no `npx skills add`, a cópia dos documentos do portal, caches e pacotes | Necessário para publicar |
| `audit/portal/` (169 `.md`, `arvore.txt`, `inventario.csv`) | Snapshot do portal (dados descarregados) | Evidência da auditoria; regenerável. Os 169 `.md` ficam fora do git por omissão |
| `audit/analise.txt` | Análise manual por documento (fonte do relatório) | Necessário para regenerar o relatório |
| `audit/trigger-evals.json` | Consultas de ativação para otimizar a `description` | Opcional |
| `reports/` (3 relatórios) | Entregáveis 10, 11 e 12 | Necessário |

### 1.4 Revisão com o skill-creator

- Anatomia (`SKILL.md` + `references/`) e *progressive disclosure* conformes: `SKILL.md` com 120 linhas; referências entre 34 e 228
  linhas (abaixo de 300, sem necessidade de índice próprio); cada referência indica quando deve ser lida.
- `description` reforçada para combater a subativação ("Usar sempre que surgir IGRP, igrpweb, IGRP Studio… mesmo sem o skill ser
  pedido"), mantendo os negativos (IGRP 3.0, v0).
- Regras de comportamento reescritas com a razão de cada uma (em vez de imperativos sem explicação).
- Os casos de teste e evals não foram incluídos no pacote, para o manter enxuto. O conjunto de ativação ficou em `audit/`
  (25 consultas, 25/25 no teste de 2026-11-21).
- Checklist do `skill-builder` (ferramenta do workspace) aplicada. Dois pontos contradizem a especificação oficial Agent Skills e
  não foram seguidos: `name` em Title Case (a spec exige minúsculas com hífenes, igual à pasta) e a recusa de campos além de
  `name`/`description` (a spec aceita `metadata`, `license`, `compatibility`, `allowed-tools`).

## Parte 2 — Ensaio nos projetos de referência (só leitura)

### 2.1 `IdeaProjects/teste`

**Versão: v1** — `cv.igrp:igrp-core(-war)` `[1.9.0,2.0.0)`, `maven.compiler.source/target 1.8`, `tomee.maven.plugin.version 8.0.16`,
overlay `cv.igrp.igrp-core-war-1.9.1.261027`.

| ID | Severidade | Achado | Fonte | Recomendação |
|---|---|---|---|---|
| T1 | Média | Password da BD em claro no `pom.xml` (`igrp.db.password`) | [ENG] | Mover para `settings.xml`/perfil Maven ou variável de ambiente; não versionar |
| T2 | Média | `igrp.workspace` = `../..` (relativo); o doc pede o caminho do projeto | [DOC 2.4.2 #1152] | Confirmar que o Studio escreve no `src`; usar caminho absoluto se não escrever |
| T3 | Baixa | `.gitignore` sem `overlays/`; projeto sem repositório git | [ENG] | Acrescentar `overlays/` ao `.gitignore` e iniciar o controlo de versões |
| T4 | Info | `reloadOnUpdate=true` com sincronização de `.class/.xml/.xsl/.properties` (o framework usa `false`) | [CÓD-v1], [PROJ] | Manter em desenvolvimento |
| T5 | Info | `log4j2` com `nosi` em `debug`; `igrp.env=dev`; autenticação `db` | [ENG] | Rever para teste e produção |

| Elemento | Categoria |
|---|---|
| `pom.xml`, `src/main/resources/config/common/main.xml`, `hibernate-igrp-core.cfg.xml`, `hibernate-igrp-core.properties`, `log4j2.xml` | Necessário |
| `target/` (inclui o TomEE embebido) | Gerado automaticamente |
| `overlays/cv.igrp.igrp-core-war-1.9.1.261027/` | Gerado automaticamente (extração do WAR do core pelo IDE) |
| `.idea/` | Gerado (IDE) |
| `.mvn/` (vazio) | Requer investigação: sem conteúdo; inofensivo; remover só com autorização |
| Aplicações | Nenhuma ainda (`src` sem `.java`/`.xsl`) |

### 2.2 `IdeaProjects/IGRP-Framework` (ramo local `igrp-horizon-dev`)

**Versão: v2** — `Config.VERSION` 2.1.1.261027, `maven.compiler.release 17`, TomEE 10.2.0, `jakarta.*`, `AuthenticationFilter`, `IGRP2.4`.

| ID | Severidade | Achado | Fonte | Recomendação |
|---|---|---|---|---|
| F1 | Alta | Três aplicações de negócio não versionadas dentro do repositório do framework (`nosi/webapps/sistema_de_gestao_de_carros`, `sistema_de_gestao_teste`, `teste` + artefactos em `IGRP2.3/app/` e ligações em `resources/`) | [ENG] | Isolar num projeto próprio (archetype horizon) ou excluir no `.gitignore`, para evitar commits acidentais no core |
| F2 | Alta | Passwords de BD em claro nos `<ligação>.<app>.properties` dessas aplicações | [ENG] | Não versionar; usar variáveis ou segredos do ambiente |
| F3 | Média | `hbm2ddl.auto=update` nos `cfg.xml` das ligações das aplicações | [CÓD-v1+v2], [PROJ] | Rever antes de teste e produção; migrações versionadas |
| F4 | Média | `src/main/docker/Dockerfile` com `openjdk:11-jre` + TomEE 8.0.10, incoerente com Java 17/TomEE 10 | [CÓD-v2] | Atualizar ou documentar como obsoleto |
| F5 | Média | Alterações locais não commitadas em `pom.xml`, `main.xml` e `context.xml` (configuração local) | git | Parametrizar (perfis/variáveis) ou manter fora dos commits |
| F6 | Info | `PagesScapePermission` inclui rotas sem login de aplicações específicas (`inps_porton`, `portondinosilha`) | [CÓD-v2] | Rever em auditoria de segurança do core |
| F7 | Baixa | `.gitlab/.gitlab/issue_templates/.gitkeep`: diretório aninhado duplicado (só `.gitkeep`) | git | Candidato a remoção, só com autorização |
| F8 | Baixa | `IGRP.iml` não ignorado; `IGRP/.settings` versionado apesar de constar do `.gitignore` | git | Ajustar `.gitignore` / índice git |

| Elemento | Categoria |
|---|---|
| `IGRP/src/**` (core, apps de sistema `igrp`, `igrp_studio`, `tutorial`), `pom.xml` (raiz e módulo), `docs/`, `.gitlab/issue_templates/*.md`, `README.md`, `LICENSE`, `CONTRIBUTING.md` | Necessário |
| `IGRP/target/`, `.idea/`, `IGRP.iml` | Gerado (IDE / build) |
| `data/` (Dockerfile, `context.xml`, `index.jsp`, `setenv.sh`, `tomcat-users.xml`) | Potencialmente obsoleto: sem referências no repositório; pode ser usado por CI externo → **requer investigação**, preservar |
| `IGRP/CLAUDE.md`, `IGRP/.agents/skills/igrp-generated-java-protected-zones`, `.claude/`, `.mcp.json` | Ferramentas de IA/IDE do utilizador; manter (o skill de protected zones sobrepõe-se em parte a `gerador-de-codigo-e-mvc.md` §2) |
| `.mvn/maven.config` (não versionado) | Configuração local; manter |

Nada foi apagado nem alterado nos projetos.

## Parte 3 — Limitações e pontos por validar

- Utilização dinâmica (BD do framework: ações, menus, reports, processos) não verificada nos projetos por falta de acesso à BD. Os
  elementos sem referências estáticas foram classificados como "requer investigação".
- A aplicabilidade à v2 dos temas comuns foi confirmada por presença de APIs e artefactos no código. O comportamento em execução de
  cada componente na v2 (sobretudo no gerador 2.4) não foi testado.
- Regras `[PROJ]` vêm de um projeto com o gerador 2.1.1. Foram incluídas só quando confirmadas no código, mas podem variar noutras builds.

## Parte 4 — Validação Java e das estruturas geradas (2026-11-21)

**Compilação pelo Studio.** Exemplos de sintaxe do Java 8 ao Java 21 compilados com as opções do `Compiler.java`
(`-encoding UTF-8 -warn:none <nível> -Xemacs`) e com o ECJ que corre de facto. O `pom.xml` declara o ECJ (v1: 3.19.0; v2: 3.44.0),
mas o TomEE carrega `org.eclipse.jdt.*` do servidor (`URLClassLoaderFirst.shouldSkip` devolve `true`, confirmado no TomEE 8.0.16 e
no 10.2.0):

| Ambiente | ECJ efetivo | Compila | Não compila |
|---|---|---|---|
| v2, TomEE 10.2.0, JVM 17, `-16` | 4.27 (servidor) | Java 8–16: `List.of`, `var`, `switch` com `->`, text blocks, `instanceof` com padrão, `record` | `sealed`/`permits`, `switch` com padrões |
| v1, TomEE 8.0.16, JDK 8 | 4.20 (servidor) | Java 8 | `List.of`, `var`, `switch` com `->`, text blocks, `record`… |
| v1 ≥ 1.8.3.240908, JDK 11, `-11` | 4.20 | Java 8 + `var` + `List.of` | `switch` com `->`, text blocks, `record`… |
| v1 ≥ 1.8.3.240908, JDK 17, `-16` | 4.20 | o mesmo que a v2 | `sealed`/`permits`, `switch` com padrões |
| v1 ≥ 1.8.3.240908 fora do TomEE, JDK 17 | só o 3.19.0 do WAR | nada: "Unrecognized option : -16" | — |

Limitações: o JDK 8 e o JDK 11 foram emulados com `--release 8`/`--release 11` no JDK 17 (não há JDK 8/11 nesta máquina).

**Estrutura MVC gerada.** Nas 87 páginas de cada ramo oficial: Model + View + Controller por página (86 com JSON/XML/XSL em
`images/IGRP/IGRP2.3/app/<app>/<pagina>/`; a v2 tem também artefactos `IGRP2.4`); todos os Controllers estendem `Controller`;
`actionIndex` + `action<Tag>`; áreas `packages_import`, `index`, uma por botão e `custom_actions`; nenhuma área `start-code` em
Model ou View. 8 Controllers sem marcadores são páginas de sistema escritas à mão.

**Ativação e carregamento.** 47/47 no teste de ativação, incluindo pedidos só com código IGRP colado e com palavras-chave como
DAO, CRUD Generator e criação de páginas; os mesmos termos fora do IGRP não ativam o skill. O Claude Code e o Codex
(CLI 0.171.0, `codex debug prompt-input`) carregam o skill instalado com `npx skills add` a partir do GitHub.
