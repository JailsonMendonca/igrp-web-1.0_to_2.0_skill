# Variantes e builds (linhas 1.x e 2.x)

> Âmbito: todas as builds da v1 (`1.x`, ex.: 1.7.4, 1.8.3, 1.9.0) e da v2 (`2.x`, ex.: 2.0.0 GA, 2.1.0, 2.1.1 e versões futuras como
> 2.2.0): onde estão publicadas, o que muda entre variantes, como identificar a build exata e como responder tendo em conta a build.
> Fontes: [MVN Central] `repo1.maven.org/maven2/cv/igrp/` (metadados de 2026-10-19); [MVN Nexus] `sonatype.nosi.cv/repository/maven-releases/`
> (2026-10-27); [CÓD-v1], [CÓD-v2]: histórico git de `Config.VERSION` e `IGRP/pom.xml` nos ramos `develop`, `igrp-horizon-dev` e `master`.
> Verificado em 2026-11-21.

## 1. Regras gerais

- A linha decide a versão: `1.0.0` ≤ versão < `2.0.0` é **v1** e `2.0.0` ≤ versão < `3.0.0` é **v2** (inclui 2.2 a 2.9.9 e 2.10+).
  As regras do skill aplicam-se a todas as builds da linha. O que só existe a partir de uma build está marcado `(≥ build)`.
  Pré-versões nos limites de um intervalo Maven: `identificacao-de-versao.md` §2.
- Formato: `M.m.p.AAMMDD[-qualificador]`, em que `AAMMDD` é a data da build (ex.: `1.9.0.261013` = 13-10-2026). Os qualificadores
  `-alpha`, `-beta`, `-RC1`, `-RC2`, `-RCM` e `-GA` só aparecem nas 2.0.0 do Maven Central [MVN Central]. Formatos antigos do
  `Config.VERSION` (todos v1): `AAMMDD` (2018-06 a 2022-05, ex.: `211115`), `VAAMMDD` (2020, ex.: `V200403`), `1.0.AAMMDD`
  (2022-06) e `M.m.p.AAMMDD.n` para reconstruções (2024-08, ex.: `1.8.3.240808.1`) [CÓD-v1].
- **Variante não listada** (ex.: `2.2.0`, `1.10.0`): aplica as regras da linha e as da última variante verificada (2.1.1 ou 1.9.1). Diz
  "variante <x> não verificada" e confirma no projeto (`Config.VERSION`, `pom.xml`, mensagens de commit `vX.Y.Z.<build>: …`). Não
  atribuas alterações a uma variante sem evidência. Em 2026-11-21 não há nenhuma `2.2.x` publicada nem no código oficial
  [MVN Central], [MVN Nexus], [CÓD-v2].
- As 2.0.0 anteriores à GA (alpha, beta, RC1, RC2, RCM) eram de pré-lançamento [MVN Central]. [ENG] Em produção usa 2.0.0 GA ou posterior.

## 2. Onde estão publicadas

| Origem | v1 | v2 |
|---|---|---|
| Maven Central | 1.7.2.230613 → 1.9.0.261013 | 2.0.0.230625-alpha → 2.1.0.261013 |
| Nexus NOSi (`nexusdeploymentrepo` no `pom.xml` gerado [PROJ v1]) | 1.6.0-alpha → 1.9.1.261027 | 2.0.0.230601 → 2.1.1.261027 |
| Tags git do repositório oficial | 1.0.0 (2020-04), 1.1.0, 1.2.0, 1.3.0, 1.4.0 (2022-07), 1.7.1.230512, v.1.8.1.240124 | — |
| Ramos git | `develop` = 1.9.1.261027 | `igrp-horizon-dev` = 2.1.1.261027 (desenvolvimento); `master` = 2.1.0.260813 |

Os intervalos `[1.9.0,2.0.0)` e `[2.0.0,3.0.0)` resolvem para a build mais alta que exista nos repositórios configurados. Com o
Nexus da NOSi, `[1.9.0,2.0.0)` dá 1.9.1.261027; só com o Maven Central dá 1.9.0.261013 [MVN]. Por isso dois ambientes podem
compilar contra builds diferentes, e uma build nova entra sem mudar o `pom.xml`. [ENG] Para reproduzir um erro ou estabilizar
produção, fixa a versão exata ou regista a build resolvida (§5).

## 3. Linha 1.x (v1) [CÓD-v1]

| Variante | Período | Java | TomEE (plugin) | Hibernate · Flyway | O que muda |
|---|---|---|---|---|---|
| 1.0–1.4 | 2020-04 → 2022-12 | 8 | 8.0.0 → 8.0.5 (plugin 8.0.10 desde 1.3) | 5.4.x → 5.6.8 (2022-05) · 7.10 → 8.5.8 | Base do modelo atual: gerador 2.3, `Core`, áreas `start-code`, `RowList`, ECJ sempre `-1.8` |
| 1.5–1.6 | 2022-12 → 2023-04 | 8 | 8.0.5 (plugin 8.0.10) | 5.6.8 · 9.x (desde 1.5.1) | `igrp.login.template` (`ds-beta`) desde 1.5.1 (fev. 2023) |
| 1.7.x | 2023-05 → 2023-12 | 8 | 8.0.14 → 8.0.15 | 5.6.14 → 5.6.15 · 9.14 → 9.21 | Primeiras builds no Maven Central (1.7.2) |
| 1.8.0–1.8.2 | 2023-12 → 2024-07 | 8 | 8.0.16 (≥ 1.8.0.240116) | 5.6.15 · 9.22.3 | Com `IGRP_ENV_VARIABLE_SCAN=true`, `${VAR}` nos `.properties` das ligações vem do ambiente (≥ 1.8.1.240215) |
| 1.8.3–1.8.5 | 2024-07 → 2026-06 | 8 | 8.0.16 | 5.6.15 · 9.22.3 | ECJ do Studio segue a JVM: 17+ → `-16`, 11 → `-11`, outra → `-1.8` (≥ 1.8.3.240908) |
| 1.9.x | 2026-06 → | 8 | 8.0.16 | 5.6.15 · 9.22.3 | Transformação XML → HTML no servidor, com cache de XSL (≥ 1.9.0.260618); 1.9.1 desde 2026-10-23 |

