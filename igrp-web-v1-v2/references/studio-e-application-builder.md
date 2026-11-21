# IGRP Studio, Application Builder e ferramentas

> Aplicabilidade: (v1+v2). Docs: 4.1–4.7, 5.1–5.4, 6.1–6.2. Verificado em 2026-11-20.

## 1. IGRP Studio [DOC 4.1 #1008], [DOC 4.2 #1005]

- Ambiente de desenvolvimento dentro do igrpweb, disponível para utilizadores com **privilégios de desenvolvedor**.
- Componentes: **Page Builder** (interface; importar páginas, gerar CRUD e DAO, novas páginas), **BPMN Designer** (processos),
  **Report Designer** (relatórios; DataSource Página, Etapa, Processo, Objeto ou Query) e **Application Builder** (aplicações).
- Login local: `http://localhost:8080/IGRP/app/webapps?r=igrp/login/login`. A Home mostra o Tutorial IGRP, o IGRP Studio e as
  aplicações (Minhas Aplicações / Outras). Single-Sign-On com Active Directory, tabela de utilizadores ou federação de identidade.
- Top menu de workflow (Mapa de Processos, Minhas Tarefas). Minha Conta: palavra-passe, idioma, perfil.
- Em produção não há Studio: a gestão de acessos faz-se pelo menu da aplicação [DOC 12.1 #1133].

## 2. Aplicações [DOC 5.1 #1020]

- Criar no Studio ou no Application Builder. **Nome** pode mudar; **Código (dad)** é único e não pode mudar.
- Application Builder: editar, criar ligações de BD, exportar, importar, criar aplicações.
- *External / Host / Custom dad*: *Custom dad* cria um WAR à parte (outra instância); *Externo* cria um JAR das classes fora do WAR,
  no mesmo local ou num URL indicado. O doc chama "inativo" ao campo External e usa-o ao mesmo tempo (inconsistente).
- Desativar uma aplicação torna-a inacessível e o código continua ocupado. [PROJ] Inativa ≠ apagada (`tbl_env.status = 0`); reativa-se
  na lista de aplicações do Studio.
- Sem Home Page definida, a aplicação não abre corretamente: define-a nas propriedades da página [DOC 5.2 #1021].

## 3. Páginas [DOC 5.2 #1021]

- Campos: Title (alterável), **Code** (único e definitivo), Enable, Público (chamável por qualquer aplicação), Application, Module
  (só organização), Home Page, **Create menu** (desligar em páginas auxiliares: novo/inserir/lookup), Componente (só sem menu).
- Cada página = package com 3 classes (ver `gerador-de-codigo-e-mvc.md`). Botões da lista: Gerar Código (abre o gerador), editar
  propriedades, pré-visualizar, exportar.
- Uma página criada mas sem conteúdo gerado não executa: gera o código no gerador.

## 4. Partilha, domínios e tipos de documento

- **Partilha geral entre aplicações**: aplicação de origem → tipo de recurso (ex.: páginas) → aplicação de destino. O recurso fica
  disponível no campo Action de botões e lookups e por URL [DOC 4.3 #1009].
- **Domínios** [DOC 4.6 #1012]: listas chave/valor partilháveis; um domínio **público** pode ser usado por todas as aplicações, mas só
  é alterado pela aplicação que o criou. Usa-se no campo Domain de combobox, radiolist e checkboxlist.
  API: `Core.findDomainByCode(nome[, app])`, `Core.findDomainDescByKey(nome, chave[, app])` [CÓD-v1+v2].
- **Tipos de documento** [DOC 4.7 #1013]: documentos de Input/Output associados a etapas BPMN (tab Forms da etapa) e associação de um Report a uma etapa.

## 5. Base de dados e File Editor

- Ligações e `cfg.xml`: ver `dados-dao-hibernate.md` §1 [DOC 6.1 #1014].
- **File Editor** [DOC 6.2 #1015]: editor web de packages, classes e ficheiros de configuração da aplicação. Grava explicitamente.
  [ENG] Editar Model/View ou partes protegidas do Controller pelo File Editor não as protege da próxima gravação no gerador.

## 6. Exportar, importar e passar entre ambientes [DOC 5.4 #1023], [DOC 17.1 #1124]

- Exportar: Application Builder → exportar → escolher funcionalidades e ficheiros → **JAR**.
- Importar: Studio → Import (separadores: aplicação, livrarias externas, script SQL, imagens). Usa o separador certo: um
  ficheiro inesperado pode causar problemas no servidor ou no Studio.
- Depois de importar, configura a ligação de BD da aplicação no ambiente de destino.
- Ambientes separados para desenvolvimento, teste e produção.
