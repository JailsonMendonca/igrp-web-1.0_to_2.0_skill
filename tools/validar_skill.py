"""Valida o pacote do skill (spec Agent Skills + portabilidade + rastreabilidade documental).

Uso (na raiz do workspace):
    python -I tools/validar_skill.py igrp-web-v1-v2 [audit/portal/inventario.csv]

Sai com codigo 1 se houver erros. So usa a biblioteca padrao.
"""
import csv
import os
import re
import sys

PORTAVEIS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
OPENAI_INTERFACE = {"display_name", "short_description", "icon_small", "icon_large", "brand_color", "default_prompt"}
FORA_AMBITO = re.compile(r"\bReact\b|\bSpring\b|New Horizon|IGRP 3|(?<![\d.,])3\.0(?![.\d)])|PL/SQL|WebLogic|\.NET|microsservi", re.I)
PERMITIDO_FORA = re.compile(r"fora|não us|nao us|exclu|out-of-scope|não aplique|v0|v3", re.I)

erros, avisos, infos = [], [], []


def frontmatter(texto):
    if not texto.startswith("---\n"):
        erros.append("SKILL.md: o frontmatter tem de começar na primeira linha com '---'")
        return {}, texto
    fim = texto.find("\n---\n", 4)
    if fim < 0:
        erros.append("SKILL.md: frontmatter sem '---' de fecho")
        return {}, texto
    bloco, corpo = texto[4:fim], texto[fim + 5:]
    dados, atual = {}, None
    for linha in bloco.split("\n"):
        if not linha.strip():
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", linha)
        if m and not linha.startswith(" "):
            k, v = m.group(1), m.group(2)
            if v == "":
                dados[k] = {}
                atual = k
            else:
                dados[k] = desaspas(v)
                atual = None
        elif atual and re.match(r"^\s+([A-Za-z0-9_.-]+):\s*(.*)$", linha):
            mk = re.match(r"^\s+([A-Za-z0-9_.-]+):\s*(.*)$", linha)
            dados[atual][mk.group(1)] = desaspas(mk.group(2), marca_tipo=True)
        else:
            erros.append(f"SKILL.md: linha de frontmatter não reconhecida: {linha!r}")
    return dados, corpo


def desaspas(v, marca_tipo=False):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1].replace('\\"', '"')
    if marca_tipo and (re.fullmatch(r"-?\d+(\.\d+)?", v) or v in ("true", "false", "yes", "no", "null")):
        return ("NAO_STRING", v)
    return v


