# Dados: ligações, Core (query), DAO/Hibernate e transações

> Aplicabilidade: (v1+v2) salvo indicação — API `Core` e `BaseActiveRecord` com os mesmos métodos nos dois ramos [CÓD-v1+v2].
> Docs: 6.1, 15.x, 18.4–18.7, 20.x, 4.5, 17.1. Verificado em 2026-11-20.

## 1. Bases de dados e ligações

- O igrpweb usa **duas bases de dados**: uma para o framework e outra(s) para as aplicações [DOC 20.2 #1113].
- Ligações da aplicação: Application Builder → Configurar Base de Dados (tipo, nome `<app>_<bd>_<n>`, URL, driver, utilizador,
  password, testar e gravar). Cada aplicação pode ter várias ligações de qualquer tipo (Oracle, PostgreSQL, MySQL, SQL Server, H2) [DOC 6.1 #1014].
- A **ligação padrão** é usada quando não indicas nenhuma [DOC 6.1].
- Cada ligação gera `<ligação>.<app>.cfg.xml` (visível no File Editor), onde se listam as classes DAO como `<mapping class=…/>` [DOC 6.1], [DOC 15.1 #1110].
- [CÓD-v1+v2] O `cfg.xml` gerado para as ligações das aplicações tem `hibernate.hbm2ddl.auto=update`
  (`ConfigDatabaseController`): ao arrancar, o Hibernate pode criar ou alterar colunas e tabelas a partir dos DAOs. A dica do portal de
  "não correr scripts" porque os DAOs atualizam a BD [DOC 17.1 #1124] depende disto. [ENG] Em produção, prefere migrações
  versionadas (Flyway já é usado pelo framework) e revê o `hbm2ddl` antes de publicar.
- A ligação do framework vem de `hibernate-igrp-core.properties` (`${igrp.db.*}`, filtrado pelo Maven), com `hbm2ddl.auto=none` [CÓD-v1+v2], [PROJ].

## 2. Escolher a ligação no código

- `Core.defaultConnection()` / `Core.defaultConnection(dad)` devolvem o nome da ligação padrão [DOC 18.4 #1129].
- As variantes sem ligação (`Core.query(sql)`, `Core.insert(tabela)`…) usam a ligação padrão da **aplicação atual** [DOC 18.4], [PROJ].
- `Core.query(null, …)` usa a ligação do IGRP (framework). O próprio gerador avisa: "change 'null' to your db connection name" [CÓD-v1+v2 `#gen-example`], [DOC 9.6].
- [PROJ] Guarda o nome da ligação numa constante em `custom_actions`. O erro típico de usar a ligação errada é `SQLGrammarException: could not extract ResultSet`.

## 3. Query (`QueryInterface`, `ResultSet`) [DOC 18.4 #1129], [DOC 18.6 #1131]

```java
/*----#start-code(index)----*/
QueryInterface q = Core.query(CONN, "SELECT id, first_name, last_name FROM public.person")
        .where("id=:person_id").addInt("person_id", Core.getParamInt("p_id"));
model.load(q);                                        // aliases = tags dos campos do formulário
model.loadTable_person(Core.query(CONN, "SELECT id, first_name, last_name FROM public.person"));
ResultSet.Record r = q.getSingleRecord();              // getInt, getString, getBigDecimal…
List<Tuple> rows = Core.query(CONN, sql).getResultList();  // javax.persistence.Tuple; pode ser null
/*----#end-code----*/
```
- Escrita: `Core.insert/update/delete(conn[, schema], tabela).addString(…).addInt(…).where("id=:id").addInt("id", id).execute()`
  devolve `ResultSet`; verifica `hasError()` [DOC 18.6].
- Variantes com `(…, displayError, tracingError)` controlam a apresentação e o registo do erro [DOC 18.4].
- **Usa sempre parâmetros nomeados** (`:nome` + `addInt/addString`). Vários exemplos do portal concatenam valores no SQL
  (#1033, #1037, #1101, #1131). [ENG] Não os reproduzas: risco de injeção de SQL.
- Os aliases das colunas têm de ser iguais às tags dos campos ou colunas da tabela, senão os dados não aparecem [DOC 10.10.3 #1031].
- [PROJ] Não uses o cast `::` do PostgreSQL: o parser de parâmetros nomeados lê `:texto` como parâmetro. Usa `CAST(x AS …)`.
  Confirmado: `NamedParameterStatement` existe nos dois ramos.
- [PROJ] Com `Core.insert` em PostgreSQL, `getKeyValue()` pode falhar porque o core executa `SET session audit…` antes do INSERT
  (`HibernateUtils.setSessionAudit`, presente nos dois ramos). Obtém o id antes (`nextval`) ou usa DAO. O exemplo de [DOC 18.5 #1130]
  usa `getKeyValue()` e por isso pode falhar nesse cenário.
- `Core.executeQuery(env|conn, sql)` devolve `ResultSet` [DOC 18.4].

## 4. DAO (`BaseActiveRecord`) [DOC 18.7 #1132]

- Classe DAO: `public class X extends BaseActiveRecord<X> implements Serializable` com anotações JPA (`javax.persistence` nas duas versões),
  no package `nosi.webapps.<app>.dao`, listada no `cfg.xml` da ligação [DOC 15.x], [CÓD-v1+v2 `nosi/base/ActiveRecord/BaseActiveRecord.java`].
- Gerar: CRUD/DAO Generator do Studio (opção GERAR DAO) [DOC 4.5 #1011]. O mapeamento manual por IDE (Eclipse JPA Tools,
  JBoss Hibernate Tools, NetBeans) é um procedimento v1 [DOC 15.1–15.3].
- Leitura: `new X().findOne(id)`, `findAll()`, `find().andWhere("campo", "=", v).orWhere(…).andWhereNotNull(c).andWhereBetween(c, d1, d2)`
  `.orderBy(c[, ORDERBY.ASC|DESC]).limit(n).one()|all()`; `getCount()`, `getMax/getAvg(…)` (blocos Blockly). Operadores:
  `isnull`, `notnull`, `=`, `!=`, `>`, `<`, `>=`, `<=`, `like`, `not like`; `andWhere` de 4 argumentos aceita funções (`lower(…)`).
  **`orderBy(c)` com um argumento ordena de forma descendente.** FK: navega com `"campoRelacao.atributo"`.
- Escrita: `insert()` devolve o objeto com o id; `update()`; `delete(id)` devolve `boolean`; verifica `hasError()` e `getError()`.
  Elimina as dependências antes do objeto pai.
- FK é mapeada como objeto da classe relacionada (`doc.setPerson(person)`), não como id.
- Recomendações oficiais: anotações JPA **nos campos** e não nos métodos; coleções com `fetch = EAGER`; coleções como `Set` [DOC 18.7].
  O exemplo NetBeans [DOC 15.3 #1112] usa `List`, o que contradiz esta recomendação: segue o 18.7.
- [PROJ] O DAO Generator pode gerar `@OneToMany(cascade = ALL)` indevidos na própria classe. Revê os DAOs gerados (voltar a gerar repõe o defeito).
- [PROJ] `setShowError(false)` evita a mensagem automática; depois verifica `hasError()`.
- Exemplo NetBeans com `javax.xml.bind` (`@XmlRootElement`): em v2 só existe `jakarta.xml.bind` [CÓD-v2].

## 5. Transações [DOC 18.5 #1130]

- Uma escrita isolada não precisa de transação [PROJ]. Para várias escritas dependentes:
  - Hibernate: `Session s = Core.getSession(conn); Transaction t = s.getTransaction(); t.begin(); s.persist(…); t.commit();`
    com `rollback()` no `catch` e `s.close()` no `finally`.
  - Query: `QueryInterface t = Core.transaction([conn]); t.begin(); t.insert(…).execute(); t.commit();` com `t.roolback()`
    (nome real do método) e `t.closeConnection()`.
  - **`keepConnection()`** em todas as consultas `BaseActiveRecord`/`QueryInterface` feitas pela mesma ligação durante a transação, para que a ligação não seja fechada a meio [DOC 18.5].
  - (v2 ≥ 2.0.0.240902) `AppSession.doInTransaction(p -> { Session s = p.session(); … return x; }, Core.getSession(conn))` faz rollback e volta a
    lançar a exceção em caso de erro [CÓD-v2], [PROJ]. Não existe na v1.
- [PROJ] Faz as validações antes de abrir a transação. Corridas entre validar e gravar resolvem-se com restrições na BD (UNIQUE, FK, trigger).

## 6. Hibernate e JPA (conceitos) [DOC 20.x]

- JPA é a especificação e o Hibernate a implementação [DOC 20.1 #1142]. O mapeamento é feito por anotações: `@Entity`, `@Table`, `@Id`, `@Column`,
  `@CreationTimestamp`, `@UpdateTimestamp`, `@Immutable` (pacote `javax.persistence` nas duas versões) [DOC 20.3 #1143], [CÓD].
- Vantagens citadas: independência da BD, menos SQL manual, cache [DOC 20.2 #1113].

## 7. Ferramentas

- **SQL Tools** (Studio): testar queries por aplicação e ligação [DOC 4.4 #1010].
- **Importar Script SQL** (Application Builder) [DOC 5.3 #1022].
- **CRUD Generator**: gera as páginas de listagem e de formulário por tabela, com query [DOC 4.5 #1011]. [PROJ] Voltar a gerar o
  CRUD da mesma tabela substitui as páginas sem preservar as áreas: gera uma vez e depois altera no Studio.
