# IGRP v1 — igrpweb "legacy"

> Âmbito: arquitetura, stack, estrutura, configuração, ambiente e execução específicos da v1.
> Os temas comuns (Studio, gerador, componentes, Core, dados, acessos) estão nos ficheiros temáticos, com aplicabilidade por regra.
> Fontes: [REPO], [DOC 2.x], [CÓD-v1 develop@6d7b32f, core 1.9.1.261027], [PROJ]. Verificado em 2026-11-20.

## 1. Identidade

- igrpweb v1, lançado em 2018; a documentação do portal foi preparada para esta versão [REPO docs/igrp_versions.md], [DOC 2.1.1 #1145].
- Core distribuído como `cv.igrp:igrp-core` (jar) + `cv.igrp:igrp-core-war` (war overlay), linha 1.x (de 1.0.0 em 2020 até
  1.9.1.261027); Maven Central e repositório NOSi `https://sonatype.nosi.cv/repository/maven-releases/` [PROJ], [CÓD-v1], [MVN].
  Este ficheiro descreve a build atual (1.9.x). Diferenças das builds anteriores (1.7, 1.8…): `variantes-e-builds.md` §3.
- Instâncias: Multi-WAR com SSO "Autentika" [REPO]. A opção *Custom dad* da aplicação cria um WAR à parte (outra instância) [DOC 5.1 #1020].

## 2. Stack técnica [CÓD-v1 `IGRP/pom.xml`]

| Camada | v1 |
|---|---|
| Java | 1.8 (`maven.compiler.source/target`); doc: "JDK8 para legacy" [DOC 2.1.1 #1145] |
| Servidor | Apache TomEE plus 8.0.16 via `tomee-maven-plugin` (embedded) |
| APIs Java EE | `javax.servlet`, `javax.ws.rs` (Jersey 2.46), `javax.xml.bind`, `javax.jws` |
| Persistência | Hibernate 5.6.15 + HikariCP, `javax.persistence` |
| Migrações | Flyway 9.22.3 (`flyway-maven-plugin`) |
| BPMN | Activiti (bpmn-model/converter 6.0.0) |
| Front-end | Bootstrap + jQuery, páginas XML + XSL, gerador 2.3 [DOC 9.1 #1024]. Até 1.8.x o browser aplica o XSL; a partir de 1.9.0.260618 o servidor devolve HTML já transformado (com `&ir_cf=xml` no URL devolve o XML) [CÓD-v1 `Controller.java`] |
| BD suportadas | PostgreSQL, MySQL, SQL Server, H2, Oracle (drivers no core) |

## 3. Estrutura de um projeto v1 (gerado por archetype)

```
pom.xml                      dependências igrp-core-war (war, overlay) + igrp-core (jar) [1.9.0,2.0.0)
                             propriedades igrp.db.user/password/dsn/driver e igrp.migration.location
src/main/resources/
  config/common/main.xml     parâmetros do igrpweb (ver §4)
  hibernate-igrp-core.cfg.xml  mapeamentos do core (hbm2ddl.auto=none, HikariCP)
  hibernate-igrp-core.properties  ligação do core = ${igrp.db.*} (filtrado pelo Maven)
  log4j2.xml
  <ligação>.<app>.cfg.xml / .properties   ligações criadas no Application Builder [DOC 6.1 #1014]
src/main/java/nosi/webapps/<app>/pages/<pagina>/   <Pagina>.java, <Pagina>View.java, <Pagina>Controller.java
src/main/java/nosi/webapps/<app>/dao/              classes DAO (opcional)
src/main/webapp/images/IGRP/IGRP2.3/app/<app>/<pagina>/   <Pagina>.json, .xml, .xsl (artefactos do gerador)
overlays/cv.igrp.igrp-core-war-<versão>/   cópia do WAR do core extraída pelo IDE — gerada, não editar
target/                      build e TomEE embebido (target/apache-tomee) — gerado
```
Fontes: [PROJ projeto v1 gerado com o archetype], [DOC 9.6 #1029], [DOC 6.1 #1014], [CÓD-v1+v2].

## 4. Configuração (`config/common/main.xml`) [PROJ], [CÓD-v1]

| Chave | Uso |
|---|---|
| `igrp.env` | `dev`, `test`, `sta` ou `prod` |
| `igrp.datasource.connection-name` | ligação do core (`hibernate-igrp-core`) |
| `igrp.workspace` | caminho absoluto do projeto, usado pelo Studio para escrever no código-fonte [DOC 2.4.2 #1152] |
| `igrp.authentication_type` | `db`, `ldap` ou `oauth2-openid` |
| `igrp.pwdRecover` | ativa a recuperação de palavra-passe |
| `ids.autentika.*` | integração com o servidor de identidade Autentika |
| `ids.oauth2-openid.*` | cliente OAuth2/OpenID (client_id, secret, endpoints) |
| `ldap.ad.*` | LDAP/Active Directory |
| `mail.*` (incl. `mail.smtp.socketFactory.*`) | SMTP para `Core.mail` [DOC 11.10 #1082] |

Na v1 estas chaves só são lidas do ficheiro (a v2 ≥ 2.0.0.250220 também as lê do ambiente). A partir de 1.8.1.240215, com
`IGRP_ENV_VARIABLE_SCAN=true`, os valores `${VAR}` no `hibernate-igrp-core.properties` e nos `<ligação>.properties` são lidos das
variáveis de ambiente, o que permite tirar as passwords de BD do repositório [CÓD-v1 `HibernateUtils.java`]. `igrp.login.template`
(`ds-beta`) existe desde 1.5.1. `igrp.secret.key` está declarada desde 1.8.3, mas nenhum código a usa [CÓD-v1].

## 5. Ambiente e execução

- Pré-requisitos: JDK 8, PostgreSQL (ou outra BD), IDE (Eclipse ou IntelliJ) [DOC 2.1.x].
- Fluxo atual: projeto gerado pelo archetype (`mvn archetype:generate -Dfilter=igrp …`) e arranque com `mvn package tomee:run`
  (ou `clean package tomee:run` no IntelliJ) [DOC 2.2.1 #1149], [DOC 2.6 #1220]. Com o plugin não é preciso um TomEE dedicado [DOC 2.1.4 #1147].
- Fluxo antigo (só histórico): importar o template do GitHub no Eclipse, Tomcat 9/TomEE 8.0.5, Build Path, "Run on Server",
  troubleshooting de servidor "unbound" [DOC 2.2.1, 2.3.x, 2.4.1, 2.4.5, 2.5]. Estes passos estão marcados como descontinuados no portal.
- Configurar `main.xml` (`igrp.workspace`), criar a BD do framework (ex.: `db_igrp`) e configurar o Flyway no `pom.xml` [DOC 2.4.2–2.4.4].
- URL: `http://localhost:8080/<artifactId>`; utilizador de demonstração documentado `demo@nosi.cv` / `demo` [DOC 2.4.5 #1004] — trocar fora do ambiente local [ENG].
- `reloadOnUpdate`: `false` no pom do framework [CÓD-v1]. O pom do projeto gerado pode ativar `true` com sincronização de `.class/.xml/.xsl/.properties` [PROJ]. Confirma no projeto.

## 6. Compilação de páginas pelo Studio

O Studio compila o Java das páginas com ECJ (`BatchCompiler`, opções `-encoding UTF-8 -warn:none <nível> -Xemacs`). A partir
de 1.8.3.240908 o nível depende da JVM em execução: Java 17+ → `-16`; Java 11 → `-11`; outra (Java 8) → `-1.8`. Nas builds
anteriores é sempre `-1.8` [CÓD-v1 `nosi/core/webapp/compiler/helpers/Compiler.java`].

**Que ECJ corre.** O `pom.xml` declara o ECJ 3.19.0 (vai para `WEB-INF/lib`), mas o TomEE carrega `org.eclipse.jdt.*` do servidor
(regra `URLClassLoaderFirst.shouldSkip`). No TomEE 8.0.16 o Studio usa por isso o `tomee/lib/ecj-4.20.jar`. Fora do TomEE, só com o
ECJ 3.19 do WAR, o nível `-16` falha em todas as páginas ("Unrecognized option : -16"): numa JVM 17+ fora do TomEE, o Studio v1 não
compila [CÓD-v1], verificado com os dois ECJ em 2026-11-21.

| JVM do servidor (TomEE 8.0.16) | Compila | Não compila |
|---|---|---|
| Java 8 | Java 8 (lambdas, streams, `Optional`) | `List.of`/`Map.of` (API Java 9), `var`, `switch` com `->`, text blocks, `record` |
| Java 11 (≥ 1.8.3.240908) | Java 8 + `var` + `List.of` | `switch` com `->`, text blocks, `instanceof` com padrão, `record` |
| Java 17+ (≥ 1.8.3.240908) | até Java 16: `var`, `switch` com `->`, text blocks, `instanceof` com padrão, `record`, `List.of` | `sealed`/`permits`, `switch` com padrões |

Num ambiente v1 típico (JDK 8, como pede o portal), escreve o código das páginas em Java 8 e sem APIs do Java 9+ [DOC 2.1.1 #1145].

## 7. Pontos a validar

- O `Dockerfile` do ramo usa `openjdk:11-jre` e TomEE 8.0.10, diferente do `pom.xml` (8.0.16) [CÓD-v1 `src/main/docker/Dockerfile`].
- As referências do portal a `db_igrp_config.xml` e às propriedades `db.*` estão desatualizadas (ver `fontes-e-inventario.md` §3).
- (1.9.x) O XSL transformado no servidor fica em cache e o ramo `develop` não a invalida quando o Studio grava a página (a v2
  invalida). Se a página continuar com o aspeto antigo depois de gravada, reinicia o servidor [CÓD-v1], deduzido do código e não
  testado (ver `variantes-e-builds.md` §6).
