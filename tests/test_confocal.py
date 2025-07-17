from src.Controller.nanodrive import MCLNanoDrive
from src.Controller.adwin import ADwinGold
import pytest
from PyQt5 import QtWidgets
import sys
import pyqtgraph as pg
from src.Model.experiments.confocal import ConfocalScan_Fast, ConfocalScan_Slow, Confocal_Point

'''
This file tests the 3 confocal experiment in confocal.py.
It uses pyqtgraph instead of the typical matplotlib as that is how the experiment _plot methods are setup.
'''
@pytest.fixture()
def get_adwin() -> ADwinGold:
    return ADwinGold()

@pytest.fixture()
def get_nanodrive() -> MCLNanoDrive:
    return MCLNanoDrive(settings={'serial':2849})


@pytest.mark.usefixtures("qtbot")
def test_confocal_fast(get_adwin, get_nanodrive,  qtbot, capsys):
    '''
    This test runs the fast confocal scan. It prints the data and creates a pyqt window
    to display the image data.

    Test passed with successful confocal image generation
    -Dylan Staples 7/17/25
    '''
    nd = get_nanodrive
    adw = get_adwin
    instr = {'nanodrive': {'instance':nd}, 'adwin': {'instance':adw}}

    with capsys.disabled():
        expt = ConfocalScan_Fast(name='confocal_scan_fast',devices=instr)
        expt.run()
        print(expt.data)

        #Asked AI on how to use pytest with pyqtgraph: (Seems to work well)
        # Setup pyqtgraph layout and plot
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        win = pg.GraphicsLayoutWidget()  # main container
        plot_item = win.addPlot()  # pyqtgraph.PlotItem
        qtbot.addWidget(win)  # allow qtbot to manage lifecycle
        # Plot the experiment data
        expt._plot([plot_item])
        pg.QtWidgets.QApplication.processEvents()
        # Optional: display and wait if you're inspecting visually
        with capsys.disabled():
            win.show()
            input("Press Enter to continue...")  # lets you view the window
        win.close()


@pytest.mark.usefixtures("qtbot")
def test_confocal_slow(get_adwin, get_nanodrive,  qtbot, capsys):
    '''
    This test runs the slow confocal scan. It prints the data and creates a pyqt window
    to display the image data. The range is limited so that it executes quickly.

    Test passed with successful confocal image generation
    -Dylan Staples 7/17/25
    '''
    nd = get_nanodrive
    adw = get_adwin
    instr = {'nanodrive': {'instance':nd}, 'adwin': {'instance':adw}}

    with capsys.disabled():
        expt = ConfocalScan_Slow(name='confocal_scan_slow',devices=instr)
        expt.settings['point_a'] = {'x':1,'y':1}
        expt.settings['point_b'] = {'x':3,'y':3}
        expt.settings['resolution'] = 1.0
        expt.run()
        print(expt.data)

        # Setup pyqtgraph layout and plot
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        win = pg.GraphicsLayoutWidget()  # main container
        plot_item = win.addPlot()  # pyqtgraph.PlotItem
        qtbot.addWidget(win)  # allow qtbot to manage lifecycle
        # Plot the experiment data
        expt._plot([plot_item])
        pg.QtWidgets.QApplication.processEvents()
        # Optional: display and wait if you're inspecting visually
        with capsys.disabled():
            win.show()
            input("Press Enter to continue...")  # lets you view the window
        win.close()

@pytest.mark.usefixtures("qtbot")
def test_confocal_point(get_adwin, get_nanodrive,  qtbot, capsys):
    '''
    This test runs the confocal point counting. It prints the data and creates a pyqt window
    to display the data point with a label.

    Test passed with successful
    -Dylan Staples 7/17/25
    '''
    nd = get_nanodrive
    adw = get_adwin
    instr = {'nanodrive': {'instance':nd}, 'adwin': {'instance':adw}}

    with capsys.disabled():
        expt = Confocal_Point(name='confocal_point',devices=instr)
        expt.settings['continuous'] = False
        expt.run()
        print(expt.data)

        # Setup pyqtgraph layout and plot
        app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        win = pg.GraphicsLayoutWidget()  # main container
        plot_item = win.addPlot()  # pyqtgraph.PlotItem
        label_item = pg.LabelItem(justify='left')  # axes_list[1]
        win.addItem(label_item)
        qtbot.addWidget(win)  # allow qtbot to manage lifecycle
        # Plot the experiment data
        expt._plot([plot_item, label_item])
        pg.QtWidgets.QApplication.processEvents()
        # Optional: display and wait if you're inspecting visually
        with capsys.disabled():
            win.show()
            input("Press Enter to continue...")  # lets you view the window
        win.close()