"""Monta a versão online (só leitura) do DN Grow Experts para o GitHub Pages.

Uso:
  1. Exporte o banco do painel com ArtifactData (list, out_dir=<pasta>) das coleções
     experts e pedidos.
  2. py -3 montar_site.py <pasta-do-export>
Gera index.html (a mesma página do painel, embrulhada como documento) e dados.json.
"""
import json, sys, pathlib, datetime

AQUI = pathlib.Path(__file__).parent
export = pathlib.Path(sys.argv[1])

def ler(col):
    pasta = export / col
    if not pasta.exists():
        return []
    out = []
    for f in sorted(pasta.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        d["id"] = f.stem
        out.append(d)
    return out

experts = ler("experts")
pedidos = ler("pedidos")
for p in pedidos:
    p.pop("prompt", None)  # o pedido completo fica só no painel do Claude

agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
(AQUI / "dados.json").write_text(json.dumps({"atualizadoEm": agora, "experts": experts, "pedidos": pedidos}, ensure_ascii=False), encoding="utf-8")

def documento(corpo):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<meta name="robots" content="noindex,nofollow">'
            '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
            '</head><body>' + corpo + '</body></html>')

# As duas páginas se ligam só no site: no Claude cada uma é um artifact separado.
LINK = '<a href="{href}" style="font:600 13px system-ui,sans-serif;color:#3550c4;text-decoration:none;border:1px solid #d6dbe8;border-radius:8px;padding:6px 12px;background:#fff">{txt}</a>'

corpo = (AQUI / "fonte" / "painel.html").read_text(encoding="utf-8")
(AQUI / "index.html").write_text(documento(corpo), encoding="utf-8")

# Página de Projetos (números por produto): vem pronta, com os dados dentro, da pasta dn-grow-projetos.
proj = AQUI.parent / "dn-grow-projetos" / "index.html"
if proj.exists():
    p = proj.read_text(encoding="utf-8")
    p = p.replace('<span class="stamp" id="stamp"></span>', '<span class="stamp" id="stamp"></span>' + LINK.format(href="./", txt="← Funil de experts"), 1)
    (AQUI / "projetos.html").write_text(documento(p), encoding="utf-8")
print(f"{len(experts)} expert(s), {len(pedidos)} pedido(s) · {agora} · projetos.html {'ok' if proj.exists() else 'ausente'}")
