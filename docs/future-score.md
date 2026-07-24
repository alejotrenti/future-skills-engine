# Future Score

## Introducción

El **Future Score** es un puntaje único que asigna Future Skills Engine a cada tecnología analizada. Su propósito es construir un ranking integrado que combine múltiples dimensiones —adopción en la industria, actividad open source e impacto académico— permitiendo comparar tecnologías de manera objetiva sin depender de una única fuente de información.

## Señales utilizadas

El Future Score se construye a partir de tres señales complementarias, cada una proveniente de una fuente distinta:

| Señal | Fuente | Aspecto que mide |
|-------|--------|------------------|
| **Uso y adopción** | Stack Overflow Developer Survey | Frecuencia de uso, popularidad y preferencias declaradas por desarrolladores |
| **Actividad comunitaria** | GitHub REST API | Número de repositorios, estrellas, forks, contribuciones y actividad general en proyectos open source |
| **Investigación** | arXiv API | Volumen de publicaciones académicas y producción científica en áreas tecnológicas específicas |

Cada fuente aporta una perspectiva diferente sobre el ecosistema de una tecnología, permitiendo evaluarla desde ángulos complementarios.

## Construcción del score

El proceso de construcción del Future Score sigue estos pasos conceptuales:

1. **Normalización**: Las métricas provenientes de cada fuente se normalizan para hacerlas comparables entre tecnologías, escalando los valores a un rango común.

2. **Agregación ponderada**: Las señales normalizadas se combinan mediante un modelo de scoring que asigna pesos relativos a cada fuente. La fórmula general es:

```
Conceptualmente, el Future Score se obtiene combinando las señales normalizadas provenientes de las distintas fuentes mediante un modelo de ponderación.

En términos generales:

Future Score = f(Stack Overflow, GitHub, arXiv)

donde *f* representa el proceso de normalización y combinación implementado por el motor de scoring.
```


3. **Ranking**: Los puntajes resultantes se ordenan para generar el ranking final de tecnologías.

## Interpretación

Un Future Score alto indica que una tecnología presenta señales consistentemente positivas en las tres dimensiones analizadas: es ampliamente adoptada por desarrolladores, muestra actividad significativa en open source y genera interés en la comunidad académica. Un puntaje bajo no implica que una tecnología sea deficiente, sino que tiene menor presencia relativa en las fuentes de datos disponibles en comparación con otras tecnologías evaluadas.

## Limitaciones

- El Future Score es un modelo de **scoring**, no un modelo predictivo ni de forecasting.
- No implementa algoritmos de **Machine Learning** ni técnicas de aprendizaje automático.
- Los resultados dependen exclusivamente de la disponibilidad y calidad de las fuentes de datos incorporadas.
- El ranking refleja el estado del ecosistema en el momento del procesamiento, sin proyectar tendencias futuras.

