# HexForge Security Lite v1.7

HexForge Security Lite es una herramienta de análisis web no invasivo construida en Python puro. Esta versión reorganiza el proyecto para que deje de verse como un único archivo con todos los checks mezclados y pase a una arquitectura modular, mantenible y lista para crecer.

## Qué cambia en esta versión

- Motor dividido en paquete `hexforge_lite/`.
- 15 módulos defensivos separados, cada uno en su propio archivo.
- Validadores dedicados para reducir ruido y hallazgos duplicados.
- Sitio web Lite renovado, manteniendo logo, contacto y PayPal.
- Licencia más clara: código disponible para uso no comercial, pero marca y nombre reservados.
- Suite de pruebas en laboratorio local con 50 casos controlados.

## Alcance de Lite

HexForge Lite se enfoca en señales defensivas de alta utilidad y baja agresividad.

### Módulos activos

1. Security headers
2. Clickjacking
3. CORS policy
4. Cookie flags
5. Cache policy
6. Redirect policy
7. Content-Type and nosniff
8. Metadata exposure
9. Comments exposure
10. Email and JWT-like exposure
11. External resources
12. Mixed content
13. Forms basics
14. robots.txt and sitemap.xml review
15. TLS basics

## Estructura

```text
hexforge-security-lite-v1.7-modular/
├── assets/
├── hexforge_lite/
│   ├── config.py
│   ├── engine.py
│   ├── fetcher.py
│   ├── models.py
│   ├── modules/
│   ├── utils/
│   └── validators/
├── tests/
├── website/
├── LICENSE
├── TRADEMARKS.md
├── README.md
├── run.sh
└── server.py
```

## Ejecutar localmente

```bash
chmod +x run.sh
./run.sh
```

Abrir en el navegador:

```text
http://localhost:8000
```

## API

### Escaneo

```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

### Salud del servicio

```bash
curl http://localhost:8000/health
```

## Pruebas locales

La suite de pruebas crea un laboratorio HTTP local con 50 escenarios controlados para validar que el motor no explote, deduplique correctamente y emita hallazgos esperados.

```bash
python3 -m unittest discover -s tests -v
```

## Licencia

El proyecto es **source-available**, no open source en sentido estricto, porque restringe uso comercial y protege la marca.

Ver:

- `LICENSE`
- `TRADEMARKS.md`
