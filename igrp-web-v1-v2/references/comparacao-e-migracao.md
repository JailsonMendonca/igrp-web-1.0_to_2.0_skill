# Comparação v1 ↔ v2 e migração

> Âmbito: diferenças, equivalências e incompatibilidades documentadas ou verificadas no código, e o procedimento de migração 1.x → 2.x.
> Fontes: [REPO docs/igrp_versions.md], [DOC 21.1 #1221], [DOC 21.2 #1223], [CÓD-v1 develop@6d7b32f], [CÓD-v2 igrp-horizon-dev@230df4c].
> Verificado em 2026-11-21. Diferença de código entre os ramos: 378 ficheiros Java alterados.
> A tabela compara as builds atuais (1.9.x e 2.1.x). Onde uma diferença depende da build, a célula indica-o. Tabelas por variante:
> `variantes-e-builds.md`.

## 1. Comparação

| Aspeto | v1 (legacy) | v2 (Horizon) | Fonte |
|---|---|---|---|
| Ano | 2018 | 2023 (GA) | [REPO] |
| Arquitetura de instâncias | Multi-WAR (Autentika SSO) | Multi-instância (link direto) | [REPO] |
| Java | 8 | 17 | [DOC 2.1.1, 21.1], [CÓD] |
| Servidor | TomEE plus 8.0.16 (desde 1.8.0; antes 8.0.0–8.0.15) | TomEE plus 9.1.x (2.0.0 até 250217), 10.0.x (desde 2.0.0.250220), 10.1.x (2.1.0), 10.2.0 (2.1.1) | [DOC 21.1], [CÓD] |
| Plataforma | Java EE 8 (`javax.*`) | Jakarta EE 10 (`jakarta.*`) | [DOC 21.1], [CÓD] |
| JPA / Hibernate | `javax.persistence`, Hibernate 5.6.15 | igual (`javax.persistence`, Hibernate 5.6.15) | [CÓD] |
| Filtros web | Encoding, ThreadLocal, StaticResourceCache | + `AuthenticationFilter` | [CÓD `web.xml`] |
| Flyway | 9.22.3 | 11.20.2 | [CÓD] |
| Activiti (BPMN) | 6.0.0 | converter 7.1.0.M6 | [CÓD] |
| Geradores de página | 2.3 | 2.3 + 2.4 (design system, temas 2.4) | [REPO], [CÓD-v2] |
| Nível de compilação no Studio | `-1.8`; desde 1.8.3.240908 segundo a JVM (`-16` / `-11` / `-1.8`) | sempre `-16` | [CÓD `Compiler.java`] |
| Configuração | `main.xml` (só ficheiro); `${VAR}` nos `.properties` com `IGRP_ENV_VARIABLE_SCAN=true` (≥ 1.8.1.240215) | `main.xml` + `${VAR}` nos `.properties`; chaves do `main.xml` por variáveis de ambiente (≥ 2.0.0.250220); `IGRP_SECRET_KEY` usado pelo `AuthenticationManager` | [CÓD-v1], [CÓD-v2] |
| Renderização das páginas | XSL no browser; no servidor desde 1.9.0.260618 (cache de XSL sem invalidação ao gravar) | XSL no browser; no servidor desde 2.0.0.260217 (cache invalidada ao gravar desde 2.1.0.260307) | [CÓD `Controller.java`] |
| `ResultSet.Record` | `RowList`, `Row` | `rowList`, `row` | [DOC 21.2], [CÓD] |
| Transações | `Core.transaction`, Hibernate `Session` | + `AppSession.doInTransaction` (≥ 2.0.0.240902) | [CÓD] |
| Archetype | archetype igrp (linha 1.x) | `igrp-archetype-horizon` | [REPO README] |

## 2. Equivalências (iguais nas duas versões)

Verificado nos dois ramos [CÓD-v1+v2]: estrutura MVC gerada e áreas `#start-code`; XSL do gerador (`XSL_CONTROLLER`, `XSL_MODEL`,
`XSL_VIEW`); Blockly; `ExtractReserveCode`; API `Core` (parâmetros, query, insert/update/delete, DAO, domínios, ficheiros,
relatórios, BPMN, email); `BaseActiveRecord`; `RemoteXML`; gestão de acessos (`Permission`); `hibernate-igrp-core.cfg.xml`;
`main.xml` (incluindo `igrp.login.template`); CRUD/DAO Generator; `hbm2ddl.auto=update` nos `cfg.xml` das ligações criadas no
Application Builder; `<version>` no XML das páginas.

## 3. Incompatibilidades a tratar ao passar código v1 → v2

1. Imports `javax.servlet.*`, `javax.ws.rs.*`, `javax.xml.bind.*`, `javax.jws.*` → `jakarta.*` [DOC 21.1 passo 4], [CÓD].
2. `org.glassfish.jersey.client.ClientConfig` → `jakarta.ws.rs.client.ClientBuilder.newBuilder().property("jersey.config.client.connectTimeout", …)` [DOC 21.2].
3. `ResultSet.Record.RowList` → `rowList`; `Row` → `row` [DOC 21.2].
4. Sintaxe Java acima de 16 não compila no Studio v2. Código Java 8 compila sem problema.
5. `javax.persistence` **não** muda: não converter para `jakarta.persistence` (Hibernate 5.6) [CÓD-v2].

## 4. Procedimento de migração 1.x → 2.x [DOC 21.1 #1221], [DOC 21.2 #1223]

0. [ENG] Escolhe a build de destino: `[2.0.0,3.0.0)` resolve para a 2.x mais recente do repositório (2.1.1.261027 no Nexus NOSi,
   2.1.0.261013 no Maven Central em 2026-11-21). Evita as 2.0.0 alpha/beta/RC. A origem pode ser qualquer 1.x; se for anterior a
   1.8.x, revê primeiro as diferenças da linha 1.x (`variantes-e-builds.md` §3).
1. No `pom.xml`, dependências `cv.igrp:igrp-core-war` (type `war`) e `cv.igrp:igrp-core` (type `jar`) com versão `[2.0.0,3.0.0)`.
2. `<maven.compiler.release>17</maven.compiler.release>` e `<tomee.maven.plugin.version>` 10.x (o doc indica 10.0.1; usa a do
   template da build escolhida, ex.: 10.2.0 na 2.1.1).
3. Se o projeto tiver `web.xml`, acrescentar:
   ```xml
   <filter>
     <display-name>AuthenticationFilter</display-name>
     <filter-name>AuthenticationFilter</filter-name>
     <filter-class>nosi.core.filter.AuthenticationFilter</filter-class>
   </filter>
   <filter-mapping>
     <filter-name>AuthenticationFilter</filter-name>
     <servlet-name>IGRP</servlet-name>
   </filter-mapping>
   ```
4. Substituir `javax` por `jakarta` onde houver erro de compilação (ver §3, que limita a troca às APIs certas).
5. Rever o `pom.xml` e o Flyway: usar a versão do template [DOC 21.2].
6. [ENG] Antes: inventariar com `grep` os imports `javax.(servlet|ws.rs|xml.bind|jws)`, as utilizações de `RowList`/`Row` e de
   `ClientConfig`. Depois: compilar com `mvn package`, arrancar com `tomee:run`, abrir e gravar cada página no Studio para confirmar
   que compila (o Studio compila com `-16`).

## 5. Limitações

- O portal só tem dois documentos de migração (21.1 e 21.2), e o 21.2 está incompleto (os itens "pom.xml" e "Flyway" não têm detalhe).
- Não há documentação oficial sobre a migração do design system 2.3 → 2.4 das páginas: não assumir conversão automática.
