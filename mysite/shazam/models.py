from django.db import models
from scipy.fftpack import fft
from scipy.io import wavfile
from math import log
from scipy.io import wavfile as wav
import numpy as np
# Create your models here.
class wavFiles(models.Model):
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=80,default=" ")

class musicsamplelibrary(object):
    
    def __init__(self,name,freq,size):
        self.name=name
        self.freq=freq
        self.db={}
        self.size=size
    
        
    def getIndex(self,value,freq):
#         print("At index")
        for j in range(len(freq)):
#             print(j)
            if freq[j][0]<=value and freq[j][1]>=value:
                return j
       
    def getfourpoints(self,chunk,freq,n):
#         print("here")
        result=[0,0,0,0]
        index=0
        value=0
        Fs=44100
        # n = len(datatum) # length of the signal
        k = np.arange(n)
        T = n/Fs
        frq = k/T # two sides frequency range
        frq = frq[:(n//2)] 
        
#         print(chunk)
        for i in range(len(chunk)):
#             print("here also")
            index=self.getIndex(frq[i],freq)
#             print("heretoo")
            value=log(abs(chunk[i])+1)
        if index is not None and result[index]<value:
            result[index]=round(value,0)
#             print("index")
#             print(result)
        return result
        
    
    def addtrack(self,name,track):
        iterations=len(track)//self.size
        chunk=[0]
        tag=-1
        for i in range(iterations):
            if int((i+1)*self.size) > len(track):
                 chunk = fft(track[int((i)*self.size) : len(track)])
                 chunk=chunk[0:len(chunk)//2]
                 
            else:
                 chunk = fft(track[int((i)*self.size) : int((i+1)*self.size)])
                 chunk=chunk[0:len(chunk)//2]
            tf = self.getfourpoints(chunk,self.freq,len(track))
            tag=hash(sum(tf))
            if tag in self.db.keys():
                if name not in self.db[tag]:
                    self.db[tag].append(name)
            else:
                self.db[tag]=[name]
            
        print("inserted in database")
        print(self.db)
