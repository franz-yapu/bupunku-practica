"""Genera index.html a partir de src/index.html.

Cada marcador <!--archivo:RUTA|LENGUAJE--> se reemplaza por el contenido real del archivo
(relativo a la raíz del repo), escapado y listo para copiar. Así la guía nunca se desfasa del código.

Uso:  python guia/build.py
"""

import html
import re
from pathlib import Path

GUIA = Path(__file__).resolve().parent
REPO = GUIA.parent
MARCADOR = re.compile(r"<!--archivo:([^|>]+)\|([a-z]+)-->")


def bloque(ruta, lenguaje):
    codigo = (REPO / ruta).read_text(encoding="utf-8").rstrip()
    nombre = ruta.split("/", 1)[1]  # sin el nombre del proyecto
    return (
        f'<figure class="codigo"><figcaption>{html.escape(nombre)}</figcaption>'
        f'<pre><code class="language-{lenguaje}">{html.escape(codigo)}</code></pre></figure>'
    )


def main():
    plantilla = (GUIA / "src" / "index.html").read_text(encoding="utf-8")
    salida = MARCADOR.sub(lambda m: bloque(m.group(1).strip(), m.group(2)), plantilla)
    destino = GUIA / "index.html"
    destino.write_text(salida, encoding="utf-8")
    print(f"Listo: {destino.relative_to(REPO)} ({len(MARCADOR.findall(plantilla))} archivos incrustados)")


if __name__ == "__main__":
    main()
