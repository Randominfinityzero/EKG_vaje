import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.signal import butter, lfilter



#(Markovič Rene, vrstica 39)
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

#(Markovič Rene, vrstica 40)
def local_max_R(y):
    N=600
    res=[]
    for i in range(N,len(y)-N):
        a1=True
        a2=True
        for ii in range(1,N,1):
            if y[i]<y[i-ii]:
                a1=False
            if y[i]<y[i+ii]:
                a2=False
        if a1 and a2:
            if len(res)>0:
                if ((i-res[len(res)-1][0])>10):
                    res.append([i,y[i]])
            else:
                res.append([i,y[i]])
    return(res)
def local_max_RS(y,res):
    RS=[]
    for i in res:
        ii=1
        S=1
        while S:
            cm=i[0]-ii
            cp=i[0]+ii
            if np.all(y[cp]<y[cp-30:cp-1]) and np.all(y[cp]<y[cp+1:cp+30]) and S:
            #if y[cp]<y[cp-1] and y[cp]<y[cp-2] and y[cp]<y[cp-3] and y[cp]<y[cp+1] and y[cp]<y[cp+2] and y[cp]<y[cp+3] and S:
                St=cp
                S=0
            ii+=1
        ii=1
        RS.append([i[0],St])
    return(np.array(RS,dtype=int).T)


t=np.linspace(0, 120, num=1000, endpoint=True)
y1=0.1*np.sin(2*np.pi/400.0*t)
ft=np.array([0.02*(2.0*random.random()-1) for i in range(len(y1))])
#print(f)
y2=0.1*np.sin(2*np.pi/10.0*t)+ft
y2[y2<0]*=abs(0.2*np.sin(2*np.pi/40.0*t[y2<0]))
plt.figure(figsize=(16,6))
k = butter_bandpass_filter(y1, 1.0, 10.0, 1000, order=1)
l = butter_bandpass_filter(y2, 1.0, 10.0, 1000, order=1)
plt.plot(t,y1+y2)
#y1 zgladi navzdol. Če je to težava, samo menjati k z y1 spodaj. Ne vem zakaj nastane zamik pri glajenju
maks=local_max_R(y1)
RS=local_max_RS(k+l,maks)
plt.plot(t,k+l)
plt.show()
print("Maksimumi in minimumi: ", maks, RS.shape)


#Viri:
"""Markovič Rene,  https://anaconda.org/rene_markovic/ecg/notebook"""