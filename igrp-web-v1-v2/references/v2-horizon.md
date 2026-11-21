# IGRP v2 — IGRP "Horizon"

> Âmbito: arquitetura, stack, estrutura, configuração, ambiente e execução específicos da v2, e aplicabilidade à v2 dos temas do portal.
> Fontes: [REPO README, docs/igrp_versions.md], [DOC 21.x], [CÓD-v2 igrp-horizon-dev@230df4c, core 2.1.1.261027], [PROJ]. Verificado em 2026-11-20.

## 1. Identidade

- IGRP Horizon v2, GA em 2023; instâncias "multi-instância (link direto)" [REPO docs/igrp_versions.md].
- Core `cv.igrp:igrp-core` + `igrp-core-war` na linha `[2.0.0,3.0.0)` [DOC 21.1 #1221]: 2.0.0 (alpha a RCM em 2023–2024, GA em
  2025), 2.1.0 (2026) e 2.1.1 (2026-10). Repositório oficial: ramos `igrp-horizon-dev` (desenvolvimento, 2.1.1) e `master` (2.1.0) [CÓD], [MVN].
- Este ficheiro descreve a build atual (2.1.x). Diferenças das builds 2.0.0 e regra para variantes futuras (ex.: 2.2.0): `variantes-e-builds.md` §4.
- A maior parte do portal foi escrita para a v1. Para a v2, usa este ficheiro, a matriz do §8 e `comparacao-e-migracao.md`.

## 2. Stack técnica [CÓD-v2 `IGRP/pom.xml`]

| Camada | v2 |
|---|---|
| Java | 17 (`maven.compiler.release`) [DOC 21.1], [REPO README: "JDK 17 or higher"] |
| Servidor | Apache TomEE plus via `tomee-maven-plugin`: 9.1.x nas 2.0.0 até 2.0.0.250217; 10.0.x desde 2.0.0.250220 (doc: 10.0.1); 10.1.x na 2.1.0; 10.2.0 na 2.1.1. `jakartaee-api` 10.0.1 |
| APIs | `jakarta.servlet`, `jakarta.ws.rs`, `jakarta.xml.bind`, `jakarta.jws` |
| Persistência | Hibernate 5.6.15 + HikariCP 5.1 — mantém **`javax.persistence`** |
| Migrações | Flyway 11.20.2 (`flyway-core`, `flyway-database-postgresql`) |
| BPMN | Activiti bpmn-converter 7.1.0.M6 |
| Compilação no Studio | Sempre nível `-16`. O `pom.xml` declara o ECJ 3.44.0, mas o TomEE carrega `org.eclipse.jdt.*` do servidor: no TomEE 10.2.0 corre o `tomee/lib/ecj-4.27.jar` [CÓD-v2], verificado em 2026-11-21 |
| Front-end | Bootstrap + jQuery XML/XSL; geradores 2.3 e 2.4 (design system). A partir de 2.0.0.260217 o servidor transforma o XML em HTML (`&ir_cf=xml` devolve o XML); desde 2.1.0.260307 o Studio invalida a cache de XSL ao gravar [CÓD-v2 `Controller.java`, `PageController.java`] |
| BD (mínimo/recomendado) | MySQL 5.7.8/8.0 · MariaDB 10.3/10.6 · PostgreSQL 11/14 · H2 2.0.204/2.1.10 · Oracle 11g/12c [REPO README] |

## 3. Estrutura (diferenças face à v1)

Mantém a estrutura de projeto da v1 (`nosi/webapps/<app>/pages|dao`, `images/IGRP/IGRP2.3/app/<app>/<pagina>/`,
`config/common/main.xml`, `hibernate-igrp-core.*`, `<ligação>.<app>.cfg.xml`). Acrescenta [CÓD-v2]:

- `src/main/webapp/images/IGRP/IGRP2.4/` — design system 2.4 (`app`, `assets`, `components`, `core`, `libs`, `plugins`, `themes`, `utils`, `xml`, `xsl`).
  As páginas podem ser geradas na versão 2.4 (`nosi/core/gui/generator/Generator2v4.java`) e as aplicações têm temas 2.4 (`EnvController`).
