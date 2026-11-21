"""Extrai a documentacao publica igrpweb (app "tutorial") de docs.igrp.cv.

Uso (a partir da raiz do workspace):
    python -I tools/extrair_portal.py audit/portal              # arvore + todos os documentos + orfaos
    python -I tools/extrair_portal.py audit/portal --imagens 1147 1020   # descodifica imagens desses p_id

Saidas em <destino>:
    <p_id>.md            texto limpo de cada documento listado no menu (cabecalho com metadados)
    orfaos/<p_id>.md     documentos acessiveis por p_id mas ausentes do menu
    inventario.csv       uma linha por documento (menu + orfaos)
    arvore.txt           arvore do menu com p_id
    img/<p_id>/n.ext     (so com --imagens)

So usa a biblioteca padrao. O conteudo descarregado e tratado como dados (nunca executado).
"""
import base64
import csv
import concurrent.futures as cf
import hashlib
import html
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

BASE = "https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/"
DOC_URL = BASE + "index&dad=tutorial&isPublic=1&lang=pt_PT&target=_blank&p_id={}"
TREE_URL = BASE + "remote_treemenu_1&dad=tutorial&isPublic=1&ctx_hidden=&p_id={}"
ROOT_URL = BASE + "index&dad=tutorial&isPublic=1&lang=pt_PT&target=_blank"
PUBLIC_URL = "https://docs.igrp.cv/IGRP/app/webapps?r=tutorial/Listar_documentos/index&p_id={}&dad=tutorial&isPublic=1"
UA = {"User-Agent": "Mozilla/5.0 (doc-audit)"}

MARCADORES = {
    "m_v1": r"java\s*(se\s*)?8\b|jdk\s*1?\.?8\b|java\s*1\.8|tomee[^0-9\n]{0,25}8\.\d|8\.0\.1\d|\[1\.\d|legacy",
    "m_v2": r"java\s*(se\s*)?17|jdk[\s-]*17|release>\s*17|jakarta|tomee[^0-9\n]{0,25}(9|10)\.\d|\[2\.\d|horizon|igrp2\.4",
    "m_eclipse": r"eclipse",
    "m_intellij": r"intellij",
    "m_tomcat": r"tomcat",
    "m_javax": r"javax\.",
    "m_outra_versao": r"igrp\s*v?3(\.0)?\b|new\s*horizon|\breact\b|spring\s*boot|pl/?sql|weblogic",
}


def get(url, remote=False, tries=3):
    headers = dict(UA)
    if remote:
        headers["X-IGRP-REMOTE"] = "1"
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            return urllib.request.urlopen(req, timeout=180).read().decode("utf-8", "replace")
        except Exception as e:  # rede instavel: tentar de novo
            last = e
    raise RuntimeError(f"falha ao obter {url}: {last}")


def tag(xml, name):
    m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", xml, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def rows(xml):
    out = []
    for r in re.findall(r"<row>(.*?)</row>", xml, re.S):
        if "treemenu_1_tmid" not in r:
            continue
        out.append({
            "titulo": tag(r, "treemenu_1_link_desc"),
            "id": tag(r, "treemenu_1_tmid"),
            "pai": tag(r, "treemenu_1_parent"),
            "filhos": tag(r, "treemenu_1_child") == "1",
        })
    return out


def arvore():
    """Devolve lista (nivel, titulo, id, pai, e_folha) pela ordem do menu."""
    topo = rows(get(ROOT_URL))
    res = []

    def desce(no, nivel):
        res.append((nivel, no["titulo"], no["id"], no["pai"], not no["filhos"]))
        if no["filhos"]:
            for f in rows(get(TREE_URL.format(no["id"]), remote=True)):
                desce(f, nivel + 1)

    for n in topo:
        desce(n, 0)
    return res


