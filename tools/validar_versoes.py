"""Valida a cobertura de versoes do skill igrp-web-v1-v2 (v1 = 1.x, v2 = 2.x).

1. Le as builds publicadas de cv.igrp:igrp-core e igrp-core-war (Maven Central e Nexus NOSi) e junta casos hipoteticos
   (1.10.0, 2.2.0, 2.9.9, 3.0.0-alpha, formatos antigos AAMMDD/VAAMMDD...).
2. Classifica cada versao com a regra do skill (references/identificacao-de-versao.md):
   1.0.0 <= v < 2.0.0 -> v1; 2.0.0 <= v < 3.0.0 -> v2; AAMMDD ou VAAMMDD (2018-2022) -> v1; 3.x ou superior -> fora de ambito.
3. Se houver Java e Maven, testa os intervalos [1.0.0,2.0.0), [1.9.0,2.0.0) e [2.0.0,3.0.0) com o mesmo motor que o Maven usa
   para resolver intervalos (maven-resolver GenericVersionScheme) e assinala as divergencias com a regra.

Uso: python -I tools/validar_versoes.py [--offline]   (so leitura; faz 4 pedidos HTTP aos metadados Maven, salvo --offline)
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

REPOS = {
    "Maven Central": "https://repo1.maven.org/maven2/cv/igrp/{a}/maven-metadata.xml",
    "Nexus NOSi": "https://sonatype.nosi.cv/repository/maven-releases/cv/igrp/{a}/maven-metadata.xml",
}
ARTEFACTOS = ("igrp-core", "igrp-core-war")
HIPOTETICAS = [
    "1.0.0", "1.10.0", "1.99.99", "1.9.9.991231", "1.8.3.240808.1",
    "2.0.0-alpha", "2.0.0", "2.2.0", "2.2.0.270101", "2.5.0-RC1", "2.9.9", "2.9.9.991231", "2.10.0", "2.99.99",
    "3.0.0-alpha", "3.0.0-RC1", "3.0.0-SNAPSHOT", "3.0.0", "3.1.0",
    "180627", "211115", "220523", "V200403", "0.0.1",
]
FAIXAS = ["[1.0.0,2.0.0)", "[1.9.0,2.0.0)", "[2.0.0,3.0.0)"]

JAVA = r"""
import org.eclipse.aether.util.version.GenericVersionScheme;
import org.eclipse.aether.version.*;
import java.nio.file.*;
import java.util.*;
public class Faixas {
  public static void main(String[] a) throws Exception {
    GenericVersionScheme s = new GenericVersionScheme();
    List<VersionConstraint> cs = new ArrayList<>();
    for (int i = 1; i < a.length; i++) cs.add(s.parseVersionConstraint(a[i]));
    for (String linha : Files.readAllLines(Path.of(a[0]))) {
      String v = linha.trim();
      if (v.isEmpty()) continue;
      Version ver = s.parseVersion(v);
      StringBuilder sb = new StringBuilder(v);
      for (VersionConstraint c : cs) sb.append('\t').append(c.containsVersion(ver) ? '1' : '0');
      System.out.println(sb);
    }
  }
}
"""


def regra_skill(v):
    if re.fullmatch(r"V?\d{6}", v):
        return "v1"  # formato antigo do Config.VERSION (2018-06 a 2022-05)
    m = re.match(r"(\d+)\.", v + ".")
    maior = int(m.group(1)) if m else -1
    return {1: "v1", 2: "v2"}.get(maior, "fora" if maior >= 3 else "inconclusivo")


def publicadas():
    vistas = {}
    for repo, url in REPOS.items():
        for a in ARTEFACTOS:
            try:
                xml = urllib.request.urlopen(url.format(a=a), timeout=30).read().decode("utf-8")
            except Exception as e:  # noqa: BLE001
                print(f"[AVISO] {repo} {a}: {e}")
                continue
            for v in re.findall(r"<version>([^<]+)</version>", xml):
                vistas.setdefault(v, set()).add(repo)
    return vistas


def maven_lib():
    home = os.environ.get("MAVEN_HOME") or os.environ.get("M2_HOME")
    if not home and shutil.which("mvn"):
        out = subprocess.run("mvn -v", shell=True, capture_output=True, text=True).stdout
        m = re.search(r"Maven home: (.+)", out)
        home = m.group(1).strip() if m else None
    if not home:
        return None
    lib = os.path.join(home, "lib")
    jars = [os.path.join(lib, f) for f in os.listdir(lib) if re.match(r"maven-resolver-(api|util)-.*\.jar$", f)]
    return os.pathsep.join(jars) if len(jars) == 2 else None


def main():
    offline = "--offline" in sys.argv
    pub = {} if offline else publicadas()
    versoes = sorted(set(pub) | set(HIPOTETICAS))
    faixas = {}
    cp = maven_lib()
    if cp and shutil.which("java"):
        with tempfile.TemporaryDirectory() as d:
            src, lst = os.path.join(d, "Faixas.java"), os.path.join(d, "versoes.txt")
            open(src, "w", encoding="utf-8").write(JAVA)
            open(lst, "w", encoding="utf-8").write("\n".join(versoes))
            r = subprocess.run(["java", "-cp", cp, src, lst, *FAIXAS], capture_output=True, text=True)
            if r.returncode:
                print("[AVISO] teste Maven falhou:", r.stderr.strip()[:300])
            for linha in r.stdout.splitlines():
                v, *bits = linha.split("\t")
                faixas[v] = [b == "1" for b in bits]
    else:
        print("[AVISO] Java ou Maven não encontrados: intervalos não testados")

    erros, notas, contagem = [], [], {}
    for v in versoes:
        cls = regra_skill(v)
        contagem[(cls, "publicada" if v in pub else "hipotética")] = contagem.get((cls, "publicada" if v in pub else "hipotética"), 0) + 1
        if v in pub and cls not in ("v1", "v2"):
            erros.append(f"publicada {v} ({'/'.join(sorted(pub[v]))}) não é classificada como v1 nem v2")
        if v in faixas:
            v1_rng, _, v2_rng = faixas[v]
            if cls == "v1" and not v1_rng and not re.fullmatch(r"V?\d{6}", v):
                (erros if v in pub else notas).append(f"{v}: regra v1, mas fora de [1.0.0,2.0.0) no Maven")
            if cls == "v2" and not v2_rng:
                (erros if v in pub else notas).append(f"{v}: regra v2, mas fora de [2.0.0,3.0.0) no Maven")
            if cls != "v1" and v1_rng:
                (erros if v in pub else notas).append(f"{v}: regra {cls}, mas DENTRO de [1.0.0,2.0.0) no Maven")
            if cls != "v2" and v2_rng:
                (erros if v in pub else notas).append(f"{v}: regra {cls}, mas DENTRO de [2.0.0,3.0.0) no Maven")

    def maximo(prefixo):
        cands = [v for v in pub if v.startswith(prefixo)]
        return max(cands, key=lambda v: [int(x) if x.isdigit() else 0 for x in re.split(r"[.-]", v)]) if cands else "-"

    print(f"Builds publicadas lidas: {len(pub)} (v1 mais alta: {maximo('1.')}; v2 mais alta: {maximo('2.')}; "
          f"≥ 2.2: {sum(1 for v in pub if re.match(r'2\.([2-9]|\d{2,})\.', v))}; 3.x: {sum(1 for v in pub if v.startswith('3.'))})")
    for (cls, tipo), n in sorted(contagem.items()):
        print(f"  {cls:13s} {tipo:10s} {n}")
    if faixas:
        print("Intervalos (motor do Maven) para casos-limite:")
        for v in HIPOTETICAS:
            if v in faixas:
                print(f"  {v:16s} regra={regra_skill(v):5s} " + " ".join(f"{f}={'sim' if b else 'não'}" for f, b in zip(FAIXAS, faixas[v])))
    for n in notas:
        print("[NOTA]", n)
    for e in erros:
        print("[ERRO]", e)
    print(f"\nResultado: {len(erros)} erro(s), {len(notas)} nota(s) sobre versões hipotéticas")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
