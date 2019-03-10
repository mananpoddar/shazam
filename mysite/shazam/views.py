from django.shortcuts import render
from shazam.models import musicsamplelibrary

from scipy.io import wavfile
from math import log
from scipy.fftpack import fft
from scipy.io import wavfile as wav
import numpy as np
# Create your views here.

#misc functions


def getIndex(value, lst):
    for j in range(len(lst)):
        if lst[j][0] <= value and lst[j][1] >= value:
            return j
def getfourpoints(chunk,freq):
#     print("here")
    result=[0,0,0,0]
    index=0
    value=0
    Fs=44100
    n = len(datatum) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[:(n//2)] 
        
#         print(chunk)
    for i in range(len(chunk)):
#             print("here also")
        index=getIndex(frq[i],freq)
#             print("heretoo")
        value=log(abs(chunk[i])+1)
    if index is not None and result[index]<value:
        result[index]=round(value,0)
#     print("index")
#     print(result)
    return result
    

def check(inp, library, freq):
    size = 1024
    iterations = len(inp)//size
    matches = {}
    tag_list=[]
    existingtags=[]
    count=0
    tag=-1
    for i in range(iterations):
        if int((i+1)* size) > len(inp):
            cmatch = fft(inp[int(i*size) : len(inp)])
            cmatch = bit[0:len(bit)//2]
        else:
            cmatch = fft(inp[int(i*size) : int((i+1)*size)])
            cmatch = cmatch[0:len(cmatch)//2]
        tf = (getfourpoints(cmatch, freq))
        tag=hash(sum(tf))
#         print("ajhdku")
#         print(tag)
        if tag in library.keys():
#             print("i am here")
            if tag not in existingtags:
                count=count+1
                existingtags.append(tag)
                tag_list.append(set(library[tag]))
#     print("count")
#     print(count)
    if count>=3:
        temp_set=tag_list[0].intersection(tag_list[1])
        for i in range(2,len(tag_list)):
            temp_set=temp_set.intersection(tag_list[i])
        print("MATCH FOUND")
        print(temp_set)
    else:
        print("MATCH NOT FOUND")
        


def index(request):
    if request.method == 'POST':
        print("post is there")    
        wavFile = request.FILES.get('wavFile')
        
        ratetum, datatum = wav.read(wavFile)#1st file in database

        ratetumcheck,datatumcheck=wav.read(wavFile)#user is inputting this wav file
        #check track
        ratesup,dataup=wav.read(wavFile) #2nd wav file in database

        bins = [[40, 80], [80, 120], [120, 180], [180, 300]]
        name = "tumsehi"
        db = musicsamplelibrary("Samplelibrary", bins, 1024)
        if type(datatum[0])!=int:
        #     print("i am here")
            datatum=datatum[:,0]
            dataup=dataup[:,0]

        db.addtrack("tumsehi", datatum)
        db.addtrack("uptown",dataup)
        #calling the main check function
        check(datatumcheck,db.db,bins)

    return render(request,"shazam/index.html")


