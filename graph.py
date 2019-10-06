# from: https://doc.qt.io/qt-5/qtcharts-nesteddonuts-example.html
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from estadisticas import Estadisticas
from logger import Logger

LOG_LEVEL = Logger.LOG_LEVEL_INFO

class Stats(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.logger = Logger(self.__class__.__name__).get()
        self.logger.handlers[0].setLevel(LOG_LEVEL)
        self.logger.info('Loading ' + self.__class__.__name__)
        self.setMinimumSize(800, 600)

        self.m_donuts = []

        self.chartView = QChartView()
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chart = self.chartView.chart()
        self.chart.legend().setVisible(True)
        self.chart.setTitle("Time Tracking System")
        self.chart.setAnimationOptions(QChart.AllAnimations)

        minSize = 0
        maxSize = 0.7
        
        donut = QPieSeries()
        
        e = Estadisticas()
        data = dict(e.getData())

        for key, value in data.items():
            #print('key :', key, 'Value :',   value)
            slice_ = QPieSlice('{}:({})'.format(key,  value), value)
            slice_.setLabelPosition(QPieSlice.LabelOutside)
            slice_.setLabelArmLengthFactor(0.3)
            slice_.setLabelVisible(True)
            slice_.setLabelColor(Qt.red)
            #slice_.setLabelPosition(QPieSlice.LabelInsideTangential)
            donut.append(slice_)
            donut.setHoleSize(minSize )
            donut.setPieSize(minSize + (maxSize - minSize) )

        self.chartView.chart().addSeries(donut)

        # create main layout
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addWidget(self.chartView, 1, 1)
        self.chartView.show()
        self.setLayout(self.mainLayout)

