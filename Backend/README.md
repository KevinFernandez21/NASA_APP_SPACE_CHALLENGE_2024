# Análisis de Eventos Sísmicos algoritmo STA/LTA
Este proyecto contiene scripts para analizar señales sísmicas usando datos del Apollo y archivos `.mseed`.

## Instrucciones para el uso
1. Clona el repositorio.
2. Asegúrate de tener instaladas las siguientes dependencias:
   - numpy
   - pandas
   - obspy
   - matplotlib
   - datetime
   - scipy
   - google-generativeai
   - noisereduce
   - python-dotenv
   - fastapi
   - uvicorn
   - python-multipart
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

La versión 3 del algoritmo incluye varias mejoras clave, aumentando la capacidad de detectar múltiples eventos en una misma señal y refinando aún más el proceso de detección de eventos sísmicos.

1. **Detección de Múltiples Eventos**:
   - Ahora el algoritmo puede manejar múltiples eventos en una misma ejecución, con una lógica más refinada que permite detectar y reportar varios eventos en señales largas.
   - Se ajustó el umbral de detección para evitar falsos positivos y mejorar la precisión.

2. **Mejora en la Visualización**:
   - Se añadieron mejoras a los gráficos generados, resaltando mejor los eventos detectados y proporcionando etiquetas detalladas para los tiempos de inicio y fin de cada evento.
   - La función característica STA/LTA se muestra junto con las detecciones para un análisis más comprensible.

3. **Reporte Detallado de Eventos**:
   - El código ahora reporta cada evento detectado en un formato detallado, mostrando con precisión los tiempos de inicio y finalización de cada evento en segundos.

### Cómo usar la versión 3

1. Ejecuta el notebook `v3_notebook.ipynb` para analizar las señales y detectar múltiples eventos con las nuevas mejoras.
2. Asegúrate de cargar los datos correctamente en la carpeta `/data` y verificar las visualizaciones generadas.


# Algoritmo  v4 

La versión 4 introduce varias mejoras clave para hacer que la detección de eventos sísmicos sea más precisa y estable, independientemente de las variaciones en las amplitudes de la señal.

1. **Normalización de Señales**:
   - Ahora el algoritmo estandariza las trazas de la señal antes de analizarlas, lo que asegura que los eventos detectados no se vean afectados por diferencias en la amplitud de la señal.

2. **Optimización del Proceso de Fusión de Eventos**:
   - Se ha implementado un nuevo parámetro llamado `min_gap`, que define el intervalo de tiempo mínimo entre dos eventos para fusionarlos. Esto mejora la precisión al evitar la fusión de eventos que no están estrechamente relacionados en el tiempo.

3. **Visualización Mejorada con Señales Normalizadas**:
   - Los gráficos ahora utilizan las señales normalizadas, mejorando la claridad de los eventos detectados. Esto hace que la interpretación de los resultados sea más precisa y consistente.

4. **Control de Umbrales STA/LTA**:
   - Se ha afinado el control de los umbrales para la detección de eventos, lo que permite una detección más precisa y confiable.

### Cómo usar la versión 4

1. Ejecuta el notebook `v4_notebook.ipynb` para procesar las señales normalizadas y detectar eventos con los nuevos controles de fusión y umbrales.
2. Asegúrate de tener los datos en el formato correcto y ejecuta el análisis en la carpeta `/data` para visualizar los resultados actualizados.


# Algoritmo  v5

La versión 5 del algoritmo introduce una mejora importante en la evaluación de la precisión de las detecciones al calcular el error absoluto entre los eventos detectados y los tiempos verdaderos de eventos conocidos.

1. **Cálculo del Error Absoluto**:
   - Ahora el código calcula el error absoluto entre el tiempo verdadero del evento y el tiempo detectado, lo que permite medir la precisión del algoritmo de detección.
   
2. **Error Absoluto Promedio**:
   - Se añade el cálculo del error absoluto promedio para todas las detecciones, proporcionando una métrica general de desempeño del algoritmo.

3. **Mejora en el Reporte de Detección**:
   - El reporte de detecciones ahora incluye tanto el tiempo detectado como el error absoluto en segundos, lo que ofrece un análisis detallado del rendimiento del algoritmo en cada evento.

4. **Corrección de Errores**:
   - Asegúrate de inicializar correctamente la variable `merged_on_off` antes de usarla para evitar errores en la ejecución.

