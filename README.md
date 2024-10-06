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