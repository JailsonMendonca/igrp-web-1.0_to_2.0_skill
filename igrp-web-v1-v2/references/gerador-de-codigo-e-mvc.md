# Gerador de Código, modelo MVC e código gerado

> Âmbito: Page Builder/Gerador de Código, ciclo XML/XSL, classes geradas, áreas preservadas, botões, Custom Return, navegação e parâmetros, Blockly.
> Aplicabilidade: (v1+v2) salvo indicação. Docs: 9.1–9.7, 11.1.1–11.1.3, 18.1, 18.3, 3.2.2. Verificado em 2026-11-20.

## 1. Como uma página funciona

- O browser recebe um **XML** (dados) com ligação para um **XSL** (modelo), e o HTML é construído no cliente. Os dados de negócio são
  preparados no servidor pelo Java da página [DOC 9.1 #1024].
- Cada página tem três classes no package `nosi.webapps.<app>.pages.<pagina>` [DOC 9.6 #1029], [DOC 18.1 #1125]:
  - `<Pagina>` (**Model**, `extends Model`): contentor de dados; campos com `@RParam(rParamName = "p_<tag>")`.
  - `<Pagina>View` (**View**, `extends View`): componentes e campos (`IGRPForm`, `IGRPToolsBar`, `IGRPButton`, `TextField`…), `render()`, `setModel()`.
  - `<Pagina>Controller` (**Controller**, `extends Controller`): `actionIndex()` e um `action<Tag>()` por botão; aplica as regras de negócio e devolve `Response`.
  - Confirmado nas 87 páginas de cada ramo oficial: todos os Controllers estendem `Controller`, as áreas são `packages_import`,
    `index`, uma por botão e `custom_actions`, nenhum Model nem View tem áreas `start-code`, e os artefactos ficam em
    `images/IGRP/IGRP2.3/app/<app>/<pagina>/` (na v2 também `IGRP2.4`) [CÓD-v1+v2], 2026-11-21.
- Artefactos do gerador em `images/IGRP/IGRP2.3/app/<app>/<pagina>/`: `<Pagina>.json` (definição do Studio), `.xml`, `.xsl` [CÓD-v1+v2], [PROJ].
  A página também é um registo na BD (ações/menus) e cria-se no Studio, nunca só com ficheiros [DOC 3.2.2 #1007], [DOC 5.2 #1021], [PROJ].

## 2. Regras do código gerado (obrigatórias)

1. **Não editar Model nem View.** São regenerados a cada gravação; alterações de layout, campos, labels e tipos fazem-se no separador DESIGN [DOC 18.1 #1125], [DOC 9.6 #1029].
2. **Código só nas áreas reservadas** do Controller [DOC 9.6], [DOC 11.1.1 #1072]:
   - `/*----#start-code(packages_import)----*/ … /*----#end-code----*/` — imports adicionais;
   - `/*----#start-code(index)----*/` e `/*----#start-code(<tag do botão>)----*/` — código de cada ação;
   - `/*----#start-code(custom_actions)----*/` — métodos auxiliares e métodos remotos (`action<Procedure>`).
   O resto (assinaturas, `model.load()`, `view.setModel`, `return this.renderView(view)`, o `return` final dos botões, os blocos `#gen-example`) é regenerado.
3. Não alterar, duplicar ou renomear os marcadores. O nome é exatamente `custom_actions`; o doc 13.3 escreve `custom actions`, o que está errado [DOC 13.3 #1101].
4. Imports: o cabeçalho é regenerado; qualquer import extra vai para `packages_import` [DOC 9.6], [PROJ].
5. Gravar no gerador e esperar a confirmação: fechar sem gravar perde o código gerado [DOC 9.1].
6. [PROJ] O merge das áreas preservadas é feito pelo gerador a partir das classes carregadas no servidor (`ExtractReserveCode`,
   presente nos dois ramos). Se acrescentares uma ação ao Controller fora do Studio, compila e reinicia o servidor antes de voltares a gravar a página no Studio. Senão, o código dessa ação perde-se.

## 3. Botões, retornos e Custom Return

- Cada botão gera `action<Tag>()` (tag `save` → `actionSave`) ao gravar a página [DOC 11.1.1 #1072].
- Propriedades: Action (página alvo), Class, Custom return, Icon, Label, Tag, Refresh Parent, Target, **Transaction** (acesso
  atribuído na Gestão de Acessos) [DOC 11.1.1].
- Targets: Alert Submit, Back, Change src, Close, Close and Refresh Parent, Confirm, FormList Lookup, Modal, New Tab, Popup, Right
  Panel, Scroll To Top, Self, Submit, Submit Ajax, Submit Form, Submit Modal, Submit Popup, Submit Right Panel, Void [DOC 11.1.1].
- Retornos [DOC 11.1.1], [DOC 18.3 #1128]:
  - `return this.renderView(view);` — desenha a página (índice);
  - `return this.redirect(app, pagina, acao[, this.queryString()]);` — padrão; novo pedido;
  - `return this.forward(app, pagina, acao[, this.queryString()]);` — reenvia os dados do Model (`p_*`); usar em erro de validação para não perder o input;
  - `Call` — usado em BPMN.
- Depois da área de cada botão o gerador emite `return this.redirect(…, this.queryString());` para a página *action* do botão [DOC 9.6].
  Consequência [PROJ, confirmado pelo XSL_CONTROLLER dos dois ramos]: **não termines a área com um `return` incondicional**
  (o `return` gerado fica inalcançável e a compilação falha). Usa `return` só dentro de condições, ou ativa o Custom Return.
- **Custom Return** [DOC 11.1.2 #1073]: o gerador deixa de emitir o `return` final e a área tem de devolver sempre um `Response`
  (ex.: `return this.forward("app","Pagina","index", this.queryString());`). Numa página nova, a primeira gravação com Custom Return
  falha a compilação, mas a página é guardada [DOC 9.1 #1024].

## 4. Parâmetros [DOC 18.3 #1128]

- Campos do Model recebem automaticamente `p_<tag>`.
- Ler: `Core.getParam("p_x")`, `getParamInt/Short/Long/Float/Double/BigDecimal/BigInteger/Array`, `Core.getParameters()`.
  Por defeito o valor é removido da sessão; a variante `(nome, isRemoved)` controla isso. No Controller: `this.getQueryString*`.
- Enviar: `this.addQueryString("nome", valor)` (forma padrão) ou `this.loadQueryString()` (todo o Model). **Não funcionam no `actionIndex`.**
  Para enviar a outra página inclui `this.queryString()` como 4.º argumento de `redirect`/`forward`.
- A partir do `actionIndex`: `view.btn_x.setLink("acao&nome=" + valor)` em botões, e `view.<lookup>.addParam("nome", valor)` em lookup/locator.
- Em tabelas, um campo `hidden` com **isKey** envia `p_<tag>` nos botões da linha (`view.<campo>.setParam(true)` é gerado) [DOC 10.10.1 #1030].

## 5. Propriedades de componentes e campos [DOC 9.4 #1027], [DOC 9.5 #1044]

- Separadores: STYLE (ID, Class, estilo), XSL (desmarcar *Default* permite editar o XSL do componente, mas bloqueia a edição das
  propriedades), COPY FROM, PROPERTIES; nos campos, RULES (eventos JS/Ajax).
- Propriedades comuns dos campos: Change (recarrega a página enviando os campos), Disabled, Field Size, Is Key, Java Type, Label,
  Maxlength, Placeholder, Readonly, Required, Right, Table, **Tag** (nome no Java), Value Parser.
- Restrições: box/tab/panel só recebem componentes; toolsbar só recebe botões; chart não recebe campos; Radio só em Table/Form List;
  Coordinates só com Map Viewer; Radio List e Checkbox List não se aplicam ao Form List; na View os campos só fazem output [DOC 9.1], [DOC 9.5].
- Página do tipo **Component** (sem menu): guarda componentes reutilizáveis copiados com COPY FROM; não é executável nem gera classes
  MVC (só XML/XSL/JSON) [DOC 9.3 #1026], [DOC 5.2 #1021].

## 6. Blockly [DOC 9.7 #1115], [DOC 10.5.4 #1116]

- O separador BLOCKLY gera Java no Controller a partir de blocos: categorias Logic, Loops, Math, Text, Variables; e as personalizadas
  Script Inicial, Core, DAO, inserir, editar, listar e apagar. As de DAO só aparecem com classes DAO mapeadas.
- O código gerado pelo Blockly **não se edita no Controller**: só se altera ou remove na workspace.
- Fluxo recomendado: montar os blocos, copiar o código gerado para a área `start-code` e editar aí [DOC 10.5.4 #1116].
- [PROJ] O código do Blockly fica antes da área preservada. Numa mesma ação não combines Blockly que gera `return` com código manual.

## 7. Colaboração e compilação

- [DOC 3.2.2 #1007] Criar uma página regista-a na BD partilhada e grava o JSON no servidor local. Gravar gera Model/View/Controller/XML/XSL
  só no servidor local, por isso é preciso fazer commit/push. Quem faz pull tem de abrir a página no gerador e **gravar** para a compilar.
- [PROJ] O Studio só copia o Java para `src/main/java` se a compilação passar. Classes novas só ficam visíveis após reiniciar o
  TomEE quando `reloadOnUpdate=false`.

## 8. Checklist da página (antes de a dar por terminada)

1. Imports extra só em `packages_import`.
2. Nenhum código fora das áreas `start-code`/`end-code`; marcadores intactos.
3. Nenhuma área termina em `return` incondicional, salvo com Custom Return.
4. Navegação para outra página com `this.queryString()` e `addQueryString`.
5. Model e View iguais aos gerados pelo Studio.
6. O código compila ao nível ECJ da versão (v1: `-1.8`, ou o da JVM desde 1.8.3.240908; v2: `-16`). Ver `v1-legacy.md` §6 e `v2-horizon.md` §6.
7. Teste final: abrir a página no Studio, gravar sem mudar nada e confirmar que compila [PROJ].
