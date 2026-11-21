# Colaboração, controlo de versões, issues e ambientes

> Aplicabilidade: fluxo (v1+v2); ferramentas Eclipse/EGit/SVN são v1. Docs: 3.1.1–3.3.1, 5.4, 16.1, 17.1. Verificado em 2026-11-20.

## 1. Como as páginas circulam entre programadores [DOC 3.2.2 #1007]

1. Criar uma página regista-a na **BD partilhada** (fica visível para os outros) e grava o JSON no servidor local.
2. Gravar gera Model, View, Controller, XML e XSL **só no servidor local**.
3. Fazer commit/push para partilhar; os outros fazem pull.
4. Quem faz pull tem de **abrir a página no gerador e gravar**, para compilar no seu servidor.

Consequências [ENG/PROJ]:
- Versiona todos os artefactos da página: `<Pagina>.json/.xml/.xsl` e as 3 classes Java.
- A BD do framework (registos de páginas, menus, ações) é partilhada ou migrada à parte do git.

## 2. Repositórios

- GitHub ou GitLab NOSi: criar repositório, adicionar remote e push; partilhar com membros e privilégios (Settings → Members) [DOC 3.1.1 #1194], [DOC 3.1.2 #1006].
- Conflitos Git: marcadores `<<<<<<<`, `=======`, `>>>>>>>`; resolver, `git add`, commit; trabalhar em ramos isolados [DOC 3.3.1 #1201].
- Subversion com Eclipse (Subversive): procedimento legacy [DOC 3.2.2].
- O repositório oficial do framework usa mensagens de commit `vX.Y.Z.<build>: <descrição>` (ex.: `v2.1.1.261027: …`) [CÓD], [PROJ].

## 3. Issues do framework [DOC 16.1 #1114]

- Antes de abrir uma issue, verifica se já existe. Usa o template Bug: resumo, passos para reproduzir, ambiente, comportamento,
  logs/capturas, info git, possíveis correções.
- O portal indica o GitLab interno da NOSi. O repositório público atual é `github.com/NOSiCode-CV/IGRP-Framework` [REPO README].

## 4. Passagem entre ambientes [DOC 5.4 #1023], [DOC 17.1 #1124]

1. Exportar a aplicação (Application Builder → exportar → funcionalidades → ficheiros → JAR).
2. Importar no ambiente de destino (Studio → Import, separador da aplicação; outros separadores para livrarias, script SQL e imagens).
3. Configurar a ligação de BD da aplicação no destino (Application Builder → Configurar Base de Dados) e o `cfg.xml` com os mapeamentos DAO.
4. Dica oficial: os DAOs e o `cfg.xml` atualizados "atualizam a BD sem scripts". Isto depende de `hbm2ddl.auto=update` [CÓD-v1+v2].
   [ENG] Em teste e produção, prefere scripts ou migrações versionadas e revistos.

Ambientes recomendados: desenvolvimento, teste, produção (`igrp.env`: `dev`, `test`, `sta`, `prod`) [DOC 5.4], [PROJ main.xml].
