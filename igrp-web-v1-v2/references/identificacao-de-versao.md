# Identificação da versão (passo obrigatório)

> Âmbito: decidir se um projeto é IGRP v1 (igrpweb "legacy", qualquer build 1.x) ou v2 (IGRP "Horizon", qualquer build 2.x) antes
> de qualquer análise ou implementação. Para a build exata (ex.: 1.9.0, 2.1.1, 2.2.0) e o que muda entre builds, ver `variantes-e-builds.md`.
> Fontes: [REPO docs/igrp_versions.md], [DOC 2.1.1 #1145], [DOC 21.1 #1221], [CÓD-v1], [CÓD-v2], [MVN]. Verificado em 2026-11-21.

## 1. Mapa oficial de versões [REPO docs/igrp_versions.md]

| | IGRP v0 | **igrpweb v1** | **IGRP Horizon v2** | iGRP New Horizon v3 |
|---|---|---|---|---|
| Front-end | Bootstrap + jQuery (XML/XSL) | Bootstrap + jQuery (XML/XSL) | Bootstrap + jQuery (XML/XSL) | React (outros previstos) |
| Back-end | WebLogic + Oracle | TomEE (8.0.16) / Hibernate | TomEE (> 8) / Hibernate | APIs Spring, .NET… |
| Linguagem | Oracle PL/SQL | Java EE (> 8) | Java EE / Jakarta (> 17) | TypeScript, Java, C#… |
| Instâncias | Instância única, código na BD | Multi-WAR (Autentika, SSO) | Multi-instância (link direto) | Microsserviços |
| Geradores | 2.1 / 2.3 | 2.3 (Bootstrap e jQuery 3) | 2.3 e 2.4 (design system) | 3 (UI e API modulares) |
| Lançamento | 2011 | 2018 | 2023 (GA) | 2025 (beta) |

Só v1 e v2 estão no âmbito deste skill. O portal chama `legacy` à v1 e `horizon` à v2 [DOC 2.1.1 #1145].

## 2. Marcadores (por ordem de força)

| # | Onde ver | v1 (legacy) | v2 (Horizon) | Fonte |
|---|---|---|---|---|
| 1 | `pom.xml` → `cv.igrp:igrp-core` e `cv.igrp:igrp-core-war` (WAR overlay) | `1.x` fixa (ex.: `1.8.3.240913`) ou intervalo `[1.x,2.0.0)` (ex.: `[1.9.0,2.0.0)`) | `2.x` fixa (ex.: `2.0.0.250518-GA`, `2.1.0.261013`) ou `[2.0.0,3.0.0)` | [DOC 21.1 #1221], [MVN] |
| 2 | `pom.xml` → versão Java | `maven.compiler.source/target` `1.8` | `maven.compiler.release` `17` (`source 11` só em builds internas de 2023) | [DOC 21.1], [CÓD] |
| 3 | `pom.xml` → `tomee.maven.plugin.version` | `8.0.x` (8.0.16 desde 1.8.0) | `9.1.x` (2.0.0 até 2.0.0.250217) ou `10.x` (doc: 10.0.1; 2.1.1: 10.2.0) | [DOC 21.1], [CÓD] |
| 4 | imports Java | `javax.servlet`, `javax.ws.rs`, `javax.xml.bind`, `javax.jws` | `jakarta.servlet`, `jakarta.ws.rs`, `jakarta.xml.bind`, `jakarta.jws` | [CÓD-v1], [CÓD-v2] |
| 5 | `WEB-INF/web.xml` | sem `nosi.core.filter.AuthenticationFilter` | filtro `AuthenticationFilter` mapeado ao servlet `IGRP` | [DOC 21.1], [CÓD-v2] |
| 6 | recursos web | só `images/IGRP/IGRP2.3` | `images/IGRP/IGRP2.3` **e** `IGRP2.4` (gerador 2.4) | [CÓD-v2 `Generator2v4`] |
| 7 | código do framework ou XML da página (`<version>`) | `nosi.core.config.Config.VERSION` = `1.x` (ramo `develop`: 1.9.1) | `Config.VERSION` = `2.x` (ramos `igrp-horizon-dev`: 2.1.1; `master`: 2.1.0) | [CÓD] |
| 8 | API de resultados | `ResultSet.Record.RowList` / `Row` | `ResultSet.Record.rowList` / `row` | [DOC 21.2 #1223], [CÓD] |
| 9 | transações (marcador fraco) | não existe `AppSession.doInTransaction` | existe a partir de 2.0.0.240902 (ausente nas 2.0.0 anteriores) | [CÓD] |
| 10 | layout antigo | `WebContent/`, projeto "IGRP-Template" Eclipse, `db_igrp_config.xml` | — | [DOC 2.2.1 #1149], [DOC 2.4.3 #1153] |

**Faixas (regra do skill).** v1 = `1.0.0` ≤ versão < `2.0.0`: qualquer 1.x (1.0 a 1.9 e eventuais 1.10 ou superiores). v2 =
`2.0.0` ≤ versão < `3.0.0`: qualquer 2.x (2.0, 2.1 e futuras 2.2 a 2.9.9, ou 2.10 ou superiores). `3.x` ou superior: fora de
âmbito (§4). O `Config.VERSION` antigo só com data (`AAMMDD`, ex.: `211115`, ou `VAAMMDD`, ex.: `V200403`; 2018-06 a 2022-05)
é v1. As tags git `0.0.1.hor`/`0.0.1.hor2` são Horizon 2.0.0.230322 (v2), não uma versão 0 [CÓD], [MVN].

Classifica pelo número maior da **versão resolvida**, não pelo intervalo do `pom.xml`. No Maven, uma pré-versão do limite
superior entra no intervalo: `3.0.0-alpha`, `-RC1` ou `-SNAPSHOT` ficariam dentro de `[2.0.0,3.0.0)`, e uma `2.0.0-alpha` sem
build ficaria dentro de `[1.x,2.0.0)`. Nenhuma build publicada tem este problema (as pré-versões da v2 são `2.0.0.<build>-alpha`),
mas uma futura teria [MVN], [ENG].

Não são marcadores: `javax.persistence` (existe nas duas, Hibernate 5.6.15), `hibernate-igrp-core.cfg.xml`,
`config/common/main.xml`, o gerador `IGRP2.3`, a classe `Core`, as áreas `#start-code` e o Blockly. São comuns às duas versões [CÓD-v1+v2].

## 3. Procedimento

1. Lê o `pom.xml` (marcadores 1–3). Se forem coerentes entre si, a versão está identificada.
2. Confirma com pelo menos um marcador de código (4, 5, 6 ou 8), sobretudo quando o `pom.xml` usa intervalos ou propriedades.
3. Se for o próprio repositório do framework, lê `Config.VERSION` e o ramo git (marcador 7).
4. Marcadores contraditórios (ex.: `[2.0.0,3.0.0)` com `source 1.8`, ou `jakarta.*` misturado com `javax.servlet`) indicam uma
   **migração incompleta**. Reporta os ficheiros em conflito e segue `comparacao-e-migracao.md`.
5. Sem evidência suficiente (ex.: só excertos de código sem imports), **pergunta** ao utilizador e não assumas a versão.
6. Se a resposta depender da build (funcionalidade marcada `(≥ build)`, intervalo no `pom.xml`, variante citada pelo utilizador
   como 1.8.3 ou 2.2.0), identifica a build resolvida e aplica `variantes-e-builds.md` §5–§6. Uma variante 1.x ou 2.x ainda não
   verificada (ex.: 2.2.0) segue as regras da linha, com a indicação "não verificado".
7. Indica sempre na resposta: versão identificada + evidências (ficheiro e valor) e, quando a souberes, a build.

## 4. Fora de âmbito

- **v0** (PL/SQL, WebLogic, código na BD) e **v3 / New Horizon** (React, Spring/.NET, microsserviços, documentação
  "IGRP 3.0"): diz que estão fora do âmbito do skill e não apliques regras de v1/v2 a esses projetos.
- Ligação no portal para a doc 3.0 [DOC 1.1 #1000]: ignorar.
