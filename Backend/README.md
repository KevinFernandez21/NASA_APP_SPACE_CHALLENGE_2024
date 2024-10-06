# Análisis de Eventos Sísmicos algoritmo STA/LTA
Este proyecto contiene scripts para analizar señales sísmicas usando datos del Apollo y archivos `.mseed`.

## Instrucciones para el uso
1. Clona el repositorio.
2. Asegúrate de tener instaladas las siguientes dependencias:
   - numpy
   - pandas
   - obspy
   - matplotlib
   - scipy
3. Organiza los datos en la carpeta `/data`.
4. Ejecuta el análisis desde el notebook o los scripts de Python.

## Ejecución
Abre el notebook en `/notebooks/v1_notebook.ipynb` para ver los pasos detallados de cómo procesar los datos de señales.


# Algoritmo  v2
La versión 2 del algoritmo introduce varias mejoras clave para la detección de eventos sísmicos, las cuales optimizan tanto el rendimiento como la precisión del análisis:

1. **Optimización del Filtrado de Eventos**:
   - Ahora los eventos detectados son filtrados y fusionados con mayor precisión para evitar la detección de eventos espurios o falsos positivos.
   - Se han añadido condiciones para evitar la fusión de eventos no relacionados y mejorar el análisis de las señales.

2. **Mejor Gestión de Eventos Detectados**:
   - El código ha sido reestructurado para realizar un recorrido más eficiente de los eventos detectados. Ahora, la detección es más rápida y precisa, con un mejor manejo de los tiempos de inicio y fin de cada evento.

3. **Visualización Mejorada**:
   - La visualización gráfica de los eventos ha sido optimizada para que sea más clara y fácil de interpretar. Las áreas de detección ahora se resaltan con mayor precisión, y se muestran etiquetas con los tiempos exactos de inicio y finalización de los eventos.

4. **Reporte Detallado de Eventos**:
   - El reporte de los eventos detectados incluye una mejor precisión numérica para los tiempos de detección, proporcionando resultados más exactos en el análisis de la señal.

### Cómo usar la versión 2

1. Ejecuta el notebook `v2_notebook.ipynb` para procesar las señales y ver los eventos detectados con las nuevas mejoras.
2. Asegúrate de seguir la estructura del proyecto para cargar los datos correctamente y visualizar los resultados con las nuevas optimizaciones.


# Algoritmo  v3



# Algoritmo  v4 



# Algoritmo  v5



# Algoritmo  v6



# Algoritmo  v7



# Algoritmo  v8
