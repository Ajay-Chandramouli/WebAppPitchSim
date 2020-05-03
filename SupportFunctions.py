import pandas as pd
import mat4py
import matplotlib.pyplot as plt
import scipy.signal as sc
import numpy as np
#Function to calculate the Power Spectral Density (PSD) of a timeseries.
def CalcPSD(t,timeseries,deltat):
    fFFT = np.fft.rfftfreq(len(t),deltat)
    dfFFT = fFFT[1] - fFFT[0]
    a = abs(np.fft.fft(timeseries)) / len(timeseries)
    PSD = 2 * a ** 2 / dfFFT
    PSD=PSD[:len(fFFT)]
    return fFFT,PSD

#This function is used to create value-label pairs for the dropdown options. Output is a list of value-label pairs.
def create_value_label_for_dropdown(label_list, value_list):
    dictlist = []
    for n, label in enumerate(label_list):
        dictlist.append({'value': value_list[n], 'label': label})
    return dictlist

"""
path = r'C:\\Host Online'
df = mat4py.loadmat(path + '\\'+ 'M000P100_T1_S1_Wsp10.mat')
#path = r'E:\Thesis backup 27 Sep\Thesis\Process results\Ensemble Averages'
#df = mat4py.loadmat(path + '\\'+ 'Ensembled M000P100 T1_S1 Wsp10.mat')
df = pd.DataFrame.from_dict(df['sig'])
#df = pd.DataFrame.from_dict(df['Result1'])
#Cols = open(path + '\\' + 'ColumnNumbers.txt','r').read().splitlines()
#Cols= [int(i)-1 for i in Cols]
#df = df.iloc[:,Cols]
df.columns = open(path + '\\' + 'Headers.txt','r').read().splitlines()
sig = df['NAcx']
#sig = np.sin(4*np.pi*df['Time'])
f,PSD = CalcPSD(df['Time'],sig,0.025)
plt.figure()
plt.semilogy(f,PSD)
#plt.vlines(df['Omega'].mean() * 2 *np.pi/60,PSD.min(),PSD.max())
plt.vlines([1*df['Omega'].mean()/(2*np.pi),2*df['Omega'].mean()/(2*np.pi),3*df['Omega'].mean()/(2*np.pi)],PSD.min(),PSD.max())
plt.xlim([0,1])
plt.grid(True)
plt.show()

ff,PSDS = sc.welch(sig,40,sc.hamming(len(sig)),noverlap=len(sig)/2,return_onesided=True)
#plt.figure()
plt.semilogy(ff,PSDS)
#plt.vlines(df['Omega'].mean() * 2 *np.pi/60,PSD.min(),PSD.max())
plt.vlines([1*df['Omega'].mean()/(2*np.pi),2*df['Omega'].mean()/(2*np.pi),3*df['Omega'].mean()/(2*np.pi)],PSD.min(),PSD.max())
plt.xlim([0,1])
plt.ylabel('Welch')
plt.grid(True)
plt.show()
"""