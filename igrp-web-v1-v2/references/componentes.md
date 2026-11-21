# Componentes do gerador (GC - Componentes)

> Aplicabilidade: (v1+v2), gerador IGRP2.3 presente nos dois ramos. A v2 tem também o gerador 2.4 [CÓD-v2].
> Docs: 10.1–10.29 (52 documentos). Os documentos "Programação Blockly" mostram o código gerado pelo Blockly a partir de blocos.
> Verificado em 2026-11-20.

## 1. Convenções gerais

- Um componente de lista (Table, Separator List, Form List) gera no Model uma classe interna `<Pagina>.<Componente>`. Cada linha é
  um objeto dessa classe, e a lista é atribuída com `model.set<Componente>(lista)` ou carregada com `model.loadTable_<x>(query)` [DOC 10.10.2 #1032].
- Componentes de apresentação recebem valores pelo Model (`model.set<Componente>_<campo>(…)`) ou pela View (`view.<x>.setValue(…)`).
- Propriedades frequentes: HasTitle, Title, Collapsible, Collapsed, Boxed; Target e Refresh Parent em componentes com link [DOC 10.4.1, 10.5.1].

## 2. Referência por componente

| Componente | Configuração (propriedades) | Programação | Doc |
|---|---|---|---|
| Form | HasTitle, Collapsible, Collapsed | `model.set…`/`get…`; `model.load(query)`; padrão `isEdit` + id hidden; `forward` em erro mantém o input | 10.5.1–10.5.4 (#1035, #1036, #1037, #1116) |
| Table | campos de saída; hidden **isKey** envia `p_<tag>` nos botões da linha | lista `<Pagina>.<Tabela>` ou `model.loadTable_<x>(Core.query(…))` com aliases = tags; filtros com `andWhere` | 10.10.1–10.10.3 (#1030–1032) |
| Filtros em tabela | botão de pesquisa com **Custom Return** e `forward` para o index; Target **Submit Ajax** recomendado | DAO `find().andWhere(…, "like", …)` | 10.10.4 #1033 |
| Checkbox em tabela | `<tag>` = id da linha, `<tag>_check` = estado (marcado quando iguais) | `Core.extractCheckBox(Core.getParamArray("p_<tag>_fk"), Core.getParamArray("p_<tag>_check_fk"))` → `getChekedIds()` / `getUncheckedIds()` | 10.10.5 #1034 |
| Form List | campos sempre editáveis; Filter, No Add, No Delete, Order Table | campos `IGRPSeparatorList.Pair` (chave/valor); linhas eliminadas em `getP_<formlist>_del()` | 10.6.1–10.6.2 (#1041, #1121) |
| Separator List | Dialog (formulário em modal), Order Table | `Pair` por campo; `<sep>_id` da linha; `getP_<sep>_edit()` e `getP_<sep>_del()`; aninhado: idem por nível | 10.7.1–10.7.4 (#1038, #1040, #1120) |
| Upload em Separator List | botão save como **submit ajax** | `Core.uploadMultiple("p_<tag>_fk")` → `List<UploadedFile>`; `Core.saveFile(bytes, nome, mime)` → id | 10.7.2 #1039 |
| Chart | Chart Type, Filter, Filter Type, Remote Filter | lista `new <Pagina>.<Chart>(eixoX, eixoY, valor)` → `model.set<Chart>(lista)`; 2D/3D conforme o Model | 10.4.1–10.4.3 (#1042, #1045, #1123) |
| Calendar | Header Views, Views | eventos com Title, Description, Id, início e fim (data e hora com separador `T`), Color | 10.1.x (#1047, #1210) |
| Carousel | imagens | `model.loadCarousel_1(Core.query(…  carousel_1_label, carousel_1_img))` | 10.2.x (#1048, #1211) |
| Circle Stat Box / Small Box / Stat Box / Info Panel | Description/Value, Link/Url, Url Label, Percent, Size, Target, Refresh Parent | `model.set<box>_val(…)`, `model.set<box>_url(Core.getIGRPLink(app, pagina, acao))` | 10.3, 10.8, 10.9, 10.18 |
| Timeline | título, texto, data | lista a partir de uma tabela | 10.11.x |
| Tree Menu | Has Tooltip, **Remote** (níveis seguintes carregados a pedido), Target, Value parser, Search, Call on load | lista `<Pagina>.Treemenu_<n>` com id, pai, filho, link | 10.12.x (#1065, #1216) |
| Vertical Menu / Treelist / Toolsbar | Dynamic Menu (botões por Java); Toolsbar: Align, Icon Inline, Outline, Style | — | 10.13, 10.27, 10.28 |
| View | só output; Imagem | `model.setView_<x>_img(Core.getLinkFile(id))` | 10.14.x (#1069, #1218) |
| Tab | Justified, Control Active | separador ativo definido no index (`model.set<tab>("1")`) | 10.26 #1062 |
| Box, Panels | só recebem componentes | — | 10.15, 10.22 |
| Iframe | Action, Boxed | `model.setIframe_1_src(url)` | 10.17 #1051 |
| Section Header, Paragraph | texto no design ou por código | `view.<x>.setValue(…)` | 10.23, 10.25 |
| Map Chart / Map Viewer / Leaflet Map | geojson Basemap, Data e Configuration (json), Tooltip; Map Viewer captura coordenadas para o campo Coordinates | — | 10.19–10.21 |
| Finger Print, Quick Button Box, Video | View Only; URL; Boxed/Text | — | 10.16, 10.24, 10.29 |

## 3. Padrões de página documentados

- **Lista + Formulário** [DOC 10.10.1 #1030]: na página de lista, botão *Add* (Modal, Refresh parent), *edit* (Submit Modal com id
  isKey) e *delete* (Submit na própria lista). A página de formulário trata `isEdit`/id e `save`. O CRUD Generator gera este padrão [DOC 4.5 #1011].
- **Dashboard** [DOC 10.4.2 #1045]: formulário de filtro com botão Custom Return que faz `forward` para o index, mais gráficos e caixas.

## 4. Limitações da documentação

Os documentos #1046, #1047, #1056, #1058, #1066, #1067 e #1068 são quase vazios e vários dos "Programação Blockly" têm o código só
em imagem. Para propriedades não documentadas, consulta o separador PROPERTIES no gerador. [PROJ] O JSON da página é a fonte de verdade das propriedades.
