import SpecialTimers
import threading
from PyQt5.QtWidgets import QMessageBox ,  QDesktopWidget
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from logger import Logger

LOG_LEVEL = Logger.LOG_LEVEL_INFO

class TimerMessageBox(QMessageBox):

    def __init__(self, parent = None, *__args):
        #QMessageBox.__init__(self)
        super().__init__(parent, *__args)
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.handlers[0].setLevel(LOG_LEVEL)
        self.logger.info('Loading ' + self.__class__.__name__)
        self.timeout = 0
        self.autoclose = True
        self.currentTime = 0
        self.logger.info('TimerMessageBox(): {}'.format(threading.currentThread()))

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.timerMB = SpecialTimers.LoopTimer(1, self.timerEvent)
            #self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.timerMB.stop()
            self.timerMB.quit()
            a = QPropertyAnimation(self, "windowOpacity".encode()) #also  b"opacity"
            a.setDuration(350)
            a.setStartValue(1)
            a.setEndValue(0)
            a.setEasingCurve(QEasingCurve.OutQuad)#QEasingCurve::OutBack
            a.start()
            self.done(0)
            
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
        
    @staticmethod
    def showWithTimeout(timeoutSeconds, message, title, icon=QMessageBox.Information, buttons=QMessageBox.NoButton):
        w = TimerMessageBox()
        w.logger.info('showWithTimeout(): {}'.format(threading.currentThread()))
        w.autoclose = True
        w.timeout = timeoutSeconds
        w.setStyleSheet("background:yellow")
        myfont = QFont("Sans Serif", 24, QFont.Bold)
        w.setFont(myfont )
        w.setText(message)
        w.setWindowTitle(title)
        w.setWindowFlags(QtCore.Qt.Popup)
#        w.setStandardButtons(QMessageBox.NoButton)
        w.setIcon(icon)
        w.setStandardButtons(buttons)
#        w.move(w.rect().center())
        w.center()
        w.exec_()
