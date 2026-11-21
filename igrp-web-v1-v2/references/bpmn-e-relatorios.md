# BPMN Designer (processos) e Report Designer (relatórios)

> Aplicabilidade: (v1+v2), com as APIs `startProcess`, `getTaskHistory`, `getProcessDefinitionByProcessKey` e `getLinkReport*` presentes
> nos dois ramos [CÓD-v1+v2]. O procedimento de instalação do Activiti [DOC 7.1] é v1. Docs: 7.1–7.7, 8.1–8.5, 4.7. Verificado em 2026-11-20.

## 1. BPMN — conceitos e configuração [DOC 7.2 #1016]

- Processo = objetivo, etapas sequenciais, inputs (documentos e informação), outputs (notificações, documentos), resultado.
  Mapa de processos, Minhas Tarefas (lista, monitorização pela coordenação, estatísticas), Consulta de Processo.
- No BPMN Designer: escolher a aplicação, definir id e nome do processo, marcar **Executable**; *user tasks* associadas a páginas.
  A página associada a uma etapa tem de estar marcada como **de processo** no gerador. Gateways têm um *default flow* e uma condição.
- Acesso às etapas: orgânica → perfis → utilizadores (como menus e transactions). Iniciar um processo exige permissão. As tarefas
  podem ser assumidas, libertadas, consultadas em detalhe e executadas.
- Motor: Activiti. O portal descreve a instalação de um projeto `activiti-rest` separado (BD `db_activiti`, Eclipse/Tomcat) [DOC 7.1 #1205]
  (procedimento v1). Versões: bpmn-model 6.0.0 (v1) e bpmn-converter 7.1.0.M6 (v2) [CÓD].

## 2. BPMN — programação [DOC 7.5 #1019], [DOC 7.7 #1141]

| API | Uso |
|---|---|
| `model.loadFromTask(...)` | carrega dados de uma etapa anterior com componentes de nomes iguais |
| `actionSave` | corresponde ao botão "Seguinte" da etapa |
| `allowTask` | devolve `true`/`false` para controlar quem vê ou executa a tarefa |
| `Core.getProcessDefinitionByProcessKey(chave)` | informações do processo (chave = Process Id) |
| `Core.startProcess(chave, idDefinicao, params)` | inicia um processo a partir de uma página; parâmetros com prefixo **`x_`** |
| `this.inputDocsHasErrors()` | valida os documentos de input antes de executar o código da etapa |
| lista `TipoDocumentoEtapa` | controla os documentos de output visíveis numa etapa |
| `Core.getTaskHistory("TaskX")` | dados da **última** execução da etapa; com `BPMNConstants.PRM_TASK_ID` mostra a etapa num Iframe (`Core.getIGRPLink("igrp","Detalhes_tarefas", …)`) |

Recomendações oficiais [DOC 7.4 #1018], [DOC 7.6 #1140]:
- Não usar a palavra "task" no id da etapa (o igrpweb acrescenta-a).
- Radio-list do tipo **String** em processos.
- Evitar tags repetidas quando se usam tabs.
- Nomes de campo associados à etapa (ex.: `email-pedido`).
- Não atribuir tarefa ao perfil autenticado.
- Tarefas paralelas em vez de lógica ad-hoc.
- Processos em tabs: classe Helper com `switch` para mostrar ou esconder etapas; páginas criadas em separado e copiadas para os tabs.

Tipos de documento de etapa (Input/Output, obrigatório) [DOC 4.7 #1013].

## 3. Report Designer [DOC 8.1 #1105], [DOC 8.2 #1106]

- Escolher a aplicação; criar o report (título e **código único**); áreas **Head** e **Body**; Gravar e Preview.
- **Data Source** sobre uma ligação da aplicação, de 4 tipos: Objeto (tabela), Etapa (processo), **Query** (mais controlo), Página.
  Submenus `default_form_report` (aplicação, orgânica, utilizador, perfil, data), `form` (colunas `[NOME]`) e `table` (tabela,
  lista de marcas ou numerada). **Chaves** restringem os dados.
- Chamar a partir do código:
  ```java
  return Core.getLinkReport("codigo", new nosi.core.webapp.Report().addParam("id", id));     // HTML
  return Core.getLinkReportPDF("codigo", new nosi.core.webapp.Report().addParam("id", id));  // PDF
  ```
  Em tabela: `linha.setVer("igrp_studio","WebReport","get-report").addParam("code","x").addParam("p_id", id)` [DOC 8.1].
- **Contra prova** [DOC 8.4 #1209]: gerada (uuid) quando não é definida, obtida com `resp.getContent()`; `new Report().setContraprova(…)`.
  Consulta com `Core.getLinkContraProva[PDF](cp)` e `Core.getRepContraProvaPDF(cp)`. Envio em anexo com `Attachment` e `Core.mail_v2(…)`.
  O footer do report pode ter um QR code com o link da contra prova [DOC 8.5 #1222].
- Report HTML por código [DOC 8.3 #1200]: modelo Java + template HTML com substituição de marcadores, `this.format = Response.FORMAT_HTML`.
  [ENG] Escapar os valores inseridos no HTML.
