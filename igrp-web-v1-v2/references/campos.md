# Campos do gerador (GC - Fields)

> Aplicabilidade: (v1+v2). Docs: 9.5, 11.1–11.26 (32 documentos). Verificado em 2026-11-20.

## 1. Regras gerais [DOC 9.5 #1044]

- Cada campo (exceto Button) gera `get<Tag>()`/`set<Tag>()` no Model e recebe o parâmetro `p_<tag>`.
- **Java Type** define o tipo no Model (String, Integer, int, String[]…). Escolhe o tipo da coluna da BD.
  [PROJ] Com `int` primitivo, a ausência de seleção chega como `0` e `@NotNull` não a apanha: valida com `Core.isNullOrZero(...)` ou usa `Integer`.
- **Maxlength** igual ao tamanho da coluna da BD, para evitar erros (Text, Text Area) [DOC 11.3.1 #1076], [DOC 11.22 #1094].
- **Change** recarrega a página enviando os campos preenchidos.

## 2. Referência por campo

| Campo | Comportamento / propriedades | Programação | Doc |
|---|---|---|---|
| Button | sem dados; gera `action<Tag>`; Target, Transaction, Custom Return… | ver `gerador-de-codigo-e-mvc.md` §3 | 11.1.1–11.1.3 |
| Text / Text Area | String; vazio devolve `""` | `model.set<x>(…)` / `model.get<x>()` | 11.3.1, 11.22 |
| Number | só números; Min/Max Value; **Calculation**: expressão com `{tag}` (incl. ternário) e Number Format `ceil`, `ceil:X`, `round`, `round:X`, `floor`, `abs`, `fixed:X` | conversões `Core.toInt(s[, defeito])` (0 em erro), `toShort`, `toLong`, `toDouble`… | 11.2.1, 11.2.2 |
| Select / Combobox | recebe `Map` chave→valor e devolve a chave; Domain; Multiple (`String[]`); Dynamic Option | `view.<x>.setValue(map)` ou `setQuery(...)`; selecionar com `model.set<x>(chave)`; `LinkedHashMap` mantém a ordem; `<null,"--select--">` bloqueia a submissão se Required | 11.4.1, 11.4.2 |
| Load Service Data (Select) | pesquisa dinâmica enquanto o utilizador escreve | `view.<x>.propertie().setProperty("load_service_data", Core.getIGRPLink(app, pagina, acao))`; o método `action<X>` recebe `p_search_data` e devolve JSON (`id`/`text`) | 11.4.4 #1224 (suportado nos dois ramos) |
| Checkbox | Switch; Integer: marcado com 1; String: marcado com `"1"`, devolve `"1"` ou `""` | `model.setActive(1)` | 11.5 #1077 |
| Checkbox List | `Map` → devolve `String[]` das chaves marcadas; Java Type `String[]`; Child Size; Domain | `model.set<x>(new String[]{…})` | 11.6 #1078 |
| Radio | em tabela: `<tag>` e `<tag>_check`; valor selecionado em `p_<tag>_fk` | `Core.getParam("p_<tag>_fk")` | 11.18 #1090 |
| Radio List | `Map` → devolve a chave; Domain | igual ao Select | 11.19 #1091 |
| Date | String `dd-MM-yyyy`; From/To; **Readonly** recomendado (data só pelo seletor) | `Core.dateToString(data, "dd-MM-yyyy")`, `Core.ToDate(str, "dd-MM-yyyy")` | 11.9 #1081 |
| Time | String `HH:mm` (24 h); hora inválida não é mostrada | `Core.dateToString(d, "HH:mm")`, `Core.ToChar(…)` | 11.24 #1096 |
| Email | valida o formato; envio por `Core.mail(…)` com SMTP no `main.xml` (`mail.smtp.*`, `mail.user`, `mail.password`) | — | 11.10 #1082 |
| External Link / Hyperlink | URL validado / link sem executar Java (Action, Target, Custom Action, Icon, Class) | — | 11.11, 11.13 |
| Hidden | guarda ids fora da vista; isKey em tabela envia `p_<tag>` | — | 11.12 #1084 |
| Image | exibição e upload; Croppie, Rounded, Auto Upload (grava e envia o id) | `view.<x>.setValue(Core.getLinkFile(id))`; id em `p_<x>` | 11.14 #1086 |
| Lookup | Action (página de lista), LookupParams (Target Field / Value Field) | a página de lista precisa de um campo **Value Parser** e de um hidden isKey | 11.15 #1087 |
| Password / Virtual Keyboard | texto escondido / teclado virtual contra keyloggers | `Core.encrypt(model.getPassword())` | 11.16, 11.26 |
| Plain Text, Separator, Color, Range, Text Editor, Coordinates | texto, separador visual, cor (Format), inteiro (RangeMin/Max), conteúdo formatado (dimensionar a coluna), coordenadas via Map Viewer | `model.set…`, `view.<x>.setLabel(…)` | 11.17, 11.21, 11.7, 11.20, 11.23, 11.8 |
| Upload File | Accept, Multiple, Rend Value, Target Rend; ficheiro em `p_<tag>` | `Integer id = Core.saveFile("p_<tag>")` (> 0 em sucesso) | 11.25 #1097 |

## 3. Observações de segurança (não oficiais)

- [ENG] `Core.encrypt` é cifra reversível com a chave do framework. Para credenciais próprias da aplicação usa hashing com sal (ex.: bcrypt).
- [ENG] Hidden, Accept do Upload e Required são controlos do cliente: valida sempre no servidor (tipo, tamanho, permissões, ids).
- [ENG] Conteúdo do Text Editor reapresentado em HTML deve ser sanitizado.
- [PROJ v2.1.1] Campos Image: o `setModel` gerado não liga o campo ao Model. Usa `view.<campo>.setValue(...)`.
