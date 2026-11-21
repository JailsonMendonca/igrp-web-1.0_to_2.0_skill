# Rules, Remote/Ajax, JavaScript e CSS

> Aplicabilidade: (v1+v2), com `RemoteXML` e `remoteComboBoxXml` presentes nos dois ramos. Docs: 13.1–13.6, 19.1. Verificado em 2026-11-20.

## 1. Rules (separador RULES do campo) [DOC 13.1 #1099]

- **Event**: Blur, Change, Click, Keyup, Load.
- **Condition**: Equals, Differs, Contains, Checked, Unchecked, Greater than, Between, Not Null, Null, Start With / Not Start With,
  End With / Not End With, RegExp / Not RegExp, Custom (`{this}` = campo atual, `{tag}` = outro campo; ex.:
  `{this}==123 || {tag_nome}=='IMP_PAG_RE'`; arrays: `{this}.includes('X')`). Sem condição, a ação corre sempre.
- **Action** sobre os **Targets**: Show, Show Icon, Hide, Hide Icon, Disable, Enable, Required, Not Required, Clean Value, Readonly,
  Not Readonly, **Remote**, **Remote Combo Box**, **Remote List**, **Notify** (Message Type, Message). **Opposite Rule** desfaz a ação quando a condição é falsa.
- Para Ajax: **Procedure** = nome do método (`action` + Procedure, programado em `custom_actions`); **Request fields** = campos enviados
  como `p_<campo>`.
- Adiciona cada combinação Action/Targets ao SeparatorList da regra antes de gravar.

## 2. Métodos remotos [DOC 13.2 #1100]

```java
/*----#start-code(custom_actions)----*/
public Response actionGetPersonData() throws IOException, IllegalArgumentException, IllegalAccessException {
    String doc = Core.getParam("p_document_number");
    nosi.core.webapp.helpers.RemoteXML xml = Core.remoteXml();
    // … procurar na BD (DAO ou query parametrizada) …
    xml.addPropertie("name", nome).addMessage("info", "Dados obtidos.");   // tipos: success, info, warning, error
    this.format = Response.FORMAT_XML;
    return this.renderView(xml.build());
}
/*----#end-code----*/
```
- Remote Combo Box [DOC 13.3 #1101]: `Core.remoteComboBoxXml(map, view.<campo>, selectedIds[, prompt])` ou
  `Core.remoteComboBoxXml(QueryInterface, "tag", selectedIds, prompt)`. Usa query parametrizada (o exemplo do doc concatena `p_department`).
- Remote List [DOC 13.4 #1102]: o método recarrega o Model e preenche a tabela (`model.loadTable_<x>(Core.query(…).where(…).addInt(…))`) e devolve `renderView(view)`.
- Checkbox/Switch e Radio em tabela [DOC 13.5 #1103], [DOC 13.6 #1104]: recebem `p_<tag>` (id da linha) e `p_<tag>_check`
  (`"true"`/`"false"`). Devolvem só uma mensagem; se a mensagem for `error`, o campo volta ao estado inicial.

## 3. JavaScript e CSS personalizados [DOC 19.1 #1126], [DOC 9.4 #1027]

- Preferir RULES. Para código próprio: definir **ID**/Class no separador STYLE do componente e escrever o código nos separadores **JS**
  e **CSS** do gerador. Também é possível incluir URLs de ficheiros (ex.: `qrcode.min.js` da biblioteca igrpweb). Inline Style para estilo de um elemento.
- [PROJ v2.1.1] O CSS/JS da página fica guardado no JSON e embutido no XSL gerado (JS em base64). Não edites o `.xsl` à mão: altera no Studio.

## 4. Boas práticas

- [DOC] Métodos remotos só em `custom_actions`; nomes `action<Procedure>`; parâmetros `p_<campo>`.
- [ENG] Validar no servidor os parâmetros recebidos por Ajax (não confiar nas Rules do cliente).
