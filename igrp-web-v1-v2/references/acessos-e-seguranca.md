# Gestão de acessos, autenticação e segurança

> Aplicabilidade: (v1+v2) salvo indicação. Docs: 12.1–12.6, 4.2, 11.x, 18.2. Código: `nosi/core/webapp/security/*`,
> `nosi/core/config/ConfigCommonMainConstants.java` [CÓD]. Verificado em 2026-11-20.

## 1. Modelo de acessos (oficial) [DOC 12.1 #1133]

- O framework gere **sessões e privilégios**. O programador não os programa: o administrador configura-os na Gestão de Acessos
  (Studio em desenvolvimento; menu da aplicação em produção, onde não há Studio).
- Hierarquia: **Aplicação → Orgânicas → Perfis → Utilizadores**. Atribuem-se **Menus**, **Transactions** e **Etapas de processo**.
  - Orgânica: entidade ou departamento [DOC 12.2 #1134].
  - Perfil: delimita o que os utilizadores podem fazer; perfil pai acompanha o filho; só herda menus e transactions da sua orgânica; tem página inicial [DOC 12.4 #1136].
  - Utilizador: é **adicionado** ao igrpweb (pode fazer login) e **convidado** para cada aplicação. Pode ter vários perfis, mas
    só um ativo por sessão (mudar em Minha Conta exige novo login, por segurança) [DOC 12.4], [DOC 12.5 #1137].
- **Menu** = página acessível no menu lateral (criado com *Create menu* ou na Gestão de Menu; hierarquia pai/filho) [DOC 12.3 #1135].
- **Transaction** = botão que não deve estar acessível a todos; marcar *Transaction* no botão e atribuir na Gestão de Acessos [DOC 12.6 #1138], [DOC 11.1.1 #1072].
- Regras oficiais: definir primeiro o âmbito da orgânica, depois os perfis. Associar menus e transactions **a perfis**; associação direta
  a utilizadores só excecionalmente [DOC 12.4].
- API: `Core.getCurrentUser()`, `getCurrentOrganization()`, `getCurrentOrganizationCode()`, `getCurrentProfile()`,
  `getCurrentProfileCode()`, `findUserById/ByUsername/ByEmail`, `findOrganizationByCode/ById`, `findProfileByCode/ById`,
  `getCurrentApp()`, `getCurrentDad()` [DOC 12.2–12.5], [DOC 18.2 #1127].

## 2. Verificação no servidor [CÓD-v1+v2]

- `nosi.core.webapp.security.Permission` tem `hasMenuPagPermition(…)`, `hasApp1PagPermition(…)` e `isPermission(transaction)`.
- `PagesScapePermission` define a lista fixa de rotas acessíveis **sem login** (login, erro, ficheiros públicos, report preview…).
  No ramo v2 essa lista inclui rotas de aplicações de negócio específicas. [ENG] Em auditoria, revê esta lista e as páginas marcadas *Público*.
- [ENG] Para ações sensíveis, verifica também no servidor (`Permission.isPermission(…)`) e não confies só na visibilidade do botão.

## 3. Autenticação e configuração

- `igrp.authentication_type` = `db` | `ldap` | `oauth2-openid`; Autentika (`ids.autentika.*`); OAuth2/OpenID (`ids.oauth2-openid.*`);
  LDAP (`ldap.ad.*`); `igrp.pwdRecover` [PROJ main.xml], [CÓD-v1+v2]. Login: AD, tabela de utilizadores ou federação [DOC 4.2 #1005].
- (v1 ≥ 1.8.1.240215, v2 ≥ 2.0.0.240215) Com `IGRP_ENV_VARIABLE_SCAN=true`, um valor `${VAR}` no `hibernate-igrp-core.properties` ou
  nos `<ligação>.properties` é lido da variável de ambiente `VAR` (`HibernateUtils`) [CÓD-v1+v2]. Serve para tirar as passwords de BD do repositório.
- (v2 ≥ 2.0.0.250220) Com a mesma variável, as chaves do `main.xml` também vêm do ambiente (`IDS_AUTENTIKA_ADMIN_PWD`, `LDAP_AD_PASSWORD`,
  `MAIL_SMTP_*`, `IGRP_SECRET_KEY`…) [CÓD-v2]. (v1) As chaves do `main.xml` só existem no ficheiro; `igrp.secret.key` está declarada mas não é usada [CÓD-v1].
- (v2) `AuthenticationFilter` no `web.xml` [DOC 21.1 #1221].

## 4. Riscos frequentes (checklist de segurança)

| Verificação | Evidência / referência |
|---|---|
| Credenciais em claro no repositório: `pom.xml` (`igrp.db.password`), `main.xml` (`ldap.ad.password`, `mail.password`, `ids.*`), `<ligação>.<app>.properties` | [ENG]; `${VAR}` nos `.properties` (v1 ≥ 1.8.1, v2); `main.xml` por variáveis de ambiente (v2 ≥ 2.0.0.250220) [CÓD] |
| Utilizador de demonstração `demo@nosi.cv`/`demo` ativo fora de desenvolvimento | [DOC 2.4.5 #1004], [ENG] |
| `igrp.env` diferente de `prod` em produção | [PROJ main.xml], [ENG] |
| SQL com concatenação de valores do utilizador | [ENG]; usar `:param` [DOC 18.6] |
| Palavras-passe próprias guardadas com `Core.encrypt` (reversível) | [DOC 11.16], [ENG]: usar hashing |
| Chaves secretas em literais (ex.: `Core.encrypt(x, "chave")`) | [DOC 18.2 #1127], [ENG] |
| Páginas *Público* e serviços sem validação | [DOC 5.2], [DOC 14.1], [ENG] |
| Botões sensíveis sem *Transaction* | [DOC 12.6] |
| Upload sem validação de tipo e tamanho no servidor | [DOC 11.25], [ENG] |
| HTML de Text Editor ou reports sem escape ou sanitização | [ENG] |
| `hbm2ddl.auto=update` nas ligações em produção | [CÓD-v1+v2], [ENG] |
| Exceções engolidas (`e.printStackTrace()`) e mensagens de erro técnicas para o utilizador | exemplos do portal; [ENG] |
| (v2) `IGRP_SECRET_KEY` não definido (usa a chave por defeito do código) | [CÓD-v2] |
| Dependências desatualizadas ou `Dockerfile` incoerente com a stack | [CÓD-v1], [CÓD-v2] |
