# Detección de anomalías en transacciones GMM
# URLs de proyecto
- [Aplicaión](https://gmm-fraud-detector.streamlit.app/)
## Descripción del proyecto.
En sistemas financieros, plataformas de pago y comercio electrónico, se generan grandes volúmenes de transacciones diariamente. Dentro de este flujo masivo de datos, pueden existir transacciones fraudulentas o comportamientos inusuales que representan riesgos económicos y de seguridad.

El problema consiste en identificar automáticamente aquellas transacciones que se desvían del comportamiento normal, sin depender necesariamente de ejemplos previamente etiquetados como fraude.

Este tipo de detección es crítico en escenarios donde:

- El fraude evoluciona constantemente.
- No se cuenta con un historial completo o confiable de casos etiquetados.
- Se requiere detección en tiempo (casi) real.

## Tipo de problema.
Este problema se clasifica como:

- Clustering (agrupamiento):
    Se busca agrupar las transacciones en función de su similitud, identificando patrones de comportamiento.
- Detección de anomalías (Anomaly Detection):
    Se pretende identificar aquellos datos que no encajan bien en ningún grupo o tienen baja probabilidad dentro de la distribución aprendida.
- Aprendizaje no supervisado:
    No se utilizan etiquetas (fraude / no fraude), sino que el modelo aprende la estructura de los datos por sí mismo.

## Enfoque con Gaussian Mixture Models (GMM).
Los Gaussian Mixture Models (GMM) son modelos probabilísticos que asumen que los datos provienen de una combinación de múltiples distribuciones gaussianas.

Idea clave:
Cada grupo de comportamiento "normal" se modela como una distribución gaussiana.
Una transacción será considerada anómala si tiene baja probabilidad de pertenecer a cualquier componente del modelo.

Funcionamiento general:
- Se entrena el modelo GMM sobre los datos históricos.
- El modelo identifica diferentes patrones (clusters).
- Para cada nueva transacción, se calcula su probabilidad de pertenencia.
- Si la probabilidad es muy baja → se marca como anomalía. 

## Seleccion del dataset.
Se hizo la seleccion del dataset en la plataforma de Kaggle ya en esta se encuentran datasets que ya estan listos para usar y que su vez son muy usados en investigacion.

### Ventajas.
- Datos limpios
- Comunidad activa
- Notebooks con ejemplos
- Acceso gratuito
- Portafolios prefesional

### Desventajas.
- Falta de contexto real
- Datos sintéticos o simulados
- Problemas de calidad
- Sobreajuste a benchmarks

Se seleccionó el dataset “Credit Card Fraud” disponible en Kaggle, publicado por Incribo. El conjunto de datos contiene aproximadamente 8,000 registros y cerca de 20 variables relacionadas con transacciones financieras, orientadas al análisis y detección de fraude en tarjetas de crédito.

## ¿Porque este dataset?
La elección de este dataset se realizó debido a que presenta características adecuadas para el desarrollo de un modelo de detección de anomalías mediante Gaussian Mixture Models (GMM) en un entorno de aprendizaje no supervisado.

Las razones fueron las siguientes:
1. Relación directa con el problema de investigación
2. Adecuado para aprendizaje no supervisado
3. Variables útiles para modelado estadístico

# Guía de despliegue-Detección de anomalías en transacciones GMM.

## Plataforma seleccionada: Stream Cloud
Esta plataforma fué seleccionada por ser gratuito, no requiere de enlaces de tarjetas y tiene integración con aplicaciones Streamlit y repositorios de GitHub. No requiere archivos de configuración adicionales como `Procfile` o `Dockerfile`.
### Requistios previos 
Antes de continuar con el despliegue, se debe tener presente:
- Cuenta activa en GitHub.
- Cuenta activa en StreamCloud - se logra enlazar con la cuenta de GitHub.
- Repositorio público.
- Notebook `01_training.ipynb` ejecutando para garantizar la generación de archivos pertenencientes al modelo.
Verificación de que el repositorio tenga la estructura propuesta por la guía propuesta por el profesor:
```
Detección de anomalías en transacciones GMM/
├── requirements.txt        ← obligatorio para que Streamlit instale dependencias
├── app/
│   └── navegation.py             ← archivo principal de la aplicación
└── models/
    ├── modelo_gmm.pkl        ← generado al ejecutar el notebook
    ├── scaler.pkl           ← generado al ejecutar el notebook
```
## Conectar el repositorio a Streamlit Cloud
- Se ingresa a [streamlit.io](https://streamlit.io/cloud).
- Se inicia sesión en la plataforma, lo enlazamos con GitHub y el repositorio.
- Se procede a crear la nueva app en la platforma.
- Se llena el requerido formulario por la plataforma.

```
| Comando | Descripción |
| `Respositorio` | JUANPIS008/Deteccion-de-Anomalias-en-transacciones---GMM |
| `Branch` | main |
| `Main File Path` | app/navegation.py |
| `App URL (opcinal)` | gmm-fraud-detector |
```

Se cerciora que todos los campos esten completos y bien digilenciados y se procede a desplegar la aplicación.
```
| Recurso | URL |
| `Repositorio de GitHub` | [Deteccion-de-Anomalias-en-transacciones---GMM](https://github.com/JUANPIS008/Deteccion-de-Anomalias-en-transacciones---GMM.git) |
| `Aplicaión` | [gmm-fraud-detector](https://gmm-fraud-detector.streamlit.app/) |
```
