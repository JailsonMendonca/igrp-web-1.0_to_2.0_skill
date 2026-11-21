# Web services e integrações

> Aplicabilidade: conceitos (v1+v2); APIs Java `javax.*` na v1 e `jakarta.*` na v2 [CÓD-v1], [CÓD-v2].
> Docs: 14.1–14.3, 4.3, 21.2. Verificado em 2026-11-20.

## 1. Página igrpweb como serviço [DOC 14.1 #1108]

- Página marcada como **Público**, chamada pelo seu link. Código no `actionIndex`, com resposta
  `this.format = Response.FORMAT_XML` (ou `FORMAT_JSON`, ou `FORMAT_HTML` [DOC 8.3 #1200]) e `return this.renderView(conteudo)`.
- Serialização XML com JAXB: v1 `javax.xml.bind`; **v2 `jakarta.xml.bind`** (o core v2 só usa jakarta) [CÓD].
- ⚠ O doc manda comentar com o File Editor as linhas geradas `view.setModel(model); return this.renderView(view);`. Essa parte é
  regenerada: a alteração perde-se na próxima gravação no gerador. Alternativa [ENG]: devolver a resposta dentro de uma condição, deixando o retorno gerado como saída por defeito, ou isolar o serviço em JAX-RS (§2).
- [ENG] Uma página pública expõe dados sem login: valida a entrada, limita os dados devolvidos e considera autenticação.

## 2. REST (JAX-RS / Jersey) [DOC 14.2 #1107]

- Disponibilizar: package `nosi.webapps.<app>.restapi` com uma classe `Configuration` que regista os pacotes dos recursos
  (`packages("p1","p2",…)`) e classes de recursos (GET/POST/PUT/DELETE).
- Consumir: cliente Jersey; `@Expose` nos DAOs serializados com Gson.
- v1: `javax.ws.rs`. v2: `jakarta.ws.rs`; troca `org.glassfish.jersey.client.ClientConfig` por
  `jakarta.ws.rs.client.ClientBuilder.newBuilder().property("jersey.config.client.connectTimeout", …).build()` e fecha o cliente [DOC 21.2 #1223].
- O documento só tem tópicos; o código está em imagens.

## 3. SOAP (JAX-WS) [DOC 14.3 #1109]

- Conceitos SOAP, WSDL, JAX-WS (`@WebService`, `@WebMethod`, `@WebParam`, `@WebResult`) e JAXB; packages `soapservices.server`/`client`.
- v1 `javax.jws` e `javax.xml.bind`; v2 `jakarta.jws` e `jakarta.xml.bind` [CÓD].
- O documento só tem tópicos.

## 4. Integrações entre aplicações

- Partilha de páginas entre aplicações e páginas públicas [DOC 4.3 #1009], [DOC 14.2 #1107].
- Identidade: Autentika (`ids.autentika.*`), OAuth2/OpenID (`ids.oauth2-openid.*`), LDAP (`ldap.ad.*`) no `main.xml` (ver `acessos-e-seguranca.md`).
- Email: `Core.mail(…)` / `Core.mail_v2(…)` com anexos (`Attachment`) [DOC 8.4 #1209], [DOC 11.10 #1082].
