'''
Created on 17 juin 2016

@author: saldenisov
'''
'''
Created on 7 juin 2016

@author: saldenisov
'''

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

import os
from utility import Configuration, remove_nan, MyException, IsnanInput
from xlrd import XLRDError

import pandas as pd
import numpy as np
import clipboard
from scipy import integrate, isnan
from utility import array_correct_template as a_c_t
from utility import background_correct as b_c
import logging
module_logger = logging.getLogger(__name__)

class QYModel:
    """
    Class QYModel is upper level data model
    """

    def __init__(self, app_folder, developing=False):
        self.logger = logging.getLogger("MAIN." + __name__)
        self.app_folder = app_folder
        self.observers = []
        self.data = {}
        self.step_E = None
        self.step_L = None
        self.filter = None
        self.reabsorption = None
        self.QY = None
        self.QY_corrected = None
        self.developing = developing
        self.HeaderLabels = ['Xe', 'Ea', 'Eb', 'Ec', 'Ed',
                             'Xl', 'La', 'Lb', 'Lc',
                             'Xc', 'Yc']
        self.datastatus = 'notfull'
        self.graphnumber = 0
        self.graphnumber_reab = 0

    def set_datastatus(self, status):
        self.datastatus = status
        self.notify_observers_datastatus()

    def set_data(self, file):
        """
        Data is being set from file

        Files extentions: xlx, xlsx
        """
        try:
            a = pd.DataFrame()
            data = pd.read_excel(file)
            self.logger.info('Data file successfully opened')
        except (MyException, XLRDError) as e:
            self.logger.info('Data file opening error')
            self.logger.error(str(e))
            return None
        try:
            """emission arrays"""
            Xe = remove_nan(data['Xe'])
            Ea = remove_nan(data['Ea'])
            Eb = remove_nan(data['Eb'])
            Ec = remove_nan(data['Ec'])

            """excitation arrays"""
            Xl = remove_nan(data['Xl'])
            La = remove_nan(data['La'])
            Lb = remove_nan(data['Lb'])
            Lc = remove_nan(data['Lc'])

            """corrections arrays"""
            try:
                Xc = remove_nan(data['Xc'])
                Yc = remove_nan(data['Yc'])
            except KeyError as e:
                self.logger.info('KeyError: no correction data, trying to open from settings')
                try:
                    path = os.path.join(self.app_folder, 'settings\\corrections.txt')
                    data_cor = pd.read_csv(path, sep='\t')
                    Xc = remove_nan(data_cor['Xc'])
                    Yc = remove_nan(data_cor['Yc'])
                    self.logger.info('Success')
                except (Exception, KeyError, OSError) as e:
                    self.logger.info('Error: problems with settings\\corrections.txt')
                    self.logger.error(str(e))

            """dilute emission array"""
            try:
                Ed = remove_nan(data['Ed'])
                self.data = {'Xe': Xe, 'Xc': Xc,
                             'Xl': Xl, 'Ea': Ea,
                             'Ed': Ed,
                             'Eb': Eb, 'Ec': Ec,
                             'La': La, 'Lb': Lb,
                             'Lc': Lc,  'Yc': Yc}
            except (KeyError, OSError) as e:
                self.logger.info('no dilute emission')
                self.logger.error(str(e))
                self.data = {'Xe': Xe, 'Xc': Xc,
                             'Xl': Xl, 'Ea': Ea,
                             'Eb': Eb, 'Ec': Ec,
                             'La': La, 'Lb': Lb,
                             'Lc': Lc,  'Yc': Yc}

            self.step_E = self.data['Xe'][1]-self.data['Xe'][0]
            self.step_L = self.data['Xl'][1]-self.data['Xl'][0]
            self.notify_observers()
        except (KeyError, OSError, NameError) as e:
            self.logger.info("""Data loading error; Check columns names:
                                Xe, Ea, Eb, Ec, Ed, Xl, La, Lb, Lc, Xc, Yc""")
            self.logger.error(str(e))
            raise MyException

    def set_data_clipboard(self, column):
        s = clipboard.paste()
        s_var = s
        n = s.count('\t', 0, s.find('\n'))
        header = ''
        for i in self.HeaderLabels[column:column+n+1]:
            header += i + '\t'
        header = header[:-1]
        header = header + '\n'
        s = header + s
        clipboard.copy(s)
        try:
            data = pd.read_clipboard()
            for i in data.keys():
                self.data[i] = remove_nan(data[i])
            self.logger.info('Data loading from clipboard successfully')
            self.notify_observers()
        except (MyException, IsnanInput) as e:
            print(e)
            self.logger.info('Data loading error; Check clipboard values')
            self.logger.error(str(e))
        finally:
            clipboard.copy(s_var)
            self.datastatus = self.check_datastatus()
            if self.datastatus == 'full' or self.datastatus == 'partlyfull':
                self.step_E = self.data['Xe'][1]-self.data['Xe'][0]
                self.step_L = self.data['Xl'][1]-self.data['Xl'][0]
                self.notify_observers_datastatus()

    def get_data_clipboard(self, columns):
        """
        Copies data from table columns
        """
        try:
            data = []
            for col in columns:
                data.append(self.data[self.HeaderLabels[col]])

            len_arr = 0
            for arr in data:
                n = len(arr)
                if len_arr < n:
                    len_arr = n
            data_str = ""
            col = 0
            while col < len_arr:
                for i in range(len(data)):
                    try:
                        data_str = data_str + "%.3f" % data[i][col]
                    except IndexError:
                        pass
                    finally:
                        if i != len(data) - 1:
                            data_str = data_str + '\t'
                        if i == len(data) - 1:
                            data_str = data_str + '\n'
                col += 1
            clipboard.copy(data_str)
            #df = pd.DataFrame(data)
            #df.to_clipboard(excel = True)
        except:
            self.logger.info('Nothing was copied')

    def check_datastatus(self):
        status = 'notfull'
        headers = list(self.HeaderLabels)
        headers.remove('Ed')
        for key in headers:
            if key in self.data:
                status = 'full'
            else:
                status = 'notfull'
                break
        if 'Ed' not in self.data and status == 'full':
            status = 'partlyfull'
        return status

    def update_data(self, row, column, value):
        try:
            value_f = float(value)
            if self.HeaderLabels[column] not in self.data:
                self.data[self.HeaderLabels[column]] = np.zeros(row+1)
                self.data[self.HeaderLabels[column]][row] = value_f
                self.table_updated(column)
            else:
                length_ = len(self.data[self.HeaderLabels[column]])
                if row + 1 > length_:
                    extra_ = np.zeros(row + 1 - length_)
                    new_ = np.append(self.data[self.HeaderLabels[column]], extra_)
                    self.data[self.HeaderLabels[column]] = new_
                    self.data[self.HeaderLabels[column]][row] = value_f

                    self.table_updated(column)
                else:
                    self.data[self.HeaderLabels[column]][row] = value_f

            self.logger.info('value in model data dict is updated')
            return True
        except ValueError as e:
            self.logger.info('cannot change cell value; not number')
            self.logger.error(str(e))
            return False

    def delete_data(self, columns=None):
        """
        Remove keys from data dict using table columns numbers
        """
        if not columns:
            self.data = {}

        else:
            for i in columns:
                try:
                    del self.data[self.HeaderLabels[i]]
                except KeyError:
                    self.logger.error('KeyError, no key in data dictionary')
            self.notify_observers()

    def calc_QY(self,
                filter,
                reabsorption,
                check_correct=True,
                check_background=True):
        self.logger.info('QY calculation started:')
        try:
            if check_background:
                Ea = b_c(self.data['Ea'])
                Eb = b_c(self.data['Eb'])
                Ec = b_c(self.data['Ec'])
                La = b_c(self.data['La'])
                Lb = b_c(self.data['Lb'])
                Lc = b_c(self.data['Lc'])
            else:
                Ea = self.data['Ea']
                Eb = self.data['Eb']
                Ec = self.data['Ec']
                La = self.data['La']
                Lb = self.data['Lb']
                Lc = self.data['Lc']

            if check_correct:
                Ea = a_c_t(self.data['Xe'], Ea, self.data['Xc'],
                           self.data['Yc'])
                Eb = a_c_t(self.data['Xe'], Eb, self.data['Xc'],
                           self.data['Yc'])
                Ec = a_c_t(self.data['Xe'], Ec, self.data['Xc'],
                           self.data['Yc'])

            Ea_i = integrate.trapz(Ea, dx=self.step_E)
            Eb_i = integrate.trapz(Eb, dx=self.step_E)
            Ec_i = integrate.trapz(Ec, dx=self.step_E)
            La_i = integrate.trapz(La, dx=self.step_L)
            Lb_i = integrate.trapz(Lb, dx=self.step_L)
            Lc_i = integrate.trapz(Lc, dx=self.step_L)
            self.A = (Lb_i - Lc_i) / Lb_i
            self.filter = filter
            self.reabsorption = reabsorption
            self.QY = ((Ec_i - Ea_i) - (1 - self.A) * (Eb_i - Ea_i)) / (self.A * La_i) * self.filter
            self.calc_QY_corrected()
            self.notify_observers_QY()
            self.logger.info('QY calculation finished successfully')
        except MyException as e:
            self.logger.info('QY calculation finished with error')
            self.logger.error(str(e))

    def calc_QY_corrected(self):
        try:
            self.QY_corrected = self.QY / (self.reabsorption + (1-self.reabsorption) * self.QY)
        except:
            pass

    def draw_graphs(self, columns):
        try:
            f = plt.figure(self.graphnumber)
            plt.xlabel('Wavelengths, nm')
            plt.ylabel('Intensity, a.u.')

            name = columns[0] + ': '
            for column in columns[1:]:
                name += column + ', '
                x = self.data[columns[0]]
                y = self.data[column]

                if len(x) > len(y):
                    y = np.append(y, np.zeros(len(x)-len(y)))
                plt.plot(x, y)

            name = name[:-2]
            f.canvas.set_window_title(name)
            plt.title(name)

            f.show()
            self.graphnumber += 1
        except:
            self.logger.info('No graph could be drawn')

    def draw_reabsorption(self, columns, reabsorption=1):
        try:
            f = plt.figure(self.graphnumber_reab)
            plt.xlabel('Wavelengths, nm')
            plt.ylabel('Intensity, a.u.')

            Xe = self.data['Xe']
            Ec = self.data['Ec']
            Ec = Ec / integrate.trapz(Ec, dx=self.step_E)
            Ed = self.data['Ed']
            Ed = Ed / integrate.trapz(Ed, dx=self.step_E) * reabsorption

            if len(Xe) > len(Ec):
                Ec = np.append(Ec, np.zeros(len(Xe)-len(Ec)))
            if len(Xe) > len(Ed):
                Ed = np.append(Ed, np.zeros(len(Xe)-len(Ed)))

            plt.plot(Xe, Ec)
            plt.plot(Xe, Ed)

            f.canvas.set_window_title('Reabsorption (' + str(reabsorption) + '; Xe: Ec, Ed)')
            plt.title('Xe: Ec, Ed')

            f.show()
            self.graphnumber_reab += 1
            self.logger.info('Reabsorption calculation finished')
        except:
            self.logger.info('No reabsortion graph could be drawn')

    def add_observer(self, inObserver):
        self.observers.append(inObserver)

    def remove_observer(self, inObserver):
        self.observers.remove(inObserver)

    def kill_observes(self):
        for observer in self.observers:
            observer.destroy()

    def table_updated(self, column):
        for x in self.observers:
            x.table_updated(column)

    def notify_observers(self):
        for x in self.observers:
            x.model_is_changed()

    def notify_observers_QY(self):
        for x in self.observers:
            x.QY_is_changed()

    def notify_observers_datastatus(self):
        for x in self.observers:
            x.datastatus_is_changed()
