# COSMICQUAKES - NASA APP SPACE CHALLENGUE
![Descripción de la imagen](./image/file.jpg)

## Video
[![Watch the video](https://img.youtube.com/vi/Qt17XqvM73Y/hqdefault.jpg)](https://www.youtube.com/watch?v=Qt17XqvM73Y)

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

#### Operation:
STA Calculation: Average of the signal in a short window.
LTA Calculation: Average of the signal in a long window.
STA/LTA Relation: The relation between STA and LTA is calculated .
Event detection: If the STA/LTA relation exceeds the threshold, a possible seismic event is detected.

### Code Integration and Versioning
[Seismic Events Analysis STA/LTA algorithm](./Backend/README.md)


## Rights and Licenses

### NASA Data
This project uses data provided by **NASA**. The data is subject to NASA's data user policy, which permits its use as long as proper attribution is given. For more information about NASA's data use policy, please see the following link:

- [NASA Data Use Policy]([https://www.nasa.gov/content/nasa-open-data-policy](https://www.nasa.gov/wp-content/uploads/2021/12/nasa-ocs-public-access-plan-may-2023.pdf))

The use of these data does not imply support from NASA for this project or its authors.

### GEMINI
The **GEMINI** algorithm used in this project for the detection of seismic events is free software and is licensed under the **[MIT license](https://opensource.org/licenses/MIT)**. This means that you may use, modify, and distribute GEMINI as long as a copy of the license is included.

### Python
This project uses **Python** for backend programming, along with various open-source libraries (such as `numpy`, `pandas`, `matplotlib`, `obspy`, etc.). Python is licensed under the **[Python Software Foundation License (PSF)](https://docs.python.org/3/license.html)**, which allows its free use in commercial and non-commercial projects.

### Astro
The frontend of this project uses **Astro**, a platform for the creation of static websites. Astro is licensed under the **[MIT License](https://opensource.org/licenses/MIT)**, allowing the use and modification of the software under the terms of this license.

### Cloud Run
The deployment of this project is managed through **Google Cloud Run**, a serverless platform for deploying containerized applications. Cloud Run allows the deployment of highly scalable web applications and APIs without managing the underlying infrastructure. For more information on Cloud Run's terms and services, please see the following link:

- [Google Cloud Run](https://cloud.google.com/run)
## Disclaimer
This project is an independent implementation and is not affiliated with or sponsored by NASA or any of the organizations or technologies mentioned.