class Texto(HTMLParser):
    """HTML do documento -> texto legivel (paragrafos, listas, tabelas, codigo, [IMG n])."""

    BLOCO = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "pre", "table", "ul", "ol", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.imgs, self.pre, self.href = [], 0, 0, None

    def handle_starttag(self, t, a):
        a = dict(a)
        if t in self.BLOCO:
            self.out.append("\n")
        if t == "li":
            self.out.append("- ")
        if t in ("h1", "h2", "h3", "h4"):
            self.out.append("#" * (int(t[1]) + 1) + " ")
        if t in ("td", "th"):
            self.out.append(" | ")
        if t == "pre":
            self.pre += 1
            self.out.append("```\n")
        if t == "img":
            self.imgs += 1
            src = a.get("src") or ""
            alt = (a.get("alt") or "").strip()
            ref = "" if src.startswith("data:") else f" {src}"
            self.out.append(f"[IMG {self.imgs}{': ' + alt if alt else ''}{ref}]")
        if t == "a":
            self.href = a.get("href")
        if t == "iframe":
            self.out.append(f"[IFRAME {a.get('src', '')}]")

    def handle_endtag(self, t):
        if t == "pre":
            self.pre = max(0, self.pre - 1)
            self.out.append("\n```\n")
        elif t == "a":
            if self.href and not self.href.startswith("javascript") and not self.href.startswith("data:"):
                self.out.append(f" <{self.href}>")
            self.href = None
        elif t in self.BLOCO:
            self.out.append("\n")

    def handle_data(self, d):
        if not self.pre:
            d = re.sub(r"[ \t\r\n\xa0]+", " ", d)
        self.out.append(d)

    def texto(self):
        s = "".join(self.out)
        s = re.sub(r"[ \t\xa0]+\n", "\n", s)
        s = re.sub(r"\n[ \t\xa0]+(?=\S)", "\n", s)
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s.strip()


def conteudo_html(xml):
    """Junta o HTML de todos os campos plaintext do conteudo (exclui o menu)."""
    corpo = xml.split("</treemenu_1>", 1)[-1]
    partes = re.findall(r'<(\w+)\s[^>]*type="plaintext"[^>]*>.*?<value>(.*?)</value>', corpo, re.S)
    return "\n".join(html.unescape(v) for _, v in partes)


def documento(pid):
    xml = get(DOC_URL.format(pid))
    titulo = tag(xml, "sectionheader_1_text")
    titulo = re.sub(r"^<label\s*/>\s*<value>|</value>$", "", titulo).strip()
    m = re.search(r"<sectionheader_1_text[^>]*>\s*<label\s*/>\s*<value>(.*?)</value>", xml, re.S)
    if m:
        titulo = html.unescape(m.group(1)).strip()
    if re.fullmatch(r"(<p>)?\s*Sectionheader\s*(</p>)?", titulo or "", re.I):
        titulo = ""  # marcador por defeito devolvido para p_id inexistente
    d = re.search(r'<atualizado_em[^>]*value="([^"]*)"', xml)
    h = conteudo_html(xml)
    p = Texto()
    p.feed(h)
    txt = p.texto()
    rel = re.findall(r'<item rel="relacionados".*?<title>(.*?)</title>.*?p_id=(\d+)', xml, re.S)
    marc = {k: len(re.findall(v, txt, re.I)) for k, v in MARCADORES.items()}
    return {
        "titulo_pagina": titulo,
        "atualizado_em": d.group(1) if d else "",
        "texto": txt,
        "imagens": p.imgs,
        "html": h,
        "relacionados": [(html.unescape(t).strip(), i) for t, i in rel],
        **marc,
    }


def numero(t):
    m = re.match(r"\s*([\d.]+)\s", t)
    return m.group(1).rstrip(".") if m else ""


def escreve_md(caminho, menu_titulo, pid, info, extra):
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {menu_titulo or info['titulo_pagina']}\n\n")
        f.write(f"- p_id: {pid}\n- URL: {PUBLIC_URL.format(pid)}\n")
        f.write(f"- Titulo na pagina: {info['titulo_pagina']}\n")
        for k, v in extra.items():
            f.write(f"- {k}: {v}\n")
        f.write(f"- Atualizado em: {info['atualizado_em']}\n")
        f.write(f"- Caracteres: {len(info['texto'])} | Imagens: {info['imagens']}\n")
        rel = "; ".join(f"{t} (#{i})" for t, i in info["relacionados"])
        f.write(f"- Relacionados: {rel or '-'}\n\n---\n\n")
        f.write(info["texto"] + "\n")


