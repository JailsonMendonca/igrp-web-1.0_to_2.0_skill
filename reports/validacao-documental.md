# Relatório de validação documental — portal igrpweb (IGRP v1 e v2)

Gerado por `tools/gerar_relatorio.py` a partir de `audit/portal/inventario.csv` (extração automática) e `audit/analise.txt` (análise documento a documento). Snapshot do portal: 2026-11-20.

## 1. Âmbito e método

- Fonte: `https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&dad=tutorial&isPublic=1` (página XML+XSL; filhos do menu via `Listar_documentos/remote_treemenu_1&p_id=<id>`; documentos via `index&p_id=<id>`).
- Extração: `tools/extrair_portal.py` (biblioteca padrão Python), texto limpo por documento em `audit/portal/<p_id>.md`.
- Validação de consistência: o número no título da página de cada documento tem de coincidir com o do menu; quando não coincide o pedido é repetido em sequência. Pedidos concorrentes chegaram a devolver o documento errado (na primeira sondagem o #1020 devolveu o #1021 e o #1147 veio vazio); na extração final todos coincidem.
- Análise: cada documento foi lido e registado (versão, tema, conceitos, tecnologias, componentes, regras, boas práticas, estado). As APIs e artefactos referidos foram confirmados no código oficial: v1 = ramo `develop` @6d7b32f (1.9.1.261027), v2 = ramo `igrp-horizon-dev` @230df4c (2.1.1.261027).
- Documentação de outras versões (IGRP 3.0, v0) não foi usada.

## 2. Resultados globais

- Menu: 21 secções  24 subgrupos  **169 documentos** (p_id 1000–1224); texto total 613 136 caracteres; 1085 imagens.
- p_id fora do menu: 72 identificadores sondados (1000–1240) devolvem apenas o marcador vazio `<p>Sectionheader</p>` — não há documentos ocultos.
- Ano da última atualização: 2020: 98, 2021: 48, 2022: 2, 2023: 3, 2024: 7, 2025: 9, 2026: 2 → 146 de 169 são anteriores à GA da v2 (2023).
- O próprio portal declara: "JDK17 para horizon ou JDK8 para legacy … esta documentação está preparada para a versão legacy por isso algum texto ou imagem pode estar desatualizada" [#1145, #1147].
- O portal corre o core `211115` (`<version>` no XML das páginas, verificado em 2026-11-21), uma build v1 de novembro de 2021, com o XSL aplicado no browser. As builds atuais são 1.9.1.261027 (v1) e 2.1.1.261027 (v2); as diferenças por build estão em `igrp-web-v1-v2/references/variantes-e-builds.md`.
- Aplicabilidade atribuída: v1+v2: 148; v1: 7; v1 (ferramenta); conceito v1+v2: 6; v1+v2 (v2: jakarta.*): 3; v2: 2; v1 (+ nota v2: JDK 17): 1; v1 (+ alternativa IntelliJ/Maven): 1; v1+v2 (fluxo); ferramenta SVN v1: 1.
- Estados (um documento pode ter vários): ok: 114; exemplo com defeitos: 20; só v1: 9; incompleto: 9; quase vazio: 8; desatualizado: 7; ligação inacessível: 4; duplicado: 3; risco: 3; contraditório: 2; curto: 1.

## 3. Problemas encontrados

### Quase vazio (8)

- 10.1.1. Calendar - Configuração (#1047): quase vazio (so 2 propriedades; resto em imagem)
- 10.11.1. Timeline - Configuração (#1063): quase vazio
- 10.13.1. Vertical Menu - Configuração (#1067): quase vazio
- 10.15. Box - Configuração (#1046): quase vazio
- 10.22. Panels - Configuração (#1056): quase vazio
- 10.24. Quick Button Box - Configuração (#1058): quase vazio
- 10.28. Treelist - Configuração (#1066): quase vazio
- 10.29. Vídeo - Configuração (#1068): quase vazio

### Incompleto (9)

- 5.3. Importar Script SQL (#1022): incompleto (so o script de exemplo; sintaxe auto_increment e MySQL/H2)
- 7.3. BPMN - Exemplo Prático (#1017): incompleto (so titulos; codigo em imagens)
- 7.6. BPMN - Dicas de Design (#1140): incompleto (so uma dica; figura)
- 10.3.1. Circle Stat Box- Configuração e Programação (#1049): programacao sem conteudo
- 10.4.2. Chart - Exemplo Prático (#1045): incompleto (codigo em imagem)
- 14.2. Serviço REST em igrpweb (#1107): incompleto (so topicos; codigo em imagens); em v2 substituir ClientConfig por ClientBuilder (#1223)
- 14.3. Serviço SOAP em igrpweb (#1109): incompleto (so topicos; codigo em imagens)
- 20.2. Uso de Hibernate e JPA em igrpweb (#1113): incompleto (secao 5 "Interagindo com base de dados utilizando" sem conteudo); versoes de drivers antigas
- 21.2. Migration Troubleshooting (#1223): ok; confirmado: RowList (v1) -> rowList (v2) em ResultSet.java [CODIGO]; incompleto (itens pom.xml/Flyway sem detalhe)

### Desatualizado (7)

- 2.1.1. Instalação Java (#1145): parcialmente desatualizado (o proprio doc declara "preparada para a versao legacy"); passos so Windows
- 2.1.4. (Opcional) Instalação Apache TomEE (#1147): desatualizado para v2 (doc declara-se legacy; v2 usa TomEE 10.x)
- 2.2.1. Geração de archetype ou Importação do Projeto (#1149): misto: topo atual; restante descontinuado (so historico v1)
- 2.4.1. Configuração do Java Build Path (#1206): v1 apenas (template Eclipse descontinuado)
- 2.4.3. Criação de base de dados e Configuração do "db_igrp_config.xml" (#1153): titulo desatualizado ("db_igrp_config.xml") vs conteudo (hibernate-igrp-core.cfg.xml); nos projetos atuais a ligacao esta em hibernate-igrp-core.properties filtrado pelo Maven (igrp.db.*) [PROJ teste]
- 2.4.4. Configuração do Pom.xml (#1219): nomes de propriedades desatualizados: o template atual usa igrp.db.user/igrp.db.password/igrp.db.dsn/igrp.db.driver e igrp.migration.location [PROJ teste]; Flyway 9.22.3 (v1) vs 11.20.2 (v2) [CODIGO]
- 2.6. Execução do Projeto no Intellij IDE (#1220): ok com referencias desatualizadas (2.2.1 "importacao GitHub", db_igrp_config.xml)

### Duplicado (3)

- 9.1. Gerador de Código (#1024): ok; texto duplicado com 9.2; ligacao para documento SharePoint interno (services.nosi.cv) nao acessivel; referencia cruzada partida ("Erro! A origem da referencia nao foi encontrada")
- 9.2. Design de Páginas (#1025): duplicado parcial de 9.1 (#1024)
- 17.1. Instrução de Passagem de Aplicações entre Ambientes (#1124): duplica 5.4 (#1023); a dica de atualizacao automatica da BD depende de hbm2ddl.auto=update - [PROJ v2.1.1] risco de alteracoes nao controladas; [ENG] preferir migracoes versionadas (Flyway ja usado pelo framework)

### Contraditório (2)

- 15.3. Mapeamento DAO com NetBeans IDE (#1112): contradiz 18.7 (recomenda Set e EAGER; aqui List/LAZY por defeito); exemplo usa javax.xml.bind (verificar disponibilidade em v2)
- 18.5. Transaction-RollBack (#1130): ok; [PROJ v2.1.1] getKeyValue() apos Core.insert falha em PostgreSQL (SET session audit) - contradiz o exemplo 2.2; em v2 existe AppSession.doInTransaction

### Exemplo com defeitos (20)

- 4.6. Gestão de Domínio (#1012): ok; exemplo final "this.manifestacao.SetValue(...remove(\"SEG\"))" com gralhas (SetValue, manfiestacao) e semantica duvidosa
- 5.1. Criação uma Nova Aplicação (#1020): ok; "External" descrito como inativo e ao mesmo tempo usado na tabela (inconsistente)
- 8.3. Report em HTML usando Classes (#1200): exemplo especifico de um projeto (classes Sis*); codigo colocado no bloco #gen-example em vez de area start-code (exemplo incorreto)
- 10.5.3. Form - Programação com Query (#1037): defeitos: SELECT concatena model.getId(); addInt('id=:id', ...) com nome de parametro errado
- 10.10.4. Filtros em Tabelas (#1033): variante query concatena valores do utilizador no SQL [ENG: injecao]
- 10.10.5. Checkbox em Tabelas - Configuração e Programação (#1034): defeitos no exemplo (variaveis trocadas, newDocument)
- 10.14.1. View - Configuração e Programação (#1069): gralha getLasrstName no exemplo
- 10.19. Leaftet Map (#1053): curto; titulo com gralha (Leaftet)
- 10.25. Section Header - Configuração e Programação (#1059): curto; gralha sectioheader_1
- 11.8. Coordinates - Configuração e Programação (#1080): defeito: condicao trainee != null || !trainee.hasError() (deveria ser &&)
- 11.16. Password - Configuração e Programação (#1088): ok; gralha Strign
- 11.18. Radio - Configuração (#1090): ok; variavel cheched/checked inconsistente
- 13.2. Remote/Ajax (#1100): ok com erros de sintaxe nos exemplos (";" antes de .addPropertie, parenteses a mais)
- 13.3. Remote Combo-box (#1101): exemplos com defeitos: marcador "custom actions " com espaco (o marcador real e custom_actions); nome de Procedure inconsistente (combo vs remoteEmployee); query concatena p_department no SQL [ENG: usar parametros nomeados]
- 13.4. Remote List (#1102): exemplo DAO nao compila (variavel empFilter fora de ambito)
- 15.3. Mapeamento DAO com NetBeans IDE (#1112): contradiz 18.7 (recomenda Set e EAGER; aqui List/LAZY por defeito); exemplo usa javax.xml.bind (verificar disponibilidade em v2)
- 18.2. Principais Métodos do Core (#1127): ok; exemplo toMap troca keyField/valueField; Javadoc referido sem ligacao verificavel
- 18.3. Parâmetros - Envio e Recepção (#1128): ok; gralha "Core.getParamLog" (o metodo e getParamLong) [CODIGO]; texto repetido
- 18.6. Interação com Base de Dados com Query (#1131): ok com defeitos nos exemplos: variante equivalente concatena o id no SQL [ENG: risco de injecao]; ";" a meio da cadeia de addString; getResultList atribuido a ResultSet
- 18.7. Interação com Base de Dados com DAO (#1132): ok com defeitos nos exemplos (Ex3 mistura person/document); [PROJ v2.1.1] DAOs gerados podem trazer @OneToMany com cascade ALL indevido

### Risco (3)

- 14.1. WebServices em igrpweb (#1108): risco: manda alterar com o File Editor a parte protegida do codigo (comentar view.setModel/renderView); essa alteracao e perdida na proxima gravacao no gerador; javax.xml.bind nao existe em v2 (usar jakarta.xml.bind)
- 17.1. Instrução de Passagem de Aplicações entre Ambientes (#1124): duplica 5.4 (#1023); a dica de atualizacao automatica da BD depende de hbm2ddl.auto=update - [PROJ v2.1.1] risco de alteracoes nao controladas; [ENG] preferir migracoes versionadas (Flyway ja usado pelo framework)
- 18.6. Interação com Base de Dados com Query (#1131): ok com defeitos nos exemplos: variante equivalente concatena o id no SQL [ENG: risco de injecao]; ";" a meio da cadeia de addString; getResultList atribuido a ResultSet

### Só v1 (9)

- 2.3.1. Adição do Servidor Apache no Eclipse (#1151): v1 apenas; fluxo substituido por tomee:run
- 2.3.2. Configuração do Servidor Apache Tomcat (#1154): v1 apenas
- 2.3.3. Configuração do Ambiente Eclipse (#1150): v1 apenas; sem regras tecnicas
- 2.4.1. Configuração do Java Build Path (#1206): v1 apenas (template Eclipse descontinuado)
- 2.4.5. Execução do Projeto igrpweb Template (#1004): v1 apenas (fluxo Eclipse)
- 2.5. Falha na sincronização Eclipse-Servidor Local (Troubleshooting) (#1202): v1 apenas
- 3.1.1. GitHub (#1194): v1 (ferramenta); passo 9 refere o GitLab (copiado do 3.1.2); numeracao de passos salta (6, 10)
- 15.1. Mapeamento DAO com Eclipse (#1110): v1 (ferramenta); package indicado como "nosi.base.activeRecord" mas o real e nosi.base.ActiveRecord [CODIGO]; em v1/v2 o CRUD/DAO Generator do Studio faz isto automaticamente (#1011)
- 15.2. Mapeamento DAO com JBoss Tools (#1111): v1 (ferramenta); ok

### Ligação inacessível (4)

- 6.1. Base de Dados - Configuração (#1014): ok; ligacao para documento SharePoint interno nao acessivel
- 7.1. Manual de instalação de Activiti no Framework igrpweb (#1205): v1 (ferramentas); ligacao de clone aponta para repositorio pessoal; versoes Activiti BPMN 6.0.0 (v1) vs converter 7.1.0.M6 (v2) [CODIGO]
- 9.1. Gerador de Código (#1024): ok; texto duplicado com 9.2; ligacao para documento SharePoint interno (services.nosi.cv) nao acessivel; referencia cruzada partida ("Erro! A origem da referencia nao foi encontrada")
- 9.5. Propriedades Comuns dos Campos (#1044): ok; ligacao para documento SharePoint interno nao acessivel

### Outras observações

- Lacuna de numeração: não existe 3.2.1 (a secção 3.2 só tem 3.2.2 Subversion).
- Duplicações de conteúdo: 9.2 repete 9.1; 17.1 repete 5.4; vários documentos repetem parágrafos internamente.
- Exemplos de código: muitos exemplos têm erros de sintaxe ou nomes trocados; o skill usa as regras e reescreve os exemplos quando necessário.
- Segurança: exemplos oficiais concatenam valores do utilizador em SQL (#1033, #1037, #1101, #1131) e cifram palavras-passe de forma reversível com `Core.encrypt` (#1088, #1098); o skill assinala-os como práticas a evitar [ENG].

## 4. Limitações

- O conteúdo em imagens (capturas de ecrã, código em imagem em #1017, #1107, #1109, #1123, etc.) e as vídeo-aulas não foram transcritos; nenhuma regra foi derivada apenas de imagens.
- Ligações para documentos SharePoint internos (`services.nosi.cv`) e para o GitLab interno da NOSi não são acessíveis publicamente.
- O portal não identifica a versão de cada documento; a aplicabilidade foi atribuída por evidência de código e por indicações explícitas do texto. Temas sem evidência ficam marcados como tal no skill.
- O snapshot pode ficar desatualizado: voltar a correr `tools/extrair_portal.py` e comparar o inventário.

## 5. Registo por documento

### 1. Sobre igrpweb

#### 1.1. igrpweb - Apresentação — #1000

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1000&dad=tutorial&isPublic=1
- Atualizado em: 24-03-2025 · 1123 caracteres · 2 imagens
- Versão: v1+v2 (apresentacao geral); contem faixa com ligacao para a doc IGRP 3.0 (excluida)  →  aplicabilidade **v1+v2**
- Tema: apresentacao da plataforma igrpweb
- Conceitos técnicos: plataforma open source NOSi; foco em etapas de negocio e processos; geracao automatica de ~80% do codigo; licenca Apache 2.0; arquitetura leve; interoperabilidade com aplicacoes nativas e de terceiros; IGRP Studio (geradores de interface, fluxos de processo e relatorios); varias bases de dados
- Tecnologias: Java, XML, XSL, JS, CSS, SQL (figura 1)
- Componentes: IGRP Studio; workflow, acessos e permissoes (figura 2)
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; arquitetura so em alto nivel (figuras nao textuais); ligacao 3.0 fora de ambito

### 2. Get Started

#### 2.1.1. Instalação Java — #1145

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1145&dad=tutorial&isPublic=1
- Atualizado em: 04-01-2025 · 5888 caracteres · 21 imagens
- Versão: v1 (texto legacy) + indicacao explicita v2: "JDK17 para horizon ou JDK8 para legacy"  →  aplicabilidade **v1 (+ nota v2: JDK 17)**
- Tema: instalacao do JDK e variaveis de ambiente
- Conceitos técnicos: JDK/JRE; JAVA_HOME, JRE_HOME, PATH; verificacao com java -version / javac -version
- Tecnologias: JDK 8 (legacy), JDK 17 (horizon), Windows
- Componentes: -
- Regras e convenções: v1 usa JDK 8; v2 usa JDK 17
- Boas práticas: verificar as variaveis de ambiente na linha de comandos
- Relações (documentos relacionados no portal): 2.1.2. Instalação Eclipse ou qualquer IDE Java (#1146)
- Estado: desatualizado — parcialmente desatualizado (o proprio doc declara "preparada para a versao legacy"); passos so Windows

#### 2.1.2. Instalação Eclipse ou qualquer IDE Java — #1146

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1146&dad=tutorial&isPublic=1
- Atualizado em: 04-01-2025 · 925 caracteres · 3 imagens
- Versão: v1 (Eclipse) com nota: pode usar IntelliJ Community e "arrancar pelo maven"  →  aplicabilidade **v1 (+ alternativa IntelliJ/Maven)**
- Tema: instalacao de IDE
- Conceitos técnicos: Eclipse IDE for Enterprise Java Developers; alternativa IntelliJ + Maven
- Tecnologias: Eclipse, IntelliJ
- Componentes: -
- Regras e convenções: -
- Boas práticas: arranque via Maven (independente do IDE)
- Relações (documentos relacionados no portal): 2.1.4. (Opcional) Instalação Apache TomEE (#1147)
- Estado: ok — ok (generico)

#### 2.1.3. Instalação PostgreSQL — #1148

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1148&dad=tutorial&isPublic=1
- Atualizado em: 28-07-2021 · 2234 caracteres · 11 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: instalacao PostgreSQL
- Conceitos técnicos: PostgreSQL usado no tutorial para os dados da aplicacao e do framework; "e possivel utilizar qualquer base de dados"; porta 5432
- Tecnologias: PostgreSQL
- Componentes: -
- Regras e convenções: -
- Boas práticas: manter porta por defeito 5432 em ambiente local
- Relações (documentos relacionados no portal): 2.2.1. Geração de archetype ou Importação do Projeto (#1149)
- Estado: ok — ok (passos de instalador genericos)

#### 2.1.4. (Opcional) Instalação Apache TomEE — #1147

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1147&dad=tutorial&isPublic=1
- Atualizado em: 04-01-2025 · 1362 caracteres · 3 imagens
- Versão: v1 (TomEE Plus 8.0.6 dedicado); nota: com "mvn package tomee:run|tomee:debug" nao e preciso TomEE dedicado  →  aplicabilidade **v1**
- Tema: instalacao opcional do Apache TomEE
- Conceitos técnicos: TomEE = Tomcat + EJB/CDI (Web Profile); servidor de deploy do igrpweb
- Tecnologias: Apache TomEE Plus 8.0.6
- Componentes: -
- Regras e convenções: TomEE dedicado e opcional quando se usa o plugin Maven tomee
- Boas práticas: preferir tomee:run / tomee:debug
- Relações (documentos relacionados no portal): 2.1.3. Instalação PostgreSQL (#1148)
- Estado: desatualizado — desatualizado para v2 (doc declara-se legacy; v2 usa TomEE 10.x)

#### 2.2.1. Geração de archetype ou Importação do Projeto — #1149

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1149&dad=tutorial&isPublic=1
- Atualizado em: 04-01-2025 · 4754 caracteres · 18 imagens
- Versão: v1+v2 (archetype atual); passos de import Eclipse marcados "DESCONTINUADOS"  →  aplicabilidade **v1+v2**
- Tema: geracao do projeto por archetype ou importacao
- Conceitos técnicos: archetype publicado no repositorio Maven; mvn archetype:generate -Dfilter=igrp -DdbUser -DdbPassword -DdbJdbcUrl; arranque mvn package tomee:run; remete para o README de NOSiCode-CV/IGRP-Framework; template Git IGRP-Java-Template-Eclipse so para contribuir/acesso privado
- Tecnologias: Maven, Eclipse, IntelliJ, Git
- Componentes: archetype igrp
- Regras e convenções: "a partir de agora e recomendado usar o archetype"
- Boas práticas: gerar projeto pelo archetype em vez de clonar template
- Relações (documentos relacionados no portal): 2.3.1. Adição do Servidor Apache no Eclipse (#1151)
- Estado: desatualizado — misto: topo atual; restante descontinuado (so historico v1)

#### 2.3.1. Adição do Servidor Apache no Eclipse — #1151

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1151&dad=tutorial&isPublic=1
- Atualizado em: 17-12-2020 · 1647 caracteres · 5 imagens
- Versão: v1 (Eclipse + TomEE Plus 8.0.5 / Tomcat 9.0)  →  aplicabilidade **v1**
- Tema: adicionar servidor no Eclipse
- Conceitos técnicos: separador Servers; runtime Tomcat 9.0 correspondente ao TomEE Plus 8
- Tecnologias: Eclipse WTP, Tomcat 9, TomEE Plus 8.0.5
- Componentes: -
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.3.2. Configuração do Servidor Apache Tomcat (#1154)
- Estado: só v1 — v1 apenas; fluxo substituido por tomee:run

#### 2.3.2. Configuração do Servidor Apache Tomcat — #1154

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1154&dad=tutorial&isPublic=1
- Atualizado em: 22-12-2020 · 1298 caracteres · 6 imagens
- Versão: v1 (Eclipse/Tomcat)  →  aplicabilidade **v1**
- Tema: configuracao do servidor Tomcat no Eclipse
- Conceitos técnicos: timeouts de arranque 120/60 em vez de 45/15; encoding UTF-8 na launch configuration
- Tecnologias: Eclipse, Tomcat
- Componentes: -
- Regras e convenções: -
- Boas práticas: UTF-8 para evitar erros de caracteres especiais; aumentar timeouts
- Relações (documentos relacionados no portal): 2.3.3. Configuração do Ambiente Eclipse (#1150)
- Estado: só v1 — v1 apenas

#### 2.3.3. Configuração do Ambiente Eclipse — #1150

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1150&dad=tutorial&isPublic=1
- Atualizado em: 27-04-2021 · 1174 caracteres · 6 imagens
- Versão: v1 (Eclipse)  →  aplicabilidade **v1**
- Tema: arrumacao do workspace Eclipse
- Conceitos técnicos: consola, separador Servers, reset do workspace
- Tecnologias: Eclipse
- Componentes: -
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.2. Configuração do ficheiro main.xml (#1152)
- Estado: só v1 — v1 apenas; sem regras tecnicas

#### 2.4.1. Configuração do Java Build Path — #1206

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1206&dad=tutorial&isPublic=1
- Atualizado em: 26-04-2021 · 2532 caracteres · 12 imagens
- Versão: v1 (Eclipse/Tomcat 9)  →  aplicabilidade **v1**
- Tema: Java Build Path do template
- Conceitos técnicos: remover pastas "(missing)" e servidor "Unbound"; adicionar Server Runtime Apache Tomcat v9.0; Order and Export
- Tecnologias: Eclipse, Tomcat 9
- Componentes: IGRP Template
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.2. Configuração do ficheiro main.xml (#1152)
- Estado: desatualizado, só v1 — v1 apenas (template Eclipse descontinuado)

#### 2.4.2. Configuração do ficheiro main.xml — #1152

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1152&dad=tutorial&isPublic=1
- Atualizado em: 17-12-2020 · 1706 caracteres · 7 imagens
- Versão: v1+v2 (ficheiro existe nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: configuracao de main.xml
- Conceitos técnicos: src/main/resources/config/common/main.xml; chave igrp.workspace = caminho absoluto do projeto (workspace)
- Tecnologias: XML properties
- Componentes: main.xml
- Regras e convenções: preencher igrp.workspace com o caminho do projeto
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.3. Criação de base de dados e Configuração do "db_igrp_config.xml" (#1153)
- Estado: ok — ok; passos com atalhos Eclipse (CTRL+SHIFT+R)

#### 2.4.3. Criação de base de dados e Configuração do "db_igrp_config.xml" — #1153

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1153&dad=tutorial&isPublic=1
- Atualizado em: 11-05-2022 · 1429 caracteres · 6 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: criacao da BD e configuracao da ligacao do framework
- Conceitos técnicos: criar BD (ex.: db_igrp) no pgAdmin; configurar hibernate-igrp-core.cfg.xml em src/main/resources
- Tecnologias: PostgreSQL, pgAdmin, Hibernate
- Componentes: hibernate-igrp-core.cfg.xml
- Regras e convenções: BD do framework criada antes do arranque
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004)
- Estado: desatualizado — titulo desatualizado ("db_igrp_config.xml") vs conteudo (hibernate-igrp-core.cfg.xml); nos projetos atuais a ligacao esta em hibernate-igrp-core.properties filtrado pelo Maven (igrp.db.*) [PROJ teste]

#### 2.4.4. Configuração do Pom.xml — #1219

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1219&dad=tutorial&isPublic=1
- Atualizado em: 02-02-2023 · 918 caracteres · 2 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: configuracao do Flyway no pom.xml
- Conceitos técnicos: Flyway Migration configurado no pom com utilizador, password e DSN da BD (exemplo db.user/db.password/db.dsn)
- Tecnologias: Maven, Flyway, PostgreSQL
- Componentes: pom.xml
- Regras e convenções: configurar o Flyway antes de arrancar
- Boas práticas: confirmar que as tags ficam bem fechadas
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004)
- Estado: desatualizado — nomes de propriedades desatualizados: o template atual usa igrp.db.user/igrp.db.password/igrp.db.dsn/igrp.db.driver e igrp.migration.location [PROJ teste]; Flyway 9.22.3 (v1) vs 11.20.2 (v2) [CODIGO]

#### 2.4.5. Execução do Projeto igrpweb Template — #1004

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1004&dad=tutorial&isPublic=1
- Atualizado em: 11-01-2021 · 1160 caracteres · 4 imagens
- Versão: v1 (Eclipse "Run on Server")  →  aplicabilidade **v1**
- Tema: executar o template
- Conceitos técnicos: Run As > Run on Server; login de demonstracao demo@nosi.cv / demo
- Tecnologias: Eclipse, Tomcat
- Componentes: IGRP Template
- Regras e convenções: -
- Boas práticas: alterar credenciais de demonstracao fora do ambiente local [ENG]
- Relações (documentos relacionados no portal): 4.2. Página Login e Página Home (#1005)
- Estado: só v1 — v1 apenas (fluxo Eclipse)

#### 2.5. Falha na sincronização Eclipse-Servidor Local (Troubleshooting) — #1202

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1202&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 1907 caracteres · 5 imagens
- Versão: v1 (Eclipse/Tomcat 9)  →  aplicabilidade **v1**
- Tema: troubleshooting de sincronizacao Eclipse-servidor
- Conceitos técnicos: servidor "unbound" por deploy mal feito ou erros em classes; voltar a adicionar Server Runtime
- Tecnologias: Eclipse, Tomcat 9
- Componentes: -
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.1. Configuração do Java Build Path (#1206)
- Estado: só v1 — v1 apenas

#### 2.6. Execução do Projeto no Intellij IDE — #1220

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1220&dad=tutorial&isPublic=1
- Atualizado em: 04-04-2023 · 6306 caracteres · 15 imagens
- Versão: v1+v2 (fluxo Maven/IntelliJ); referencias a db_igrp_config.xml herdadas  →  aplicabilidade **v1+v2**
- Tema: executar o projeto no IntelliJ
- Conceitos técnicos: clone do IGRP-Template, importar como Maven, Trust Project; main.xml igrp.workspace; run Maven "clean package tomee:run" (Embedded TomEE); http://localhost:8080/IGRP-Template/; login demo
- Tecnologias: IntelliJ, Maven, TomEE embebido
- Componentes: main.xml, pom.xml
- Regras e convenções: executar com tomee:run do plugin Maven
- Boas práticas: configuracao de run Maven reutilizavel
- Relações (documentos relacionados no portal): 2.4.4. Configuração do Pom.xml (#1219); 2.4.5. Execução do Projeto igrpweb Template (#1004); 2.4.3. Criação de base de dados e Configuração do "db_igrp_config.xml" (#1153); 2.4.2. Configuração do ficheiro main.xml (#1152)
- Estado: ok, desatualizado — ok com referencias desatualizadas (2.2.1 "importacao GitHub", db_igrp_config.xml)

### 3. Trabalho Colaborativo/Controlo de versões

#### 3.1.1. GitHub — #1194

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1194&dad=tutorial&isPublic=1
- Atualizado em: 23-12-2020 · 4121 caracteres · 23 imagens
- Versão: v1 (Eclipse/EGit; template); conceito v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: alojar o projeto no GitHub
- Conceitos técnicos: criar repositorio; adicionar remote e push a partir do Eclipse (Git Repositories)
- Tecnologias: Git, GitHub, Eclipse
- Componentes: -
- Regras e convenções: -
- Boas práticas: versionar o projeto num repositorio remoto
- Relações (documentos relacionados no portal): 3.1.2. NOSi GITLab (#1006)
- Estado: só v1 — v1 (ferramenta); passo 9 refere o GitLab (copiado do 3.1.2); numeracao de passos salta (6, 10)

#### 3.1.2. NOSi GITLab — #1006

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1006&dad=tutorial&isPublic=1
- Atualizado em: 23-12-2020 · 7147 caracteres · 27 imagens
- Versão: v1 (Eclipse); conceito v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: alojar e partilhar no GitLab NOSi
- Conceitos técnicos: git.nosi.cv com credenciais NOSi; membros e privilegios (Settings > Members); importar projeto partilhado; colaboradores fazem commit/pull das suas paginas
- Tecnologias: Git, GitLab
- Componentes: -
- Regras e convenções: -
- Boas práticas: partilhar repositorio com membros e privilegios definidos
- Relações (documentos relacionados no portal): 1.1. igrpweb - Apresentação (#1000)
- Estado: ok — ok (especifico do GitLab interno NOSi)

#### 3.2.2. Subversion — #1007

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1007&dad=tutorial&isPublic=1
- Atualizado em: 23-12-2020 · 4473 caracteres · 9 imagens
- Versão: v1+v2 (mecanismo de colaboracao); ferramenta SVN/Eclipse v1  →  aplicabilidade **v1+v2 (fluxo); ferramenta SVN v1**
- Tema: controlo de versoes (fluxo) e Subversion
- Conceitos técnicos: criar pagina gera Page.json no servidor local e regista a pagina na BD partilhada (visivel aos outros); ao gravar sao gerados Model, View, Controller, XML e XSL so no servidor local; commit + push enviam-nos; os outros fazem pull e, como a pagina nao esta compilada, devem abri-la no editor de paginas e gravar para compilar; Subversive SVN no Eclipse; Sourcetree
- Tecnologias: SVN, Git, Eclipse
- Componentes: Page.json, BD partilhada
- Regras e convenções: apos pull de paginas, abrir no gerador e gravar para compilar
- Boas práticas: versionar todos os artefactos da pagina (JSON/XML/XSL/Java)
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004)
- Estado: ok — ok; mistura SVN com terminologia Git (push/pull); texto final truncado

#### 3.3.1. Resolver Conflitos do Git — #1201

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1201&dad=tutorial&isPublic=1
- Atualizado em: 19-07-2021 · 3682 caracteres · 2 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: resolver conflitos Git
- Conceitos técnicos: conflitos de merge; marcadores <<<<<<< ======= >>>>>>>; git status; resolver e commit
- Tecnologias: Git
- Componentes: -
- Regras e convenções: -
- Boas práticas: trabalhar em ramos isolados
- Relações (documentos relacionados no portal): 3.1.1. GitHub (#1194)
- Estado: ok — ok (generico)

### 4. IGRP Studio

#### 4.1. IGRP Studio - Apresentação — #1008

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1008&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 1217 caracteres · 5 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: IGRP Studio - apresentacao
- Conceitos técnicos: componentes do Studio: Page Builder (interface, importar paginas, gerar CRUD, gerar DAO, novas paginas), BPMN Designer, Report Designer (DataSource: Pagina, Etapa, Processo, Objeto ou Query), Application Builder (pesquisar/criar/alterar/eliminar aplicacoes)
- Tecnologias: -
- Componentes: Page Builder, BPMN Designer, Report Designer, Application Builder
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004)
- Estado: ok — ok

#### 4.2. Página Login e Página Home — #1005

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1005&dad=tutorial&isPublic=1
- Atualizado em: 23-12-2020 · 3943 caracteres · 7 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: pagina de login e Home
- Conceitos técnicos: varias aplicacoes no mesmo espaco com Single-Sign-On; autenticacao por ActiveDirectory, tabela de utilizadores ou federacao de identidade; URL local webapps?r=igrp/login/login; utilizador demo; Home com Tutorial IGRP, IGRP Studio e aplicacoes (Minhas Aplicacoes / Outras); Studio so para utilizadores com privilegios de desenvolvedor; Home Page Builder com Application Builder, Access Management, SQL Tool, Domain Management; top menu de workflow (Mapa de Processos, Minhas Tarefas); Minha Conta (palavra-passe, idioma, perfil)
- Tecnologias: SSO, AD
- Componentes: login, Home, Studio
- Regras e convenções: acesso ao Studio depende de privilegios de desenvolvedor
- Boas práticas: [ENG] remover/alterar o utilizador demo fora de desenvolvimento
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004)
- Estado: ok — ok

#### 4.3. Partilha Geral entre Aplicações — #1009

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1009&dad=tutorial&isPublic=1
- Atualizado em: 16-10-2020 · 1380 caracteres · 3 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: partilha geral entre aplicacoes
- Conceitos técnicos: partilhar recursos (ex.: paginas) da aplicacao de origem para a de destino; o recurso fica disponivel no campo Action de botoes/lookup e por URL
- Tecnologias: -
- Componentes: Partilha geral (Studio)
- Regras e convenções: -
- Boas práticas: reutilizar paginas entre aplicacoes em vez de as recriar
- Relações (documentos relacionados no portal): 4.1. IGRP Studio - Apresentação (#1008)
- Estado: ok — ok

#### 4.4. SQL Tools — #1010

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1010&dad=tutorial&isPublic=1
- Atualizado em: 16-10-2020 · 1714 caracteres · 6 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: SQL Tools
- Conceitos técnicos: testar queries escolhendo aplicacao e ligacao; resultado em tabela dinamica
- Tecnologias: SQL
- Componentes: SQL Tool
- Regras e convenções: -
- Boas práticas: testar queries antes de as usar no codigo
- Relações (documentos relacionados no portal): 4.3. Partilha Geral entre Aplicações (#1009)
- Estado: ok — ok

#### 4.5. CRUD/DAO Generator — #1011

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1011&dad=tutorial&isPublic=1
- Atualizado em: 16-10-2020 · 2426 caracteres · 6 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: CRUD/DAO Generator
- Conceitos técnicos: CRUD Generator gera duas paginas por tabela (listagem e formulario) com abordagem por query; escolher aplicacao, ligacao e schema; DAO Generator gera classes DAO (get/set) pelas mesmas etapas, opcao GERAR DAO
- Tecnologias: SQL, Hibernate
- Componentes: CRUD Generator, DAO Generator
- Regras e convenções: -
- Boas práticas: util para aprendizagem
- Relações (documentos relacionados no portal): 4.1. IGRP Studio - Apresentação (#1008); 4.4. SQL Tools (#1010)
- Estado: ok — ok; [PROJ v2.1.1] gerar de novo o CRUD da mesma tabela substitui as paginas sem preservar areas; rever DAOs gerados

#### 4.6. Gestão de Domínio — #1012

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1012&dad=tutorial&isPublic=1
- Atualizado em: 28-07-2021 · 4721 caracteres · 6 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de dominios
- Conceitos técnicos: dominios padronizam valores (nome/valor) partilhaveis entre aplicacoes; dominio publico usavel por todas mas so alteravel pela aplicacao que o criou; usar em combobox/radiolist (checkboxlist possivel); Core.findDomainByCode(nome[,app]), Core.findDomainDescByKey(nome,chave[,app])
- Tecnologias: -
- Componentes: Dominio, combobox, radiolist, checkboxlist
- Regras e convenções: dominio publico so e alterado pela aplicacao criadora
- Boas práticas: usar dominios para listas pequenas de valores em vez de tabelas
- Relações (documentos relacionados no portal): 11.4.1. Select/ComboBox - Configuração e Programação (#1070); 11.4.2. Campo de Seleção - Programação com DAO (#1071)
- Estado: exemplo com defeitos — ok; exemplo final "this.manifestacao.SetValue(...remove(\"SEG\"))" com gralhas (SetValue, manfiestacao) e semantica duvidosa

#### 4.7. Gestão Tipo Documento — #1013

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1013&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 2335 caracteres · 4 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de tipo de documento
- Conceitos técnicos: tipos de documento (aplicacao, nome, codigo, descricao) usados como Input/Output numa etapa BPMN; associacao na etapa (tab Forms, lookup Associar Documentos, obrigatorio); associacao de Report a etapa
- Tecnologias: BPMN
- Componentes: Tipo de documento, etapa
- Regras e convenções: documentos de upload de processo sao configurados separadamente da pagina da etapa
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

### 5. Application Builder

#### 5.1. Criação uma Nova Aplicação — #1020

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1020&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 3946 caracteres · 15 imagens
- Versão: v1+v2 (conceito); opcoes External/Custom dad ligadas ao modelo de instancias  →  aplicabilidade **v1+v2**
- Tema: criacao de aplicacao
- Conceitos técnicos: Nome (alteravel), Codigo/dad (unico, nao alteravel), External, Host/Custom dad: Custom dad cria WAR a parte (outra instancia), Externo cria JAR das classes fora do WAR; Application Builder: editar, ligacoes de BD, exportar, importar; aplicacao desativada fica inacessivel e o codigo nao pode ser reutilizado
- Tecnologias: WAR/JAR
- Componentes: Application Builder
- Regras e convenções: codigo da aplicacao e definitivo; desativar nao liberta o codigo
- Boas práticas: -
- Relações (documentos relacionados no portal): 2.4.5. Execução do Projeto igrpweb Template (#1004); 4.5. CRUD/DAO Generator (#1011); 6.1. Base de Dados - Configuração (#1014)
- Estado: exemplo com defeitos — ok; "External" descrito como inativo e ao mesmo tempo usado na tabela (inconsistente)

#### 5.2. Criação de uma Nova Página — #1021

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1021&dad=tutorial&isPublic=1
- Atualizado em: 08-05-2021 · 5075 caracteres · 14 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: criacao de pagina
- Conceitos técnicos: Title (alteravel), Code (unico, nao alteravel), Enable, Publico (chamavel por qualquer aplicacao), Application, Module (so organizacao), Home Page, Create menu (desligar para paginas de novo/inserir/lookup), Componente (so sem menu; nao gera classes MVC, so XML/XSL/JSON); cada pagina = package com 3 classes; sem Home Page ou sem codigo gerado a aplicacao/pagina nao executa
- Tecnologias: -
- Componentes: Page Builder, File editor
- Regras e convenções: codigo de pagina unico e definitivo; pagina sem conteudo gerado nao executa
- Boas práticas: desativar Create menu em paginas auxiliares
- Relações (documentos relacionados no portal): 4.1. IGRP Studio - Apresentação (#1008); 5.1. Criação uma Nova Aplicação (#1020)
- Estado: ok — ok

#### 5.3. Importar Script SQL — #1022

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1022&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 699 caracteres · 3 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: importar script SQL
- Conceitos técnicos: importar DDL/script para criar objetos na BD
- Tecnologias: SQL
- Componentes: Import
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 4.4. SQL Tools (#1010); 5.1. Criação uma Nova Aplicação (#1020)
- Estado: incompleto — incompleto (so o script de exemplo; sintaxe auto_increment e MySQL/H2)

#### 5.4. Exportar e Importar Aplicação — #1023

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1023&dad=tutorial&isPublic=1
- Atualizado em: 08-01-2021 · 4293 caracteres · 7 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: exportar e importar aplicacao
- Conceitos técnicos: exportar a partir do Application Builder escolhendo funcionalidades e ficheiros -> ficheiro JAR; importar no Studio (Import) com separadores aplicacao, livrarias externas, script SQL, imagens; usado para partilha e passagem entre ambientes (desenvolvimento, teste, producao)
- Tecnologias: JAR
- Componentes: Application Builder, Import
- Regras e convenções: importar no separador correto (ficheiro errado pode causar problemas no servidor/Studio)
- Boas práticas: ambientes distintos para desenvolvimento, teste e producao
- Relações (documentos relacionados no portal): 6.1. Base de Dados - Configuração (#1014); 6.2. File Editor (#1015); 17.1. Instrução de Passagem de Aplicações entre Ambientes (#1124)
- Estado: ok — ok

### 6. Base de Dados (BD) - Configuração

#### 6.1. Base de Dados - Configuração — #1014

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1014&dad=tutorial&isPublic=1
- Atualizado em: 16-10-2020 · 4519 caracteres · 12 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: configuracao de base de dados da aplicacao
- Conceitos técnicos: Hibernate/JPA; cada aplicacao pode usar varias BD (oracle, postgresql, mysql, sqlserver, h2); Application Builder > Configurar Base de Dados: tipo, nome da ligacao (<app>_<bd>_<n>), URL, driver, utilizador, password, testar e gravar; ligacao padrao usada quando nao se indica ligacao; ficheiro <ligacao>.<aplicacao>.cfg.xml no File editor para mapear classes DAO
- Tecnologias: Hibernate, JDBC (Oracle, PostgreSQL, MySQL, SQL Server, H2)
- Componentes: Application Builder, ligacoes, cfg.xml
- Regras e convenções: a ligacao padrao aplica-se quando nao se especifica ligacao
- Boas práticas: indicar a ligacao explicitamente no codigo [PROJ]
- Relações (documentos relacionados no portal): -
- Estado: ok, ligação inacessível — ok; ligacao para documento SharePoint interno nao acessivel

#### 6.2. File Editor — #1015

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1015&dad=tutorial&isPublic=1
- Atualizado em: 17-10-2020 · 1464 caracteres · 5 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: File Editor
- Conceitos técnicos: editor web de packages, classes e ficheiros de configuracao da aplicacao; gravar explicitamente; menu de contexto por ficheiro
- Tecnologias: -
- Componentes: File Editor
- Regras e convenções: alteracoes nao gravadas perdem-se
- Boas práticas: -
- Relações (documentos relacionados no portal): 6.1. Base de Dados - Configuração (#1014)
- Estado: ok — ok (texto repetido)

### 7. BPMN Designer

#### 7.1. Manual de instalação de Activiti no Framework igrpweb — #1205

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1205&dad=tutorial&isPublic=1
- Atualizado em: 10-01-2022 · 6834 caracteres · 28 imagens
- Versão: v1 (procedimento Eclipse/Tomcat; motor Activiti externo activiti-rest); conceito v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: instalacao do Activiti para o BPMN Designer
- Conceitos técnicos: Activiti (motor BPMN Java) instalado como projeto separado activiti-rest (repositorio NOSiCode-CV/activiti), BD propria db_activiti configurada em db_properties; teste em /activiti-rest/service/repository/deployments; credenciais de demonstracao kermit; depois criar processo no BPMN Designer
- Tecnologias: Activiti, PostgreSQL, Eclipse, Tomcat
- Componentes: activiti-rest, BPMN Designer
- Regras e convenções: o BPMN Designer depende de um motor Activiti acessivel
- Boas práticas: [ENG] alterar credenciais de demonstracao do motor
- Relações (documentos relacionados no portal): 7.2. BPMN - Business Process Model Notation (#1016); 7.4. BPMN - Criação de Processos com Tabs (#1018); 7.3. BPMN - Exemplo Prático (#1017); 7.6. BPMN - Dicas de Design (#1140)
- Estado: ligação inacessível — v1 (ferramentas); ligacao de clone aponta para repositorio pessoal; versoes Activiti BPMN 6.0.0 (v1) vs converter 7.1.0.M6 (v2) [CODIGO]

#### 7.2. BPMN - Business Process Model Notation — #1016

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1016&dad=tutorial&isPublic=1
- Atualizado em: 17-10-2020 · 13499 caracteres · 44 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: processos BPMN no igrpweb
- Conceitos técnicos: processo = objetivo, etapas sequenciais, inputs, outputs, resultado; Mapa de processos; Minhas Tarefas (lista, monitorizacao por coordenacao, estatisticas); Consulta Processo; exemplo "Nha Feria": aplicacao, id/nome do processo, Executable; user tasks associadas a paginas (pagina marcada como "processo" no gerador); gateway com default flow e condicao; acesso a etapas: organica > perfis > utilizadores; iniciar processo (so com permissao); assumir, libertar, ver detalhe e executar tarefa
- Tecnologias: BPMN 2.0, Activiti
- Componentes: BPMN Designer, Mapa de processos, Minhas Tarefas
- Regras e convenções: pagina associada a etapa deve estar marcada como de processo; acesso as etapas atribuido como menus/transactions
- Boas práticas: rever a gestao de acessos antes de publicar processos
- Relações (documentos relacionados no portal): 4.7. Gestão Tipo Documento (#1013)
- Estado: ok — ok

#### 7.3. BPMN - Exemplo Prático — #1017

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1017&dad=tutorial&isPublic=1
- Atualizado em: 17-10-2020 · 7102 caracteres · 36 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: BPMN - exemplo pratico
- Conceitos técnicos: topicos: dominio, criar processo, pagina de registo, preencher model com dados de etapa (TaskValidacaoController), ler parametros de processo/etapa (p_justificacao), injetar variavel na etapa
- Tecnologias: BPMN
- Componentes: Task<Etapa>Controller
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 7.2. BPMN - Business Process Model Notation (#1016)
- Estado: incompleto — incompleto (so titulos; codigo em imagens)

#### 7.4. BPMN - Criação de Processos com Tabs — #1018

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1018&dad=tutorial&isPublic=1
- Atualizado em: 17-10-2020 · 5791 caracteres · 9 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: processos BPMN com tabs
- Conceitos técnicos: todas as etapas numa pagina com tabs e classe Helper (switch-case) para mostrar/ocultar; mapa de processos; distribuicao de tarefas (disponiveis, minhas, gerir - transaction para coordenadores; transferir, alterar prioridade); consulta de processos
- Tecnologias: BPMN
- Componentes: tab, box, Helper
- Regras e convenções: nao usar "task" no id da etapa (o igrpweb acrescenta-o); radio-list do tipo String em processos; evitar tags repetidas entre tabs; nao atribuir tarefa ao perfil atualmente autenticado
- Boas práticas: nomes de campos associados a etapa (ex.: email-pedido); paginas criadas em separado e copiadas para os tabs
- Relações (documentos relacionados no portal): 4.7. Gestão Tipo Documento (#1013); 7.2. BPMN - Business Process Model Notation (#1016); 7.3. BPMN - Exemplo Prático (#1017)
- Estado: ok — ok (codigo em imagens)

#### 7.5. BPMN - Funções Úteis — #1019

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1019&dad=tutorial&isPublic=1
- Atualizado em: 13-03-2024 · 4908 caracteres · 4 imagens
- Versão: v1+v2 (APIs confirmadas nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: BPMN - funcoes uteis
- Conceitos técnicos: Model.loadFromTask (carrega dados de etapa anterior com componentes de nomes iguais); actionSave = botao "Seguinte"; allowTask (true/false controla quem ve a tarefa); Core.getProcessDefinitionByProcessKey(chave); Core.startProcess(chave, id, params) com parametros prefixo x_; inputDocsHasErrors() valida documentos de input; lista TipoDocumentoEtapa para documentos de output; Core.getTaskHistory(idEtapa) devolve os dados da ultima execucao da etapa
- Tecnologias: Activiti
- Componentes: Core, BPMNConstants, TipoDocumentoEtapa
- Regras e convenções: parametros de processo com prefixo x_
- Boas práticas: validar documentos de input antes de executar codigo da etapa
- Relações (documentos relacionados no portal): 7.7. BPMN - Dicas de Programação (#1141); 7.3. BPMN - Exemplo Prático (#1017); 7.2. BPMN - Business Process Model Notation (#1016); 7.4. BPMN - Criação de Processos com Tabs (#1018); 7.6. BPMN - Dicas de Design (#1140)
- Estado: ok — ok (exemplos em imagens)

#### 7.6. BPMN - Dicas de Design — #1140

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1140&dad=tutorial&isPublic=1
- Atualizado em: 03-11-2020 · 641 caracteres · 1 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: BPMN - dicas de design
- Conceitos técnicos: tarefas paralelas (gateway paralelo) evitam logica para chamar etapas em modal
- Tecnologias: BPMN
- Componentes: -
- Regras e convenções: -
- Boas práticas: usar tarefas paralelas em vez de logica ad-hoc
- Relações (documentos relacionados no portal): 7.2. BPMN - Business Process Model Notation (#1016); 7.3. BPMN - Exemplo Prático (#1017); 7.4. BPMN - Criação de Processos com Tabs (#1018); 7.5. BPMN - Funções Úteis (#1019)
- Estado: incompleto — incompleto (so uma dica; figura)

#### 7.7. BPMN - Dicas de Programação — #1141

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1141&dad=tutorial&isPublic=1
- Atualizado em: 03-11-2020 · 544 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: BPMN - dicas de programacao
- Conceitos técnicos: mostrar etapas anteriores num Iframe: model.setIframe_1_src(Core.getIGRPLink("igrp","Detalhes_tarefas","index&target=_blank&"+BPMNConstants.PRM_TASK_ID+"="+Core.getTaskHistory("Task2").getId()))
- Tecnologias: -
- Componentes: Iframe, BPMNConstants
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 7.5. BPMN - Funções Úteis (#1019); 10.17. Iframe - Configuração (#1051)
- Estado: ok — ok (curto)

### 8. Report Designer

#### 8.1. Report Designer — #1105

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1105&dad=tutorial&isPublic=1
- Atualizado em: 21-06-2021 · 7846 caracteres · 17 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Report Designer - apresentacao
- Conceitos técnicos: ferramenta do Studio para desenhar, parametrizar e gerar documentos; aplicacao, Reports, Head, Body, Gravar, Preview; Data Source; invocar por link ou botao; Core.getLinkReport(codigo[, Report]); Core.getLinkReportPDF(codigo, new Report().addParam(...)); em tabela: linha.setVer("igrp_studio","WebReport","get-report").addParam("code",...).addParam("p_id",...)
- Tecnologias: HTML, PDF
- Componentes: Report Designer, nosi.core.webapp.Report
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 8.2. Report Designer - Exemplos Práticos (#1106)
- Estado: ok — ok; exemplos de link/botao so com titulos; ciclo for truncado no texto

#### 8.2. Report Designer - Exemplos Práticos — #1106

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1106&dad=tutorial&isPublic=1
- Atualizado em: 16-02-2024 · 20012 caracteres · 31 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Report Designer - exemplos praticos
- Conceitos técnicos: criar report (titulo, codigo unico); Data Source por ligacao da aplicacao com 4 tipos: Objeto (tabela), Etapa (processo), Query, Pagina; "Datasource App"; submenus default_form_report (aplicacao, organica, utilizador, perfil, data), form (colunas [NOME]) e table (tabela, lista de marcas, lista numerada); chaves para filtrar; chamar com Core.getLinkReport("codigo", new Report().addParam("chave","?")) num botao
- Tecnologias: SQL, HTML
- Componentes: Report Designer, Data Source, Report
- Regras e convenções: codigo de report unico; definir chaves para restringir dados
- Boas práticas: Data Source Query para controlo exato dos dados
- Relações (documentos relacionados no portal): 8.1. Report Designer (#1105); 8.3. Report em HTML usando Classes (#1200); 8.4. Report Designer - Funções Úteis (#1209)
- Estado: ok — ok

#### 8.3. Report em HTML usando Classes — #1200

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1200&dad=tutorial&isPublic=1
- Atualizado em: 19-03-2021 · 6254 caracteres · 10 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: report em HTML usando classes
- Conceitos técnicos: modelo Java proprio + template HTML com substituicao de marcadores ({header}, {user_name}, ...); devolver com this.format = Response.FORMAT_HTML e renderView(String)
- Tecnologias: HTML, Java
- Componentes: Response
- Regras e convenções: -
- Boas práticas: [ENG] escapar valores inseridos no HTML (risco de XSS)
- Relações (documentos relacionados no portal): 8.1. Report Designer (#1105); 8.2. Report Designer - Exemplos Práticos (#1106)
- Estado: exemplo com defeitos — exemplo especifico de um projeto (classes Sis*); codigo colocado no bloco #gen-example em vez de area start-code (exemplo incorreto)

#### 8.4. Report Designer - Funções Úteis — #1209

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1209&dad=tutorial&isPublic=1
- Atualizado em: 27-09-2021 · 1747 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Report Designer - funcoes uteis
- Conceitos técnicos: Core.getLinkReport(codigo, Report) gera contra prova (uuid) obtida em resp.getContent(); Report.setContraprova(...); Core.getLinkReportPDF; Core.getLinkContraProva / getLinkContraProvaPDF / getRepContraProvaPDF para consultar report gerado; envio em anexo com Attachment e Core.mail_v2
- Tecnologias: PDF, email
- Componentes: Report, Attachment, Core.mail_v2
- Regras e convenções: -
- Boas práticas: usar contra prova para verificacao de documentos emitidos
- Relações (documentos relacionados no portal): 8.1. Report Designer (#1105); 8.2. Report Designer - Exemplos Práticos (#1106); 8.3. Report em HTML usando Classes (#1200)
- Estado: ok — ok; exemplo com enderecos de email reais e sintaxe invalida (aspas)

#### 8.5. Report Designer - Exemplo HTML com Footer modificado — #1222

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1222&dad=tutorial&isPublic=1
- Atualizado em: 16-02-2024 · 6419 caracteres · 1 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: report HTML com footer modificado
- Conceitos técnicos: footer com QR code da contra prova (link igrp_studio/web-report/get-contraprova&ctprov=...); atributos footer/no/tag no HTML do report; CSS de pagina
- Tecnologias: HTML, CSS
- Componentes: Report Designer
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 8.4. Report Designer - Funções Úteis (#1209); 8.1. Report Designer (#1105); 8.2. Report Designer - Exemplos Práticos (#1106); 8.3. Report em HTML usando Classes (#1200)
- Estado: ok — ok (exemplo especifico)

### 9. Gerador de Código (GC)

#### 9.1. Gerador de Código — #1024

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1024&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 11956 caracteres · 18 imagens
- Versão: v1+v2 (gerador formgen, separadores DESIGN/XML/XSL/JAVA iguais nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Gerador de Codigo (Page Builder) - visao geral e funcionamento XML/XSL
- Conceitos técnicos: drag and drop de componentes e campos; separadores DESIGN, XML, XSL, JAVA; linhas (ROW) e colunas (COL); gravar e aguardar feedback de sucesso (fechar sem gravar perde o codigo); botoes Custom Return causam falha de compilacao na gravacao mas a informacao da pagina e guardada; o browser recebe XML (dados) + XSL (modelo) e constroi o HTML no cliente; dados preparados no servidor pelo Java da pagina
- Tecnologias: XML, XSL(T) no browser, JavaScript, CSS, Java
- Componentes: box/tab/panel so recebem componentes; form e table recebem varios campos; toolsbar so recebe button; chart nao recebe campos
- Regras e convenções: aplicacao e pagina criadas antes no Application Builder / Page Builder; gravar antes de fechar
- Boas práticas: -
- Relações (documentos relacionados no portal): 4.1. IGRP Studio - Apresentação (#1008)
- Estado: ok, duplicado, ligação inacessível — ok; texto duplicado com 9.2; ligacao para documento SharePoint interno (services.nosi.cv) nao acessivel; referencia cruzada partida ("Erro! A origem da referencia nao foi encontrada")

#### 9.2. Design de Páginas — #1025

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1025&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 5645 caracteres · 15 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: design de paginas no gerador
- Conceitos técnicos: igual a 9.1 (linhas, colunas, drop, botoes duplicar/propriedades/eliminar/arrastar, restricoes por componente); esquema de funcionamento detalhado (figura)
- Tecnologias: -
- Componentes: idem 9.1
- Regras e convenções: idem 9.1
- Boas práticas: -
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024)
- Estado: duplicado — duplicado parcial de 9.1 (#1024)

#### 9.3. Copiar Componentes de outra Página — #1026

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1026&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 1954 caracteres · 3 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: copiar componentes de outra pagina (COPY FROM)
- Conceitos técnicos: pagina do tipo "Component" guarda componentes padrao reutilizaveis; nao pode ser executada nem constar do menu; separador COPY FROM nas propriedades do componente
- Tecnologias: -
- Componentes: separatorList (exemplo), COPY FROM
- Regras e convenções: paginas Component nao sao executaveis nem entram no menu
- Boas práticas: centralizar componentes repetidos numa pagina Component (padronizacao e upgrade)
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024); 9.2. Design de Páginas (#1025)
- Estado: ok — ok

#### 9.4. Propriedades dos Componentes e Campos — #1027

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1027&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 2059 caracteres · 5 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: propriedades de componentes e campos
- Conceitos técnicos: separadores STYLE (ID, Class, estilo), XSL (desmarcar Default permite editar o XSL do componente mas bloqueia a edicao de propriedades), COPY FROM, PROPERTIES; nos campos: RULES (eventos JavaScript/Ajax)
- Tecnologias: XSL, CSS, JavaScript
- Componentes: todos
- Regras e convenções: XSL personalizado (Default desmarcado) impede editar as propriedades no gerador
- Boas práticas: preferir propriedades/RULES a XSL personalizado [inferido]
- Relações (documentos relacionados no portal): 5.2. Criação de uma Nova Página (#1021); 9.1. Gerador de Código (#1024); 9.2. Design de Páginas (#1025)
- Estado: ok — ok; promete lista de propriedades que esta em 9.5

#### 9.5. Propriedades Comuns dos Campos — #1044

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1044&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 3641 caracteres · 2 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: propriedades comuns dos campos
- Conceitos técnicos: Change (recarrega a pagina enviando os campos), Disabled, Field Size, Is Key (valor enviado nos botoes de tabela), Java Type, Label, Maxlength, Placeholder, Readonly, Required (*), Right, Table (SeparatorList), Tag (nome no Java), Value Parser (hiperligacao para selecionar linha quando aberta por Lookup); cada campo (exceto Button) gera get/set no Model; Radio so em Table/Form List; Coordinates so com Map Viewer; Radio List e Checkbox List nao aplicaveis ao Form List; em View os campos so fazem output
- Tecnologias: -
- Componentes: campos em geral
- Regras e convenções: Tag define o nome Java; restricoes de campo por componente acima
- Boas práticas: -
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024)
- Estado: ok, ligação inacessível — ok; ligacao para documento SharePoint interno nao acessivel

#### 9.6. Geração de Código - Exemplo — #1029

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1029&dad=tutorial&isPublic=1
- Atualizado em: 18-10-2020 · 12376 caracteres · 3 imagens
- Versão: v1+v2 (estrutura gerada confirmada nos XSL_MODEL/VIEW/CONTROLLER dos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: codigo gerado - exemplo
- Conceitos técnicos: ao gravar a pagina e criado o package nosi.webapps.<app>.pages.<pagina> com PageModel (extends Model, @RParam p_<tag>), PageView (extends View; campos Field, IGRPForm, IGRPToolsBar, IGRPButton; render/setModel) e PageController (extends Controller; actionIndex com model.load(), view, renderView); cada botao gera action<Tag>; areas reservadas packages_import, index, <acao>, custom_actions; bloco #gen-example com exemplos; retorno redirect(app, pagina, acao, this.queryString())
- Tecnologias: Java
- Componentes: Model, View, Controller, IGRPForm, IGRPToolsBar, IGRPButton, TextField
- Regras e convenções: o programador so altera as tres areas reservadas; restantes areas do PageController nao devem ser alteradas; actionIndex poe a informacao no ecra
- Boas práticas: explorar Model/View gerados para conhecer os metodos de manipulacao
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024); 9.2. Design de Páginas (#1025)
- Estado: ok — ok

#### 9.7. igrpweb Blockly — #1115

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1115&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 4981 caracteres · 8 imagens
- Versão: v1+v2 (Blockly e IGRP.blockly.java.xsl presentes nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: IGRP Blockly (separador BLOCKLY)
- Conceitos técnicos: integracao Google Blockly que gera Java no Controller; workspace com bloco inicial com as acoes do DESIGN; botoes de refresh (apos mudar campos), salvaguarda e restauro; blocos padrao Logic, Loops, Math, Text, Variables; 8 categorias personalizadas: Script Inicial, Core, DAO, inserir, editar, listar, apagar (DAO e CRUD so com classes DAO mapeadas); o codigo gerado nao pode ser alterado no Controller, so na workspace
- Tecnologias: Google Blockly, Java
- Componentes: Blockly
- Regras e convenções: codigo gerado pelo Blockly so se altera/remove na workspace; conhecer o design da pagina antes de programar em blocos
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.2. Table - Programação com Classes DAO (#1032); 10.5.2. Form - Programação com classes DAO (#1036)
- Estado: ok — ok; [PROJ v2.1.1] o codigo Blockly e escrito antes da area preservada - nao combinar Blockly com return e codigo manual na mesma acao

### 10. GC - Componentes

#### 10.1.1. Calendar - Configuração — #1047

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1047&dad=tutorial&isPublic=1
- Atualizado em: 20-08-2021 · 478 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Calendar - configuracao
- Conceitos técnicos: Header Views (botoes de navegacao), Views (formas de exibicao)
- Tecnologias: -
- Componentes: calendar
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.5.1. Form - Configuração (#1035); 10.5.2. Form - Programação com classes DAO (#1036)
- Estado: quase vazio — quase vazio (so 2 propriedades; resto em imagem)

#### 10.1.2. Calendar - Programação Blockly — #1210

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1210&dad=tutorial&isPublic=1
- Atualizado em: 02-09-2021 · 1047 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Calendar - Blockly
- Conceitos técnicos: marcacoes com Title, Description (tooltip), Id, Calendar Start/End (data-hora), Color
- Tecnologias: -
- Componentes: calendar, Blockly
- Regras e convenções: o separador T entre data e hora nao pode ser removido
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.1.1. Calendar - Configuração (#1047)
- Estado: ok — ok (codigo em imagem)

#### 10.2.1. Carousel - Configuração — #1048

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1048&dad=tutorial&isPublic=1
- Atualizado em: 20-08-2021 · 993 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Carousel - configuracao
- Conceitos técnicos: carousel como cabecalho com imagens; model.loadCarousel_1(Core.query(null, SELECT ... as carousel_1_label, ... as carousel_1_img))
- Tecnologias: -
- Componentes: carousel
- Regras e convenções: aliases carousel_1_label / carousel_1_img
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; usa Core.query(null, ...) = ligacao do IGRP

#### 10.2.2. Carousel - Programação Blockly — #1211

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1211&dad=tutorial&isPublic=1
- Atualizado em: 20-08-2021 · 829 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Carousel - Blockly
- Conceitos técnicos: upload de imagens numa tabela DAO e listagem no carousel
- Tecnologias: -
- Componentes: carousel, upload, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.2.1. Carousel - Configuração (#1048)
- Estado: ok — ok (codigo em imagem)

#### 10.3.1. Circle Stat Box- Configuração e Programação — #1049

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1049&dad=tutorial&isPublic=1
- Atualizado em: 25-08-2021 · 794 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Circle Stat Box - configuracao
- Conceitos técnicos: Description, Link, Percent Text, Percent Value, Size, Target
- Tecnologias: -
- Componentes: circle stat box
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: incompleto — programacao sem conteudo

#### 10.3.2. Circle Stat Box- Programação Blockly — #1212

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1212&dad=tutorial&isPublic=1
- Atualizado em: 25-08-2021 · 1162 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Circle Stat Box - Blockly
- Conceitos técnicos: percentagem com filtros where/filter; arredondamento com Precision
- Tecnologias: -
- Componentes: circle stat box, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.1. Circle Stat Box- Configuração e Programação (#1049)
- Estado: ok — ok (codigo em imagem)

#### 10.4.1. Chart - Configuração e Programação — #1042

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1042&dad=tutorial&isPublic=1
- Atualizado em: 27-10-2020 · 3329 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Chart - configuracao e programacao
- Conceitos técnicos: HasTitle, Label, Tag, Text, Title, Collapsible, Chart Type, Filter, Filter Type, Remote Filter; dados: lista de Pagina.Chart(eixoX, eixoY, valor) e model.setChart(lista)
- Tecnologias: -
- Componentes: chart
- Regras e convenções: ordem dos parametros: eixo X, eixo Y, valor
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.4.2. Chart - Exemplo Prático (#1045); 10.4.3. Chart - Programação com Blockly (#1123)
- Estado: ok — ok

#### 10.4.2. Chart - Exemplo Prático — #1045

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1045&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 2088 caracteres · 9 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Chart - exemplo pratico
- Conceitos técnicos: dashboard com form + botao Custom Return que faz forward para actionIndex; graficos simples e multi-serie; stat/circle/small box
- Tecnologias: -
- Componentes: chart, form, button
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.4.1. Chart - Configuração e Programação (#1042)
- Estado: incompleto — incompleto (codigo em imagem)

#### 10.4.3. Chart - Programação com Blockly — #1123

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1123&dad=tutorial&isPublic=1
- Atualizado em: 27-08-2021 · 2005 caracteres · 6 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Chart - Blockly
- Conceitos técnicos: graficos 2D/3D (ver o model); agrupar, estatistica (soma, media, max, min, contagem), filtros de nulos
- Tecnologias: -
- Componentes: chart, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.4.1. Chart - Configuração e Programação (#1042); 10.4.2. Chart - Exemplo Prático (#1045)
- Estado: ok — ok (codigo em imagem)

#### 10.5.1. Form - Configuração — #1035

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1035&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 704 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form - configuracao
- Conceitos técnicos: HasTitle, Collapsible, Collapsed
- Tecnologias: -
- Componentes: form
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok (curto)

#### 10.5.2. Form - Programação com classes DAO — #1036

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1036&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 3207 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form - programacao com DAO
- Conceitos técnicos: parametro isEdit + id hidden (@RParam p_id) para editar; actionSave insert/update conforme id; forward em erro repoe os dados submetidos
- Tecnologias: -
- Componentes: form, hidden, button (submit)
- Regras e convenções: id mapeado automaticamente para p_id
- Boas práticas: usar forward em erro para manter o input
- Relações (documentos relacionados no portal): 10.5.1. Form - Configuração (#1035)
- Estado: ok — ok (chavetas por fechar no exemplo)

#### 10.5.3. Form - Programação com Query — #1037

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1037&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 1406 caracteres · 0 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form - programacao com query
- Conceitos técnicos: model.load(query) com aliases iguais as tags; Core.insert/update(...).execute(); forward em erro
- Tecnologias: -
- Componentes: form
- Regras e convenções: aliases das colunas = tags dos campos
- Boas práticas: usar forward em erro
- Relações (documentos relacionados no portal): 10.5.1. Form - Configuração (#1035); 10.5.2. Form - Programação com classes DAO (#1036)
- Estado: exemplo com defeitos — defeitos: SELECT concatena model.getId(); addInt('id=:id', ...) com nome de parametro errado

#### 10.5.4. Form - Programação com Blockly — #1116

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1116&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 3805 caracteres · 5 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form - Blockly
- Conceitos técnicos: blocos para preencher (editar) e inserir/editar via DAO; codigo gerado no Controller
- Tecnologias: -
- Componentes: form, Blockly
- Regras e convenções: -
- Boas práticas: copiar o codigo gerado para a area start-code e editar ai
- Relações (documentos relacionados no portal): 9.7. igrpweb Blockly (#1115)
- Estado: ok — ok

#### 10.6.1. Form-List - Configuração e Programação — #1041

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1041&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 11174 caracteres · 10 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form-List - configuracao e programacao
- Conceitos técnicos: campos sempre abertos; Filter, No Add, No Delete, Order Table; cada campo recebe IGRPSeparatorList.Pair; linhas Model.Formlist; ids eliminados em getP_formlist_del(); setLink('save&isEdit=true')
- Tecnologias: -
- Componentes: formlist
- Regras e convenções: campos do formlist sao Pair (chave/valor)
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 10.6.2. Programação de Form-List com Blockly — #1121

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1121&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 3956 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Form-List - Blockly
- Conceitos técnicos: listar e gravar form-list na mesma transacao do form (mutacao do bloco save); FK set.IdUser(); form-list ja tem id por linha
- Tecnologias: -
- Componentes: formlist, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.6.1. Form-List - Configuração e Programação (#1041)
- Estado: ok — ok

#### 10.7.1. Separador-List - Configuração e Programação — #1038

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1038&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 10400 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Separator-List - configuracao e programacao
- Conceitos técnicos: Dialog (formulario em modal), Order Table; linhas Model.Sep com campos Pair; <sep>_id da linha; getP_<sep>_edit() e getP_<sep>_del() indicam linhas editadas/eliminadas
- Tecnologias: -
- Componentes: separatorlist
- Regras e convenções: tratar novas, editadas e eliminadas separadamente
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 10.7.2. Upload em Separador List - Configuração e Programação — #1039

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1039&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 1995 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Upload em Separator-List
- Conceitos técnicos: botao save como submit ajax; Core.uploadMultiple('p_<tag>_fk') devolve List<UploadedFile>; Core.saveFile(bytes, nome, mime) devolve id do ficheiro
- Tecnologias: -
- Componentes: separatorlist, upload
- Regras e convenções: -
- Boas práticas: verificar file.getSize() > 0
- Relações (documentos relacionados no portal): 10.7.1. Separador-List - Configuração e Programação (#1038)
- Estado: ok — ok (id fixo 227 no exemplo)

#### 10.7.3. Separador-List dentro de outro Separador-List — #1040

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1040&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 10511 caracteres · 6 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Separator-List dentro de Separator-List
- Conceitos técnicos: listas aninhadas com <sep>_id e getP_<sep>_edit/_del por nivel
- Tecnologias: -
- Componentes: separatorlist
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.7.1. Separador-List - Configuração e Programação (#1038); 10.7.2. Upload em Separador List - Configuração e Programação (#1039)
- Estado: ok — ok

#### 10.7.4. Programação de Separador-Lista com Blockly — #1120

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1120&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 3335 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Separator-List - Blockly
- Conceitos técnicos: programacao igual a form-list; o separator-list nem sempre edita todas as linhas
- Tecnologias: -
- Componentes: separatorlist, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.21. Separador - Configuração e Programação (#1093); 10.7.1. Separador-List - Configuração e Programação (#1038); 10.7.2. Upload em Separador List - Configuração e Programação (#1039)
- Estado: ok — ok

#### 10.8.1. Small Box - Configuração e Programação — #1060

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1060&dad=tutorial&isPublic=1
- Atualizado em: 11-09-2021 · 623 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Small Box - configuracao
- Conceitos técnicos: Refresh Parent (modal), Target, Url, Url Label
- Tecnologias: -
- Componentes: small box
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.1. Circle Stat Box- Configuração e Programação (#1049); 10.24. Quick Button Box - Configuração (#1058)
- Estado: ok — ok

#### 10.8.2. Small Box - Programação Blockly — #1213

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1213&dad=tutorial&isPublic=1
- Atualizado em: 11-09-2021 · 1508 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Small Box - Blockly
- Conceitos técnicos: estatistica (getMax) via DAO: model.setSmallbox_1_val / setSmallbox_1_url(Core.getIGRPLink(app,pagina,acao))
- Tecnologias: -
- Componentes: small box, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.2. Circle Stat Box- Programação Blockly (#1212); 10.9.1. Stat Box - Configuração e Programação (#1061); 10.8.1. Small Box - Configuração e Programação (#1060)
- Estado: ok — ok

#### 10.9.1. Stat Box - Configuração e Programação — #1061

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1061&dad=tutorial&isPublic=1
- Atualizado em: 11-09-2021 · 549 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Stat Box - configuracao
- Conceitos técnicos: Refresh Parent, Target, Url, Url Label
- Tecnologias: -
- Componentes: stat box
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.1. Circle Stat Box- Configuração e Programação (#1049); 10.24. Quick Button Box - Configuração (#1058)
- Estado: ok — ok

#### 10.9.2. Stat Box - Programação Blockly — #1214

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1214&dad=tutorial&isPublic=1
- Atualizado em: 11-09-2021 · 1462 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Stat Box - Blockly
- Conceitos técnicos: getAvg com where like; model.setStatbox_1_val
- Tecnologias: -
- Componentes: stat box, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.2. Circle Stat Box- Programação Blockly (#1212); 10.8.2. Small Box - Programação Blockly (#1213); 10.9.1. Stat Box - Configuração e Programação (#1061)
- Estado: ok — ok

#### 10.10.1. Table - Configuração — #1030

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1030&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 8245 caracteres · 19 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Table - configuracao
- Conceitos técnicos: List_page + Form_page; campo id hidden isKey envia p_<tag> nos botoes de tabela (view.<campo>.setParam(true)); botoes edit (Submit Modal, Refresh parent), delete (Submit), add na toolsbar (Modal); classe interna Pagina.Tabela
- Tecnologias: -
- Componentes: table, hidden isKey, button, toolsbar
- Regras e convenções: campo isKey para passar o id da linha
- Boas práticas: CRUD Generator como referencia
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024)
- Estado: ok — ok

#### 10.10.2. Table - Programação com Classes DAO — #1032

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1032&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 9049 caracteres · 8 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Table - programacao com DAO
- Conceitos técnicos: componentes de lista geram classe interna no Model; List<Pagina.Tabela> + model.setTabela(lista)
- Tecnologias: -
- Componentes: table
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.3. Table - Programação com Query (#1031); 10.10.1. Table - Configuração (#1030)
- Estado: ok — ok

#### 10.10.3. Table - Programação com Query — #1031

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1031&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 3385 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Table - programacao com query
- Conceitos técnicos: model.loadTable_<x>(Core.query(conn, sql)) com aliases iguais as tags; filtros com query.andWhere; ajustar linhas apos carregar; link de report por linha
- Tecnologias: -
- Componentes: table
- Regras e convenções: aliases = tags (caso contrario nao funciona)
- Boas práticas: filtros por andWhere (parametrizado)
- Relações (documentos relacionados no portal): 10.10.1. Table - Configuração (#1030)
- Estado: ok — ok

#### 10.10.4. Filtros em Tabelas — #1033

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1033&dad=tutorial&isPublic=1
- Atualizado em: 19-10-2020 · 3622 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Filtros em tabelas
- Conceitos técnicos: botao search com Custom Return que faz forward para index; target Submit Ajax preferivel a Submit Form; filtro DAO com andWhere like
- Tecnologias: -
- Componentes: table, form, button
- Regras e convenções: Custom Return no botao de pesquisa
- Boas práticas: Submit Ajax para nao recarregar a pagina inteira
- Relações (documentos relacionados no portal): 10.10.1. Table - Configuração (#1030); 10.10.3. Table - Programação com Query (#1031); 10.10.2. Table - Programação com Classes DAO (#1032)
- Estado: exemplo com defeitos — variante query concatena valores do utilizador no SQL [ENG: injecao]

#### 10.10.5. Checkbox em Tabelas - Configuração e Programação — #1034

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1034&dad=tutorial&isPublic=1
- Atualizado em: 08-08-2024 · 3343 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Checkbox em tabelas
- Conceitos técnicos: checkbox = <tag> (id da linha) + <tag>_check; dispensa hidden; Core.extractCheckBox(p_<tag>_fk, p_<tag>_check_fk) -> CheckBoxHelper.getChekedIds()/getUncheckedIds()
- Tecnologias: -
- Componentes: table, checkbox
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.4. Filtros em Tabelas (#1033); 10.10.1. Table - Configuração (#1030); 13.5. Remote com Switch em Table (#1103)
- Estado: exemplo com defeitos — defeitos no exemplo (variaveis trocadas, newDocument)

#### 10.10.6. Table - Programação com Blockly — #1117

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1117&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 4946 caracteres · 7 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Table - Blockly
- Conceitos técnicos: bloco table com setters por coluna; filtros andWhere/andWhereBetween; botao pesquisar Custom Return; FK para outra classe DAO
- Tecnologias: -
- Componentes: table, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 9.7. igrpweb Blockly (#1115); 10.5.4. Form - Programação com Blockly (#1116)
- Estado: ok — ok

#### 10.11.1. Timeline - Configuração — #1063

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1063&dad=tutorial&isPublic=1
- Atualizado em: 13-09-2021 · 325 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Timeline - configuracao
- Conceitos técnicos: titulo, texto e data por item
- Tecnologias: -
- Componentes: timeline
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: quase vazio — quase vazio

#### 10.11.2. Timeline - Programação Blockly — #1215

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1215&dad=tutorial&isPublic=1
- Atualizado em: 13-09-2021 · 1128 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Timeline - Blockly
- Conceitos técnicos: fases de um pedido a partir de tabela
- Tecnologias: -
- Componentes: timeline, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.11.1. Timeline - Configuração (#1063)
- Estado: ok — ok

#### 10.12.1. Tree Menu - Configuração e Programação — #1065

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1065&dad=tutorial&isPublic=1
- Atualizado em: 16-09-2021 · 5033 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Tree Menu - configuracao e programacao
- Conceitos técnicos: Has Tooltip, Remote (niveis seguintes carregados por pedido), Target, Value parser, Search, Call on load; exemplo do proprio portal (Listar_documentos.Treemenu_1)
- Tecnologias: -
- Componentes: treemenu
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; confirmado: o portal usa a acao remote_treemenu_1 para os filhos

#### 10.12.2. Tree-Menu - Programação Blockly — #1216

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1216&dad=tutorial&isPublic=1
- Atualizado em: 17-09-2021 · 2988 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Tree Menu - Blockly
- Conceitos técnicos: dois niveis (level 1/2) e formulario carregado pelo p_id do link
- Tecnologias: -
- Componentes: treemenu, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.12.1. Tree Menu - Configuração e Programação (#1065)
- Estado: ok — ok

#### 10.13.1. Vertical Menu - Configuração — #1067

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1067&dad=tutorial&isPublic=1
- Atualizado em: 17-09-2021 · 126 caracteres · 0 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Vertical Menu - configuracao
- Conceitos técnicos: Dynamic Menu (botoes por Java)
- Tecnologias: -
- Componentes: vertical menu
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.12.1. Tree Menu - Configuração e Programação (#1065)
- Estado: quase vazio — quase vazio

#### 10.13.2. Vertical Menu - Programação Blockly — #1217

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1217&dad=tutorial&isPublic=1
- Atualizado em: 17-09-2021 · 2180 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Vertical Menu - Blockly
- Conceitos técnicos: lista com links e Target Submit Ajax; formulario pelo id
- Tecnologias: -
- Componentes: vertical menu, Blockly
- Regras e convenções: -
- Boas práticas: Submit Ajax para atualizar so componentes
- Relações (documentos relacionados no portal): 10.13.1. Vertical Menu - Configuração (#1067)
- Estado: ok — ok

#### 10.14.1. View - Configuração e Programação — #1069

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1069&dad=tutorial&isPublic=1
- Atualizado em: 24-09-2021 · 1341 caracteres · 2 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: View - configuracao e programacao
- Conceitos técnicos: so output; Imagem; model.setView_<x>_img(Core.getLinkFile(id))
- Tecnologias: -
- Componentes: view
- Regras e convenções: campos da View so fazem output
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: exemplo com defeitos — gralha getLasrstName no exemplo

#### 10.14.2. View - Programação Blockly — #1218

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1218&dad=tutorial&isPublic=1
- Atualizado em: 24-09-2021 · 938 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: View - Blockly
- Conceitos técnicos: preencher View por id; campo de imagem por defeito removivel
- Tecnologias: -
- Componentes: view, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.14.1. View - Configuração e Programação (#1069)
- Estado: ok — ok

#### 10.15. Box - Configuração — #1046

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1046&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 274 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Box - configuracao
- Conceitos técnicos: encapsula outros componentes
- Tecnologias: -
- Componentes: box
- Regras e convenções: box so recebe componentes
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.1. Table - Configuração (#1030); 10.5.1. Form - Configuração (#1035)
- Estado: quase vazio — quase vazio

#### 10.16. Finger Print -   Configuração — #1050

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1050&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 432 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Finger Print - configuracao
- Conceitos técnicos: impressoes digitais, foto e assinatura (ex.: CNI); View Only
- Tecnologias: -
- Componentes: finger print
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: curto — curto

#### 10.17. Iframe - Configuração — #1051

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1051&dad=tutorial&isPublic=1
- Atualizado em: 25-04-2021 · 503 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Iframe - configuracao
- Conceitos técnicos: Action, Boxed; model.setIframe_1_src(url)
- Tecnologias: -
- Componentes: iframe
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 10.18. Info-Painel - Configuração — #1052

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1052&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 509 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Info-Painel - configuracao
- Conceitos técnicos: Refresh Parent, Target, Value, Url
- Tecnologias: -
- Componentes: info painel
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.1. Circle Stat Box- Configuração e Programação (#1049)
- Estado: ok — ok

#### 10.19. Leaftet Map — #1053

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1053&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 377 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Leaflet Map
- Conceitos técnicos: marcar pontos no mapa (Cabo Verde); Markers Table
- Tecnologias: -
- Componentes: leaflet map
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: exemplo com defeitos — curto; titulo com gralha (Leaftet)

#### 10.20. Map Chart - Configuração — #1054

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1054&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 1059 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Map Chart - configuracao
- Conceitos técnicos: Basemap (geojson), Basemap Label, Configuration (json), Data (json), Export, Tooltip, Tooltip Format
- Tecnologias: -
- Componentes: map chart
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.19. Leaftet Map (#1053)
- Estado: ok — ok

#### 10.21. Map Viewer - Configuração — #1055

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1055&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 1489 caracteres · 5 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Map Viewer - configuracao
- Conceitos técnicos: Basemap, Default; capturar coordenadas para campo Coordinates (Action para a pagina do mapa)
- Tecnologias: -
- Componentes: map viewer, coordinates
- Regras e convenções: campo Coordinates usa Map Viewer
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.19. Leaftet Map (#1053); 10.20. Map Chart - Configuração (#1054)
- Estado: ok — ok

#### 10.22. Panels - Configuração — #1056

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1056&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 273 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Panels - configuracao
- Conceitos técnicos: paineis colapsaveis de componentes
- Tecnologias: -
- Componentes: panels
- Regras e convenções: panel so recebe componentes
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.15. Box - Configuração (#1046)
- Estado: quase vazio — quase vazio

#### 10.23. Paragraph - Configuração — #1057

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1057&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 3150 caracteres · 3 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Paragraph - configuracao
- Conceitos técnicos: exemplo Hello World; Boxed; texto definido no design ou por codigo (view.<paragrafo>.setValue)
- Tecnologias: -
- Componentes: paragraph, section header
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 10.24. Quick Button Box - Configuração — #1058

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1058&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 257 caracteres · 1 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Quick Button Box - configuracao
- Conceitos técnicos: caixa-botao para URL
- Tecnologias: -
- Componentes: quick button box
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.3.1. Circle Stat Box- Configuração e Programação (#1049); 10.22. Panels - Configuração (#1056)
- Estado: quase vazio — quase vazio

#### 10.25. Section Header - Configuração e Programação — #1059

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1059&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 236 caracteres · 0 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Section Header - configuracao e programacao
- Conceitos técnicos: titulo fixo ou por codigo: view.<sectionheader>.setValue(...)
- Tecnologias: -
- Componentes: section header
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: exemplo com defeitos — curto; gralha sectioheader_1

#### 10.26. Tab - Configuração e Programação — #1062

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1062&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 2706 caracteres · 6 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Tab - configuracao e programacao
- Conceitos técnicos: Justified, Control Active; separador ativo definido no index (ex.: model.setClients('1'))
- Tecnologias: -
- Componentes: tab
- Regras e convenções: tab so recebe componentes
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.15. Box - Configuração (#1046)
- Estado: ok — ok

#### 10.27. Toolsbar - Configuração — #1064

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1064&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 1297 caracteres · 4 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Toolsbar - configuracao
- Conceitos técnicos: Align, Dynamic Menu, Icon Inline, Outline, Style
- Tecnologias: -
- Componentes: toolsbar
- Regras e convenções: toolsbar so recebe botoes
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 10.28. Treelist - Configuração — #1066

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1066&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 118 caracteres · 0 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Treelist - configuracao
- Conceitos técnicos: lista de botoes com links
- Tecnologias: -
- Componentes: treelist
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: quase vazio — quase vazio

#### 10.29. Vídeo - Configuração — #1068

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1068&dad=tutorial&isPublic=1
- Atualizado em: 20-10-2020 · 180 caracteres · 0 imagens
- Versão: v1+v2 (componente do gerador IGRP2.3 presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Video - configuracao
- Conceitos técnicos: Boxed, Text (URL do video)
- Tecnologias: -
- Componentes: video
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: quase vazio — quase vazio

### 11. GC - Fields

#### 11.1.1. Button - Configuração e Programação — #1072

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1072&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 8980 caracteres · 8 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Button - configuracao e programacao
- Conceitos técnicos: sem dados no Model; cada botao gera action<Tag> ao gravar; propriedades Action, Class, Custom return, Icon, Fields (Change Src), Label, Tag, Parent (Tree List), Refresh Parent, Service (BizTalk, inativo), Target, Transaction; Targets: Alert Submit, Back, Change src, Close, Close and Refresh Parent, Confirm, FormList Lookup, Modal, New Tab, Popup, Right Panel, Scroll To Top, Self, Submit, Submit Ajax, Submit Form, Submit Modal, Submit Popup, Submit Right Panel, Void; retornos renderView(view), redirect(app,pagina,acao[,queryString]) (padrao, novo GET), forward(...) (mantem o input submetido; util em erro), Call (BPMN); bloco #gen-example
- Tecnologias: -
- Componentes: button
- Regras e convenções: metodo = action + Tag; areas fora das reservadas nao podem ser alteradas; Transaction para botoes restritos
- Boas práticas: forward em erro de validacao; redirect apos sucesso
- Relações (documentos relacionados no portal): 10.27. Toolsbar - Configuração (#1064)
- Estado: ok — ok

#### 11.1.2. Custom Return — #1073

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1073&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 596 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Custom Return
- Conceitos técnicos: ativar Custom Return impede a geracao automatica do return do metodo do botao; o programador tem de devolver o Response (ex.: return this.forward(...))
- Tecnologias: -
- Componentes: button
- Regras e convenções: com Custom Return a area preservada tem de devolver sempre um Response; sem ele, nao terminar a area com return incondicional [PROJ v2.1.1 - unreachable statement]
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.1.1. Button - Configuração e Programação (#1072)
- Estado: ok — ok (curto); [PROJ] a 1.a gravacao de pagina nova com Custom Return falha a compilacao (tambem referido em 9.1)

#### 11.1.3. Programação de botão Editar e Eliminar com Blockly — #1118

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1118&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 2117 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Botoes Editar/Eliminar com Blockly
- Conceitos técnicos: editar envia chave primaria + isEdit; eliminar escolhe classe DAO e chave; detalhes envia so a chave
- Tecnologias: -
- Componentes: button, table, Blockly
- Regras e convenções: blocos de envio de parametros exigem um campo isKey na tabela
- Boas práticas: -
- Relações (documentos relacionados no portal): 9.7. igrpweb Blockly (#1115); 10.5.4. Form - Programação com Blockly (#1116); 10.10.6. Table - Programação com Blockly (#1117)
- Estado: ok — ok

#### 11.2.1. Number - Configuração e Programação — #1074

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1074&dad=tutorial&isPublic=1
- Atualizado em: 10-03-2021 · 3003 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Number - configuracao e programacao
- Conceitos técnicos: so numeros; Java Type (Integer, Double, String...); Min/Max Value; conversoes Core.toInt(valor[,defeito]) (0 em erro), toShort, toLong, toDouble, toFloat, toBigDecimal...
- Tecnologias: -
- Componentes: number
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.2.2. Number - Propriedade Calculation (#1075)
- Estado: ok — ok; exemplo de preenchimento colocado na area save

#### 11.2.2. Number - Propriedade Calculation — #1075

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1075&dad=tutorial&isPublic=1
- Atualizado em: 05-02-2024 · 1797 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Number - propriedade Calculation
- Conceitos técnicos: expressao matematica com {tag} dos campos (incl. ternario); Number Format: ceil, ceil:X, round, round:X, floor, abs, fixed:X (combinaveis por virgula)
- Tecnologias: -
- Componentes: number
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.2.1. Number - Configuração e Programação (#1074)
- Estado: ok — ok (2024)

#### 11.3.1. Text - Configuração e Programação — #1076

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1076&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1106 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Text - configuracao e programacao
- Conceitos técnicos: recebe/devolve String; vazio devolve ""; set/get no Model
- Tecnologias: -
- Componentes: text
- Regras e convenções: maxlength igual ao tamanho da coluna na BD
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; propriedades listadas (Url, Target) parecem copiadas de outro componente

#### 11.4.1. Select/ComboBox - Configuração e Programação — #1070

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1070&dad=tutorial&isPublic=1
- Atualizado em: 06-09-2024 · 7733 caracteres · 4 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Select/ComboBox - configuracao e programacao
- Conceitos técnicos: recebe Map chave->valor e devolve a chave; Domain; Dynamic Option; Multiple (String[]); HashMap ordena por chave, LinkedHashMap mantem a ordem; opcao <null, "--select--"> bloqueia submissao se Required; selecionar com model.set<tag>(chave); view.<tag>.setValue(map) ou setQuery
- Tecnologias: -
- Componentes: select/combobox
- Regras e convenções: Java Type coerente com a coluna (ex.: Integer)
- Boas práticas: LinkedHashMap para ordem controlada
- Relações (documentos relacionados no portal): 11.4.3. Preencher Combobox, Checkbox, Radiolist com Blockly (#1119); 4.6. Gestão de Domínio (#1012); 13.3. Remote Combo-box (#1101)
- Estado: ok — ok (2024)

#### 11.4.2. Campo de Seleção - Programação com DAO — #1071

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1071&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 2482 caracteres · 0 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Campo de selecao com DAO
- Conceitos técnicos: Map a partir de findAll(); posicionar valor em edicao; gravar FK com findOne(model.get<tag>())
- Tecnologias: -
- Componentes: select/combobox
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 4.6. Gestão de Domínio (#1012); 11.4.1. Select/ComboBox - Configuração e Programação (#1070)
- Estado: ok — ok

#### 11.4.3. Preencher Combobox, Checkbox, Radiolist com Blockly — #1119

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1119&dad=tutorial&isPublic=1
- Atualizado em: 17-08-2021 · 1946 caracteres · 3 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Combobox/Checkbox/Radiolist com Blockly
- Conceitos técnicos: bloco option chave-valor manual ou a partir de DAO (chave = id)
- Tecnologias: -
- Componentes: select, checkboxlist, radiolist, Blockly
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 9.7. igrpweb Blockly (#1115); 10.5.4. Form - Programação com Blockly (#1116); 10.10.6. Table - Programação com Blockly (#1117)
- Estado: ok — ok

#### 11.4.4. Load Service Data — #1224

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1224&dad=tutorial&isPublic=1
- Atualizado em: 06-08-2026 · 3962 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Load Service Data
- Conceitos técnicos: Select com pesquisa dinamica por servico da propria aplicacao: view.<campo>.propertie().setProperty("load_service_data", Core.getIGRPLink(app,pagina,acao)); valor inicial com Map; metodo action<X> recebe p_search_data e devolve JSON (id/text)
- Tecnologias: -
- Componentes: select
- Regras e convenções: -
- Boas práticas: usar em listas grandes para nao carregar tudo na abertura
- Relações (documentos relacionados no portal): 11.4.3. Preencher Combobox, Checkbox, Radiolist com Blockly (#1119); 11.4.1. Select/ComboBox - Configuração e Programação (#1070); 13.3. Remote Combo-box (#1101)
- Estado: ok — ok (2026); suportado nos dois ramos: select2.init.js envia p_search_data [CODIGO]

#### 11.5. Check-box - Configuração e Programação — #1077

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1077&dad=tutorial&isPublic=1
- Atualizado em: 08-08-2024 · 4065 caracteres · 3 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Check-box - configuracao e programacao
- Conceitos técnicos: valor boleano; Switch; Integer: marcado com 1; String: marcado com "1" e devolve "1" ou ""
- Tecnologias: -
- Componentes: checkbox
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.5. Checkbox em Tabelas - Configuração e Programação (#1034); 13.5. Remote com Switch em Table (#1103)
- Estado: ok — ok (2024); exemplo com system.out (minuscula)

#### 11.6. Check-box List - Configuração — #1078

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1078&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1880 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Check-box List - configuracao
- Conceitos técnicos: Map chave->valor; devolve String[] das chaves marcadas; Child Size; Domain; Java Type String[]
- Tecnologias: -
- Componentes: checkboxlist
- Regras e convenções: Java Type String[]
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.5. Checkbox em Tabelas - Configuração e Programação (#1034); 11.5. Check-box - Configuração e Programação (#1077)
- Estado: ok — ok; referencia cruzada partida

#### 11.7. Color - Configuração e Programação — #1079

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1079&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 939 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Color - configuracao e programacao
- Conceitos técnicos: Format do codigo de cor; set/get String (ex.: #f6ba00); comportamento diferente em tabela
- Tecnologias: -
- Componentes: color
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.8. Coordinates - Configuração e Programação — #1080

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1080&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 4956 caracteres · 10 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Coordinates - configuracao e programacao
- Conceitos técnicos: Action (pagina) e Map (Map Viewer) para captar coordenadas; get/set como qualquer campo
- Tecnologias: -
- Componentes: coordinates, map viewer
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.19. Leaftet Map (#1053); 10.20. Map Chart - Configuração (#1054)
- Estado: exemplo com defeitos — defeito: condicao trainee != null || !trainee.hasError() (deveria ser &&)

#### 11.9. Date - Configuração e Programação — #1081

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1081&dad=tutorial&isPublic=1
- Atualizado em: 07-08-2025 · 4521 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Date - configuracao e programacao
- Conceitos técnicos: String dd-MM-yyyy; Readonly recomendado (data so pelo seletor); Class; From/To (intervalo); Core.dateToString(data, formato); Core.formatDate; Core.ToDate(str, formato) -> java.sql.Date
- Tecnologias: -
- Componentes: date
- Regras e convenções: formato dd-MM-yyyy
- Boas práticas: campo Readonly para evitar formatos invalidos
- Relações (documentos relacionados no portal): -
- Estado: ok — ok (2025); exemplo usa padrao dd-mm-yyyy (mm = minutos)

#### 11.10. Email - Configuração e Programação — #1082

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1082&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 4992 caracteres · 3 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Email - configuracao e programacao
- Conceitos técnicos: valida formato de email; envio de email configurado em main.xml (mail.smtp.host, port, auth, socketFactory, mail.user, mail.password) e Core.mail(...)
- Tecnologias: -
- Componentes: email, main.xml
- Regras e convenções: -
- Boas práticas: [ENG] nao guardar a password de email em claro no repositorio
- Relações (documentos relacionados no portal): 11.3.1. Text - Configuração e Programação (#1076)
- Estado: ok — ok

#### 11.11. External Link - Configuração e Programação — #1083

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1083&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 716 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: External Link - configuracao e programacao
- Conceitos técnicos: input/output de URLs com validacao de formato
- Tecnologias: -
- Componentes: external link
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.12. Hidden - Configuração e Programação — #1084

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1084&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1037 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Hidden - configuracao e programacao
- Conceitos técnicos: guarda valores (ids) fora da vista; em tabela com isKey envia p_<tag> nos botoes da linha
- Tecnologias: -
- Componentes: hidden
- Regras e convenções: -
- Boas práticas: [ENG] o valor hidden e manipulavel pelo cliente: validar no servidor
- Relações (documentos relacionados no portal): 11.2.1. Number - Configuração e Programação (#1074)
- Estado: ok — ok

#### 11.13. Hyperlink - Configuração e Programação — #1085

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1085&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 8302 caracteres · 7 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Hyperlink - configuracao e programacao
- Conceitos técnicos: link para localizacoes dentro/fora da aplicacao sem executar Java; Action, Button (SeparatorList), Buttons Size, Custom Action, Class, Icon, Target, Show Header; exemplo de link para ficheiro em modal
- Tecnologias: -
- Componentes: hyperlink, table
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.1.1. Button - Configuração e Programação (#1072); 11.11. External Link - Configuração e Programação (#1083)
- Estado: ok — ok

#### 11.14. Image - Configuração e Programação — #1086

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1086&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1744 caracteres · 3 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Image - configuracao e programacao
- Conceitos técnicos: exibicao e upload; Croppie (recorte), Rounded, Auto Upload (grava na BD e envia o id); view.<campo>.setValue(Core.getLinkFile(id)); id em p_<campo>
- Tecnologias: -
- Componentes: image
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; [PROJ v2.1.1] o setModel gerado nao liga o campo img ao Model: usar view.<campo>.setValue

#### 11.15. Lookup - Configuração e Programação — #1087

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1087&dad=tutorial&isPublic=1
- Atualizado em: 23-04-2021 · 6502 caracteres · 8 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Lookup - configuracao e programacao
- Conceitos técnicos: Action (pagina de lista), LookupParams (Target Field / Value Field), Class; pagina de lista com campo Value Parser e hidden isKey; preenche lookup e hidden na origem
- Tecnologias: -
- Componentes: lookup, table, hidden
- Regras e convenções: a tabela da pagina de lookup precisa de um campo value parser
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.1. Table - Configuração (#1030)
- Estado: ok — ok

#### 11.16. Password - Configuração e Programação — #1088

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1088&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 812 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Password - configuracao e programacao
- Conceitos técnicos: esconde o texto; Virtual Keyboard opcional; Core.encrypt(password) com a chave padrao
- Tecnologias: -
- Componentes: password
- Regras e convenções: -
- Boas práticas: [ENG] para credenciais usar hashing (ex.: bcrypt) e nao cifra reversivel
- Relações (documentos relacionados no portal): 11.3.1. Text - Configuração e Programação (#1076)
- Estado: exemplo com defeitos — ok; gralha Strign

#### 11.17. Plain-text - Configuração e Programação — #1089

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1089&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 948 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Plain-text - configuracao e programacao
- Conceitos técnicos: exibe texto/espaco num componente; Clear (linha inteira); model.set<tag>(texto)
- Tecnologias: -
- Componentes: plaintext
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.3.1. Text - Configuração e Programação (#1076)
- Estado: ok — ok

#### 11.18. Radio - Configuração — #1090

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1090&dad=tutorial&isPublic=1
- Atualizado em: 24-07-2021 · 689 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Radio - configuracao
- Conceitos técnicos: como checkbox: <tag> e <tag>_check; valor selecionado obtido com Core.getParam("p_<tag>_fk")
- Tecnologias: -
- Componentes: radio, table
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.10.5. Checkbox em Tabelas - Configuração e Programação (#1034); 11.6. Check-box List - Configuração (#1078); 11.5. Check-box - Configuração e Programação (#1077)
- Estado: exemplo com defeitos — ok; variavel cheched/checked inconsistente

#### 11.19. RadioList - Configuração e Programação — #1091

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1091&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1459 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: RadioList - configuracao e programacao
- Conceitos técnicos: Map chave->valor; devolve a chave; Child Size; Domain; Java Type
- Tecnologias: -
- Componentes: radiolist
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 11.5. Check-box - Configuração e Programação (#1077); 11.6. Check-box List - Configuração (#1078)
- Estado: ok — ok

#### 11.20. Range - Configuração e Programação — #1092

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1092&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1051 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Range - configuracao e programacao
- Conceitos técnicos: inteiro (aceita negativos); RangeMin, RangeMax
- Tecnologias: -
- Componentes: range
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.21. Separador - Configuração e Programação — #1093

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1093&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 677 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Separador - configuracao e programacao
- Conceitos técnicos: organiza campos em Form/View/SeparatorList; view.<tag>.setLabel(...)
- Tecnologias: -
- Componentes: separator
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.22. Text-Area - Configuração e Programação — #1094

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1094&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 826 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Text-Area - configuracao e programacao
- Conceitos técnicos: texto longo; vazio devolve ""
- Tecnologias: -
- Componentes: textarea
- Regras e convenções: maxlength igual ao tamanho da coluna na BD
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.23. Text-Editor - Configuração e Programação — #1095

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1095&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 968 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Text-Editor - configuracao e programacao
- Conceitos técnicos: devolve conteudo formatado (marcacao) em vez de texto puro
- Tecnologias: -
- Componentes: texteditor
- Regras e convenções: dimensionar a coluna para incluir as tags de formatacao
- Boas práticas: [ENG] sanitizar o HTML guardado antes de o voltar a mostrar
- Relações (documentos relacionados no portal): 11.3.1. Text - Configuração e Programação (#1076)
- Estado: ok — ok

#### 11.24. Time - Configuração e Programação — #1096

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1096&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 1248 caracteres · 1 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Time - configuracao e programacao
- Conceitos técnicos: String HH:mm (24h); hora invalida nao e exibida; Core.dateToString / Core.ToChar
- Tecnologias: -
- Componentes: time
- Regras e convenções: formato HH:mm
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok

#### 11.25. Upload File - Configuração e Programação — #1097

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1097&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 8275 caracteres · 3 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Upload File - configuracao e programacao
- Conceitos técnicos: Accept (extensoes), Class, Multiple, Rend Value, Target Rend; ficheiro em p_<tag>; Core.saveFile("p_<tag>") devolve id (>0 em sucesso); atualizar ficheiro existente
- Tecnologias: -
- Componentes: upload
- Regras e convenções: -
- Boas práticas: [ENG] validar tipo e tamanho no servidor (Accept e so no cliente)
- Relações (documentos relacionados no portal): 11.13. Hyperlink - Configuração e Programação (#1085)
- Estado: ok — ok

#### 11.26. Virtual Keyboard - Configuração — #1098

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1098&dad=tutorial&isPublic=1
- Atualizado em: 21-10-2020 · 886 caracteres · 2 imagens
- Versão: v1+v2 (campo do gerador presente nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Virtual Keyboard - configuracao
- Conceitos técnicos: alternativa ao Password contra keyloggers; Core.encrypt na captura
- Tecnologias: -
- Componentes: virtual keyboard
- Regras e convenções: -
- Boas práticas: [ENG] idem 11.16 (hashing para credenciais)
- Relações (documentos relacionados no portal): 11.16. Password - Configuração e Programação (#1088)
- Estado: ok — ok

### 12. Gestão de Acessos

#### 12.1. Gestão de Acessos — #1133

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1133&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 4703 caracteres · 18 imagens
- Versão: v1+v2 (Permission/hasMenuPagPermition e isPermission presentes nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: gestao de acessos (visao geral)
- Conceitos técnicos: sessoes e privilegios implementados no framework; administrador gere menus e transactions atribuidos hierarquicamente a Organicas > Perfis > Utilizadores; acesso no Studio (desenvolvimento) e pelo menu da aplicacao em producao (sem Studio); fluxo: criar organica, perfil, convidar utilizador
- Tecnologias: -
- Componentes: Gestao de Acesso, Organica, Perfil, Utilizador, Menu, Transaction
- Regras e convenções: em producao a gestao de acesso e feita pelo administrador atraves do menu da aplicacao
- Boas práticas: o programador foca-se no negocio; privilegios configurados, nao programados
- Relações (documentos relacionados no portal): 4.1. IGRP Studio - Apresentação (#1008); 9.1. Gerador de Código (#1024)
- Estado: ok — ok; texto repetido; [CODIGO] lista fixa de rotas sem login em PagesScapePermission (verificar em auditoria)

#### 12.2. Gestão de Orgânica — #1134

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1134&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 3280 caracteres · 6 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de organicas
- Conceitos técnicos: organica = entidade/departamento; nome, codigo, aplicacao; estado; atribuir menus, transactions e processos; Core.getCurrentUser().getOrganica(), getCurrentOrganization(), getCurrentOrganizationCode(), findOrganizationByCode/ById; Organization.getId/getCode/getName/getStatus/getProfilesType
- Tecnologias: -
- Componentes: Organization
- Regras e convenções: transactions/menus atribuem-se primeiro a organica
- Boas práticas: -
- Relações (documentos relacionados no portal): 12.1. Gestão de Acessos (#1133)
- Estado: ok — ok

#### 12.3. Gestão de Menu — #1135

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1135&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 3853 caracteres · 16 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de menus
- Conceitos técnicos: menu = pagina acessivel no menu lateral; criado com "Create menu" na pagina ou na Gestao de Menu; hierarquia pai/filho; aplicacao, pagina alvo, nome, menu pai, posicao, target; atribuir a organica e depois a perfil (perfil so ve menus da sua organica)
- Tecnologias: -
- Componentes: Menu
- Regras e convenções: menus de perfil limitados aos da organica
- Boas práticas: -
- Relações (documentos relacionados no portal): 12.1. Gestão de Acessos (#1133)
- Estado: ok — ok; referencia cruzada partida ("Erro! A origem da referencia...")

#### 12.4. Gestão de Perfil — #1136

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1136&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 4691 caracteres · 14 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de perfis
- Conceitos técnicos: perfis por organica; perfil pai acompanha o filho; pagina inicial do perfil; perfis so herdam menus/transactions da organica; convidar utilizadores ja registados; um utilizador pode ter varios perfis mas so um ativo por sessao (mudar em Minha Conta); Core.getCurrentProfile(), getCurrentProfileCode(), findProfileByCode/ById; ProfileType
- Tecnologias: -
- Componentes: ProfileType
- Regras e convenções: associar permissoes a perfis; associacao direta a utilizadores so excecionalmente; definir primeiro o ambito da organica, depois dos perfis
- Boas práticas: permissoes por perfil (nao por utilizador)
- Relações (documentos relacionados no portal): 12.1. Gestão de Acessos (#1133); 12.2. Gestão de Orgânica (#1134); 12.3. Gestão de Menu (#1135)
- Estado: ok — ok

#### 12.5. Gestão de Utilizadores — #1137

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1137&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 4962 caracteres · 12 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de utilizadores
- Conceitos técnicos: adicionar utilizador (login no igrpweb) vs convidar para aplicacao (SysAdmin); atribuir menus/transactions/etapas; Core.getCurrentUser(), findUserById/ByUsername/ByEmail; User.getId/getName/getEmail/getUser_name/getProfile/getOrganica/getAplicacao/getStatus
- Tecnologias: -
- Componentes: User
- Regras e convenções: utilizador so acede a uma aplicacao depois de convidado
- Boas práticas: -
- Relações (documentos relacionados no portal): 12.1. Gestão de Acessos (#1133); 12.2. Gestão de Orgânica (#1134); 12.3. Gestão de Menu (#1135); 12.4. Gestão de Perfil (#1136)
- Estado: ok — ok

#### 12.6. Gestão de Transações — #1138

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1138&dad=tutorial&isPublic=1
- Atualizado em: 26-10-2020 · 3011 caracteres · 13 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: gestao de transactions
- Conceitos técnicos: transaction = botao que nao deve estar acessivel a todos; definido como transaction nas propriedades do botao no gerador e atribuido na Gestao de Acesso a organica, depois a perfis/utilizadores
- Tecnologias: -
- Componentes: Transaction, botao
- Regras e convenções: botoes sensiveis (ex.: eliminar) definidos como transaction e atribuidos so a quem deve executar
- Boas práticas: [ENG] validar tambem no servidor as acoes sensiveis (Permission.isPermission) e nao confiar so na visibilidade do botao
- Relações (documentos relacionados no portal): 4.6. Gestão de Domínio (#1012); 12.1. Gestão de Acessos (#1133); 12.3. Gestão de Menu (#1135); 12.4. Gestão de Perfil (#1136)
- Estado: ok — ok

### 13. GC - Remote

#### 13.1. Rules (Eventos de JavaScript e Ajax) — #1099

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1099&dad=tutorial&isPublic=1
- Atualizado em: 10-02-2026 · 6040 caracteres · 7 imagens
- Versão: v1+v2 (RULES, RemoteXML e remoteComboBoxXml presentes nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: Rules - eventos JavaScript e Ajax
- Conceitos técnicos: separador RULES do campo; propriedades Name, Event (Blur, Change, Click, Keyup, Load), Condition (Equals, Differs, Contains, Checked, Unchecked, Greater than, Between, Not Null, Null, Start/End With e negacoes, RegExp, Not RegExp, Custom com {this}/{tag}), Value, Opposite Rule, Targets, Action (Show, Show Icon, Hide, Hide Icon, Disable, Enable, Required, Not Required, Clean Value, Readonly, Not Readonly, Remote, Remote Combo Box, Remote List, Notify + Message Type/Message), Procedure (metodo action<Procedure> em custom_actions), Request fields (recebidos como p_<campo>); varias combinacoes Action/Targets por regra (adicionar ao SeparatorList antes de gravar)
- Tecnologias: JavaScript, Ajax
- Componentes: RULES, campos
- Regras e convenções: metodo remoto = action + Procedure, programado em custom_actions; parametros p_<tag>
- Boas práticas: usar RULES antes de JS proprio; alternativa: ID no STYLE + funcoes no separador JS
- Relações (documentos relacionados no portal): 13.2. Remote/Ajax (#1100); 9.1. Gerador de Código (#1024); 11.4.1. Select/ComboBox - Configuração e Programação (#1070); 13.3. Remote Combo-box (#1101); 13.4. Remote List (#1102); 13.5. Remote com Switch em Table (#1103); 13.6. Remote com Radio em Table (#1104)
- Estado: ok — ok (atualizado 2026; exemplos Custom/RegExp recentes)

#### 13.2. Remote/Ajax — #1100

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1100&dad=tutorial&isPublic=1
- Atualizado em: 19-02-2021 · 6724 caracteres · 4 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Remote/Ajax
- Conceitos técnicos: Action Remote preenche campos; metodo action<Procedure> em custom_actions recebe p_<request field>; resposta XML com this.format = Response.FORMAT_XML e renderView(String); Core.remoteXml().addPropertie(tag,valor).addMessage(tipo,texto).build() (tipos success, info, warning, error); Core.remoteComboBoxXml(Map, view.campo, selectedIds[, prompt]) e (QueryInterface, tag, selectedIds, prompt)
- Tecnologias: Ajax, XML
- Componentes: RemoteXML, Response
- Regras e convenções: resposta remota em XML com FORMAT_XML
- Boas práticas: usar o builder RemoteXML em vez de XML manual
- Relações (documentos relacionados no portal): 11.4.1. Select/ComboBox - Configuração e Programação (#1070); 11.4.2. Campo de Seleção - Programação com DAO (#1071)
- Estado: exemplo com defeitos — ok com erros de sintaxe nos exemplos (";" antes de .addPropertie, parenteses a mais)

#### 13.3. Remote Combo-box — #1101

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1101&dad=tutorial&isPublic=1
- Atualizado em: 26-12-2023 · 3906 caracteres · 4 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Remote Combo Box
- Conceitos técnicos: evento change no combobox; Action Remote Combo Box; Targets; Procedure; Request Fields; preencher via DAO (Core.toMap + Core.remoteComboBoxXml) ou query
- Tecnologias: Ajax
- Componentes: combobox
- Regras e convenções: idem 13.1
- Boas práticas: -
- Relações (documentos relacionados no portal): 13.2. Remote/Ajax (#1100); 11.4.1. Select/ComboBox - Configuração e Programação (#1070)
- Estado: exemplo com defeitos — exemplos com defeitos: marcador "custom actions " com espaco (o marcador real e custom_actions); nome de Procedure inconsistente (combo vs remoteEmployee); query concatena p_department no SQL [ENG: usar parametros nomeados]

#### 13.4. Remote List — #1102

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1102&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 4528 caracteres · 3 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Remote List
- Conceitos técnicos: Action Remote List preenche uma tabela; model.loadTable_<tabela>(Core.query(...).where(...).addInt(...)); variante DAO preenche lista de linhas Model.Table_<x> e model.setTable_<x>
- Tecnologias: Ajax
- Componentes: table, combobox
- Regras e convenções: idem 13.1
- Boas práticas: parametros nomeados na query
- Relações (documentos relacionados no portal): 13.2. Remote/Ajax (#1100); 13.3. Remote Combo-box (#1101)
- Estado: exemplo com defeitos — exemplo DAO nao compila (variavel empFilter fora de ambito)

#### 13.5. Remote com Switch em Table — #1103

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1103&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 4039 caracteres · 2 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Remote com Switch/Checkbox em tabela
- Conceitos técnicos: checkbox em tabela = dois valores: <tag> (id da linha) e <tag>_check (estado); marcado quando iguais; parametros p_<tag> e p_<tag>_check ("true"/"false"); resposta so com mensagem; em erro o campo volta ao estado inicial
- Tecnologias: Ajax
- Componentes: table, checkbox/switch
- Regras e convenções: preencher <tag> com o id e <tag>_check com o id (marcado) ou outro valor
- Boas práticas: devolver mensagem de sucesso/erro
- Relações (documentos relacionados no portal): 13.2. Remote/Ajax (#1100); 13.3. Remote Combo-box (#1101); 13.4. Remote List (#1102)
- Estado: ok — ok

#### 13.6. Remote com Radio em Table — #1104

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1104&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 5174 caracteres · 2 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: Remote com Radio em tabela
- Conceitos técnicos: radio em tabela = <tag> (id) e <tag>_check; transacao Hibernate com keepConnection num metodo auxiliar em custom_actions
- Tecnologias: Ajax, Hibernate
- Componentes: table, radio
- Regras e convenções: idem 13.5
- Boas práticas: metodos auxiliares privados em custom_actions
- Relações (documentos relacionados no portal): 13.2. Remote/Ajax (#1100); 13.3. Remote Combo-box (#1101); 13.4. Remote List (#1102); 13.5. Remote com Switch em Table (#1103)
- Estado: ok — ok

### 14. Web Services

#### 14.1. WebServices em igrpweb — #1108

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1108&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 6516 caracteres · 3 imagens
- Versão: v1 (exemplo usa javax.xml.bind.JAXB); v2 requer jakarta.xml.bind [CODIGO]  →  aplicabilidade **v1+v2 (v2: jakarta.*)**
- Tema: pagina igrpweb como webservice
- Conceitos técnicos: pagina publica (Publico) chamada pelo seu link; codigo no actionIndex; devolve XML/JSON com this.format = Response.FORMAT_XML ou FORMAT_JSON e renderView(String); classes de dados anotadas para JAXB
- Tecnologias: JAXB, XML, JSON
- Componentes: pagina publica, Response
- Regras e convenções: a pagina tem de ser publica para ser chamada de fora da aplicacao
- Boas práticas: [ENG] proteger servicos publicos (autenticacao/validacao) quando expoem dados
- Relações (documentos relacionados no portal): 14.2. Serviço REST em igrpweb (#1107)
- Estado: risco — risco: manda alterar com o File Editor a parte protegida do codigo (comentar view.setModel/renderView); essa alteracao e perdida na proxima gravacao no gerador; javax.xml.bind nao existe em v2 (usar jakarta.xml.bind)

#### 14.2. Serviço REST em igrpweb — #1107

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1107&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 8392 caracteres · 37 imagens
- Versão: v1 (javax.ws.rs); v2 usa jakarta.ws.rs [CODIGO]  →  aplicabilidade **v1+v2 (v2: jakarta.*)**
- Tema: servicos REST
- Conceitos técnicos: JAX-RS com Jersey (server/client); package nosi.webapps.<app>.restapi com classe Configuration que regista os pacotes; recursos GET/POST/PUT/DELETE; consumir com cliente Jersey (anotacao @Expose em DAO para Gson); partilha de paginas entre aplicacoes; paginas publicas com link hostname/dad
- Tecnologias: JAX-RS, Jersey, Gson
- Componentes: restapi, paginas publicas
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: incompleto — incompleto (so topicos; codigo em imagens); em v2 substituir ClientConfig por ClientBuilder (#1223)

#### 14.3. Serviço SOAP em igrpweb — #1109

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1109&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 5274 caracteres · 20 imagens
- Versão: v1 (javax.jws); v2 jakarta.jws [CODIGO]  →  aplicabilidade **v1+v2 (v2: jakarta.*)**
- Tema: servicos SOAP
- Conceitos técnicos: SOAP (envelope, header, body), WSDL, JAX-WS (@WebService, @WebMethod, @WebParam, @WebResult), JAXB; package soapservices.server/client; geracao de cliente pelo IDE
- Tecnologias: JAX-WS, JAXB, WSDL
- Componentes: -
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 14.2. Serviço REST em igrpweb (#1107); 14.1. WebServices em igrpweb (#1108)
- Estado: incompleto — incompleto (so topicos; codigo em imagens)

### 15. BD - Mapeamento DAO

#### 15.1. Mapeamento DAO com Eclipse — #1110

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1110&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 10476 caracteres · 35 imagens
- Versão: v1 (ferramentas Eclipse/JPA Facets); conceito de mapeamento v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: mapeamento DAO com Eclipse (JPA Entities from Tables)
- Conceitos técnicos: mapear tabelas em classes Java num package dao da aplicacao; ligacao de BD no Eclipse (driver PostgreSQL); JPA facet; gerar entidades; chave primaria "auto"; superclasse BaseActiveRecord<T> (substituir T pelo nome da classe); copiar a lista de classes do persistence.xml para <session-factory> do ficheiro <ligacao>.<app>.cfg.xml criado pelo Application Builder
- Tecnologias: Eclipse, JPA, Hibernate, PostgreSQL JDBC 42.2.5
- Componentes: BaseActiveRecord, cfg.xml da ligacao, package dao
- Regras e convenções: classes DAO estendem BaseActiveRecord<Classe> e sao listadas como <mapping class> no cfg.xml da ligacao
- Boas práticas: manter Associations fetch por defeito salvo conhecimento de ORM
- Relações (documentos relacionados no portal): -
- Estado: só v1 — v1 (ferramenta); package indicado como "nosi.base.activeRecord" mas o real e nosi.base.ActiveRecord [CODIGO]; em v1/v2 o CRUD/DAO Generator do Studio faz isto automaticamente (#1011)

#### 15.2. Mapeamento DAO com JBoss Tools — #1111

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1111&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 5142 caracteres · 22 imagens
- Versão: v1 (Eclipse JBoss Tools); conceito v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: mapeamento DAO com JBoss/Hibernate Tools
- Conceitos técnicos: Hibernate Code Generation (Domain code, DAO code); reveng.xml; copiar classes para session-factory do cfg.xml; import nosi.base.ActiveRecord.BaseActiveRecord; extends BaseActiveRecord<Classe> implements Serializable
- Tecnologias: Eclipse, JBoss Tools, Hibernate Tools
- Componentes: BaseActiveRecord
- Regras e convenções: idem 15.1
- Boas práticas: -
- Relações (documentos relacionados no portal): 15.1. Mapeamento DAO com Eclipse (#1110)
- Estado: só v1 — v1 (ferramenta); ok

#### 15.3. Mapeamento DAO com NetBeans IDE — #1112

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1112&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 5602 caracteres · 17 imagens
- Versão: v1 (exemplo com javax.persistence e javax.xml.bind); conceito v1+v2  →  aplicabilidade **v1 (ferramenta); conceito v1+v2**
- Tema: mapeamento DAO com NetBeans
- Conceitos técnicos: Entity Classes from Database; tipo de colecao List; classe estende BaseActiveRecord e muda o package para nosi.webapps.<app>.dao; listar no cfg.xml
- Tecnologias: NetBeans, JPA (javax.persistence), JAXB (javax.xml.bind)
- Componentes: BaseActiveRecord
- Regras e convenções: idem 15.1
- Boas práticas: -
- Relações (documentos relacionados no portal): 15.1. Mapeamento DAO com Eclipse (#1110); 15.2. Mapeamento DAO com JBoss Tools (#1111)
- Estado: contraditório, exemplo com defeitos — contradiz 18.7 (recomenda Set e EAGER; aqui List/LAZY por defeito); exemplo usa javax.xml.bind (verificar disponibilidade em v2)

### 16. Issue Tracker

#### 16.1. Como Reportar Issues em igrpweb — #1114

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1114&dad=tutorial&isPublic=1
- Atualizado em: 22-10-2020 · 6105 caracteres · 10 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: reportar issues do framework
- Conceitos técnicos: issue tracker em git.nosi.cv/igrp-web/igrp-web-framework/issues (credenciais AD); verificar duplicados; template Bug com resumo, passos, ambiente, comportamento, logs, info git, possiveis correcoes
- Tecnologias: GitLab
- Componentes: -
- Regras e convenções: verificar se a issue ja existe antes de abrir
- Boas práticas: issues com passos de reproducao e ambiente
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; texto repetido; o repositorio publico atual e github.com/NOSiCode-CV/IGRP-Framework [REPO README]

### 17. Passagem de Aplicações entre Ambientes

#### 17.1. Instrução de Passagem de Aplicações entre Ambientes — #1124

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1124&dad=tutorial&isPublic=1
- Atualizado em: 08-01-2021 · 9269 caracteres · 14 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: passagem de aplicacoes entre ambientes
- Conceitos técnicos: exportar (JAR) e importar (igual a 5.4); configurar a BD da aplicacao no ambiente destino (tipo, nome da ligacao, URL, driver, utilizador, password, testar e gravar; ligacao padrao); <ligacao>.<app>.cfg.xml com o mapeamento das classes DAO; dica: tester nao corre scripts porque DAO + cfg.xml atualizam a BD
- Tecnologias: JAR, Hibernate
- Componentes: Application Builder, File editor, cfg.xml
- Regras e convenções: configurar a ligacao de BD apos importar
- Boas práticas: ambientes separados (dev/teste/producao)
- Relações (documentos relacionados no portal): 6.1. Base de Dados - Configuração (#1014); 6.2. File Editor (#1015); 5.4. Exportar e Importar Aplicação (#1023)
- Estado: duplicado, risco — duplica 5.4 (#1023); a dica de atualizacao automatica da BD depende de hbm2ddl.auto=update - [PROJ v2.1.1] risco de alteracoes nao controladas; [ENG] preferir migracoes versionadas (Flyway ja usado pelo framework)

### 18. Dicas de Programação

#### 18.1. Modelo MVC — #1125

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1125&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 4850 caracteres · 4 imagens
- Versão: v1+v2 (padrao MVC e areas preservadas presentes nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: modelo MVC do igrpweb
- Conceitos técnicos: cada pagina tem PageModel (contentor de dados), PageView (constroi o conteudo/XML) e PageController (regras de negocio, Core, Hibernate, devolve XML); pedido chama um metodo do Controller (geralmente actionIndex); view.setModel(model); area reservada /*----#start-code(x)----*/ ... /*----#end-code----*/ preserva codigo em regeneracoes
- Tecnologias: Java, XML, Hibernate/JDBC
- Componentes: Model, View, Controller, Core
- Regras e convenções: o programador nao precisa nem deve alterar PageView e PageModel (gerados); programar no PageController, dentro da area reservada; alteracoes de layout no separador DESIGN
- Boas práticas: separar apresentacao e negocio
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024); 9.6. Geração de Código - Exemplo (#1029)
- Estado: ok — ok

#### 18.2. Principais Métodos do Core — #1127

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1127&dad=tutorial&isPublic=1
- Atualizado em: 12-11-2020 · 4198 caracteres · 0 imagens
- Versão: v1+v2 (metodos confirmados em nosi.core nos dois ramos)  →  aplicabilidade **v1+v2**
- Tema: principais metodos da classe Core
- Conceitos técnicos: testes logicos (isNull, isNotNull, isNullOrZero, isNotNullOrZero, isNotNullMultiple, isArraySameSize, isInt/isFloat/isDouble, isUploadedFiles); JSON (toJson, toJsonWithJsonBuilder, fromJson, fromJsonWithJsonBuilder); Map (toMap com prompt para combobox); criptografia (encrypt/decrypt com chave padrao ou chave secreta); aplicacao (getCurrentApp, getCurrentAppId, getCurrentDad, findApplicationByDad, findApplicationById)
- Tecnologias: Java, JSON (Gson)
- Componentes: nosi.core.webapp.Core, nosi.webapps.igrp.dao.Application
- Regras e convenções: -
- Boas práticas: [ENG] nao fixar chaves secretas no codigo (o exemplo usa uma literal)
- Relações (documentos relacionados no portal): 10.10.2. Table - Programação com Classes DAO (#1032); 10.5.2. Form - Programação com classes DAO (#1036)
- Estado: exemplo com defeitos — ok; exemplo toMap troca keyField/valueField; Javadoc referido sem ligacao verificavel

#### 18.3. Parâmetros - Envio e Recepção — #1128

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1128&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 10199 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: envio e rececao de parametros
- Conceitos técnicos: campos do Model mapeados para parametro p_<tag> (@RParam); Core.getParam/getParamInt/Short/Long/Float/Double/BigDecimal/BigInteger/Array/getParameters (com variante isRemoved, removendo da sessao por defeito); metodos do Controller getQueryString*, ; addQueryString (padrao), loadQueryString (todo o Model), forward (envia o Model como p_*), redirect; 4.o argumento this.queryString() obrigatorio para enviar parametros a outra pagina; addQueryString/loadQueryString nao funcionam no actionIndex; setLink em botoes e addParam em lookup/locator para enviar parametros a partir do actionIndex
- Tecnologias: Java
- Componentes: Model (@RParam), Controller, Core, botoes, lookup
- Regras e convenções: incluir this.queryString() em redirect/forward para outra pagina; no actionIndex usar setLink/addParam
- Boas práticas: usar addQueryString como forma padrao
- Relações (documentos relacionados no portal): 11.1.3. Programação de botão Editar e Eliminar com Blockly (#1118); 18.2. Principais Métodos do Core (#1127)
- Estado: exemplo com defeitos — ok; gralha "Core.getParamLog" (o metodo e getParamLong) [CODIGO]; texto repetido

#### 18.4. Métodos do Core para Base de dados — #1129

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1129&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 3267 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: metodos do Core para base de dados
- Conceitos técnicos: Core.defaultConnection([dad]); Core.transaction([conn]); Core.insert/update/delete(tabela | conn,tabela | conn,schema,tabela [,displayError,tracingError]) -> BaseQueryInterface; Core.query(sql | sql,Config_env | conn,sql | conn,sql,Class ...); Core.executeQuery(env|conn, sql) -> ResultSet
- Tecnologias: JDBC/Hibernate
- Componentes: Core, QueryInterface, BaseQueryInterface, ResultSet, Config_env
- Regras e convenções: -
- Boas práticas: indicar sempre o nome da ligacao (as variantes sem ligacao usam a ligacao por defeito da aplicacao atual) [PROJ]
- Relações (documentos relacionados no portal): 10.10.2. Table - Programação com Classes DAO (#1032); 10.5.3. Form - Programação com Query (#1037); 18.2. Principais Métodos do Core (#1127)
- Estado: ok — ok (lista de assinaturas sem explicacao)

#### 18.5. Transaction-RollBack — #1130

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1130&dad=tutorial&isPublic=1
- Atualizado em: 23-12-2021 · 4594 caracteres · 1 imagens
- Versão: v1+v2 (Core.transaction, keepConnection e roolback existem nos dois ramos); AppSession.doInTransaction so em v2 [CODIGO]  →  aplicabilidade **v1+v2**
- Tema: transacoes com commit/rollback
- Conceitos técnicos: transacao Hibernate via Core.getSession(conn) + session.getTransaction/begin/persist/commit/rollback/close; transacao por query via Core.transaction(): begin, insert..execute, commit, roolback (nome real do metodo), closeConnection; keepConnection() obrigatorio ao usar a mesma ligacao (BaseActiveRecord ou QueryInterface) durante uma transacao
- Tecnologias: Hibernate Session/Transaction, JDBC
- Componentes: Core, QueryInterface, BaseActiveRecord
- Regras e convenções: dentro de uma transacao usar keepConnection() nas consultas pela mesma ligacao; fechar a sessao/ligacao no finally
- Boas práticas: rollback no catch; mensagens Core.setMessageSuccess/Error
- Relações (documentos relacionados no portal): 10.10.2. Table - Programação com Classes DAO (#1032); 10.5.3. Form - Programação com Query (#1037); 11.4.2. Campo de Seleção - Programação com DAO (#1071)
- Estado: ok, contraditório — ok; [PROJ v2.1.1] getKeyValue() apos Core.insert falha em PostgreSQL (SET session audit) - contradiz o exemplo 2.2; em v2 existe AppSession.doInTransaction

#### 18.6. Interação com Base de Dados com Query — #1131

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1131&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 6625 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: interacao com BD via Query
- Conceitos técnicos: Core.query(conn, sql).where("id=:p").addInt(...) e model.load(query); getSingleRecord() -> ResultSet.Record (getInt/getString/...); model.loadTable_<tabela>(Core.query(...)) para varias linhas; getResultList() -> List<Tuple> (javax.persistence.Tuple); Core.insert/update/delete(conn,schema,tabela).addString/addInt.where.execute() -> ResultSet, hasError()
- Tecnologias: SQL, javax.persistence.Tuple
- Componentes: Core, QueryInterface, ResultSet, Model.load, loadTable
- Regras e convenções: nomes/aliases das colunas iguais aos nomes dos campos do formulario/tabela
- Boas práticas: parametros nomeados (:nome + addInt/addString) em vez de concatenacao
- Relações (documentos relacionados no portal): 6.1. Base de Dados - Configuração (#1014); 10.10.3. Table - Programação com Query (#1031); 10.5.3. Form - Programação com Query (#1037)
- Estado: exemplo com defeitos, risco — ok com defeitos nos exemplos: variante equivalente concatena o id no SQL [ENG: risco de injecao]; ";" a meio da cadeia de addString; getResultList atribuido a ResultSet

#### 18.7. Interação com Base de Dados com DAO — #1132

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1132&dad=tutorial&isPublic=1
- Atualizado em: 20-01-2025 · 12363 caracteres · 9 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: interacao com BD via classes DAO (BaseActiveRecord)
- Conceitos técnicos: findOne(id), findAll(), find().andWhere/orWhere/where/andWhereNotNull/andWhereBetween/orderBy/limit/one/all; navegacao de FK "campo.atributo"; operadores isnull/notnull, =, !=, >, <, >=, <=, like, not like; andWhere de 4 parametros com funcoes (lower(...)); orderBy de 1 parametro e DESCENDENTE; ORDERBY.ASC/DESC; setShowConsoleSql; insert() devolve o objeto com id; update(); delete(id) devolve boolean; hasError()/getError(); FK mapeada como objeto da classe relacionada
- Tecnologias: Hibernate/JPA, HQL
- Componentes: BaseActiveRecord, ORDERBY
- Regras e convenções: anotacoes JPA nos campos e nao nos metodos; colecoes com fetch EAGER; colecoes como Set (nao ordenadas)
- Boas práticas: eliminar dependencias antes do objeto pai; verificar hasError apos insert/update
- Relações (documentos relacionados no portal): 11.4.2. Campo de Seleção - Programação com DAO (#1071); 10.10.2. Table - Programação com Classes DAO (#1032); 15.1. Mapeamento DAO com Eclipse (#1110); 10.5.2. Form - Programação com classes DAO (#1036)
- Estado: exemplo com defeitos — ok com defeitos nos exemplos (Ex3 mistura person/document); [PROJ v2.1.1] DAOs gerados podem trazer @OneToMany com cascade ALL indevido

### 19. GC - Javascript e CSS

#### 19.1. Código Javascript e CSS Personalizado — #1126

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1126&dad=tutorial&isPublic=1
- Atualizado em: 25-10-2020 · 4340 caracteres · 12 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: JavaScript e CSS personalizados
- Conceitos técnicos: RULES cobrem a maioria dos eventos; separador STYLE (ID, Class, Inline Style); separadores JS e CSS do gerador com inclusao de URLs de ficheiros (ex.: qrcode.min.js da biblioteca igrpweb) e codigo proprio; identificar componentes por ID
- Tecnologias: JavaScript, CSS
- Componentes: box (exemplo)
- Regras e convenções: definir ID no componente para o referenciar no JS/CSS da pagina
- Boas práticas: preferir RULES; JS/CSS proprio pelos separadores do gerador
- Relações (documentos relacionados no portal): 9.1. Gerador de Código (#1024); 9.4. Propriedades dos Componentes e Campos (#1027); 9.6. Geração de Código - Exemplo (#1029)
- Estado: ok — ok; [PROJ v2.1.1] o JS/CSS fica embutido no XSL gerado (nao editar o XSL a mao)

### 20. BD - Hibernate em igrpweb

#### 20.1. Conceitos de Hibernate, ORM e JPA — #1142

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1142&dad=tutorial&isPublic=1
- Atualizado em: 06-11-2020 · 3459 caracteres · 3 imagens
- Versão: v1+v2 (conceptual)  →  aplicabilidade **v1+v2**
- Tema: conceitos Hibernate, ORM e JPA
- Conceitos técnicos: JPA como especificacao; Hibernate como implementacao; mapeamento por anotacoes preferido a XML; entidades
- Tecnologias: Hibernate, JPA, JDBC
- Componentes: -
- Regras e convenções: -
- Boas práticas: -
- Relações (documentos relacionados no portal): 20.2. Uso de Hibernate e JPA em igrpweb (#1113)
- Estado: ok — ok (generico; ligacoes externas)

#### 20.2. Uso de Hibernate e JPA em igrpweb — #1113

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1113&dad=tutorial&isPublic=1
- Atualizado em: 06-11-2020 · 7596 caracteres · 31 imagens
- Versão: v1+v2 (conceito); ferramentas Eclipse v1  →  aplicabilidade **v1+v2**
- Tema: uso de Hibernate e JPA no igrpweb
- Conceitos técnicos: vantagens JPA (independencia de BD, cache, etc.); o igrpweb usa duas bases de dados: uma para o framework e outra(s) para as aplicacoes; Hibernate Tools no Eclipse; drivers MySQL 8.0.15 / PostgreSQL 42.2.5
- Tecnologias: Hibernate, JPA, Eclipse Hibernate Tools
- Componentes: -
- Regras e convenções: separar BD do framework e BD das aplicacoes
- Boas práticas: -
- Relações (documentos relacionados no portal): 10.20. Map Chart - Configuração (#1054); 15.1. Mapeamento DAO com Eclipse (#1110); 15.2. Mapeamento DAO com JBoss Tools (#1111)
- Estado: incompleto — incompleto (secao 5 "Interagindo com base de dados utilizando" sem conteudo); versoes de drivers antigas

#### 20.3. Anotações de Hibernate — #1143

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1143&dad=tutorial&isPublic=1
- Atualizado em: 20-07-2021 · 1697 caracteres · 0 imagens
- Versão: v1+v2  →  aplicabilidade **v1+v2**
- Tema: anotacoes Hibernate
- Conceitos técnicos: @Entity, @Table, @Id, @Column (default: nome da classe/propriedade), @CreationTimestamp, @UpdateTimestamp, @Immutable; anotacoes JPA em javax.persistence; sem ficheiro hbm
- Tecnologias: Hibernate, JPA 2
- Componentes: -
- Regras e convenções: anotacoes JPA do pacote javax.persistence (valido em v1 e v2, que mantem javax.persistence com Hibernate 5.6) [CODIGO]
- Boas práticas: anotacoes nos campos (#1132)
- Relações (documentos relacionados no portal): 20.2. Uso de Hibernate e JPA em igrpweb (#1113); 20.1. Conceitos de Hibernate, ORM e JPA (#1142)
- Estado: ok — ok; numeracao interna salta passos (1, 3)

### 21. Migração

#### 21.1. Migração de uma versão 1.X.X para 2.X.X — #1221

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1221&dad=tutorial&isPublic=1
- Atualizado em: 25-06-2025 · 1189 caracteres · 0 imagens
- Versão: v2 (migracao 1.x -> 2.x)  →  aplicabilidade **v2**
- Tema: migracao de projeto Maven de 1.X.X para 2.X.X
- Conceitos técnicos: cv.igrp:igrp-core-war e igrp-core [2.0.0,3.0.0); maven.compiler.release 17; tomee.maven.plugin.version 10.0.1; web.xml: filtro nosi.core.filter.AuthenticationFilter mapeado ao servlet IGRP (opcional se existir web.xml); substituir javax por jakarta onde der erro
- Tecnologias: Maven, Java 17, TomEE 10, Jakarta EE
- Componentes: pom.xml, web.xml, AuthenticationFilter
- Regras e convenções: as 4 etapas acima
- Boas práticas: -
- Relações (documentos relacionados no portal): -
- Estado: ok — ok; confirmado: AuthenticationFilter so existe em v2; v2 usa jakarta.servlet/jakarta.ws.rs mas mantem javax.persistence (Hibernate 5.6) [CODIGO]; o ramo v2 ja usa TomEE 10.2.0 [CODIGO]

#### 21.2. Migration Troubleshooting — #1223

- Endereço: https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id=1223&dad=tutorial&isPublic=1
- Atualizado em: 12-01-2025 · 1261 caracteres · 0 imagens
- Versão: v2 (troubleshooting de migracao)  →  aplicabilidade **v2**
- Tema: problemas tipicos ao migrar para 2.x
- Conceitos técnicos: substituir org.glassfish.jersey.client.ClientConfig por jakarta.ws.rs.client.ClientBuilder (propriedades jersey.config.client.connectTimeout/readTimeout); ResultSet.Record.RowList -> rowList; ResultSet.Record.Row -> row; rever pom.xml; Flyway na versao do template
- Tecnologias: Jakarta RESTful WS, Jersey, Flyway
- Componentes: nosi.core.webapp.databse.helpers.ResultSet
- Regras e convenções: renomeacoes RowList/Row
- Boas práticas: fechar o Client REST (client.close())
- Relações (documentos relacionados no portal): 21.1. Migração de uma versão 1.X.X para 2.X.X (#1221)
- Estado: ok, incompleto — ok; confirmado: RowList (v1) -> rowList (v2) em ResultSet.java [CODIGO]; incompleto (itens pom.xml/Flyway sem detalhe)
