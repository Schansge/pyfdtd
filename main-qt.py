import sys, os
os.environ['QT_API'] = 'pyside'
import matplotlib
matplotlib.use('Qt4Agg')
 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
from pyfdtd import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.init_FDTD()
        self.init_gui()

    def init_gui(self):
        self.fig = Figure(figsize=(600,600))
        self.ax = self.fig.add_subplot(111)
        self.setCentralWidget(FigureCanvas(self.fig))

    def init_FDTD(self):
        # source function
        @source
        def f(t):
            x = t - 1000e-12
            return 40.0*math.exp(-x**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*20e9*x)

        # mask functions
        def surface1(x, y):
            if x - 0.02*math.sin(2.0*math.pi*8.0*y) - 0.11 > 0.0:
                return 1.0

            return 0.0

        def surface2(x, y):
            if x - 0.02*math.sin(2.0*math.pi*8.0*y) - 0.09 < 0.0:
                return 1.0

            return 0.0

        # create solver
        self.solver = solver(field(0.2, 0.4, deltaX=0.001))

        # add material
        self.solver.material['electric'][surface1] = material.epsilon(sigma=59.1e6)
        self.solver.material['electric'][surface2] = material.epsilon(sigma=59.1e6)

        # add source
        self.solver.source[masks.ellipse(0.1, 0.05, 5, 0.001)] = f

        # iterate
        self.history = self.solver.solve(1e-9, saveHistory=True)

    def plot(self):
#        ims = []
#        for f in self.history:
#            im = self.ax.imshow(numpy.fabs(f), norm=colors.Normalize(0.0, 10.0))
#            ims.append([im])
#
#        ani = animation.ArtistAnimation(self.fig, ims, interval=50)
        self.ax.imshow(numpy.fabs(self.history[-1]))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.plot()
    window.show()
    sys.exit(app.exec_())