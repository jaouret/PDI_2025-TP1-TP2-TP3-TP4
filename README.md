# Protocolos de Internet

## Instructivos para el desarrollo de los trabajos prácticos.

### Consideraciones generales

Para el desarrollo de los trabajos cada alumno trabajará en forma individual con su propia computadora o utlizando las computadoras del LIR A, en caso de estar disponibles.
Se asume que los alumnos cuentan con los conocimentos de programación y de redes de comunicación adquiridos en materias previas.
Al final de cada clase utilizaremos Kahoot para fijar algunos conceptos y calificar para el final corto.

### Los trabajos prácticos serán desarrollados utilizando los siguientes lenguajes y herramientas:
- Lenguajes: C, C++, Python.
- IDE: VSC, PyCharm.
- Frameworks: Flask.
- Documentación: Jupyter Notebook.
- Control de versionado y repositorio: Github.
- - Ir al siguiente repositorio: https://github.com/jaouret/PDI_2025-TP1-TP2-TP3-TP4.git

### Sistemas Operativos
- Linux (Se recomienda la distribución Ubuntu 22 o superior, por su simplicidad de uso y disponibilidad de herramientas)
- WSL (Windows Subsystem for Linux - Versión Ubuntu disponible en el Windows Store)
- Mac OS. Tiene Unix Nativo con algunas diferencias a Linux pero se pueden utilizar todos los lenguajes y herramientas descriptas.

#### Importante: no se trabajará sobre el entorno Windows nativo.

Se asume que los alumnos poseen el conocimiento necesario para la instalación del sistema operativo Linux a utlizar. La cátedra puede asistir en este proceso.

## Algunos instructivos.

### Cómo instalar y usar WSL
### Cómo instalar e usar Jupyter Notebook. (Python y C)

**Instalación en Ubuntu (Linux)**
Actualizar el sistema. Abrir terminal y ejecutar:
````
sudo apt update && sudo apt upgrade -y
````

Instalar Python y pip.
Jupyter Notebook requiere Python y pip para su instalación. 
````
sudo apt install python3 python3-pip -y
````
Crear un entorno virtual (opcional).
Para evitar conflictos entre dependencias.
````
python3 -m venv jupyter_env
source jupyter_env/bin/activate
````
Instalar e iniciar Jupyter Notebook.
Con el entorno activado, instalar Jupyter:
````
pip install jupyter
jupyter notebook
````
Jupyter en segundo plano.
````
nohup jupyter notebook > jupyter.log 2>&1 &
````

**Instalación en Windows (WSL - Windows Subsystem for Linux)**
Instalar WSL y Ubuntu
Instalar desde Windows Store o ejecutar en PowerShell como administrador:
````
wsl --install
````
Si WSL está instalado, actualízarlo:
````
wsl --update
````
Abrir Ubuntu en WSL y seguir los pasos de instalación para Ubuntu (ver arriba).

Acceder a Jupyter desde Windows. Después de iniciar Jupyter en WSL con jupyter notebook, aparecerá una URL como:
````
http://localhost:8888/?token=XXXXXXXXXX
````
Copiar y pegar en el navegador de Windows para acceder a Jupyter Notebook.


### Kahoot

### Cómo acceder a los trabajos prácticos











