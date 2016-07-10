# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:21:01 2016

@author: saldenisov
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps

file_name='test-excel.xlsx'
filter_v=0.00538


def remove_nan(a):
    return np.array([value for value in a if not np.isnan(value)])
    
def spectral_correction(a,b,c,d):
    cc = c
    i = 0
    for val in a:
        if val in b:
            index = np.where(b == val)[0]
            cc[i] = cc[i] * d[index]
        i += 1
    return cc

def init(file_name):
    """
    Read data from excel and forms numpy arrays
    """
    try:
        data = pd.read_excel(file_name)
    #Form numpy arrays
    #Emission arrays
        Xe = remove_nan(data['Xe'])
        Ea = remove_nan(data['Ea'])
        Eb = remove_nan(data['Eb'])
        Ec = remove_nan(data['Ec'])
    #Excitation arrays
        Xl = remove_nan(data['Xl'])
        La = remove_nan(data['La'])
        Lb = remove_nan(data['Lb'])
        Lc = remove_nan(data['Lc'])
    #Correction arrays
        Xc = np.array(data['Xc'])
        Yc = np.array(data['Yc'])
        return {'Xe': Xe, 'Xc': Xc, 'Xl': Xl}, {'Ea': Ea, 'Eb': Eb, 'Ec': Ec, 
                'La': La, 'Lb': Lb, 'Lc': Lc,  'Yc': Yc}, data
    except Exception as error:
         print('Error: ', str(error), 'in def init(file_name)')

def main():
        
    command=['init']
    #command=['ymax','max']

    while command[0] != 'quit' and  command[0] != 'q':
        
        if command[0]=='init':
            #File = input('File: ')
            File = 'test-excel.xlsx'
            try:
                ArX, ArY, Data = init(File)
            except Exception as error:
                print('Error: ', str(error), 'in command init')
                
        if command[0] == 'zero_correct':
            if len(command)>1:
                if command[1] == 'all':
                    for key in ArY:
                        ArY[key] = ArY[key]-np.min(ArY[key])
                    print('Zero correction is done for all.')
                        
                if command[1] in ArY:
                    ArY[command[1]] = ArY[command[1]]-np.min(ArY[command[1]])
                    print(command[1]+' is zero corrected')
                    
            else:
                print("""Write what you want to correct. Example: zero_correct all 
                or zero_correct La""")
        
        if command[0] =='spec_corr':
            E=('Ec', 'Eb', 'Ea')
            
            for elem in E:
                ArY[elem] = spectral_correction(ArX['Xe'], ArX['Xc'], ArY[elem], ArY['Yc'])
            print('Spectral correction is done.')
                
        
        if command[0] == 'calc':
            SEa = simps(ArY['Ea'], ArX['Xe'])
            SEb = simps(ArY['Eb'], ArX['Xe'])
            SEc = simps(ArY['Ec'], ArX['Xe'])
            
            SLa = simps(ArY['La'], ArX['Xl'])
            SLb = simps(ArY['Lb'], ArX['Xl'])
            SLc = simps(ArY['Lc'], ArX['Xl'])
            
            A = (SLb-SLc) / SLb
            
            QY = (SEc-SEa-(1-A)*(SEb-SEa)) / (A*SLa) * filter_v
            
            print('QY: ' + str(QY))
        

        if command[0] == 'push_back':
            if len(command)>1:
                if command[1] == 'all':
                    for key in ArY:
                        ArY[key]=remove_nan(Data[key])
                    print('All is pushed back')
                        
                if command[1] in ArY:
                     ArY[command[1]]=remove_nan(Data[command[1]])
                     print(command[1]+' is pushed back')
                    
            else:
                print("""Write what you want to push_back. Example: push_back all 
                or push_back La""")
        
        if command[0] == 'plot':
            if len(command) == 3:
                try:
                    plt.plot(ArX[command[1]], ArY[command[2]])
                    plt.show()
                except:
                    print('Wrong plot command')
                    
            else:
                print('Passed nothing to plot')
                
        
        com = input('Write a command: ')
        com = " ".join(com.split()) 
        command = str.split(com)

if __name__ == '__main__':
    sys.exit(main())