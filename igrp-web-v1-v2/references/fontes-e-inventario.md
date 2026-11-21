# Fontes, etiquetas e inventário da documentação

> Âmbito: política de fontes do skill e inventário dos 169 documentos do portal oficial.
> Versões: v1 (igrpweb "legacy", builds 1.x) e v2 (IGRP "Horizon", builds 2.x). Verificado em 2026-11-21.

## 1. Fontes e hierarquia

| Etiqueta | Fonte | Peso |
|---|---|---|
| `[DOC n.n #p_id]` | Portal oficial `docs.igrp.cv`, app `tutorial` (169 documentos). URL de cada documento: `https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=<p_id>&dad=tutorial&isPublic=1` | Fonte principal |
| `[REPO <ficheiro>]` | Repositório oficial `github.com/NOSiCode-CV/IGRP-Framework` (`README.md`, `docs/igrp_versions.md`). O próprio portal remete para este README em [DOC 2.2.1 #1149]. | Oficial, complementar |
| `[CÓD-v1 <caminho>]` | Código oficial, ramo `develop` @6d7b32f (core 1.9.1.261027). | Evidência |
| `[CÓD-v2 <caminho>]` | Código oficial, ramo `igrp-horizon-dev` @230df4c (core 2.1.1.261027). | Evidência |
| `[CÓD-v1+v2]` | Comportamento ou API confirmado nos dois ramos. | Evidência |
| `[PROJ]` | Regra empírica observada num projeto real (gerador 2.1.1) e confirmada no código oficial. | Evidência de projeto |
| `[MVN Central]`, `[MVN Nexus]`, `[MVN]` | Metadados dos repositórios Maven do core: `repo1.maven.org/maven2/cv/igrp/` (2026-10-19) e `sonatype.nosi.cv/repository/maven-releases/` (2026-10-27). Servem para datar e listar builds. | Evidência |
| `[ENG]` | Recomendação geral de engenharia de software. **Não é regra oficial do IGRP.** | Recomendação |

Regras de uso:

1. A doc do portal prevalece sobre as outras fontes. Quando o código oficial contradiz a doc, indica as duas e aplica o comportamento do código da versão identificada, assinalando a divergência.
2. O portal declara-se "preparado para a versão legacy" e chama `horizon` à v2 [DOC 2.1.1 #1145]. A maior parte dos documentos não distingue versões. Neste skill, um tema só é marcado `(v1+v2)` quando as APIs e os artefactos que descreve existem nos dois ramos oficiais.
3. Não uses documentação do IGRP 3.0 ("New Horizon") nem do IGRP v0 (PL/SQL) como fonte, comparação ou recomendação.
4. Se uma informação não estiver em nenhuma das fontes acima, diz que não está documentada. Não a inventes.
5. Ao citar, usa a etiqueta e, para o portal, o número da secção e o `p_id`.

## 2. Exclusões e alertas sobre o portal

| Item | Tratamento |
|---|---|
| Faixa e ligação para a documentação IGRP 3.0 no doc 1.1 (#1000) | Excluída (outra versão) |
| O portal corre o core `211115` (`<version>` no XML de 2026-11-21), uma build v1 de novembro de 2021, com XSL aplicado no browser | Confirma que a maior parte da doc descreve a v1 antiga: valida as builds atuais no código (`variantes-e-builds.md`) |
| Passos marcados "DESCONTINUADOS" no doc 2.2.1 (#1149) (importar o template Eclipse) | Só como histórico v1 |
| Ligações para documentos SharePoint internos (`services.nosi.cv`) em #1014, #1024, #1044 | Inacessíveis; não usadas |
| Vídeo-aulas e conteúdo em imagens (1085 imagens nos 169 docs) | Não verificáveis como texto; regras não derivadas apenas de imagens |
| p_id 1000–1240 fora do menu (72 sondados) | Não existem (o portal devolve um marcador vazio) |
| Documentos quase vazios (#1046, #1047, #1056, #1058, #1066, #1067, #1068) | Só identificam o componente; nenhuma regra derivada deles |
| Exemplos de código com defeitos (ver estado no inventário) | Usar a regra, não copiar o exemplo sem rever |
| Exemplos que concatenam valores do utilizador em SQL (#1037, #1131, #1033, #1101) | Não reproduzir; usar parâmetros nomeados [DOC 18.6 #1131] |

## 3. Correções às fontes verificadas no código

| Doc | O doc diz | Código oficial |
|---|---|---|
| 18.3 #1128 | `Core.getParamLog(...)` | O método é `Core.getParamLong(...)` [CÓD-v1+v2] |
| 18.5 #1130 | `transactionQuery.roolback()` | `roolback()` é mesmo o nome do método em `QueryInterface` [CÓD-v1+v2] |
| 15.1 #1110 | `nosi.base.activeRecord.BaseActiveRecord` | `nosi.base.ActiveRecord.BaseActiveRecord` [CÓD-v1+v2] |
| 2.4.3 #1153 | Título refere `db_igrp_config.xml` | O conteúdo e o código usam `hibernate-igrp-core.cfg.xml` + `hibernate-igrp-core.properties` (`${igrp.db.*}`) [CÓD-v1+v2] |
| 2.4.4 #1219 | Propriedades `db.user/db.password/db.dsn` | O template atual usa `igrp.db.user/igrp.db.password/igrp.db.dsn/igrp.db.driver` e `igrp.migration.location` [PROJ] |
| 21.1 #1221 | TomEE 10.0.1 | O TomEE depende da build: 9.1.x nas 2.0.0 até 2.0.0.250217, 10.0.x desde 2.0.0.250220, 10.1.x na 2.1.0 e 10.2.0 na 2.1.1 [CÓD-v2 `IGRP/pom.xml`] |
| 21.2 #1223 | `ResultSet.Record.RowList` → `rowList` | Confirmado: `RowList` (v1) e `rowList` (v2) [CÓD `nosi/core/webapp/databse/helpers/ResultSet.java`] |

## 4. Inventário (169 documentos)

Aplicabilidade: `v1+v2` = conceitos e APIs presentes nos dois ramos; `v1` = ferramentas ou procedimentos legacy (Eclipse, Tomcat 9, JDK 8, SVN); `v2` = específico da v2.
O registo completo por documento (conceitos, tecnologias, componentes, regras, práticas, relações) está no relatório de validação documental, fora do pacote do skill.

<!-- INVENTARIO:INICIO -->
| Nº | Título | p_id | Atualizado | Aplicabilidade | Estado |
|---|---|---|---|---|---|
| 1.1 | igrpweb - Apresentação | 1000 | 24-03-2025 | v1+v2 | ok |
| 2.1.1 | Instalação Java | 1145 | 04-01-2025 | v1 (+ nota v2: JDK 17) | desatualizado |
| 2.1.2 | Instalação Eclipse ou qualquer IDE Java | 1146 | 04-01-2025 | v1 (+ alternativa IntelliJ/Maven) | ok |
| 2.1.3 | Instalação PostgreSQL | 1148 | 28-07-2021 | v1+v2 | ok |
| 2.1.4 | (Opcional) Instalação Apache TomEE | 1147 | 04-01-2025 | v1 | desatualizado |
| 2.2.1 | Geração de archetype ou Importação do Projeto | 1149 | 04-01-2025 | v1+v2 | desatualizado |
| 2.3.1 | Adição do Servidor Apache no Eclipse | 1151 | 17-12-2020 | v1 | só v1 |
| 2.3.2 | Configuração do Servidor Apache Tomcat | 1154 | 22-12-2020 | v1 | só v1 |
| 2.3.3 | Configuração do Ambiente Eclipse | 1150 | 27-04-2021 | v1 | só v1 |
| 2.4.1 | Configuração do Java Build Path | 1206 | 26-04-2021 | v1 | desatualizado, só v1 |
| 2.4.2 | Configuração do ficheiro main.xml | 1152 | 17-12-2020 | v1+v2 | ok |
| 2.4.3 | Criação de base de dados e Configuração do "db_igrp_config.xml" | 1153 | 11-05-2022 | v1+v2 | desatualizado |
| 2.4.4 | Configuração do Pom.xml | 1219 | 02-02-2023 | v1+v2 | desatualizado |
| 2.4.5 | Execução do Projeto igrpweb Template | 1004 | 11-01-2021 | v1 | só v1 |
| 2.5 | Falha na sincronização Eclipse-Servidor Local (Troubleshooting) | 1202 | 17-08-2021 | v1 | só v1 |
| 2.6 | Execução do Projeto no Intellij IDE | 1220 | 04-04-2023 | v1+v2 | ok, desatualizado |
| 3.1.1 | GitHub | 1194 | 23-12-2020 | v1 (ferramenta); conceito v1+v2 | só v1 |
| 3.1.2 | NOSi GITLab | 1006 | 23-12-2020 | v1 (ferramenta); conceito v1+v2 | ok |
| 3.2.2 | Subversion | 1007 | 23-12-2020 | v1+v2 (fluxo); ferramenta SVN v1 | ok |
| 3.3.1 | Resolver Conflitos do Git | 1201 | 19-07-2021 | v1+v2 | ok |
| 4.1 | IGRP Studio - Apresentação | 1008 | 17-08-2021 | v1+v2 | ok |
| 4.2 | Página Login e Página Home | 1005 | 23-12-2020 | v1+v2 | ok |
| 4.3 | Partilha Geral entre Aplicações | 1009 | 16-10-2020 | v1+v2 | ok |
| 4.4 | SQL Tools | 1010 | 16-10-2020 | v1+v2 | ok |
| 4.5 | CRUD/DAO Generator | 1011 | 16-10-2020 | v1+v2 | ok |
| 4.6 | Gestão de Domínio | 1012 | 28-07-2021 | v1+v2 | exemplo com defeitos |
| 4.7 | Gestão Tipo Documento | 1013 | 17-08-2021 | v1+v2 | ok |
| 5.1 | Criação uma Nova Aplicação | 1020 | 18-10-2020 | v1+v2 | exemplo com defeitos |
| 5.2 | Criação de uma Nova Página | 1021 | 08-05-2021 | v1+v2 | ok |
| 5.3 | Importar Script SQL | 1022 | 18-10-2020 | v1+v2 | incompleto |
| 5.4 | Exportar e Importar Aplicação | 1023 | 08-01-2021 | v1+v2 | ok |
| 6.1 | Base de Dados - Configuração | 1014 | 16-10-2020 | v1+v2 | ok, ligação inacessível |
| 6.2 | File Editor | 1015 | 17-10-2020 | v1+v2 | ok |
| 7.1 | Manual de instalação de Activiti no Framework igrpweb | 1205 | 10-01-2022 | v1 (ferramenta); conceito v1+v2 | ligação inacessível |
| 7.2 | BPMN - Business Process Model Notation | 1016 | 17-10-2020 | v1+v2 | ok |
| 7.3 | BPMN - Exemplo Prático | 1017 | 17-10-2020 | v1+v2 | incompleto |
| 7.4 | BPMN - Criação de Processos com Tabs | 1018 | 17-10-2020 | v1+v2 | ok |
| 7.5 | BPMN - Funções Úteis | 1019 | 13-03-2024 | v1+v2 | ok |
| 7.6 | BPMN - Dicas de Design | 1140 | 03-11-2020 | v1+v2 | incompleto |
| 7.7 | BPMN - Dicas de Programação | 1141 | 03-11-2020 | v1+v2 | ok |
| 8.1 | Report Designer | 1105 | 21-06-2021 | v1+v2 | ok |
| 8.2 | Report Designer - Exemplos Práticos | 1106 | 16-02-2024 | v1+v2 | ok |
| 8.3 | Report em HTML usando Classes | 1200 | 19-03-2021 | v1+v2 | exemplo com defeitos |
| 8.4 | Report Designer - Funções Úteis | 1209 | 27-09-2021 | v1+v2 | ok |
| 8.5 | Report Designer - Exemplo HTML com Footer modificado | 1222 | 16-02-2024 | v1+v2 | ok |
| 9.1 | Gerador de Código | 1024 | 18-10-2020 | v1+v2 | ok, duplicado, ligação inacessível |
| 9.2 | Design de Páginas | 1025 | 18-10-2020 | v1+v2 | duplicado |
| 9.3 | Copiar Componentes de outra Página | 1026 | 18-10-2020 | v1+v2 | ok |
| 9.4 | Propriedades dos Componentes e Campos | 1027 | 18-10-2020 | v1+v2 | ok |
| 9.5 | Propriedades Comuns dos Campos | 1044 | 20-10-2020 | v1+v2 | ok, ligação inacessível |
| 9.6 | Geração de Código - Exemplo | 1029 | 18-10-2020 | v1+v2 | ok |
| 9.7 | igrpweb Blockly | 1115 | 17-08-2021 | v1+v2 | ok |
| 10.1.1 | Calendar - Configuração | 1047 | 20-08-2021 | v1+v2 | quase vazio |
| 10.1.2 | Calendar - Programação Blockly | 1210 | 02-09-2021 | v1+v2 | ok |
| 10.2.1 | Carousel - Configuração | 1048 | 20-08-2021 | v1+v2 | ok |
| 10.2.2 | Carousel - Programação Blockly | 1211 | 20-08-2021 | v1+v2 | ok |
| 10.3.1 | Circle Stat Box- Configuração e Programação | 1049 | 25-08-2021 | v1+v2 | incompleto |
| 10.3.2 | Circle Stat Box- Programação Blockly | 1212 | 25-08-2021 | v1+v2 | ok |
| 10.4.1 | Chart - Configuração e Programação | 1042 | 27-10-2020 | v1+v2 | ok |
| 10.4.2 | Chart - Exemplo Prático | 1045 | 20-10-2020 | v1+v2 | incompleto |
| 10.4.3 | Chart - Programação com Blockly | 1123 | 27-08-2021 | v1+v2 | ok |
| 10.5.1 | Form - Configuração | 1035 | 19-10-2020 | v1+v2 | ok |
| 10.5.2 | Form - Programação com classes DAO | 1036 | 19-10-2020 | v1+v2 | ok |
| 10.5.3 | Form - Programação com Query | 1037 | 19-10-2020 | v1+v2 | exemplo com defeitos |
| 10.5.4 | Form - Programação com Blockly | 1116 | 17-08-2021 | v1+v2 | ok |
| 10.6.1 | Form-List - Configuração e Programação | 1041 | 19-10-2020 | v1+v2 | ok |
| 10.6.2 | Programação de Form-List com Blockly | 1121 | 17-08-2021 | v1+v2 | ok |
| 10.7.1 | Separador-List - Configuração e Programação | 1038 | 19-10-2020 | v1+v2 | ok |
| 10.7.2 | Upload em Separador List - Configuração e Programação | 1039 | 19-10-2020 | v1+v2 | ok |
| 10.7.3 | Separador-List dentro de outro Separador-List | 1040 | 19-10-2020 | v1+v2 | ok |
| 10.7.4 | Programação de Separador-Lista com Blockly | 1120 | 17-08-2021 | v1+v2 | ok |
| 10.8.1 | Small Box - Configuração e Programação | 1060 | 11-09-2021 | v1+v2 | ok |
| 10.8.2 | Small Box - Programação Blockly | 1213 | 11-09-2021 | v1+v2 | ok |
| 10.9.1 | Stat Box - Configuração e Programação | 1061 | 11-09-2021 | v1+v2 | ok |
| 10.9.2 | Stat Box - Programação Blockly | 1214 | 11-09-2021 | v1+v2 | ok |
| 10.10.1 | Table - Configuração | 1030 | 19-10-2020 | v1+v2 | ok |
| 10.10.2 | Table - Programação com Classes DAO | 1032 | 19-10-2020 | v1+v2 | ok |
| 10.10.3 | Table - Programação com Query | 1031 | 19-10-2020 | v1+v2 | ok |
| 10.10.4 | Filtros em Tabelas | 1033 | 19-10-2020 | v1+v2 | exemplo com defeitos |
| 10.10.5 | Checkbox em Tabelas - Configuração e Programação | 1034 | 08-08-2024 | v1+v2 | exemplo com defeitos |
| 10.10.6 | Table - Programação com Blockly | 1117 | 17-08-2021 | v1+v2 | ok |
| 10.11.1 | Timeline - Configuração | 1063 | 13-09-2021 | v1+v2 | quase vazio |
| 10.11.2 | Timeline - Programação Blockly | 1215 | 13-09-2021 | v1+v2 | ok |
| 10.12.1 | Tree Menu - Configuração e Programação | 1065 | 16-09-2021 | v1+v2 | ok |
| 10.12.2 | Tree-Menu - Programação Blockly | 1216 | 17-09-2021 | v1+v2 | ok |
| 10.13.1 | Vertical Menu - Configuração | 1067 | 17-09-2021 | v1+v2 | quase vazio |
| 10.13.2 | Vertical Menu - Programação Blockly | 1217 | 17-09-2021 | v1+v2 | ok |
| 10.14.1 | View - Configuração e Programação | 1069 | 24-09-2021 | v1+v2 | exemplo com defeitos |
| 10.14.2 | View - Programação Blockly | 1218 | 24-09-2021 | v1+v2 | ok |
| 10.15 | Box - Configuração | 1046 | 20-10-2020 | v1+v2 | quase vazio |
| 10.16 | Finger Print -   Configuração | 1050 | 20-10-2020 | v1+v2 | curto |
| 10.17 | Iframe - Configuração | 1051 | 25-04-2021 | v1+v2 | ok |
| 10.18 | Info-Painel - Configuração | 1052 | 20-10-2020 | v1+v2 | ok |
| 10.19 | Leaftet Map | 1053 | 20-10-2020 | v1+v2 | exemplo com defeitos |
| 10.20 | Map Chart - Configuração | 1054 | 20-10-2020 | v1+v2 | ok |
| 10.21 | Map Viewer - Configuração | 1055 | 20-10-2020 | v1+v2 | ok |
| 10.22 | Panels - Configuração | 1056 | 20-10-2020 | v1+v2 | quase vazio |
| 10.23 | Paragraph - Configuração | 1057 | 20-10-2020 | v1+v2 | ok |
| 10.24 | Quick Button Box - Configuração | 1058 | 20-10-2020 | v1+v2 | quase vazio |
| 10.25 | Section Header - Configuração e Programação | 1059 | 20-10-2020 | v1+v2 | exemplo com defeitos |
| 10.26 | Tab - Configuração e Programação | 1062 | 20-10-2020 | v1+v2 | ok |
| 10.27 | Toolsbar - Configuração | 1064 | 20-10-2020 | v1+v2 | ok |
| 10.28 | Treelist - Configuração | 1066 | 20-10-2020 | v1+v2 | quase vazio |
| 10.29 | Vídeo - Configuração | 1068 | 20-10-2020 | v1+v2 | quase vazio |
| 11.1.1 | Button - Configuração e Programação | 1072 | 21-10-2020 | v1+v2 | ok |
| 11.1.2 | Custom Return | 1073 | 21-10-2020 | v1+v2 | ok |
| 11.1.3 | Programação de botão Editar e Eliminar com Blockly | 1118 | 17-08-2021 | v1+v2 | ok |
| 11.2.1 | Number - Configuração e Programação | 1074 | 10-03-2021 | v1+v2 | ok |
| 11.2.2 | Number - Propriedade Calculation | 1075 | 05-02-2024 | v1+v2 | ok |
| 11.3.1 | Text - Configuração e Programação | 1076 | 21-10-2020 | v1+v2 | ok |
| 11.4.1 | Select/ComboBox - Configuração e Programação | 1070 | 06-09-2024 | v1+v2 | ok |
| 11.4.2 | Campo de Seleção - Programação com DAO | 1071 | 21-10-2020 | v1+v2 | ok |
| 11.4.3 | Preencher Combobox, Checkbox, Radiolist com Blockly | 1119 | 17-08-2021 | v1+v2 | ok |
| 11.4.4 | Load Service Data | 1224 | 06-08-2026 | v1+v2 | ok |
| 11.5 | Check-box - Configuração e Programação | 1077 | 08-08-2024 | v1+v2 | ok |
| 11.6 | Check-box List - Configuração | 1078 | 21-10-2020 | v1+v2 | ok |
| 11.7 | Color - Configuração e Programação | 1079 | 21-10-2020 | v1+v2 | ok |
| 11.8 | Coordinates - Configuração e Programação | 1080 | 22-10-2020 | v1+v2 | exemplo com defeitos |
| 11.9 | Date - Configuração e Programação | 1081 | 07-08-2025 | v1+v2 | ok |
| 11.10 | Email - Configuração e Programação | 1082 | 21-10-2020 | v1+v2 | ok |
| 11.11 | External Link - Configuração e Programação | 1083 | 22-10-2020 | v1+v2 | ok |
| 11.12 | Hidden - Configuração e Programação | 1084 | 21-10-2020 | v1+v2 | ok |
| 11.13 | Hyperlink - Configuração e Programação | 1085 | 21-10-2020 | v1+v2 | ok |
| 11.14 | Image - Configuração e Programação | 1086 | 21-10-2020 | v1+v2 | ok |
| 11.15 | Lookup - Configuração e Programação | 1087 | 23-04-2021 | v1+v2 | ok |
| 11.16 | Password - Configuração e Programação | 1088 | 21-10-2020 | v1+v2 | exemplo com defeitos |
| 11.17 | Plain-text - Configuração e Programação | 1089 | 21-10-2020 | v1+v2 | ok |
| 11.18 | Radio - Configuração | 1090 | 24-07-2021 | v1+v2 | exemplo com defeitos |
| 11.19 | RadioList - Configuração e Programação | 1091 | 21-10-2020 | v1+v2 | ok |
| 11.20 | Range - Configuração e Programação | 1092 | 21-10-2020 | v1+v2 | ok |
| 11.21 | Separador - Configuração e Programação | 1093 | 21-10-2020 | v1+v2 | ok |
| 11.22 | Text-Area - Configuração e Programação | 1094 | 21-10-2020 | v1+v2 | ok |
| 11.23 | Text-Editor - Configuração e Programação | 1095 | 21-10-2020 | v1+v2 | ok |
| 11.24 | Time - Configuração e Programação | 1096 | 21-10-2020 | v1+v2 | ok |
| 11.25 | Upload File - Configuração e Programação | 1097 | 21-10-2020 | v1+v2 | ok |
| 11.26 | Virtual Keyboard - Configuração | 1098 | 21-10-2020 | v1+v2 | ok |
| 12.1 | Gestão de Acessos | 1133 | 25-10-2020 | v1+v2 | ok |
| 12.2 | Gestão de Orgânica | 1134 | 25-10-2020 | v1+v2 | ok |
| 12.3 | Gestão de Menu | 1135 | 25-10-2020 | v1+v2 | ok |
| 12.4 | Gestão de Perfil | 1136 | 25-10-2020 | v1+v2 | ok |
| 12.5 | Gestão de Utilizadores | 1137 | 25-10-2020 | v1+v2 | ok |
| 12.6 | Gestão de Transações | 1138 | 26-10-2020 | v1+v2 | ok |
| 13.1 | Rules (Eventos de JavaScript e Ajax) | 1099 | 10-02-2026 | v1+v2 | ok |
| 13.2 | Remote/Ajax | 1100 | 19-02-2021 | v1+v2 | exemplo com defeitos |
| 13.3 | Remote Combo-box | 1101 | 26-12-2023 | v1+v2 | exemplo com defeitos |
| 13.4 | Remote List | 1102 | 22-10-2020 | v1+v2 | exemplo com defeitos |
| 13.5 | Remote com Switch em Table | 1103 | 22-10-2020 | v1+v2 | ok |
| 13.6 | Remote com Radio em Table | 1104 | 22-10-2020 | v1+v2 | ok |
| 14.1 | WebServices em igrpweb | 1108 | 22-10-2020 | v1+v2 (v2: jakarta.*) | risco |
| 14.2 | Serviço REST em igrpweb | 1107 | 22-10-2020 | v1+v2 (v2: jakarta.*) | incompleto |
| 14.3 | Serviço SOAP em igrpweb | 1109 | 22-10-2020 | v1+v2 (v2: jakarta.*) | incompleto |
| 15.1 | Mapeamento DAO com Eclipse | 1110 | 22-10-2020 | v1 (ferramenta); conceito v1+v2 | só v1 |
| 15.2 | Mapeamento DAO com JBoss Tools | 1111 | 22-10-2020 | v1 (ferramenta); conceito v1+v2 | só v1 |
| 15.3 | Mapeamento DAO com NetBeans IDE | 1112 | 22-10-2020 | v1 (ferramenta); conceito v1+v2 | contraditório, exemplo com defeitos |
| 16.1 | Como Reportar Issues em igrpweb | 1114 | 22-10-2020 | v1+v2 | ok |
| 17.1 | Instrução de Passagem de Aplicações entre Ambientes | 1124 | 08-01-2021 | v1+v2 | duplicado, risco |
| 18.1 | Modelo MVC | 1125 | 25-10-2020 | v1+v2 | ok |
| 18.2 | Principais Métodos do Core | 1127 | 12-11-2020 | v1+v2 | exemplo com defeitos |
| 18.3 | Parâmetros - Envio e Recepção | 1128 | 25-10-2020 | v1+v2 | exemplo com defeitos |
| 18.4 | Métodos do Core para Base de dados | 1129 | 25-10-2020 | v1+v2 | ok |
| 18.5 | Transaction-RollBack | 1130 | 23-12-2021 | v1+v2 | ok, contraditório |
| 18.6 | Interação com Base de Dados com Query | 1131 | 25-10-2020 | v1+v2 | exemplo com defeitos, risco |
| 18.7 | Interação com Base de Dados com DAO | 1132 | 20-01-2025 | v1+v2 | exemplo com defeitos |
| 19.1 | Código Javascript e CSS Personalizado | 1126 | 25-10-2020 | v1+v2 | ok |
| 20.1 | Conceitos de Hibernate, ORM e JPA | 1142 | 06-11-2020 | v1+v2 | ok |
| 20.2 | Uso de Hibernate e JPA em igrpweb | 1113 | 06-11-2020 | v1+v2 | incompleto |
| 20.3 | Anotações de Hibernate | 1143 | 20-07-2021 | v1+v2 | ok |
| 21.1 | Migração de uma versão 1.X.X para 2.X.X | 1221 | 25-06-2025 | v2 | ok |
| 21.2 | Migration Troubleshooting | 1223 | 12-01-2025 | v2 | ok, incompleto |
<!-- INVENTARIO:FIM -->
