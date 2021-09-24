from collections import deque

import pyqtgraph as pg
import numpy as np
from scipy.optimize import curve_fit

class TimepixSetupHistogram():

    def __init__(self, plt, label_left, label_bottom, units):
        self.plt = plt
        self.plot_data_item = self.__setup_hist_ui(label_left, label_bottom, units)
        self.snapshot_plot_data_item = self.__add_plot_data_item()
        self.plot_curve_item = self.__setup_gaussian_fit_ui()
        # self.__setup_text_items()
        self.__setup_legend()

        self.buffer = None

    def __add_plot_data_item(self):
        plot_data_item = pg.PlotDataItem()
        self.plt.addItem(plot_data_item)
        return plot_data_item

    def __setup_hist_ui(self, label_left, label_bottom, units):
        plot_data_item = self.__add_plot_data_item()
        self.plt.setLabel('bottom', text=label_bottom, units=units)
        self.plt.setLabel('left', text=label_left)
        return plot_data_item

    def __setup_gaussian_fit_ui(self):
        plot_curve_item = pg.PlotCurveItem()
        self.plt.addItem(plot_curve_item)
        return plot_curve_item

    def __setup_legend(self):
        legend = self.plt.getPlotItem().addLegend(offset=(-5, 5))
        style = pg.PlotDataItem(pen='k')
        legend.addItem(style, '')
        self.legend_label_fwhm = legend.getLabel(style)
        # legend_label_fwhm.setText('Something else')
        style = pg.PlotDataItem(pen='k')
        legend.addItem(style, '')
        self.legend_label_standard_deviation = legend.getLabel(style)

        style = pg.PlotDataItem(pen='k')
        legend.addItem(style, '')
        self.legend_label_rms = legend.getLabel(style)

    def init_buffer(self, number_packets):
        self.buffer = deque(maxlen=number_packets)

    def clear_buffer(self):
        if self.buffer is not None:
            self.buffer.clear()

    def snapshot(self, tot_bins):
        y, x = np.histogram([], tot_bins)
        # TODO: Fix this to be transparent and change the color to something other than blue
        # TODO: Display in addition: number of entries, mean of distribution, for 2d hist (mean and RMS) in x and y, 
        # TODO: Rename the snapshot button to reference
        # TODO: add curves to legend
        self.snapshot_plot_data_item.setData(x, sum(self.buffer), stepMode='center', fillLevel=0, brush=(255, 0, 0, 75))
        

    def refresh(self, tot, tot_bins):
        y, x = np.histogram(tot, tot_bins)
        self.buffer.append(y)
        y = sum(self.buffer)
        self.plot_data_item.setData(x, y, stepMode='center', fillLevel=0, brush=(0, 0, 255, 255))

        index = y.argmax()
        y_max = y.max()
        while y[index] > y_max / 2:
            index += 1

        sigma_0 = (x[index] - x[y.argmax()]) * 2
        popt, pcov = curve_fit(
            TimepixSetupHistogram.__gauss_fwhm, x[:-1], y, p0=[y_max, x[y.argmax()], sigma_0]
        )
        A, mu, fwhm = popt
        self.legend_label_fwhm.setText(f'FWHM: {fwhm:.2f}')
        self.legend_label_standard_deviation.setText(f'std.: {np.std(y) / len(self.buffer):.2f}')
        self.legend_label_rms.setText(f'RMS: {np.sqrt(np.mean(np.square(y))) / len(self.buffer):.2f}')
        self.plot_curve_item.setData(x, TimepixSetupHistogram.__gauss_fwhm(x, *popt))

    @staticmethod
    def __gauss_fwhm(x, *p):
        A, mu, fwhm = p
        return A * np.exp(-((x - mu) ** 2) / (2.0 * (fwhm ** 2) / (4 * 2 * np.log(2))))