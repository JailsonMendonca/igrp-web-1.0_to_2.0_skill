# Checklist de conformidade arquitetural

> Uso: confirmar que uma implementação nova ou alterada respeita a arquitetura da versão identificada. Cada item: Conforme / Não conforme / N/A, com evidência.

## 1. Comum a v1 e v2

| # | Requisito | Fonte |
|---|---|---|
| 1 | Páginas criadas no Studio (registo na BD + JSON), não só por ficheiros | [DOC 5.2 #1021], [DOC 3.2.2 #1007] |
| 2 | Estrutura `nosi.webapps.<app>.pages.<pagina>` com Model/View/Controller gerados; DAOs em `nosi.webapps.<app>.dao` | [DOC 9.6 #1029], [DOC 15.x] |
| 3 | Lógica só nas áreas reservadas; Model e View intactos | [DOC 18.1 #1125] |
| 4 | Navegação por `redirect`/`forward`/`renderView` com `this.queryString()` quando necessário | [DOC 11.1.1 #1072], [DOC 18.3 #1128] |
| 5 | Acesso a dados pela API `Core` (query parametrizada) ou DAO `BaseActiveRecord`, com ligação explícita registada no Application Builder | [DOC 18.4–18.7], [DOC 6.1] |
| 6 | Cada DAO listado no `cfg.xml` da sua ligação | [DOC 6.1 #1014] |
| 7 | Controlo de acesso por menus, transactions e etapas atribuídos a perfis; sem lógica de autorização *ad hoc* que duplique o framework | [DOC 12.x] |
| 8 | Interações Ajax por RULES e métodos `action<Procedure>` em `custom_actions` com resposta `RemoteXML` | [DOC 13.x] |
| 9 | JS/CSS no Studio (separadores JS/CSS, STYLE), não editando o XSL gerado | [DOC 19.1 #1126], [PROJ] |
| 10 | Relatórios no Report Designer (`Core.getLinkReport*`) e processos no BPMN Designer (`Core.startProcess`, etapas com páginas de processo) | [DOC 8.x], [DOC 7.x] |
| 11 | Configuração em `main.xml` e `hibernate-igrp-core.*`; ligações das apps em `<ligação>.<app>.cfg.xml/.properties` | [PROJ], [CÓD] |
| 12 | Componentes reutilizáveis em páginas Component (COPY FROM) e partilha entre aplicações | [DOC 9.3], [DOC 4.3] |
| 13 | Nenhuma tecnologia estranha à stack sem justificação (ex.: outro ORM, outro servidor, framework front-end SPA) | [ENG] |

## 2. Específico v1

| # | Requisito | Fonte |
|---|---|---|
| v1-1 | `cv.igrp` `[1.x,2.0.0)` (qualquer build 1.x), Java 8, TomEE 8.0.x; build resolvida identificada | [DOC 2.1.1], [CÓD-v1], [MVN] |
| v1-2 | APIs `javax.servlet`, `javax.ws.rs`, `javax.xml.bind`, `javax.jws`; nenhum `jakarta.*` | [CÓD-v1] |
| v1-3 | Código das páginas compatível com o nível de compilação: `-1.8`, ou o da JVM a partir de 1.8.3.240908 (Java 8 → `-1.8`) | [CÓD-v1 `Compiler.java`] |
| v1-4 | `ResultSet.Record.RowList` / `Row` | [CÓD-v1] |

## 3. Específico v2

| # | Requisito | Fonte |
|---|---|---|
| v2-1 | `cv.igrp` `[2.0.0,3.0.0)` (qualquer build 2.x), `maven.compiler.release` 17, TomEE 10.x (9.1.x nas 2.0.0 até 2.0.0.250217); build resolvida identificada | [DOC 21.1 #1221], [CÓD-v2], [MVN] |
| v2-2 | `jakarta.servlet`, `jakarta.ws.rs`, `jakarta.xml.bind`, `jakarta.jws`; **`javax.persistence` mantido** | [CÓD-v2] |
| v2-3 | `AuthenticationFilter` no `web.xml` (se existir `web.xml`) | [DOC 21.1] |
| v2-4 | Código das páginas compila a nível Java 16 (ECJ `-16`) | [CÓD-v2] |
| v2-5 | `ResultSet.Record.rowList` / `row`; cliente REST com `ClientBuilder` | [DOC 21.2 #1223] |
| v2-6 | Segredos por variáveis de ambiente quando `IGRP_ENV_VARIABLE_SCAN=true` (`${VAR}` nos `.properties`; chaves do `main.xml` ≥ 2.0.0.250220); `IGRP_SECRET_KEY` definido | [CÓD-v2], [ENG] |
| v2-7 | Páginas no gerador 2.3 ou 2.4 de forma consistente dentro da aplicação | [CÓD-v2], [ENG] |

## 4. Resultado

Indica a percentagem de itens conformes, os não conformes com correção proposta e os N/A justificados. Separa claramente o que é
regra oficial ([DOC]), evidência ([CÓD]/[PROJ]) e recomendação ([ENG]).
