# CosmicQuakes
## Members
● Esleiter Jose Fajardo Laya  
● Aiston Ariel Salazar Vargas  
● Diego Enzo Javier Araujo Ortega  
● Víctor Daniel Borbor Gutiérrez  
● Kevin David Fernandez Sanchez


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

##Algoritmo STA/LTA (Short-Term Average / Long-Term Average)
El algoritmo STA/LTA es una técnica ampliamente utilizada en sismología para la detección automática de eventos sísmicos. Se basa en comparar el promedio de amplitudes en una ventana de corto plazo (STA) con una ventana de largo plazo (LTA) para identificar cambios abruptos en la señal que pueden indicar la llegada de un evento sísmico.

###Funcionamiento:
Cálculo de STA: Promedio de la señal en una ventana corta.
Cálculo de LTA: Promedio de la señal en una ventana larga.
Relación STA/LTA: Se calcula la relación entre STA y LTA.
Detección de eventos: Si la relación STA/LTA excede un umbral, se detecta un posible evento sísmico.

###Parámetros importantes:
Tamaño de ventanas STA/LTA: Se ajustan según el ruido de fondo y la señal.
Umbral STA/LTA: Valor que define cuándo se detecta un evento, comúnmente entre 3 y 5.

###Aplicaciones:
Detección de terremotos en tiempo real.
Alerta sísmica temprana.
Monitorización de actividad volcánica.
Este algoritmo es simple, eficiente y se adapta bien a entornos de monitoreo en tiempo real, aunque es sensible al ruido y requiere ajuste de umbrales.

### Pitch
https://docs.google.com/document/d/1o_0bz3-MW2KJ5bCeEsQu4_z5OBKg2tfOF56gWJRCYOI/edit?usp=sharing

### Research
https://drive.google.com/drive/folders/1DtINUjPLPX3I8YHnhkOQI5IKpdufvh_4?usp=sharing