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

corpo = (AQUI / "fonte" / "painel.html").read_text(encoding="utf-8")
html = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="robots" content="noindex,nofollow">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'
        '</head><body>' + corpo + '</body></html>')
(AQUI / "index.html").write_text(html, encoding="utf-8")
print(f"{len(experts)} expert(s), {len(pedidos)} pedido(s) · {agora}")
