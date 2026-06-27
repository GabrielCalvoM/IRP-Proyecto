# IRP-Proyecto

## Estructura

### Interfaz

No implementado aún

### Reconocedor

Para el reconocedor, se implementaron los siguientes scripts:

> - preprocesado.py: transforma la imagen para poder ser procesada por el detector YOLO, ajustando el tamaño y margen de la misma.
> - detector.py: contiene las funciones necesarias para poder identificar, clasificar y filtrar los objetos detectados por el modelo YOLO.
> - main.py: contiene el flujo de prueba para el detector YOLO con las imágenes seleccionadas.

También se tienen los siguientes subdirectorios para el reconocedor:

> - modelos: contiene los modelos entrenados de YOLO para el reconocedeor de vehículos.
> - tests: contiene todas las imágenes que utiliza el flujo de pruebas del detector.
> - boxes: almacena las imágenes con las cajas delimitando los objetos procesados de la imagen correspondiente.

### Tracking

Para el seguimiento, se implementaron los siguientes scripts:

> - seguidor.py: implementa ByteTrack para relacionar los ids de las cajas entre fotogramas de un video.
> - contador.py: utiliza las detecciones del seguidor para obtener la cantidadd de vehículos que transitan en una carretera.
