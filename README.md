# Future Skills Engine

**Future Skills Engine** es una plataforma de inteligencia tecnológica que integra múltiples fuentes de información para analizar el estado actual del ecosistema tecnológico y generar un ranking de tecnologías mediante un modelo de scoring llamado **Future Score**.

---

## Descripción general

La plataforma procesa señales provenientes de tres fuentes distintas:

- **Stack Overflow Developer Survey** — Adopción, uso y preferencias de tecnologías entre desarrolladores
- **GitHub REST API** — Actividad open source, métricas de repositorios y participación comunitaria
- **arXiv API** — Producción científica e interés académico en temas tecnológicos

Todos los datos fluyen a través de una arquitectura **Medallion (Bronze → Silver → Gold)** orquestada por Apache Airflow, con los resultados visualizados en un dashboard desarrollado con Streamlit. El objetivo es transformar datos heterogéneos en indicadores comparables que faciliten el análisis de tecnologías emergentes.

---

## Objetivo

Proporcionar información clara y basada en datos sobre las tendencias tecnológicas, combinando adopción en la industria, actividad comunitaria e investigación académica en un sistema de ranking unificado.

El **Future Score** ayuda a responder preguntas como:

- ¿Qué tecnologías están ganando terreno?
- ¿Dónde hay mayor momentum en open source?
- ¿Qué áreas de investigación están emergiendo?

---

## Características principales

| Característica | Descripción |
|----------------|-------------|
| **Integración multi-fuente** | Combina datos de encuestas, repositorios e investigación académica |
| **Pipeline ETL automatizado** | Orquestación del flujo de datos mediante Apache Airflow |
| **Arquitectura Medallion** | Bronze (crudo) → Silver (limpio) → Gold (analítico) |
| **Dashboard interactivo** |Aplicación Streamlit compuesta por una página principal y siete vistas analíticas. |
| **Ranking de tecnologías** | Cálculo del Future Score a partir de señales combinadas |

---

## Arquitectura resumida

```
Fuentes de datos
     ↓
 Capa Bronze (ingesta cruda)
     ↓
 Capa Silver (limpieza y validación)
     ↓
  Capa Gold (tablas analíticas)
     ↓
 Future Skills Engine (scoring)
     ↓
   Dashboard (Streamlit)
```

---

## Stack tecnológico

| Categoría | Herramientas |
|-----------|--------------|
| Lenguaje | Python 3.10+ |
| Procesamiento de datos | Pandas, SQLAlchemy |
| Base de datos | PostgreSQL |
| Orquestación | Apache Airflow |
| Contenerización | Docker, Docker Compose |
| Visualización | Streamlit |
| APIs | GitHub REST API, arXiv API |

---

## Resultados

Actualmente el proyecto integra información proveniente de tres fuentes de datos y genera:

- 215 tecnologías analizadas.
- 7 tablas analíticas en la capa Gold.
- Future Score para cada tecnología.
- Dashboard interactivo con 8 vistas (Home + 7 páginas analíticas).

---

## Estructura del proyecto

```
Future-Skills-Engine/
├── airflow/
├── data/
├── notebooks/
├── sql/
├── src/
│   ├── config/
│   ├── dashboard/
│   ├── extract/
│   ├── transform/
│   └── utils/
├── docker-compose.yml
└── README.md
```

---

## Ejecución local

### Requisitos previos

- Docker y Docker Compose
- Token de acceso personal de GitHub (para acceso a la API)

### Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/alejotrenti/future-skills-engine
cd future-skills-engine
```

2. Configurar variables de entorno

```bash
cp .env
```

Edita el archivo `.env` con tu token de GitHub y credenciales de base de datos.

3. Iniciar los servicios

```bash
docker-compose up -d
```

4. Acceder a los servicios

| Servicio | URL |
|----------|-----|
| Airflow UI | http://localhost:8080 |
| Dashboard Streamlit | http://localhost:8501 |

5. Ejecutar el pipeline

Ejecutar los DAGs respetando el orden de las capas:

```bash
docker-compose exec airflow airflow dags trigger bronze_github_dag
docker-compose exec airflow airflow dags trigger bronze_stackoverflow_dag
docker-compose exec airflow airflow dags trigger bronze_arxiv_dag
docker-compose exec airflow airflow dags trigger silver_github_dag
docker-compose exec airflow airflow dags trigger silver_stackoverflow_dag
docker-compose exec airflow airflow dags trigger silver_arxiv_dag
docker-compose exec airflow airflow dags trigger gold_layer_builder_dag
```

---

## Roadmap

- [ ] Agregar nuevas fuentes de datos (Twitter/X, Hacker News, ofertas de trabajo)
- [ ] Implementar monitoreo de calidad de datos y alertas
- [ ] Añadir capacidad de backfill histórico
- [ ] Optimizar el modelo de scoring con retroalimentación de usuarios
- [ ] Ampliar el dashboard con filtros personalizados y opciones de exportación
- [ ] Agregar pipeline CI/CD para pruebas y despliegue

---

## Documentación

La documentación detallada está disponible en el directorio `docs/`:

- [Visión general de la arquitectura](docs/arquitectura.md)
- [Detalles del pipeline](docs/pipeline.md)
- [Metodología del Future Score](docs/future-score.md)
- [Guía del dashboard](docs/dashboard.md)

---

## Autor

**Tu Nombre**

- GitHub: [@alejotrenti](https://github.com/alejotrenti)
- Correo: aletrenti@outlook.com