- `WEB-INF/web.xml` com o filtro `nosi.core.filter.AuthenticationFilter` mapeado ao servlet `IGRP` [DOC 21.1 #1221].
- `src/main/tomee/conf/server.xml`, `webapp/index.html`, `index.js`, `package.json` (no repositório do framework).

## 4. Configuração

- Mesmas chaves de `main.xml` que a v1 (ver `v1-legacy.md` §4), incluindo `igrp.login.template` (ex.: `ds-beta`, comentado por
  defeito; existe também na v1 desde 1.5.1). A v2 deixa de usar `mail.smtp.socketFactory.*` [CÓD-v2 `config/common/main.xml`].
- **Variáveis de ambiente** (ativadas com `IGRP_ENV_VARIABLE_SCAN=true`):
  - `${VAR}` no `hibernate-igrp-core.properties` e nos `<ligação>.properties` (≥ 2.0.0.240215; igual na v1 ≥ 1.8.1) [CÓD-v1+v2 `HibernateUtils.java`];
  - (≥ 2.0.0.250220, só v2) `IGRP_ENV`, `IGRP_WORKSPACE`, `IGRP_AUTHENTICATION_TYPE`, `IDS_AUTENTIKA_*`, `LDAP_AD_*`, `MAIL_SMTP_*`,
    `IGRP_SECRET_KEY`, entre outras, sobrepõem-se ao `main.xml`.
  `IGRP_SHOW_CONFIGURATION` mostra a configuração no arranque [CÓD-v2 `nosi/core/config/ConfigCommonMainConstants.java`].
  Usa-as para tirar segredos do repositório [ENG].
- `igrp.secret.key` / `IGRP_SECRET_KEY` define a chave secreta usada pelo `AuthenticationManager`. Sem ela é usada uma chave por defeito do código [CÓD-v2].

## 5. Ambiente e execução

- Pré-requisitos: JDK 17+, BD compatível (§2) [REPO README], [DOC 2.1.1 #1145].
- Gerar projeto: `mvn archetype:generate -Dfilter=igrp` e escolher `igrp-archetype-horizon`. Propriedades `dbJdbcUrl`
  (`jdbc:postgresql://localhost:5432/db_igrp`), `dbUser` (`postgres`), `dbPassword`, `dbJdbcDriver` (`org.postgresql.Driver`), por
  exemplo `mvn archetype:generate -Dfilter=igrp -DdbUser=… -DdbPassword=… -DdbJdbcUrl=…` [REPO README], [DOC 2.2.1 #1149].
- Arrancar: `mvn package tomee:run` → `http://127.0.0.1:8080/{artifactId}` [REPO README].
- `reloadOnUpdate=false` no framework: classes novas ou alteradas fora do Studio só ficam visíveis após reiniciar o TomEE [CÓD-v2 `IGRP/pom.xml`], [PROJ].

## 6. Compilação de páginas pelo Studio

Nível ECJ sempre `-16` [CÓD-v2 `Compiler.java`]. O código das páginas tem de compilar em Java 16. Podes usar `var`, `record`,
text blocks, `switch` com `->`, `instanceof` com padrão e `List.of()`. Não uses `sealed`/`permits` (Java 17) nem *pattern matching*
em `switch` (Java 21) [PROJ]. Confirmado compilando com o ECJ 4.27 do TomEE 10.2.0 e `-16` em 2026-11-21 [CÓD-v2].

## 7. Diferenças de código a aplicar na v2

| Tema | v2 | Fonte |
|---|---|---|
| Servlet, REST, JAXB, JAX-WS | `jakarta.*` (em vez de `javax.*`) | [DOC 21.1], [CÓD-v2] |
| JPA | continua `javax.persistence` | [CÓD-v2] |
| Cliente REST | `jakarta.ws.rs.client.ClientBuilder` (+ `jersey.config.client.*`) em vez de `org.glassfish.jersey.client.ClientConfig` | [DOC 21.2 #1223] |
| Linhas de `ResultSet.Record` | `rowList` / `row` (em vez de `RowList` / `Row`) | [DOC 21.2], [CÓD] |
| Transação multi-escrita | `AppSession.doInTransaction(p -> …, Core.getSession(conn))` disponível a partir de 2.0.0.240902 | [CÓD-v2], [PROJ] |

## 8. Matriz de aplicabilidade dos temas do portal à v2

| Tema (docs) | v2 | Evidência |
|---|---|---|
| Studio, Application Builder, BD, File Editor (4.x, 5.x, 6.x) | Aplicável | páginas `igrp_studio/*` e `igrp/*` nos dois ramos [CÓD-v1+v2] |
| Gerador, MVC, áreas preservadas, Custom Return, Blockly (9.x, 18.1, 11.1.x) | Aplicável; v2 acrescenta gerador 2.4 | `formgen/util/java/XSL_*.xsl`, `ExtractReserveCode`, `IGRP.blockly.java.xsl` nos dois ramos |
| Componentes e campos (10.x, 11.x) | Aplicável | plugins IGRP2.3 nos dois ramos; Load Service Data (`select2.init.js`, `p_search_data`) também em IGRP2.4 |
| Core, parâmetros, BD, query, DAO (18.2–18.7, 15.x, 20.x) | Aplicável; mudanças do §7 | API `Core` com os mesmos *overloads* nos dois ramos |
| Remote/Rules, JS/CSS (13.x, 19.1) | Aplicável | `RemoteXML`, `remoteComboBoxXml` nos dois ramos |
| Web services (14.x) | Aplicável com `jakarta.*` | §7 |
| BPMN e relatórios (7.x, 8.x) | Aplicável (instalação do Activiti 7.1 é procedimento v1) | `startProcess`, `getTaskHistory`, `getLinkReport*` nos dois ramos |
| Gestão de acessos (12.x) | Aplicável | `nosi/core/webapp/security/Permission.java` nos dois ramos |
| Ambiente Eclipse/Tomcat/JDK 8/SVN (2.3.x–2.5, 3.2.2, 15.1–15.3) | Não aplicável como procedimento | v2 = JDK 17 + `tomee:run` |
| Migração (21.x) | Específico v2 | — |

## 9. Pontos a validar

- O `Dockerfile` do ramo v2 continua com `openjdk:11-jre` + TomEE 8.0.10, incompatível com Java 17/TomEE 10 [CÓD-v2 `src/main/docker/Dockerfile`].
- Exemplos do portal com `javax.xml.bind` (#1108, #1112) não compilam em v2 sem trocar para `jakarta.xml.bind` [CÓD-v2: o core só usa `jakarta.xml.bind`].
- O portal (21.1) indica TomEE 10.0.1; a 2.1.1 usa 10.2.0 e as 2.0.0 até 2.0.0.250217 usam 9.1.x. Segue o template/archetype do projeto.
