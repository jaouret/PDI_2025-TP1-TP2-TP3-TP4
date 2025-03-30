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

### Cómo instalar y usar WSL.
### Cómo instalar e usar Jupyter Notebook. (Python y C).
### Cómo usar un entorno gráfico en WSL.

**Instalación en Ubuntu (Linux)(en MacOS es similar, Python se instala con [brew install python]**
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

### Como usar C/C++ en Jupyter
**Usar el kernel de C con xeus-cling**
Este método permite ejecutar código C directamente en celdas de Jupyter.
Instalar dependencias
Abrir una terminal y ejecutar:
````
pip install jupyter
conda install -c conda-forge xeus-cling
````
Iniciar Jupyter Notebook
````
jupyter notebook
````
Crear un nuevo notebook con el kernel de C
En Jupyter Notebook, hacer clic en New
Seleccionar C++17 (Cling)
Escribir y ejecutar código en C, por ejemplo:
````c
#include <stdio.h>

int main() {
    printf("Hola, Jupyter en C!\n");
    return 0;
}
````
Nota: xeus-cling está optimizado para C++, pero se puede ejecutar código en C con algunas adaptaciones.

**Usar %%bash para compilar y ejecutar código C**
Si no se instala un kernel adicional, se puede usar %%bash para ejecutar comandos de compilación en celdas de Jupyter.
Compilar y ejecutar código en una celda
````c
%%bash
echo '#include <stdio.h>
int main() {
    printf("Hola, Jupyter desde C!\n");
    return 0;
}' > programa.c
````
````
gcc programa.c -o programa
./programa
````
Escribir y ejecutar código en múltiples celdas
Celda 1: Crear el código fuente
````c
%%writefile programa.c
#include <stdio.h>
int main() {
    printf("Hola desde Jupyter en C!\n");
    return 0;
}
````
Compilar el programa
````
!gcc programa.c -o programa
````
Ejecutar el programa
````
!./programa
````

**Breves conceptos para usar Jupyter**

Tipos de Celdas
````
Código: Ejecuta código en Python u otros lenguajes compatibles.
Markdown: Permite escribir texto con formato, ecuaciones (LaTeX), enlaces e imágenes.
````

Uso de tecla combinadas (shortcuts)
````
Shift + Enter → Ejecuta la celda y pasa a la siguiente.
Ctrl + Enter → Ejecuta la celda sin moverse.
Esc + A → Agrega una celda arriba.
Esc + B → Agrega una celda abajo.
Esc + M → Convierte la celda a Markdown.
Esc + Y → Convierte la celda a Código.
````
Ejecutar Código en Partes
````
Dividir el código en celdas pequeñas para ejecutar por partes sin reiniciar todo.
Usar %%time para medir el tiempo de ejecución de una celda.
````
Importar Bibliotecas
Ejemplo con NumPy y Pandas:
````
import numpy as np
import pandas as pd
````
Graficar en Jupyter
Usar matplotlib para gráficos:
````
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.show()
````
Cargar Datos
Para leer un archivo CSV:
````
df = pd.read_csv("archivo.csv")
df.head()
````
Guardar y Cerrar
````
Guardar: Ctrl + S
````
Descargar Notebook: 
````
Archivo → Descargar como → .ipynb o .py
````
Cerrar:
````
Kernel → Restart & Clear Output y luego cerrar la pestaña.
````

**Instalar un entorno gráfico (opcional)**

En Windows 11, Microsoft ha integrado WSLg (Windows Subsystem for Linux GUI), lo que permite ejecutar aplicaciones gráficas sin necesidad de configuraciones adicionales. Elegir GNOME, XFCE o KDE.
````
sudo apt update && sudo apt install xfce4 -y
startxfce4
sudo apt install firefox -y
firefox
````
Se abrirá Firefox en Windows con WSLg desde WSL.

Para escritorio completo como GNOME:
````
sudo apt install ubuntu-desktop -y
````

### Kahoot!

- Crear una Cuenta en Kahoot
- Abrir https://kahoot.com en el navegador.
- Abrir https://kahoot.it en celulares o instalar app.
- Ingresar el PIN de juego y apellido/nombre. El PIN del juego se indicará en cada clase.
- Una vez que todos estén ingresados iniciamos el juego.
- La pregunta aparece en la pantalla del profesor.
- Los alumnos seleccionan respuestas desde su celular.
-- Se tiene en cuenta la velocidad de respuesta para el puntaje.
- Después de cada pregunta, Kahoot muestra quién va ganando.
- Al final, se muestra un podio con los mejores puntajes.

### Cómo acceder a los trabajos prácticos

Ir a: https://github.com/jaouret/PDI_2025-TP1-TP2-TP3-TP4.git










