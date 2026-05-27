# Detecci-n-de-Anomal-as-en-transacciones---GMM

## Descripcion del proyecto
En sistemas financieros, plataformas de pago y comercio electrónico, se generan grandes volúmenes de transacciones diariamente. Dentro de este flujo masivo de datos, pueden existir transacciones fraudulentas o comportamientos inusuales que representan riesgos económicos y de seguridad.

El problema consiste en identificar automáticamente aquellas transacciones que se desvían del comportamiento normal, sin depender necesariamente de ejemplos previamente etiquetados como fraude.

Este tipo de detección es crítico en escenarios donde:

- El fraude evoluciona constantemente.
- No se cuenta con un historial completo o confiable de casos etiquetados.
- Se requiere detección en tiempo (casi) real.

## Tipo de problema
Este problema se clasifica como:

- Clustering (agrupamiento):
    Se busca agrupar las transacciones en función de su similitud, identificando patrones de comportamiento.
- Detección de anomalías (Anomaly Detection):
    Se pretende identificar aquellos datos que no encajan bien en ningún grupo o tienen baja probabilidad dentro de la distribución aprendida.
- Aprendizaje no supervisado:
    No se utilizan etiquetas (fraude / no fraude), sino que el modelo aprende la estructura de los datos por sí mismo.

## Enfoque con Gaussian Mixture Models (GMM)
Los Gaussian Mixture Models (GMM) son modelos probabilísticos que asumen que los datos provienen de una combinación de múltiples distribuciones gaussianas.

Idea clave:
Cada grupo de comportamiento "normal" se modela como una distribución gaussiana.
Una transacción será considerada anómala si tiene baja probabilidad de pertenecer a cualquier componente del modelo.

Funcionamiento general:
- Se entrena el modelo GMM sobre los datos históricos.
- El modelo identifica diferentes patrones (clusters).
- Para cada nueva transacción, se calcula su probabilidad de pertenencia.
- Si la probabilidad es muy baja → se marca como anomalía. 

## Seleccion del dataset
Se hizo la seleccion del dataset en la plataforma de Kaggle ya en esta se encuentran datasets que ya estan listos para usar y que su vez son muy usados en investigacion.

### Ventajas
- Datos limpios
- Comunidad activa
- Notebooks con ejemplos
- Acceso gratuito
- Portafolios prefesional

### Desventajas
- Falta de contexto real
- Datos sintéticos o simulados
- Problemas de calidad
- Sobreajuste a benchmarks

Se seleccionó el dataset “Credit Card Fraud” disponible en Kaggle, publicado por Incribo. El conjunto de datos contiene aproximadamente 8,000 registros y cerca de 20 variables relacionadas con transacciones financieras, orientadas al análisis y detección de fraude en tarjetas de crédito.

## Porque este dataset?
La elección de este dataset se realizó debido a que presenta características adecuadas para el desarrollo de un modelo de detección de anomalías mediante Gaussian Mixture Models (GMM) en un entorno de aprendizaje no supervisado.

Las razones fueron las siguientes:
1. Relación directa con el problema de investigación
2. Adecuado para aprendizaje no supervisado
3. Variables útiles para modelado estadístico




# Selección y justificación del servicio de despliegue en la nube

## Contexto de la decisión
Para el despliegue de esta aplicación la cuál esta basada en la detección de anomalías bancarias con GMM, se hizo un breve estudio e investigación sobre las seis plataformas referenciadas en los lineamentos de la actividad propuesta por el profesor; dichas plataformas son las siguientes: Cloud, Render, Heroku, Google Cloud Run, AWS, Streamlit y Azure. El equipo se basó en tres criterios principales: costo cero sin la necesidad anclar una tarjeta de crédito, compatibilidad directa con el stack tecnólogico del proyecto (Streamlit + scikit-learn), y sinmplicidad de configuración para un equipo de desarrollo universitario.

# Servicio Principal-Streamlit Cloud
## ¿Qué es?
Streamlit Cloud es una plataforma de despliegue administrada y gratuita, fué creada por los mismo desarrolladore del framework Streamlit. Su diseño es basado especificamente para el alojamiento de aplicaciones construidas con esta libreria, esto favorece la compatibilidad entre el entorno de desarrollo y el entorno de producción.
## ¿Cómo funciona?
Streamlit Cloud se logra conectar directamente a un repositorio público en GitHub. En el momento en el cuál se configura el despliegue, la plataforma leerá el archivo requirements.txt del repositorio, este instala automáticamente todas las dependencias necesarias en un entorno virtual aislado, levantando la aplicación enfocándose en el archivo principal indicado.
Cada vez que se realiza un nuevo git push **git push** a la rama principal, la plataforma detectará el cambio y redespliega la aplicación de manera automática sin intervención manual. 
## ¿Cómo se usa en este proyecto?
## Justificación de elección
Se eligió Stream Cloud como plataforma principal debido que como equipo tuvimos en cuenta el hecho de que es gratuita y no requiere anclar niguna tarjeta para poder obtener sus servicios, a diferencia de de AWS, Azure y Google Cloud Platform plataformas las cuáles exigen tarjeta para poder usar los tier gratuitos. Al estar diseñada exclusivamente para apliaciones Streamlit, no requiere de un archivo de configuración adicional como lo es Procfile (Heroku) o Dockerfile (Google Cloud Platform), reduciendo así la complejidad operativa. La integración nativa con GitHub permite que se pueda mantener un flujo de trabajo continuo donde cada mejora que se le haga al código se verá reflejado automáticamente. 