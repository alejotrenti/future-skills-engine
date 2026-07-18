# 🚀 Future Skills Engine

## Motor de análisis y predicción de tendencias tecnológicas

**Future Skills Engine** es un proyecto de Data Engineering y Data Science orientado a identificar las tecnologías y habilidades que están ganando relevancia en el ecosistema tecnológico.

El sistema integra múltiples fuentes de datos como encuestas de desarrolladores, actividad de repositorios y publicaciones científicas para construir un pipeline completo que transforma datos crudos en insights accionables sobre el futuro de las habilidades digitales.

El proyecto implementa una arquitectura moderna de datos basada en capas **Bronze → Silver → Gold**, utilizando **Apache Airflow** para la orquestación, **PostgreSQL** como almacenamiento analítico y **Streamlit** para la visualización.

---

# 🎯 Objetivo del proyecto

El crecimiento constante de nuevas tecnologías hace difícil identificar qué herramientas tendrán mayor impacto en los próximos años.

Future Skills Engine busca responder preguntas como:

* ¿Qué tecnologías están creciendo más rápido?
* ¿Qué lenguajes y frameworks tienen mayor adopción?
* ¿Qué herramientas están aumentando su actividad en GitHub?
* ¿Qué áreas tecnológicas están recibiendo más investigación científica?
* ¿Cuáles podrían ser las skills más relevantes del futuro?

---

# 🏗️ Arquitectura del sistema

```text
                    Fuentes de datos

        Stack Overflow Survey
                 |
                 |
          GitHub API
                 |
                 |
            arXiv API
                 |
                 ▼

              Bronze Layer
          Datos originales/raw

                 |
                 ▼

              Silver Layer
       Limpieza + transformación
        + normalización de datos

                 |
                 ▼

               Gold Layer
        Métricas y datasets analíticos

                 |
                 ▼

          Streamlit Dashboard
        Visualización e insights
```

---

# 🛠️ Stack tecnológico

| Área                 | Tecnología              |
| -------------------- | ----------------------- |
| Lenguaje             | Python                  |
| Procesamiento        | Pandas                  |
| Base de datos        | PostgreSQL              |
| Orquestación         | Apache Airflow          |
| Contenedores         | Docker / Docker Compose |
| Dashboard            | Streamlit               |
| APIs                 | GitHub API, arXiv API   |
| SQL                  | SQLAlchemy              |
| Control de versiones | Git / GitHub            |

---

# 📂 Estructura del proyecto

```text
Future-Skills-Engine/

├── airflow/
│   └── dags/
│
├── data/
│   └── raw/
│
├── src/
│   │
│   ├── extract/
│   │   ├── stackoverflow/
│   │   ├── github/
│   │   └── arxiv/
│   │
│   ├── load/
│   │
│   ├── transform/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   │
│   └── dashboard/
│       ├── app.py
│       ├── db.py
│       └── pages/
│
├── sql/
│   └── init.sql
│
├── docker-compose.yml
│
└── README.md
```

---

# 🥉 Bronze Layer — Datos originales

La capa Bronze almacena la información tal como llega desde las fuentes externas.

Fuentes actuales:

## Stack Overflow Developer Survey

Contiene información sobre:

* Lenguajes utilizados
* Frameworks
* Bases de datos
* Cloud providers
* Herramientas de desarrollo
* Experiencia profesional

Tabla:

```sql
bronze.stackoverflow_raw
```

---

## GitHub API

Recolecta información sobre actividad del ecosistema open source:

* Repositorios
* Lenguajes utilizados
* Estrellas
* Forks
* Actividad reciente
* Tendencias de proyectos

---

## arXiv API

Incorpora información del ámbito científico:

* Papers publicados
* Categorías de investigación
* Frecuencia de publicación
* Áreas tecnológicas emergentes

---

# 🥈 Silver Layer — Datos procesados

La capa Silver transforma los datos originales en estructuras limpias listas para análisis.

Procesos realizados:

* Limpieza de datos
* Normalización
* Eliminación de duplicados
* Conversión de formatos
* Separación de entidades
* Clasificación de tecnologías

Ejemplo de tablas:

```sql
silver.respondents

silver.skills

silver.github_repositories

silver.research_papers
```

---

# 🥇 Gold Layer — Métricas analíticas

La capa Gold contiene información preparada para consumo del dashboard.

Ejemplos:

## Skill Trends

Ranking de tecnologías basado en adopción actual.

Métricas:

* Tecnología
* Categoría
* Cantidad de usuarios
* Ranking

---

## Skill Growth

Modelo de crecimiento de habilidades combinando diferentes señales:

* Adopción de desarrolladores
* Actividad en GitHub
* Producción científica
* Evolución temporal

---

# 📊 Dashboard

El dashboard desarrollado con Streamlit permite explorar las tendencias generadas por el pipeline.

Funcionalidades:

* 📈 Ranking de tecnologías
* 🔥 Skills en crecimiento
* 🔎 Exploración por categorías
* 📊 Métricas generales
* 📉 Evolución temporal

El dashboard consume únicamente tablas Gold, manteniendo una separación correcta entre procesamiento y visualización.

---

# ⚙️ Pipeline de datos

La ejecución completa sigue el flujo:

```text
Extracción desde APIs / CSV
            |
            ▼
Carga Bronze
            |
            ▼
Transformaciones Silver
            |
            ▼
Modelado Gold
            |
            ▼
Dashboard Analytics
```

La ejecución está automatizada mediante DAGs de Apache Airflow.

---

# 🚀 Ejecución local

Clonar repositorio:

```bash
git clone https://github.com/usuario/Future-Skills-Engine.git
```

Ingresar al proyecto:

```bash
cd Future-Skills-Engine
```

Levantar servicios:

```bash
docker compose up --build
```

Servicios disponibles:

| Servicio            | URL                   |
| ------------------- | --------------------- |
| Airflow             | http://localhost:8080 |
| Streamlit Dashboard | http://localhost:8501 |

---

# 📚 Fuentes de datos

* Stack Overflow Developer Survey
* GitHub REST API
* arXiv API

---

# 🧠 Conceptos aplicados

Este proyecto demuestra experiencia práctica en:

* Data Engineering
* ETL / ELT pipelines
* Arquitectura Medallion
* Data Warehousing
* Orquestación con Airflow
* Integración con APIs
* Modelado dimensional
* SQL avanzado
* Visualización de datos
* Contenedores Docker

---

# 🔮 Próximas mejoras

* Modelo Machine Learning para forecasting de skills
* Predicción de tecnologías emergentes
* Incorporación de datos de ofertas laborales
* Deploy en cloud
* Sistema de scoring de tecnologías
* API propia para consultas
* CI/CD automático

---

# 👨‍💻 Autor

**Alejo Treni**

Proyecto personal enfocado en Data Engineering, Data Science y análisis de tendencias tecnológicas.

---

⭐ Si este proyecto te resulta interesante, ¡dejá una estrella!