def num_tuple(n):
    return tuple(int(x) for x in n.split(".") if x.isdigit())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    skill = os.path.abspath(sys.argv[1])
    inv_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join("audit", "portal", "inventario.csv")
    nome_pasta = os.path.basename(skill.rstrip("\\/"))

    # ficheiros e codificacao
    ficheiros = []
    for raiz, _, nomes in os.walk(skill):
        for n in nomes:
            ficheiros.append(os.path.join(raiz, n))
    for f in ficheiros:
        rel = os.path.relpath(f, skill).replace("\\", "/")
        dados = open(f, "rb").read()
        if dados.startswith(b"\xef\xbb\xbf"):
            erros.append(f"{rel}: tem BOM UTF-8")
        try:
            dados.decode("utf-8")
        except UnicodeDecodeError:
            erros.append(f"{rel}: não é UTF-8")
        if b"\r\n" in dados:
            avisos.append(f"{rel}: fins de linha CRLF")
        if not re.fullmatch(r"SKILL\.md|references/[a-z0-9-]+\.md|agents/openai\.yaml", rel):
            avisos.append(f"{rel}: ficheiro fora da estrutura esperada")

    skill_md = os.path.join(skill, "SKILL.md")
    if not os.path.exists(skill_md):
        erros.append("SKILL.md em falta")
        return fim()
    texto = open(skill_md, encoding="utf-8").read()
    fm, corpo = frontmatter(texto)

    # name / description / campos
    nome = fm.get("name", "")
    if not nome:
        erros.append("name em falta")
    else:
        if len(nome) > 64 or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", nome):
            erros.append(f"name inválido: {nome!r} (minúsculas, dígitos, hífenes simples; máx. 64)")
        if nome != nome_pasta:
            erros.append(f"name {nome!r} diferente do nome da pasta {nome_pasta!r}")
    desc = fm.get("description", "")
    if not isinstance(desc, str) or not (1 <= len(desc) <= 1024):
        erros.append(f"description com {len(desc) if isinstance(desc, str) else '?'} caracteres (1–1024)")
    elif re.search(r"[<>]", desc):
        erros.append("description contém '<' ou '>' (o claude.ai e o validador do skill-creator rejeitam)")
    elif len(desc) > 1024 - 100:
        avisos.append(f"description próxima do limite ({len(desc)}/1024)")
    if "compatibility" in fm and len(fm["compatibility"]) > 500:
        erros.append("compatibility com mais de 500 caracteres")
    for k in fm:
        if k not in PORTAVEIS:
            erros.append(f"campo de frontmatter não portável: {k} (claude.ai/API rejeitam campos fora de {sorted(PORTAVEIS)})")
    if "allowed-tools" in fm:
        avisos.append("allowed-tools é experimental e varia entre plataformas")
    if isinstance(fm.get("metadata"), dict):
        for k, v in fm["metadata"].items():
            if isinstance(v, tuple):
                erros.append(f"metadata.{k} não é string (use aspas): {v[1]}")
    elif "metadata" in fm:
        erros.append("metadata tem de ser um mapa string→string")

    linhas = texto.count("\n") + 1
    if linhas >= 500:
        erros.append(f"SKILL.md com {linhas} linhas (máx. recomendado 500)")
    tokens = len(corpo) / 4
    (avisos if tokens > 5000 else infos).append(f"corpo do SKILL.md ≈ {int(tokens)} tokens (recomendado < 5000); {linhas} linhas")
    infos.append(f"description: {len(desc)} caracteres")

    # ligacoes: SKILL.md -> references (um nivel)
    ligados = set()
    for alvo in re.findall(r"\]\(([^)#\s]+)\)", corpo):
        if re.match(r"https?://", alvo):
            continue
        caminho = os.path.normpath(os.path.join(skill, alvo))
        if not os.path.exists(caminho):
            erros.append(f"SKILL.md: ligação partida {alvo}")
        ligados.add(os.path.relpath(caminho, skill).replace("\\", "/"))
    refs = sorted(os.path.relpath(f, skill).replace("\\", "/") for f in ficheiros if "/references/" in f.replace("\\", "/"))
    for r in refs:
        if r not in ligados:
            erros.append(f"{r} não está ligado diretamente a partir do SKILL.md")
        conteudo = open(os.path.join(skill, r), encoding="utf-8").read()
        for alvo in re.findall(r"\]\(([^)#\s]+\.md)\)", conteudo):
            avisos.append(f"{r}: ligação markdown para outro ficheiro ({alvo}) — evitar cadeias de referências")

    # rastreabilidade: p_id citados e cobertura
    if not os.path.exists(inv_path):
        avisos.append(f"inventário não encontrado ({inv_path}); verificações de citação ignoradas")
        return fim()
    inv = [r for r in csv.DictReader(open(inv_path, encoding="utf-8")) if r["origem"] == "menu"]
    pids = {r["p_id"] for r in inv}
    textos = {r: open(os.path.join(skill, r), encoding="utf-8").read() for r in refs}
    textos["SKILL.md"] = texto
    todos = "\n".join(t for k, t in textos.items() if not k.endswith("fontes-e-inventario.md"))
    for k, t in textos.items():
        for pid in set(re.findall(r"#(1\d{3})\b", t)):
            if pid not in pids:
                erros.append(f"{k}: cita p_id #{pid} que não existe no inventário")
    numeros_citados = set(re.findall(r"(?<![\d.#])(\d{1,2}(?:\.\d{1,2}){1,2})(?![\d])", todos))
    intervalos = [(num_tuple(a), num_tuple(b)) for a, b in
                  re.findall(r"(\d{1,2}(?:\.\d{1,2}){1,2})(?:\.x)?\s*[–-]\s*(\d{1,2}(?:\.\d{1,2}){1,2})", todos)]
    sem_cobertura = []
    for r in inv:
        n, pid = r["numero"], r["p_id"]
        pai = n.rsplit(".", 1)[0] if n.count(".") >= 2 else None
        coberto = (f"#{pid}" in todos or n in numeros_citados or (pai and pai in numeros_citados)
                   or any(a <= num_tuple(n) <= b for a, b in intervalos))
        if not coberto:
            sem_cobertura.append(f"{n} (#{pid})")
    if sem_cobertura:
        avisos.append(f"{len(sem_cobertura)} documentos sem citação nas referências temáticas: {', '.join(sem_cobertura)}")
    infos.append(f"cobertura: {len(inv) - len(sem_cobertura)}/{len(inv)} documentos citados nas referências temáticas")
    etiquetas = {e: len(re.findall(re.escape(e), "\n".join(textos.values()))) for e in ("[DOC", "[CÓD", "[REPO", "[MVN", "[PROJ", "[ENG")}
    infos.append("etiquetas de fonte: " + ", ".join(f"{k}]={v}" for k, v in etiquetas.items()))

    # conteudo fora de ambito
    for k, t in textos.items():
        for i, linha in enumerate(t.split("\n"), 1):
            if FORA_AMBITO.search(linha) and not PERMITIDO_FORA.search(linha) and not k.endswith("identificacao-de-versao.md"):
                avisos.append(f"{k}:{i}: menção a outra versão/tecnologia fora de âmbito: {linha.strip()[:110]}")

    # agents/openai.yaml
    oy = os.path.join(skill, "agents", "openai.yaml")
    if os.path.exists(oy):
        sec = None
        for linha in open(oy, encoding="utf-8"):
            if re.match(r"^[a-z_]+:\s*$", linha):
                sec = linha.split(":")[0]
                if sec not in ("interface", "policy", "dependencies"):
                    erros.append(f"agents/openai.yaml: secção desconhecida {sec}")
            m = re.match(r"^\s+([a-z_]+):", linha)
            if m and sec == "interface" and m.group(1) not in OPENAI_INTERFACE:
                avisos.append(f"agents/openai.yaml: campo interface.{m.group(1)} não documentado")
            if m and sec == "policy" and m.group(1) != "allow_implicit_invocation":
                avisos.append(f"agents/openai.yaml: campo policy.{m.group(1)} não documentado")
        if nome and f"${nome}" not in open(oy, encoding="utf-8").read():
            avisos.append("agents/openai.yaml: default_prompt não menciona $" + nome)
    return fim()


def fim():
    for titulo, lst in (("ERRO", erros), ("AVISO", avisos), ("INFO", infos)):
        for x in lst:
            print(f"[{titulo}] {x}")
    print(f"\nResultado: {len(erros)} erro(s), {len(avisos)} aviso(s)")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
