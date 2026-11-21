# Checklist de auditoria de projetos IGRP v1/v2

> Uso: auditar um projeto existente. Cada achado indica evidência (ficheiro:linha), versão, fonte (`[DOC]`/`[CÓD]`/`[PROJ]`/`[ENG]`),
> severidade (Crítica / Alta / Média / Baixa / Info) e recomendação. **Nunca apagar ou alterar ficheiros sem autorização explícita.**

## 0. Pré-auditoria

- [ ] Versão identificada com evidências (`identificacao-de-versao.md`). Se for inconclusiva, perguntar.
- [ ] Build do core identificada (fixa no `pom.xml` ou resolvida: `overlays/`, `WEB-INF/lib/igrp-core-<build>.jar`, `<version>` no XML) e funcionalidades `(≥ build)` confirmadas (`variantes-e-builds.md` §5–§6).
- [ ] Tipo de repositório: projeto de aplicação (archetype + overlay) ou o próprio IGRP-Framework (core + apps de sistema).
- [ ] Estado do git (`git status`): alterações locais e ficheiros não versionados. Não fazer checkout ou reset em repositórios com alterações.

## 1. Estrutura e configuração

- [ ] `pom.xml`: versões coerentes (core, Java, TomEE, Flyway) com a versão identificada; repositório Maven do core.
- [ ] `config/common/main.xml`: `igrp.env`, `igrp.workspace` (caminho absoluto válido), `igrp.authentication_type`, integrações; segredos (§4).
- [ ] `hibernate-igrp-core.cfg.xml` / `.properties` (ligação do core por `${igrp.db.*}`); `<ligação>.<app>.cfg.xml` com `<mapping>` de todos os DAOs e só desses.
- [ ] `web.xml` (v2: `AuthenticationFilter`); `log4j2.xml`.
- [ ] Coerência entre o código e os artefactos do gerador: para cada `pages/<p>/` existem `<P>.java`, `<P>View.java`, `<P>Controller.java` e `images/IGRP/IGRP2.3/app/<app>/<p>/<P>.json/.xml/.xsl`.
- [ ] `Dockerfile` e scripts de execução coerentes com a stack.

## 2. Código das páginas (`gerador-de-codigo-e-mvc.md` §8)

- [ ] Imports extra só em `packages_import`; código só nas áreas `start-code`; marcadores intactos e emparelhados.
- [ ] Model e View sem edições manuais (comparar com o JSON e voltar a gravar no Studio, se possível).
- [ ] Nenhuma área de botão termina com `return` incondicional sem Custom Return.
- [ ] Código compatível com o nível ECJ (v1: `-1.8`, ou o da JVM desde 1.8.3.240908; v2: `-16`).
- [ ] Blockly e código manual não duplicados na mesma ação.
- [ ] Imports `javax.*`/`jakarta.*` corretos para a versão (lembrar: `javax.persistence` é válido nas duas).

## 3. Dados

- [ ] Ligação explícita (nada de `Core.query(null, …)` para tabelas da aplicação; nada de ligação errada).
- [ ] Queries parametrizadas; sem concatenação de input; sem `::` (PostgreSQL).
- [ ] `hasError()` verificado; nulls tratados (`getResultList()` pode devolver `null`).
- [ ] Transações com rollback e `keepConnection()`; validações antes da transação.
- [ ] DAOs: estendem `BaseActiveRecord<X>`, anotações nos campos, coleções `Set`/`EAGER`, sem `cascade = ALL` indevido.
- [ ] `hbm2ddl.auto` revisto por ambiente; migrações Flyway versionadas.

## 4. Segurança (`acessos-e-seguranca.md` §4)

- [ ] Segredos em claro (pom, `main.xml`, `.properties`, código).
- [ ] Utilizador demo; `igrp.env`; páginas públicas; `PagesScapePermission`; botões sensíveis com Transaction.
- [ ] Validação no servidor de uploads, hidden e parâmetros; escape de HTML; tratamento de exceções.
- [ ] Palavras-passe com hashing; chaves secretas fora do código (v2: `IGRP_SECRET_KEY`).

## 5. Necessidade de ficheiros e diretórios

Classifica **cada** elemento numa categoria e justifica:

| Categoria | Critério | Ação recomendada |
|---|---|---|
| Necessário | Referenciado por código, configuração, BD ou build | Manter |
| Gerado automaticamente | `target/`, `overlays/` (extração do WAR do core pelo IDE), `bin/`, `.class`, `.idea/`, `.settings/`, `.classpath`, `.project`, `*.iml`, cópias em `target/apache-tomee` | Manter fora do git (`.gitignore`); não editar |
| Gerado pelo gerador, mas versionado | Model, View, XML/XSL/JSON das páginas | Manter e versionar; não editar à mão |
| Duplicado | Mesmo conteúdo em dois sítios sem papel distinto | Propor consolidação |
| Potencialmente obsoleto | Sem referências estáticas | **Requer investigação** (ver abaixo) |
| Requer investigação | Utilização não confirmável | Preservar e documentar |

Antes de propor eliminar algo, verifica (no IGRP a utilização é muitas vezes dinâmica):
1. Referências estáticas: imports, `grep` do nome da classe, página, tag ou ficheiro.
2. **BD do framework**: a página ou ação pode estar registada (ações, menus, transactions, perfis, partilhas) e ser chamada por
   URL `webapps?r=<app>/<pagina>/<acao>` sem nenhuma referência no código [DOC 5.2], [DOC 3.2.2], [PROJ].
3. Reflexão e convenções: Controllers são encontrados por nome (`action<Tag>`, `ExtractReserveCode`); métodos remotos
   `action<Procedure>` são referenciados apenas no JSON/XSL (RULES).
4. Configuração: `<mapping class>` nos `cfg.xml`, propriedades do `pom.xml`, `main.xml`, migrações Flyway (**nunca** remover migrações já aplicadas).
5. Artefactos do gerador: JSON/XML/XSL de uma página existente são necessários mesmo sem referências Java.
6. Reports, processos BPMN, domínios e tipos de documento vivem na BD e referenciam páginas e códigos.

Se não for possível confirmar (ex.: sem acesso à BD), classifica como **Requer investigação** e preserva.
Qualquer eliminação exige autorização explícita do utilizador, com a lista exata de ficheiros e a justificação.

## 6. Relatório de auditoria (formato)

1. Versão e evidências. 2. Resumo (contagem por severidade). 3. Achados (tabela: ID, área, severidade, evidência, fonte, recomendação).
4. Avaliação de ficheiros e diretórios (tabela por categoria). 5. Riscos de manutenção. 6. Limitações (o que não foi possível verificar).
