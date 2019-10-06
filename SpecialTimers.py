'''
Created on 29 abr. 2019

@author: Rodrigo
'''
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, Qt

class DelayedCall(QThread):

    uiThreadSignal = QtCore.pyqtSignal()

    def __init__(self, delay, callback, parent=None):
        super().__init__(parent)
        self.uiThreadSignal.connect(callback, Qt.QueuedConnection)
        self.mRunning = True
        self.delay = delay
        self.start()

    def run(self):
        while self.mRunning:
            time.sleep(self.delay)
            self.stop()
            self.uiThreadSignal.emit()
    
    def stop(self):
        self.mRunning = False
       
    def timerThreadCallback(self):
        self.uiThreadSignal.emit()

class LoopTimer(QThread):
    uiThreadSignal = QtCore.pyqtSignal()

    def __init__(self, interval, callbackFn, parent=None):
        super().__init__(parent)
        self.uiThreadSignal.connect(callbackFn, Qt.QueuedConnection)
        self.mRunning = True
        self.interval = interval
        self.start()

    def run(self):
        while self.mRunning:
            time.sleep(self.interval)
            self.uiThreadSignal.emit()                       

    def stop(self):
        self.mRunning = False

class ReseteableTimer(QThread):
    uiThreadSignal = QtCore.pyqtSignal()

    def __init__(self, interval, callbackFn, parent=None):
        super().__init__(parent)
        self.uiThreadSignal.connect(callbackFn, Qt.QueuedConnection)
        self.mRunning = True
        self.tick = 0
        self.interval = interval
        self.sleep_time = self.interval * 10
        self.tick_sleep_time = 0.1
        self.start()

    def run(self):
        while self.mRunning:
            if(self.tick<=self.sleep_time):
                self.tick+=1
                time.sleep(self.tick_sleep_time)
            else:
                self.tick = 0
                self.uiThreadSignal.emit()      

    def stop(self):
        self.mRunning = False
    
    def restart(self):
        self.stop()
        self.tick = 0
        self.mRunning = True