def extrai_imagens(destino, pids):
    for pid in pids:
        h = conteudo_html(get(DOC_URL.format(pid)))
        pasta = os.path.join(destino, "img", str(pid))
        os.makedirs(pasta, exist_ok=True)
        n = 0
        for mime, b64 in re.findall(r'src="data:image/([a-z+]+);base64,([^"]+)"', h):
            n += 1
            ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(mime, mime)
            with open(os.path.join(pasta, f"{n}.{ext}"), "wb") as f:
                f.write(base64.b64decode(b64 + "=" * (-len(b64) % 4)))
        print(f"{pid}: {n} imagens -> {pasta}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    destino = sys.argv[1]
    os.makedirs(destino, exist_ok=True)
    if "--imagens" in sys.argv:
        extrai_imagens(destino, sys.argv[sys.argv.index("--imagens") + 1:])
        return

    arv = arvore()
    with open(os.path.join(destino, "arvore.txt"), "w", encoding="utf-8", newline="\n") as f:
        for nivel, t, i, pai, folha in arv:
            f.write(f"{'  ' * nivel}{t} | id={i}{'' if folha else ' [+]'}\n")

    folhas = [(t, i, pai) for nivel, t, i, pai, folha in arv if folha and nivel > 0]
    pais = {i: t for _, t, i, _, _ in arv}
    seccao = {}
    for nivel, t, i, pai, _ in arv:
        seccao[i] = t if nivel == 0 else seccao.get(pai, "")

    with cf.ThreadPoolExecutor(4) as ex:
        infos = dict(zip([i for _, i, _ in folhas], ex.map(documento, [i for _, i, _ in folhas])))
    # pedidos concorrentes ja devolveram o documento errado: repetir em sequencia quando o numero nao coincide
    for t, pid, _ in folhas:
        for _ in range(3):
            if numero(infos[pid]["titulo_pagina"]) == numero(t) and infos[pid]["texto"]:
                break
            infos[pid] = documento(pid)

    # orfaos: p_id no intervalo dos documentos que nao aparecem no menu
    ids_menu = {int(i) for _, i, _ in folhas}
    candidatos = [str(i) for i in range(min(ids_menu), max(ids_menu) + 17) if i not in ids_menu]
    with cf.ThreadPoolExecutor(4) as ex:
        orf = dict(zip(candidatos, ex.map(documento, candidatos)))

    hashes = {}
    for pid, info in list(infos.items()) + list(orf.items()):
        if info["texto"]:
            hashes.setdefault(hashlib.sha1(info["texto"].encode()).hexdigest(), []).append(pid)

    def estado(pid, info, menu_titulo):
        e = []
        if not info["titulo_pagina"] and not info["texto"]:
            e.append("vazio")
        elif len(re.sub(r"\[IMG [^\]]*\]|<[^>]+>", "", info["texto"]).strip()) < 200:
            e.append("quase_vazio")
        dup = [p for p in hashes.get(hashlib.sha1(info["texto"].encode()).hexdigest(), []) if p != pid] if info["texto"] else []
        if dup:
            e.append("conteudo_igual_a:" + "+".join(dup))
        if menu_titulo and info["titulo_pagina"] and numero(menu_titulo) != numero(info["titulo_pagina"]):
            e.append("titulo_divergente")
        return ";".join(e) or "ok"

    campos = ["origem", "seccao", "numero", "titulo_menu", "titulo_pagina", "p_id", "pai_id", "url", "atualizado_em",
              "caracteres", "imagens", "relacionados", *MARCADORES.keys(), "estado"]
    os.makedirs(os.path.join(destino, "orfaos"), exist_ok=True)
    with open(os.path.join(destino, "inventario.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(campos)
        for t, pid, pai in folhas:
            info = infos[pid]
            est = estado(pid, info, t)
            escreve_md(os.path.join(destino, f"{pid}.md"), t, pid, info,
                       {"Seccao": seccao.get(pid, ""), "Grupo": pais.get(pai, ""), "Estado": est})
            w.writerow(["menu", seccao.get(pid, ""), numero(t), t, info["titulo_pagina"], pid, pai, PUBLIC_URL.format(pid),
                        info["atualizado_em"], len(info["texto"]), info["imagens"],
                        " ".join(i for _, i in info["relacionados"]), *[info[k] for k in MARCADORES], est])
        for pid, info in orf.items():
            if not info["titulo_pagina"] and not info["texto"]:
                continue
            est = estado(pid, info, "")
            escreve_md(os.path.join(destino, "orfaos", f"{pid}.md"), "", pid, info, {"Estado": "fora do menu;" + est})
            w.writerow(["orfao", "", numero(info["titulo_pagina"]), "", info["titulo_pagina"], pid, "", PUBLIC_URL.format(pid),
                        info["atualizado_em"], len(info["texto"]), info["imagens"],
                        " ".join(i for _, i in info["relacionados"]), *[info[k] for k in MARCADORES], est])

    n_orf = sum(1 for i in orf.values() if i["titulo_pagina"] or i["texto"])
    print(f"menu: {len(arv)} nos, {len(folhas)} documentos; orfaos com conteudo: {n_orf}/{len(candidatos)}")


if __name__ == "__main__":
    main()
