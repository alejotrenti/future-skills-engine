# Pipeline de datos

## Introducción

El pipeline de datos de Future Skills Engine extrae información desde múltiples fuentes, la transforma mediante un proceso ETL y genera datasets analíticos listos para su análisis. El proceso sigue la arquitectura Medallion, avanzando progresivamente desde datos crudos hasta datasets analíticos listos para usar.

## Flujo general

```
Stack Overflow ──┐
GitHub API    ──┼──► Bronze ──► Silver ──► Gold
arXiv API     ──┘
```

## Etapas del pipeline

### Bronze

La capa Bronze recibe los datos directamente desde cada fuente externa, almacenándolos en su formato original sin aplicar transformaciones significativas. Su propósito principal es preservar la información tal como fue obtenida, preservando la trazabilidad y permitiendo su reprocesamiento cuando sea necesario.

### Silver

La capa Silver aplica procesos de limpieza y validación sobre los datos crudos. Se eliminan registros duplicados, se corrigen inconsistencias de formato y se normalizan los esquemas para obtener una representación estructurada y consistente de la información. El resultado es una base consistente para la construcción de métricas analíticas.

### Gold

La capa Gold construye datasets analíticos a partir de los datos limpios. Se realizan agregaciones y transformaciones orientadas al análisis, generando tablas con métricas agregadas y vistas listas para ser utilizadas por el Future Skills Engine y el dashboard.

## Orquestación

Apache Airflow coordina la ejecución del pipeline mediante DAGs (Directed Acyclic Graphs) que definen el flujo de ejecución del pipeline. Existen DAGs independientes para la extracción de cada fuente y para cada capa de procesamiento, permitiendo ejecuciones modulares, reintentos automáticos y monitoreo centralizado del estado del pipeline.
