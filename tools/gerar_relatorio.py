"""Gera o inventario do skill e o relatorio de validacao documental.

Uso (na raiz do workspace):
    python -I tools/gerar_relatorio.py

Entradas:  audit/portal/inventario.csv (de extrair_portal.py) e audit/analise.txt (analise manual por p_id)
Saidas:    igrp-web-v1-v2/references/fontes-e-inventario.md (tabela entre marcadores INVENTARIO)
           reports/validacao-documental.md
"""
import collections
import csv
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(RAIZ, "audit", "portal", "inventario.csv")
ANA = os.path.join(RAIZ, "audit", "analise.txt")
FONTES = os.path.join(RAIZ, "igrp-web-v1-v2", "references", "fontes-e-inventario.md")
REL = os.path.join(RAIZ, "reports", "validacao-documental.md")

APLIC_MANUAL = {
    "1107": "v1+v2 (v2: jakarta.*)", "1108": "v1+v2 (v2: jakarta.*)", "1109": "v1+v2 (v2: jakarta.*)",
    "1110": "v1 (ferramenta); conceito v1+v2", "1111": "v1 (ferramenta); conceito v1+v2",
    "1112": "v1 (ferramenta); conceito v1+v2", "1205": "v1 (ferramenta); conceito v1+v2",
    "1145": "v1 (+ nota v2: JDK 17)", "1147": "v1", "1146": "v1 (+ alternativa IntelliJ/Maven)",
    "1194": "v1 (ferramenta); conceito v1+v2", "1006": "v1 (ferramenta); conceito v1+v2",
    "1007": "v1+v2 (fluxo); ferramenta SVN v1",
}

CATEGORIAS = [
    ("quase vazio", r"quase vazio"),
    ("incompleto", r"incompleto|sem conteudo|so titulos|so topicos"),
    ("desatualizado", r"desatualizad|descontinuado"),
    ("duplicado", r"duplica"),
    ("contraditório", r"contradiz|contradicao"),
    ("exemplo com defeitos", r"defeito|erros de sintaxe|gralha|nao compila|troca |trocadas|concatena|variavel|errado|incorreto|inconsistente"),
    ("risco", r"risco"),
    ("só v1", r"v1 apenas|^v1 \(ferramenta\)"),
    ("ligação inacessível", r"sharepoint|nao acessivel|inacessivel|repositorio pessoal"),
]


def le_analise():
    blocos, atual = {}, None
    for linha in open(ANA, encoding="utf-8"):
        linha = linha.rstrip("\n")
        if linha.startswith("@"):
            atual = linha[1:].strip()
            blocos[atual] = {}
        elif atual and ":" in linha and not linha.startswith("#"):
            k, v = linha.split(":", 1)
            blocos[atual][k.strip()] = v.strip()
    return blocos


def aplicabilidade(pid, versao):
    if pid in APLIC_MANUAL:
        return APLIC_MANUAL[pid]
    v = versao.strip()
    for pref in ("v1+v2", "v2", "v1"):
        if v.startswith(pref):
            return pref
    return v.split(" ")[0]


