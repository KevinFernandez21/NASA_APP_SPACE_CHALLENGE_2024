# CosmicQuakes

## Members
● Esleiter Jose Fajardo Laya  
● Aiston Ariel Salazar Vargas  
● Diego Enzo Javier Araujo Ortega  
● Víctor Daniel Borbor Gutiérrez  
● Kevin David Fernandez Sanchez

## Video


## Back-End Installation
### Create a virtual environment called 'env'
```
python -m venv env
```

### Activate the virtual environment
```
env/Scripts/activate
```

### Install dependencies from requierements.txt
````
pip install -r requirements.txt
````

## Front-End Installation
### 
```
cd cosmic-web-page
```

### Install dependencies
```
npm install
```

### Init frontend
```
npm start
```

## STA/LTA Algorithm (Short-Term Average / Long-Term Average)
The STA/LTA algorithm is a technique widely used in seismology for the automatic detection of seismic events. It is based on comparing the average amplitudes in a short-term window (STA) with a long-term window (LTA) to identify abrupt changes in the signal that may indicate the arrival of a seismic event.

### Operation:
STA Calculation: Average of the signal in a short window.
LTA Calculation: Average of the signal in a long window.
STA/LTA Relation: The relation between STA and LTA is calculated .
Event detection: If the STA/LTA relation exceeds the threshold, a possible seismic event is detected.

### Important parameters:
STA/LTA windows size: They are adjusted based on background noise and the signal.
STA/LTA threshold: The value that defines when an event is detected, commonly between 3 and 5.

### Aplications:
Earthquake detection in real time.
Seismic early warning.
Volcanic activity monitoring.
This algorithm is simple, efficient and adapts well to real-time monitoring environments, although is sensitive to noise and requires threshold adjustments.

### Pitch
https://docs.google.com/document/d/1o_0bz3-MW2KJ5bCeEsQu4_z5OBKg2tfOF56gWJRCYOI/edit?usp=sharing

### Research
https://drive.google.com/drive/folders/1DtINUjPLPX3I8YHnhkOQI5IKpdufvh_4?usp=sharing

## Derechos y Licencias

### Datos de la NASA
Este proyecto utiliza datos proporcionados por la **NASA**. Los datos están sujetos a la política de uso de datos de la NASA, que permite su uso siempre que se dé el reconocimiento adecuado. Para más información sobre la política de uso de datos de la NASA, consulta el siguiente enlace:

- [Política de uso de datos de la NASA](https://www.nasa.gov/content/nasa-open-data-policy)

El uso de estos datos no implica un respaldo por parte de la NASA hacia este proyecto o sus autores.

### GEMINI
El algoritmo **GEMINI** utilizado en este proyecto para la detección de eventos sísmicos es software libre y está licenciado bajo la **[Licencia MIT](https://opensource.org/licenses/MIT)** (o la licencia que corresponda, dependiendo de GEMINI). Esto significa que puedes usar, modificar y distribuir GEMINI, siempre que se incluya una copia de la licencia.

### Python
Este proyecto utiliza **Python** para la programación backend, junto con diversas bibliotecas de código abierto (como `numpy`, `pandas`, `matplotlib`, `obspy`, etc.). Python está licenciado bajo la **[Licencia Python Software Foundation (PSF)](https://docs.python.org/3/license.html)**, que permite su libre uso en proyectos comerciales y no comerciales.

### Astro
El frontend de este proyecto utiliza **Astro**, una plataforma para la creación de sitios web estáticos. Astro está licenciado bajo la **[Licencia MIT](https://opensource.org/licenses/MIT)**, permitiendo el uso y modificación del software bajo los términos de esta licencia.

### Disclaimer
Este proyecto es una implementación independiente y no está afiliado ni patrocinado por la NASA ni por ninguna de las organizaciones o herramientas mencionadas.
