# Arquitectura

## Visión general

Future Skills Engine sigue una arquitectura **Medallion** (Bronze → Silver → Gold) para procesar datos provenientes de tres fuentes externas: Stack Overflow Developer Survey, GitHub REST API y arXiv API. El flujo completo está orquestado por Apache Airflow y los resultados finales se exponen a través de un dashboard interactivo desarrollado con Streamlit.

## Diagrama de flujo

```
┌──────────────────┐
│   Stack Overflow │
│   Developer      │
│   Survey         │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   GitHub REST    │
│   API            │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   arXiv API      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│          Bronze Layer                │
│   - Ingesta de datos crudos          │
│   - Almacenamiento sin               │
│     transformaciones                 │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│          Silver Layer                │
│   - Limpieza y validación            │
│   - Estandarización de formatos      │
│   - Deduplicación                    │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│           Gold Layer                 │
│   - Tablas analíticas                │
│   - Datos agregados y                │
│     preparados para consumo          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│     Future Skills Engine             │
│   - Cálculo del Future Score         │
│   - Generación de ranking            │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      Streamlit Dashboard             │
│   - Visualización interactiva        │
│   - Exploración de tendencias        │
└──────────────────────────────────────┘
```

## Componentes de la arquitectura

### Bronze Layer

La capa Bronze es responsable de la ingesta inicial de datos desde cada fuente. Los datos se almacenan en su formato original, sin aplicar transformaciones, garantizando la trazabilidad y la posibilidad de reprocesar desde el punto de origen.

### Silver Layer

La capa Silver aplica procesos de limpieza, validación y estandarización. Los datos se normalizan en un formato consistente, se eliminan duplicados y se corrigen errores de calidad. Esta capa actúa como fuente única de verdad para las capas superiores.

### Gold Layer

La capa Gold contiene tablas analíticas optimizadas para consumo. Los datos se agregan y estructuran según las necesidades del negocio, eliminando complejidad innecesaria y proporcionando vistas listas para el análisis.

### Future Skills Engine

Este componente consume las tablas de la capa Gold para calcular el **Future Score** de cada tecnología. El engine genera un ranking integrado que combina las señales de las tres fuentes originales, sin implementar modelos predictivos ni de machine learning.

### Dashboard

El dashboard, desarrollado con Streamlit, consulta directamente las tablas Gold y los resultados del Future Skills Engine. Ofrece una interfaz interactiva para explorar tendencias, crecimiento, actividad open source e impacto de investigación.
