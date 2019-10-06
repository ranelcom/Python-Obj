# Bug Debounce Buttons
Se cre� un modulo nuevo, basado en *QThreads*, GPIOControl.py, el que consta de 1 clase base que reemplaza el uso de *RPi.Gpio* manual, dado que la integra y genera un nivel de abstracci�n que permite manejar eficientemente los rebotes de todos los botones, generando un mensaje tipo *pyqtSignal*. Es una clase no-bloqueante ya que corre en una hebra separada y en *background*.

El constructor inicia con una configuraci�n por defecto de ubicaci�n de los botones, pero si estos se llegaran a modificar, se deben modificar en *config.ini*

El mensaje env�a una tupla consistente en el bot�n y si fue presionado o no. Peri�dicamente, cada 50ms, se revisa si se genero un cambio de estado. S�lo env�a mensaje frente a 2 situaciones:
* Cambio de estado del boton ON-OFF u OFF-ON.
* Presi�n simultanea de la combinaci�n de botones de apagado seguro(RED + BLUE + DOWN) durante al menos 3 segundos.

## loader.py
Nuevo script que permite cargar cualquier script *python3* como subproceso de manera que frente a una excepci�n no controlada, vuelve a cargar el subproceso.
Ej.

```bash
sudo ./loader.py Timetracker.py
```

## Sincronizacion del RTC por script
Dado que el RTC DS3231 que posee la placa interfaz dise�ada para el proyecto IOTTTM, fue considerada interfaz I2C, facilmente se puede comunicar y obtener o grabar una fecha en el RTC usando el script *rtc.py*. El uso es el siguiente por consola:

Para leer la fecha del RTC, en formato Chileno d/m/a H:M:S, por ejemplo.

```bash
pi@ttm000:~/timetracking $ python3 rtc.py
21/8/2019 1:15:39
 ```

Si la necesitamos en formato norteamericano, agregamos el argumento US:

```bash
pi@ttm000:~/timetracking $ python3 rtc.py US
8/21/2019 1:15:39
 ```

Para escribir la fecha al RTC, es muy importante ingresar la fecha en el formato 'dd/mm/aa h:m:s' manteniendo las comillas. Por ejemplo si queremos fijar el 21 de agosto del 2019 a las 11:15:00 escribiremos:

```bash
pi@ttm000:~/timetracking $ python3 rtc.py '21/8/2019 11:15:00'
 ```

Adicionalmente se escribieron dos scripts bash para traspasar la hora del sistema al RTC, y del RTC al sistema.

Para traspasar la hora del sistema al RTC usamos el script *sincro_date_to_rtc.sh*:

```bash
pi@ttm000:~/timetracking $ ./sincro_date_to_rtc.sh 
21/08/2019 13:58:45
 ```

Y la opcion inversa, para traspasar la hora del RTC al sistema usamos como superusuario el script *sincro_rtc_to_date.sh*:

```bash
pi@ttm000:~/timetracking $ sudo ./sincro_rtc_to_date.sh 
8/21/2019 14:1:8
Wed Aug 21 14:01:08 -04 2019
 ```


## Sincronizacion del RTC directo en Raspbian
Como el RTC DS3231 que posee la placa interfaz dise�ada para el proyecto IOTTTM, fue considerada interfaz I2C, es muy f�cil integrar el RTC en el S.O. tan solo agregando una linea a /boot/config.txt

```
dtoverlay=i2c-rtc,ds3231
```

Una vez agregada al final del archivo esa linea, es necesario realizar un reboot y posteriormente a eso se podr�n usar los siguientes comandos:

Para leer el reloj de tiempo real

```
sudo hwclock -r
```

Para modificar la hora del sistema.

```
sudo date -s "2019/08/19 15:00"
```

Para escribir la hora del sistema en el reloj de tiempo real. Es importante entender que la opcion de escribir toma la hora del sistema y la graba en el reloj de tiempo real. 

```
sudo hwclock -w
```

Para obtener ayuda de mas comandos del reloj de tiempo real

```
sudo hwclock -h
```

# Bug Timetracking QTimer
Se creo un modulo nuevo, basado en QThreads, SpecialTimers.py el que consta de 3 clases que reemplazan la clase QTimer que genera errores si es iniciada en una hebra y terminada en otra. Estas nuevas clases controla con se�ales las hebras correspondientes mejorando el manejo.

Tambi�n se modifico el constructor de las clases para dejar la ruta del "parent" y de esa manera evitar que se destruyera un objeto activo.
## LoopTimer
Esta clase recibe una un timeout en segundos y una funci�n callback, la que sera llamada peri�dicamente si no se invoca el m�todo **stop** y **quit**.

## ReseteableTimer
Esta clase es similar a LoopTimer, recibe los mismos par�metros y cuenta con un m�todo adicional **restart** que reinicia el conteo e impide llamar a la funcion callback. Util para el modo "screen saver"

## DelayedCall
Id�ntica a LoopTimer, con la diferencia que se ejecuta una �nica vez.

### Bugs futuros a tratar
* Manejo de botones. El manejo actual no considera el debounce real de un bot�n, sino que el tiempo que dura su presi�n. Por este motivo hay ocasiones en que da la impresi�n que los botones no fueron presionados y hay que presionarlos 2 veces ya que queda memorizada su presi�n, pero no su liberaci�n.
* Control de temperatura por ventilador. Se definir� en config.ini una temperatura m�nima y m�xima de operaci�n para definir una histeresis.
