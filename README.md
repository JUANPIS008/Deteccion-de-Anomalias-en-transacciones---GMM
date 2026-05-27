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

## Definicion de variables
 La aplicación web utilizará features relacionados con el comportamiento financiero del usuario y las características de la transacción.

 1. Monto de la transacción
    Representa el valor monetario de la transacción realizada.

    Tipo de dato: Float

    Importancia: El monto es uno de los indicadores más importantes en detección de fraude, ya que las transacciones fraudulentas suelen presentar:
    - Valores inusualmente altos.
    - Compras fuera del patrón habitual.
    - Cambios bruscos en el comportamiento financiero.

2. Hora de la transacción
    Corresponde a la hora exacta en que se realiza la transacción.

    Tipo de dato: Integer

    Importancia: Los usuarios suelen tener patrones horarios repetitivos, las transacciones realizadas en horarios inusuales pueden indicar fraude.

3. Ubicación
    Representa la ubicación geográfica desde donde se realiza la transacción.

    Tipo de dato: String

    Importancia: Permite identificar
    - Cambios inesperados de ubicación.
    - Compras en regiones no habituales.
    - Accesos sospechosos.

4. Tipo de comercio
    Categoría del establecimiento donde se realiza la compra.

    Tipo de dato: String

    Importancia: Los usuarios suelen comprar en categorías similares. Cambios repentinos pueden representar comportamiento anómalo.

5. Método de pago
    Indica el medio utilizado para realizar la transacción:

    - Crédito.
    - Débito.
    - Transferencia.
    - Billetera digital.

    Tipo de dato: String

    Importancia: Cambios inesperados en el método de pago pueden indicar actividad sospechosa.

6. Dispositivo utilizado
    Tipo de dispositivo desde el cual se realiza la operación:

    - Móvil,
    - Computador,
    - Tablet.

    Tipo de dato: String

    Importancia: Permite detectar
    - Accesos desde dispositivos no habituales.
    - Cambios inesperados de comportamiento.