def categorias(estado):
    e = estado.lower()
    cats = [nome for nome, rx in CATEGORIAS if re.search(rx, e)]
    if not cats:
        return ["ok"] if e.startswith("ok") else [e.split(";")[0][:40]]
    if e.startswith("ok") and "exemplo com defeitos" not in cats and "risco" not in cats:
        cats.insert(0, "ok")
    return cats


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    inv = [r for r in csv.DictReader(open(INV, encoding="utf-8")) if r["origem"] == "menu"]
    ana = le_analise()
    titulos = {r["p_id"]: r["titulo_menu"] for r in inv}
    faltam = [r["p_id"] for r in inv if r["p_id"] not in ana]
    if faltam:
        raise SystemExit(f"analise em falta para: {faltam}")

    # 1) tabela do inventario no skill
    linhas = ["| Nº | Título | p_id | Atualizado | Aplicabilidade | Estado |", "|---|---|---|---|---|---|"]
    for r in inv:
        a = ana[r["p_id"]]
        num = r["numero"]
        tit = re.sub(r"^\s*[\d.]+\s*", "", r["titulo_menu"]).replace("|", "/")
        linhas.append(f"| {num} | {tit} | {r['p_id']} | {r['atualizado_em']} | "
                      f"{aplicabilidade(r['p_id'], a.get('versao', ''))} | {', '.join(categorias(a.get('estado', '')))} |")
    texto = open(FONTES, encoding="utf-8").read()
    texto = re.sub(r"(<!-- INVENTARIO:INICIO -->).*?(<!-- INVENTARIO:FIM -->)",
                   lambda m: m.group(1) + "\n" + "\n".join(linhas) + "\n" + m.group(2), texto, flags=re.S)
    open(FONTES, "w", encoding="utf-8", newline="\n").write(texto)

    # 2) relatorio de validacao documental
    anos = collections.Counter(r["atualizado_em"][-4:] for r in inv)
    aplic = collections.Counter(aplicabilidade(r["p_id"], ana[r["p_id"]].get("versao", "")) for r in inv)
    cats = collections.Counter(c for r in inv for c in categorias(ana[r["p_id"]].get("estado", "")))
    seccoes = collections.OrderedDict()
    for r in inv:
        seccoes.setdefault(r["seccao"], []).append(r)
    total_chars = sum(int(r["caracteres"]) for r in inv)
    total_imgs = sum(int(r["imagens"]) for r in inv)

    out = []
    w = out.append
    w("# Relatório de validação documental — portal igrpweb (IGRP v1 e v2)\n")
    w("Gerado por `tools/gerar_relatorio.py` a partir de `audit/portal/inventario.csv` (extração automática) "
      "e `audit/analise.txt` (análise documento a documento). Snapshot do portal: 2026-11-20.\n")
    w("## 1. Âmbito e método\n")
    w("- Fonte: `https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&dad=tutorial&isPublic=1` "
      "(página XML+XSL; filhos do menu via `Listar_documentos/remote_treemenu_1&p_id=<id>`; documentos via `index&p_id=<id>`).")
    w("- Extração: `tools/extrair_portal.py` (biblioteca padrão Python), texto limpo por documento em `audit/portal/<p_id>.md`.")
    w("- Validação de consistência: o número no título da página de cada documento tem de coincidir com o do menu; "
      "quando não coincide o pedido é repetido em sequência. Pedidos concorrentes chegaram a devolver o documento "
      "errado (na primeira sondagem o #1020 devolveu o #1021 e o #1147 veio vazio); na extração final todos coincidem.")
    w("- Análise: cada documento foi lido e registado (versão, tema, conceitos, tecnologias, componentes, regras, "
      "boas práticas, estado). As APIs e artefactos referidos foram confirmados no código oficial: v1 = ramo `develop` "
      "@6d7b32f (1.9.1.261027), v2 = ramo `igrp-horizon-dev` @230df4c (2.1.1.261027).")
    w("- Documentação de outras versões (IGRP 3.0, v0) não foi usada.\n")
    w("## 2. Resultados globais\n")
    w(f"- Menu: 21 secções, 24 subgrupos, **{len(inv)} documentos** (p_id {min(int(r['p_id']) for r in inv)}–"
      f"{max(int(r['p_id']) for r in inv)}); texto total {total_chars:,} caracteres; {total_imgs} imagens.".replace(",", " "))
    w("- p_id fora do menu: 72 identificadores sondados (1000–1240) devolvem apenas o marcador vazio `<p>Sectionheader</p>` — não há documentos ocultos.")
    w("- Ano da última atualização: " + ", ".join(f"{k}: {v}" for k, v in sorted(anos.items())) +
      f" → {sum(v for k, v in anos.items() if k in ('2020', '2021'))} de {len(inv)} são anteriores à GA da v2 (2023).")
    w("- O próprio portal declara: \"JDK17 para horizon ou JDK8 para legacy … esta documentação está preparada para a "
      "versão legacy por isso algum texto ou imagem pode estar desatualizada\" [#1145, #1147].")
    w("- O portal corre o core `211115` (`<version>` no XML das páginas, verificado em 2026-11-21), uma build v1 de novembro de 2021, "
      "com o XSL aplicado no browser. As builds atuais são 1.9.1.261027 (v1) e 2.1.1.261027 (v2); as diferenças por build estão em "
      "`igrp-web-v1-v2/references/variantes-e-builds.md`.")
    w("- Aplicabilidade atribuída: " + "; ".join(f"{k}: {v}" for k, v in aplic.most_common()) + ".")
    w("- Estados (um documento pode ter vários): " + "; ".join(f"{k}: {v}" for k, v in cats.most_common()) + ".\n")
    w("## 3. Problemas encontrados\n")
    for nome, _ in CATEGORIAS:
        ids = [r for r in inv if nome in categorias(ana[r["p_id"]].get("estado", ""))]
        if ids:
            w(f"### {nome.capitalize()} ({len(ids)})\n")
            for r in ids:
                w(f"- {r['titulo_menu']} (#{r['p_id']}): {ana[r['p_id']].get('estado', '')}")
            w("")
    w("### Outras observações\n")
    w("- Lacuna de numeração: não existe 3.2.1 (a secção 3.2 só tem 3.2.2 Subversion).")
    w("- Duplicações de conteúdo: 9.2 repete 9.1; 17.1 repete 5.4; vários documentos repetem parágrafos internamente.")
    w("- Exemplos de código: muitos exemplos têm erros de sintaxe ou nomes trocados; o skill usa as regras e "
      "reescreve os exemplos quando necessário.")
    w("- Segurança: exemplos oficiais concatenam valores do utilizador em SQL (#1033, #1037, #1101, #1131) e cifram "
      "palavras-passe de forma reversível com `Core.encrypt` (#1088, #1098); o skill assinala-os como práticas a evitar [ENG].\n")
    w("## 4. Limitações\n")
    w("- O conteúdo em imagens (capturas de ecrã, código em imagem em #1017, #1107, #1109, #1123, etc.) e as vídeo-aulas "
      "não foram transcritos; nenhuma regra foi derivada apenas de imagens.")
    w("- Ligações para documentos SharePoint internos (`services.nosi.cv`) e para o GitLab interno da NOSi não são acessíveis publicamente.")
    w("- O portal não identifica a versão de cada documento; a aplicabilidade foi atribuída por evidência de código e "
      "por indicações explícitas do texto. Temas sem evidência ficam marcados como tal no skill.")
    w("- O snapshot pode ficar desatualizado: voltar a correr `tools/extrair_portal.py` e comparar o inventário.\n")
    w("## 5. Registo por documento\n")
    for sec, rows in seccoes.items():
        w(f"### {sec}\n")
        for r in rows:
            a = ana[r["p_id"]]
            rel = " ".join(f"#{i}" for i in r["relacionados"].split() if i)
            rel_t = "; ".join(f"{titulos.get(i, '?')} (#{i})" for i in r["relacionados"].split() if i) or "-"
            w(f"#### {r['titulo_menu']} — #{r['p_id']}\n")
            w(f"- Endereço: {r['url']}")
            w(f"- Atualizado em: {r['atualizado_em']} · {r['caracteres']} caracteres · {r['imagens']} imagens")
            w(f"- Versão: {a.get('versao', '')}  →  aplicabilidade **{aplicabilidade(r['p_id'], a.get('versao', ''))}**")
            for campo, rot in (("tema", "Tema"), ("conceitos", "Conceitos técnicos"), ("tecnologias", "Tecnologias"),
                               ("componentes", "Componentes"), ("regras", "Regras e convenções"),
                               ("praticas", "Boas práticas")):
                w(f"- {rot}: {a.get(campo, '-')}")
            w(f"- Relações (documentos relacionados no portal): {rel_t}")
            w(f"- Estado: {', '.join(categorias(a.get('estado', '')))} — {a.get('estado', '')}\n")
    os.makedirs(os.path.dirname(REL), exist_ok=True)
    open(REL, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print(f"inventario: {len(inv)} linhas; relatorio: {REL}")
    print("aplicabilidade:", dict(aplic))
    print("estados:", dict(cats))


if __name__ == "__main__":
    main()
