import time
import RPi.GPIO as GPIO
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt

class GPIOControl(QThread):
    changedValue = QtCore.pyqtSignal(tuple)
    button_conf = { "green":22, "red":27, "blue":17, "up":6, "down": 5}
    button_status = { "green":1, "red":1, "blue":1, "up":1, "down": 1 }
    old_button_status = { "green":1, "red":1, "blue":1, "up":1, "down": 1 }
    delay_shutdown = 60
    countdown = delay_shutdown
        
    def __init__(self, button_conf=None, parent=None):
        super().__init__(parent)
        #Inicializo disccionarios de botones y status
        if button_conf is not None:
            self.button_conf = button_conf
        chan_list = [int(self.button_conf ['green']), int(self.button_conf ['red']), int(self.button_conf ['blue']), int(self.button_conf ['up']), int(self.button_conf ['down'])]        
        button_list = ["green", "red", "blue", "up", "down"]

        #Inicializo GPIO y canales
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(chan_list , GPIO.IN) #, pull_up_down=GPIO.PUD_UP
        
        #Inicializo estatus botones. Primera lectura GPIO
        for button_name, button_gpio_num in self.button_conf.items():
            self.button_status[button_name] = GPIO.input(int(button_gpio_num))
        self.mRunning = True

    
    def run(self):
        while self.mRunning:
            #Guarda el estado anterior de cada boton y refresca su estado. Accion directa de GPIO
            for button_name, button_gpio_num in self.button_conf.items():
                self.old_button_status[button_name] = self.button_status[button_name]
                self.button_status[button_name] = GPIO.input(int(button_gpio_num))    

            #Si se hace la combinacion de botones de apagado, espera el delay_shutdown y apaga
            if( ~self.button_status["red"] & ~self.button_status["blue"] & ~self.button_status["down"] & self.button_status["up"] & self.button_status["green"]):
                self.countdown-=1
                if(self.countdown == 0):
                    self.countdown=self.delay_shutdown 
                    self.changedValue.emit(("ShutDown", 1))               
            else:
                self.countdown=self.delay_shutdown

            #Revisa si el boton cambio su estado anterior. Si es asi, envia un Signal changedValue
            for button_name in self.button_conf.keys():
                if(self.old_button_status[button_name] != self.button_status[button_name]):
                    self.changedValue.emit((button_name, self.button_status[button_name]))    
            
            #Muestrea cada 50ms
            delay = .05                         
            time.sleep(delay)
            
    def stop(self):
        self.mRunning = False
        self.quit()
        self.wait()
        self.deleteLater() 
        GPIO.cleanup()
        print ("GPIO CleanUP")
