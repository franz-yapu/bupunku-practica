# Guía Angular y Flask

Sitio estático con la guía de `angular-buscador` y `flask-biblioteca`.

- `src/index.html`: la plantilla (texto, estilos y JS). Los marcadores `<!--archivo:RUTA|lenguaje-->` se reemplazan por el código real.
- `build.py`: genera `index.html` (el que se publica). **Correrlo cada vez que cambie la plantilla o el código de los proyectos**, y commitear `index.html`.
- `Dockerfile` + `nginx.conf`: sirven `index.html` con nginx.

```bash
python3 guia/build.py
docker build -t guia guia && docker run --rm -p 8080:80 guia   # http://localhost:8080
```

## Publicar en guia.vertexall.com (Coolify)

El DNS `*.vertexall.com` ya apunta al VPS y Traefik saca el certificado, así que basta con crear la app:

1. Coolify → proyecto nuevo `guia` → **+ New Resource** → **Public Repository** →
   `https://github.com/franz-yapu/bupunku-practica`, rama `main`.
2. Build pack: **Dockerfile**. Base directory: `/guia`. Puerto expuesto: `80`.
3. Domains: `https://guia.vertexall.com`.
4. **Deploy**. Para actualizar: `python3 guia/build.py`, commit, push y **Redeploy**
   (o activar *Auto Deploy* con el webhook de GitHub).

Verificar: `curl -sI https://guia.vertexall.com | head -1` → `HTTP/2 200`.
