# HexForge Security Lite v1.6 Community

Herramienta comunitaria de análisis web seguro para aprendizaje, revisión básica y demostraciones técnicas.

## Características

- 30 checks activos.
- Límite comunitario ampliado: 50 URLs por sesión del servidor.
- Análisis de cabeceras HTTP, HTML básico, enlaces HTTP, scripts externos, metadatos y TLS básico.
- Resultados con evidencia, ubicación y recomendación.
- Interfaz multilenguaje básica.
- Sin exportación DOCX/PDF/ZIP en Lite.
- Uso no comercial sin autorización.

## Ejecutar localmente

```bash
chmod +x run.sh
./run.sh
```

Abrir:

```text
http://localhost:8000
```

## Deploy en Render

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
python3 server.py
```

El servidor lee automáticamente la variable `PORT` de Render.

## Licencia

Uso personal, educativo y comunitario permitido. Uso comercial no permitido sin autorización expresa del autor.
