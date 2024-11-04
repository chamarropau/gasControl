## Interfaz Gráfica de Usuario (GUI) en PyQt5

Al seleccionar el modo de ejecución **GUI**, se despliega una aplicación desarrollada en PyQt5 que permite una gestión visual e interactiva del sistema. La interfaz está organizada en varias secciones funcionales, cada una dedicada a configurar diferentes aspectos del sistema de control y automatización.

![image](https://github.com/user-attachments/assets/6f023621-4c96-4785-a63b-453606cdf0d8)




#### Área de Visualización

La sección superior de la ventana presenta el **Área de Visualización**, donde se muestran los resultados y datos en tiempo real generados por el sistema. Este espacio central permite al usuario monitorear el estado del software y cualquier información relevante en el proceso de análisis de gases.

#### Modo Manual

En la parte inferior izquierda se encuentra la sección **Manual Mode**, destinada a la configuración y control manual de los dispositivos y parámetros del sistema. Incluye las siguientes opciones:

- **Enable Manual Mode**: Activando esta casilla, el usuario habilita el modo manual, lo que permite personalizar cada uno de los parámetros de forma independiente.
- **Measurement Time, Acquisition Time, Saving Time**: Estas entradas permiten configurar los tiempos de medición, adquisición y almacenamiento, expresados en minutos, para controlar la duración de cada operación.
- **MFCs (Mass Flow Controllers)**: Cada controlador de flujo de masa (MFC3, MFC6, MFC9, MFC12, MFC16, MFC20) tiene un campo de entrada para ajustar manualmente su flujo específico. Esta configuración es útil para personalizar las tasas de flujo en experimentos que requieren valores precisos.
- **Electrical Type**: Al hacer clic en este botón, se despliega un cuadro de diálogo (*QtDialog*) que permite al usuario especificar el tipo de configuración eléctrica para los experimentos, proporcionando una capa adicional de personalización. La funcionalidad exacta de este diálogo se describirá en secciones posteriores.

<div align="center">
    <img src="https://github.com/user-attachments/assets/9daa15d5-55a9-4fd9-921a-2969766863e8" alt="image">
</div>

<br>

Al hacer clic en el botón **Electrical Type** en el **Modo Manual**, se despliega un cuadro de diálogo (*QtDialog*) que permite seleccionar el tipo de medición eléctrica que se utilizará en el sistema. Este diálogo presenta seis opciones de medición, cada una con sus propios campos configurables para adaptarse a diferentes tipos de análisis. A continuación se describe cada opción en detalle:

<div align="center">
    <img src="https://github.com/user-attachments/assets/61cc2c31-5521-486f-972f-c796a5be2031" alt="image">
</div>
<br>

- **ManualIV**: Configuración manual para mediciones de corriente en función del voltaje (I-V). Al seleccionar esta opción, el usuario puede ingresar el **voltaje** deseado y elegir la **unidad** adecuada (mV, µV, o V) según los requerimientos de precisión del experimento.

<div align="center">
    <img src="https://github.com/user-attachments/assets/84001481-efe8-4d18-a495-f58fa3792923" alt="image">
</div>
<br>

- **ManualVI**: Configuración manual para mediciones de voltaje en función de la corriente (V-I). En esta modalidad, el usuario introduce la **intensidad** deseada y selecciona la **unidad** correspondiente (mA, µA, o A).
<div align="center">
    <img src="https://github.com/user-attachments/assets/3896612a-36f3-477f-94d0-581aa330268f" alt="image">
</div>
<br>

- **AutomaticIV**: Configuración automática para mediciones de corriente en función del voltaje (I-V) en un rango específico. Esta opción permite especificar un **voltaje inicial** y un **voltaje final**, así como la **unidad** (mV, µV, o V). Además, el usuario puede definir el número de **steps** (pasos) en los que se dividirá el rango, permitiendo una medición continua y precisa.
<div align="center">
    <img src="https://github.com/user-attachments/assets/bc7d6da4-7275-45c6-a044-8db6025c448d" alt="image">
</div>
<br>

- **AutomaticVI**: Configuración automática para mediciones de voltaje en función de la corriente (V-I) en un rango determinado. Similar a *AutomaticIV*, esta opción requiere ingresar una **intensidad inicial** y una **intensidad final**, junto con la **unidad** (mA, µA, o A) y el número de **steps** para realizar las mediciones en intervalos específicos.
<div align="center">
    <img src="https://github.com/user-attachments/assets/8c285163-6088-41a6-b674-038eb5fd5b92" alt="image">
</div>
<br>

- **AutomaticIT**: Configuración automática para mediciones de corriente en función del tiempo (I-T). Al elegir esta opción, el usuario introduce un **voltaje** y selecciona la **unidad** correspondiente. Este tipo de medición es útil para estudios donde la corriente varía con el tiempo bajo un voltaje constante.
<div align="center">
    <img src="https://github.com/user-attachments/assets/036cccb4-c252-4578-a9d8-426f1c157a60" alt="image">
</div>
<br>

- **AutomaticVT**: Configuración automática para mediciones de voltaje en función del tiempo (V-T). En esta modalidad, el usuario puede ingresar la **intensidad** y seleccionar la **unidad** (mA, µA, o A), permitiendo analizar el comportamiento del voltaje a lo largo del tiempo bajo una corriente constante.
<div align="center">
    <img src="https://github.com/user-attachments/assets/cf43288c-0400-4fc0-9308-c5be6eefb96d" alt="image">
</div>
<br>

Este cuadro de diálogo es dinámico y ajusta sus campos de entrada según la opción seleccionada, proporcionando una interfaz intuitiva y eficiente para los distintos tipos de medición eléctrica.



#### Modo Automático

A la derecha del Modo Manual, se encuentra la sección **Automatic Mode**, diseñada para configuraciones automáticas mediante la importación de datos externos. Las opciones en esta sección incluyen:

- **Enable Automatic Mode**: Esta casilla habilita el modo automático, permitiendo que el sistema configure y ejecute automáticamente según los datos especificados.
- **Import Excel**: Un botón que permite cargar un archivo Excel con los parámetros de control y medición previamente definidos. Este método es ideal para realizar experimentos o procesos repetitivos sin necesidad de ingresar manualmente cada valor.
- **Sheet Name**: Un campo de entrada donde el usuario debe especificar el nombre de la hoja dentro del archivo Excel que contiene los datos a importar.

<div align="center">
    <img src="https://github.com/user-attachments/assets/9dcbf182-81c8-4c4a-829d-258b42d94221" alt="image">
</div>
<br>

#### Selección de Keithley

En la parte inferior central, el usuario puede seleccionar entre **One Keithley** o **Two Keithley**. Esta opción define si se usará uno o dos dispositivos Keithley para la medición, lo cual puede influir en la precisión y el tipo de datos recopilados durante la ejecución del programa.

#### Botón de Ejecución

Finalmente, en la parte inferior de la ventana se encuentra el botón **RUN**. Al presionarlo, se inicia el flujo principal del programa con los parámetros seleccionados, ya sea en modo manual o automático, y con una o dos Keithleys según la configuración.
