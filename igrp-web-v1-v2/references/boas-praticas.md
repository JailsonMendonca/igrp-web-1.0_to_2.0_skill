# Catálogo de boas práticas

> Três níveis, nunca misturados:
> **A — Documentadas** (regra explícita no portal) · **B — Observadas** nos exemplos oficiais ou no código oficial / projetos ·
> **C — Engenharia geral** (recomendação; não é regra IGRP). Aplicabilidade (v1+v2) salvo indicação. Verificado em 2026-11-20.

## A. Boas práticas explicitamente documentadas

| # | Prática | Fonte |
|---|---|---|
| A1 | Não alterar Model nem View; programar no Controller, nas áreas reservadas; layout no separador DESIGN | [DOC 18.1 #1125], [DOC 9.6 #1029] |
| A2 | As áreas fora das reservadas não podem ser alteradas (imports em `packages_import`, auxiliares em `custom_actions`) | [DOC 9.6], [DOC 11.1.1 #1072] |
| A3 | Gravar no gerador e esperar a confirmação; fechar sem gravar perde o código | [DOC 9.1 #1024] |
| A4 | Enviar parâmetros com `addQueryString` (forma padrão) e incluir `this.queryString()` em `redirect`/`forward` para outra página; no `actionIndex` usar `setLink`/`addParam` | [DOC 18.3 #1128] |
| A5 | Usar `forward` em caso de erro, para repor os dados do formulário | [DOC 11.1.1], [DOC 10.5.2 #1036] |
| A6 | Botões restritos definidos como **Transaction** e atribuídos na Gestão de Acessos | [DOC 12.6 #1138] |
| A7 | Permissões atribuídas a **perfis**; associação direta a utilizadores só excecionalmente; definir primeiro o âmbito da orgânica | [DOC 12.4 #1136] |
| A8 | DAO: anotações JPA nos campos; coleções `EAGER`; coleções `Set` | [DOC 18.7 #1132] |
| A9 | Transações com várias operações dependentes: commit/rollback; `keepConnection()` nas consultas pela mesma ligação | [DOC 18.5 #1130] |
| A10 | Aliases das colunas iguais às tags dos campos (`model.load`, `loadTable`) | [DOC 18.6 #1131], [DOC 10.10.3 #1031] |
| A11 | Maxlength dos campos de texto igual ao tamanho da coluna na BD | [DOC 11.3.1 #1076], [DOC 11.22 #1094] |
| A12 | Campos Date em Readonly (data só pelo seletor) | [DOC 11.9 #1081] |
| A13 | Desligar *Create menu* em páginas auxiliares (novo, inserir, lookup) | [DOC 5.2 #1021] |
| A14 | Componentes reutilizáveis numa página **Component** com COPY FROM; partilhar páginas entre aplicações em vez de as recriar | [DOC 9.3 #1026], [DOC 4.3 #1009] |
| A15 | Preferir RULES a JS próprio; para JS/CSS próprio usar ID no STYLE e os separadores JS/CSS | [DOC 13.1 #1099], [DOC 19.1 #1126] |
| A16 | BPMN: sem "task" no id da etapa; radio-list String; sem tags repetidas em tabs; não atribuir tarefa ao perfil autenticado; parâmetros de processo com prefixo `x_`; validar documentos de input | [DOC 7.4 #1018], [DOC 7.5 #1019] |
| A17 | Blockly: copiar o código gerado para a área `start-code` e editar aí; o código do Blockly não se edita no Controller | [DOC 10.5.4 #1116], [DOC 9.7 #1115] |
| A18 | Ambientes separados (desenvolvimento, teste, produção) e passagem por exportação/importação | [DOC 5.4 #1023], [DOC 17.1 #1124] |
| A19 | Gerar projetos com o archetype (não clonar o template antigo) e arrancar com `tomee:run` | [DOC 2.2.1 #1149], [REPO README] |
| A20 | Verificar se a issue já existe antes de a reportar; usar o template Bug | [DOC 16.1 #1114] |
| A21 | Depois de um pull de páginas, abri-las no gerador e gravar para compilar | [DOC 3.2.2 #1007] |
| A22 | (v2) Migração: dependências `[2.0.0,3.0.0)`, Java 17, TomEE 10, `AuthenticationFilter`, `javax`→`jakarta` onde der erro | [DOC 21.1 #1221] |

## B. Práticas observadas (exemplos oficiais, código oficial, projetos)

| # | Prática | Fonte |
|---|---|---|
| B1 | Usar parâmetros nomeados (`:p` + `addInt/addString`) em queries | exemplos [DOC 18.6], [DOC 10.10.3] |
| B2 | Verificar `hasError()` após `insert/update/execute`; mensagens com `Core.setMessageSuccess/Error/Info/Warning` | [DOC 18.6], [DOC 18.7] |
| B3 | Guardar o nome da ligação numa constante em `custom_actions`; não usar `null` (ligação do framework) nas tabelas da aplicação | [PROJ], [CÓD `#gen-example`] |
| B4 | Não terminar a área de um botão com `return` incondicional (salvo com Custom Return) | [PROJ], [CÓD-v1+v2 `XSL_CONTROLLER.xsl`] |
| B5 | Rever os DAOs gerados (`@OneToMany` com `cascade = ALL` indevido) e não voltar a gerar o CRUD de uma tabela já gerada | [PROJ] |
| B6 | Evitar o cast `::` do PostgreSQL no SQL passado ao IGRP (usar `CAST`) | [PROJ], [CÓD `NamedParameterStatement`] |
| B7 | Validar antes de abrir uma transação; garantir a integridade na BD (UNIQUE, FK, triggers) | [PROJ] |
| B8 | (v2 ≥ 2.0.0.240902) `AppSession.doInTransaction` para várias escritas na mesma sessão | [CÓD-v2], [PROJ] |
| B9 | Classes alteradas fora do Studio: recompilar e reiniciar o TomEE antes de voltar a gravar no Studio (`reloadOnUpdate=false`) | [PROJ], [CÓD pom] |
| B10 | `LinkedHashMap` para listas com ordem controlada em combobox | [DOC 11.4.1 #1070] |
| B11 | Teste final de uma página: abrir no Studio, gravar sem mudar nada e confirmar que compila | [PROJ] |

## C. Recomendações gerais de engenharia (não oficiais)

| # | Recomendação |
|---|---|
| C1 | Nunca concatenar input do utilizador em SQL (vários exemplos do portal fazem-no) |
| C2 | Segredos fora do repositório (`IGRP_ENV_VARIABLE_SCAN=true` + `${VAR}` nos `.properties`: v1 ≥ 1.8.1 e v2; chaves do `main.xml`: v2 ≥ 2.0.0.250220); remover o utilizador demo fora de desenvolvimento |
| C3 | Credenciais da aplicação com hashing (não `Core.encrypt`) |
| C4 | Validar no servidor tudo o que vem do cliente (hidden, upload, Rules, parâmetros Ajax, páginas públicas) |
| C5 | Migrações versionadas (Flyway) em vez de `hbm2ddl.auto=update` em teste e produção |
| C6 | Tratar exceções com registo (log4j2 já configurado) e mensagens funcionais; evitar `printStackTrace()` silencioso |
| C7 | Lógica de negócio reutilizável em classes de serviço/DAO e chamada a partir das áreas preservadas, para que o Controller fique fino |
| C8 | Versionar todos os artefactos do gerador (JSON/XML/XSL + Java) e excluir os gerados de build (`target/`, `overlays/`) |
| C9 | Manter o `Dockerfile` e o `pom.xml` coerentes (versões de Java e TomEE) |
| C10 | Escapar ou sanitizar HTML gerado por código (reports HTML, Text Editor) |
| C11 | Fixar a build do core (ou registar a build resolvida) em vez de depender só de intervalos `[x,y)`, que mudam de build sem aviso (`variantes-e-builds.md` §2) |