### Cómo usar la versión 5

1. Ejecuta el notebook `v5_notebook.ipynb` para analizar los eventos sísmicos y calcular los errores absolutos y promedio en las detecciones.
2. Revisa los resultados generados para comparar la precisión del algoritmo con los tiempos verdaderos de eventos conocidos.



# Algoritmo  v6

La versión 6 del algoritmo introduce la capacidad de generar gráficos y guardarlos en formato de imagen, así como una interfaz interactiva para etiquetar y guardar las señales detectadas.

1. **Generación y Guardado de Gráficas**:
   - Ahora el algoritmo genera gráficos de las señales detectadas y los guarda como archivos `.png`. Se puede ingresar un nombre o número para etiquetar cada gráfica al guardar, facilitando la identificación de las evidencias.

2. **Interfaz Interactiva**:
   - Se ha añadido una función interactiva (`input()`) que permite al usuario ingresar manualmente el nombre o número de la evidencia antes de que la gráfica de cada señal sea guardada. Esto proporciona más flexibilidad en el manejo de diferentes eventos.

3. **Visualización de Señales Detallada**:
   - Cada evento detectado genera un gráfico con un título que indica el número de la señal, y se muestran los tiempos de inicio y fin de cada evento detectado, lo que ayuda a visualizar claramente los segmentos de señal relevantes.

4. **Reporte de Eventos Detectados**:
   - El código sigue mostrando los tiempos de inicio y fin de los eventos detectados, con el formato ya conocido de versiones anteriores.

### Cómo usar la versión 6

1. Ejecuta el notebook `v6_notebook.ipynb` para procesar los eventos sísmicos.
2. Cuando el algoritmo detecte una señal, se generará un gráfico y se solicitará ingresar un nombre o número para guardar el archivo de imagen.
3. Revisa los gráficos generados para analizar los eventos detectados y compararlos visualmente.

# Algoritmo  v7

La versión 7 del algoritmo introduce una visualización más eficiente de los eventos detectados y simplifica el flujo de generación de gráficas.

1. **Visualización de Señales Mejorada**:
   - Cada señal detectada se visualiza automáticamente mediante una gráfica detallada, mostrando los tiempos de inicio y fin de cada evento.

2. **Generación Automática de Gráficas**:
   - Las gráficas se generan y se muestran automáticamente para cada evento detectado. A diferencia de versiones anteriores, no se solicita al usuario que ingrese un nombre de archivo, haciendo que el proceso sea más directo.

3. **Simplificación del Proceso de Visualización**:
   - La interacción del usuario ha sido eliminada y las gráficas se generan de forma automática sin necesidad de guardar archivos de imagen.

4. **Reporte de Eventos Detectados**:
   - El código sigue mostrando los tiempos de inicio y fin de cada evento detectado en consola.

### Cómo usar la versión 7

1. Ejecuta el notebook `v7_notebook.ipynb` para procesar los eventos sísmicos y visualizar automáticamente las gráficas de los eventos detectados.
2. Revisa los gráficos generados para analizar los eventos detectados y los tiempos de los eventos relevantes.



# Algoritmo  v8(final)

La versión 8 del algoritmo implementa **GEMINI**, una mejora significativa para la detección y análisis de eventos sísmicos, enfocada en la validación y filtrado de eventos según criterios de duración mínima.

1. **Implementación de GEMINI**:
   - GEMINI se utiliza para detectar eventos sísmicos con mayor precisión, asegurando que solo los eventos que cumplen con los criterios predefinidos se consideren válidos.

2. **Filtrado por Duración Mínima**:
   - Los eventos detectados se filtran automáticamente según su duración mínima, eliminando aquellos que no cumplen con los requisitos.

3. **Visualización Mejorada**:
   - Los eventos detectados se visualizan claramente en gráficos, con líneas verticales que indican los puntos de activación y desactivación (trigger on y trigger off) en el sismograma.

4. **Reporte Detallado de Eventos**:
   - El código reporta en consola los eventos válidos, mostrando los tiempos de inicio y fin en segundos.

### Cómo usar la versión 8

1. Ejecuta el notebook `v8_notebook.ipynb` para procesar eventos sísmicos utilizando GEMINI.
2. Los eventos detectados se mostrarán automáticamente en gráficos con indicadores de activación y desactivación.
3. Los tiempos de los eventos válidos se mostrarán en consola para un análisis detallado.