## 4. Linha 2.x (v2) [CÓD-v2]

| Variante | Período | Java | TomEE | O que muda |
|---|---|---|---|---|
| 2.0.0 internas | 2023-03 → 2023-05 | 11 | 9.0.0 | Primeiros commits Horizon; nunca publicadas. Um `pom.xml` `[2.0.0,…)` com `source 11` vem desta fase |
| 2.0.0 alpha/beta | 2023-06 → 2023-10 | 17 | 9.1.0 | Já com `jakarta.*`, `AuthenticationFilter`, `rowList`/`row`, ECJ `-16`; gerador 2.4 (`IGRP2.4`) a partir das builds de julho de 2023 (ex.: 2.0.0.230706-alpha) |
| 2.0.0 RC1/RC2 | 2023-11 → 2024-03 | 17 | 9.1.x | `${VAR}` nos `.properties` das ligações com `IGRP_ENV_VARIABLE_SCAN=true` (≥ 2.0.0.240215) |
| 2.0.0 RCM | 2024-06 → 2024-11 | 17 | 9.1.3 | `AppSession.doInTransaction` (≥ 2.0.0.240902) |
| 2.0.0 GA e seguintes | 2025-02 → 2026-02 | 17 | 9.1.3 até 2.0.0.250217 (inclui 250216-GA); 10.0.x ≥ 2.0.0.250220 (Central: 250321-GA); 10.1.x ≥ 2.0.0.260123 | Chaves do `main.xml` lidas de variáveis de ambiente (≥ 2.0.0.250220); transformação XML → HTML no servidor (≥ 2.0.0.260217) |
| 2.1.0 | 2026-02-22 → 2026-10 | 17 | 10.1.x (`master` 2.1.0.260813: 10.1.4) | O Studio invalida a cache de XSL ao gravar a página (≥ 2.1.0.260307); correções de JS/Ajax e encoding de JS (notas de commit) |
| 2.1.1 | 2026-10-22 → | 17 | 10.2.0 | Acessibilidade nos templates (ARIA, `alt`, botões semânticos), cache de recursos, disponibilidade de processos BPMN (notas de commit `v2.1.1.2610xx`) |
| 2.2.x ou posterior | — | — | — | Não publicada em 2026-11-21: regras da v2 + "não verificado" (§1) |

## 5. Identificar a build exata

1. `pom.xml`: com versão fixa, é essa. Com intervalo, vê a build resolvida:
   - pasta `overlays/cv.igrp.igrp-core-war-<build>/` (IntelliJ) e `target/<artifactId>/WEB-INF/lib/igrp-core-<build>.jar` [PROJ v1];
   - `~/.m2/repository/cv/igrp/igrp-core-war/<build>/` (builds descarregadas) ou `mvn dependency:list` [ENG].
2. Em execução: o XML de cada página traz `<version>` no cabeçalho, com o valor de `Config.VERSION` [CÓD-v1+v2 `Config.java`]. Nas
   builds que transformam no servidor, acrescenta `&ir_cf=xml` ao URL para receber o XML em vez do HTML [CÓD-v1+v2 `Controller.java`].
   Exemplo: o portal docs.igrp.cv devolve `<version>211115</version>`, uma build v1 de novembro de 2021.
3. Repositório do framework: `nosi.core.config.Config.VERSION` e o ramo (§2).
4. Quando a build for relevante para a resposta, indica-a: `Versão: v2 (2.1.0.261013) — evidências: …`.

## 6. Responder tendo em conta a build

- Funcionalidade `(≥ build)` num projeto com build anterior: diz que não existe nessa build e dá a alternativa da mesma linha.
  Ex.: v2 anterior a 2.0.0.240902 não tem `AppSession.doInTransaction` → `Core.transaction(conn)` ou `Session` do Hibernate com
  `rollback()` (`dados-dao-hibernate.md` §5). v1 anterior a 1.8.1.240215 não lê `${VAR}` → segredos no ficheiro, fora do controlo de
  versões [ENG].
- Build desconhecida: responde para a última build verificada da linha e diz o que depende da build.
- Atualizar dentro da linha (ex.: 1.8.3 → 1.9.x, 2.0.0 → 2.1.x) não é migração: não muda `javax`/`jakarta` nem o modelo de
  páginas. Revê a tabela da linha, compila, abre e grava as páginas no Studio e testa [ENG]. Passar de 1.x para 2.x é migração
  (`comparacao-e-migracao.md`).
- (v1 ≥ 1.9.0.260618) O XSL compilado fica em cache no servidor e, no ramo `develop`, nenhum código chama
  `Controller.invalidateXslCache`. Na v2, o Studio invalida a cache ao gravar (≥ 2.1.0.260307) [CÓD-v1], [CÓD-v2 `PageController`].
  Se uma página v1 1.9.x mantiver o aspeto antigo depois de gravada no Studio, reinicia o servidor antes de procurar outra causa
  (deduzido do código, não testado em execução).
- (v2 até 2.0.0.250217, incluindo 2.0.0.250216-GA) O servidor é TomEE 9.1.x. O doc 21.1 (TomEE 10.0.1) só corresponde ao core a
  partir de 2.0.0.250220 [DOC 21.1 #1221], [CÓD-v2].
