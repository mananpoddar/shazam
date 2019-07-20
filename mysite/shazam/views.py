from django.shortcuts import render
from scipy.io import wavfile
from math import log
from scipy.fftpack import fft
from scipy.io import wavfile as wav
import numpy as np
import sounddevice as sd
import numpy as np
# import pyaudio
# duration = 5  # seconds
# fs=44100
# # Create your views here.
# objct = wavFiles.objects.all()

# bins = [[40, 80], [80, 120], [120, 180], [180, 300]]
# name = "tumsehi"
# db = musicsamplelibrary("Samplelibrary", bins, 1024)
# #misc functions



def index(request):
    if request.method == 'POST':
        # print(data1)
        wavFile = request.FILES.get('wavFile')
        ratetumcheck,datatumcheck=wav.read(wavFile)#user is inputting this wav file

        # duration = 5  # seconds
        # fs=44100
        # sd.default.samplerate = fs
        # sd.default.channels = 1
        # myarray = sd.rec(int(duration * fs),blocking=True)
        # print("RECORDING AUDIO")
        # print(myarray)
        # print("AUDIO RECODING COMPLETE ")
        # sd.play(myarray, fs)
        # sd.wait()
        # print("PLAYING COMPELETE")
        # # ratetumcheck, datatumcheck = wav.read('./shazamData/uptown0010.wav')
        # # ratetumcheck1, datatumcheck1 = wav.read('./shazamData/uptownextranoise.wav')
        # # ratetumcheck1, datatumcheck2 = wav.read('./shazamData/tumsehirandomnoise.wav')
        # datatumcheck = myarray
        # from scipy.io.wavfile import write

        # data = myarray # 44100 random samples between -1 and 1
        # scaled = np.int16(data/np.max(np.abs(data)) * 32767)
        # write('test.wav', 44100,scaled )
        # ratetumcheck,datatumcheck=wav.read('test.wav')#user is inputting this wav file


        temp_set = check(datatumcheck[:,0], db.db, bins)
        # check(datatumcheck1, db.db, bins)
        # check(datatumcheck2, db.db, bins)


        # global duration,fs
        # print("post is there")    
        # sd.default.samplerate = fs
        # sd.default.channels = 2
        # myarray = sd.rec(int(duration * fs),blocking=True)
        # print(myarray)
        # sd.play(myarray, fs)
        # sd.wait()
        # print("PLAYING COMPELETE")
        

        
      

        # wavFile = request.FILES.get('wavFile')



        # ratetumcheck,datatumcheck=wav.read(wavFile)#user is inputting this wav file
        # # datatumcheck = myarray[:,0]
        # datatumcheck = datatumcheck[:,0]
        # print(datatumcheck)
        # #check track
        # # ratesup,dataup=wav.read(wavFile) #2nd wav file in database
        # # if type(datatumcheck[0])!=int:
        # #         datatumcheck=datatumcheck[:,0]
        # temp_set = check(datatumcheck,db.db,bins)
        #     # dataup=dataup[:,0]
        
        # # db.addtrack("uptown",dataup)
        # #calling the main check function
        return render(request,"shazam/result.html",{"temp_set":temp_set})

    return render(request,"shazam/index.html")




ratetum, datatum = wav.read('./shazamData/tumsehisample10.wav')  # add track
ratetum1, datatum1 = wav.read('./shazamData/tumsehi1020.wav')  # add track
ratetum2, datatum2 = wav.read('./shazamData/tumsehi2030.wav')  # add track
ratetum3, datatum3 = wav.read('./shazamData/tumsehi3040.wav')  # add track
ratetum4, datatum4 = wav.read('./shazamData/tumsehi4050.wav')  # add track
ratetum5, datatum5 = wav.read('./shazamData/tumsehi5060.wav')  # add track

rateup1, dataup1 = wav.read('./shazamData/uptown0010.wav')  # add track
rateup2, dataup2 = wav.read('./shazamData/uptown1020.wav')  # add track
rateup3, dataup3 = wav.read('./shazamData/uptown2030.wav')  # add track
rateup4, dataup4 = wav.read('./shazamData/uptown3040.wav')  # add track
rateup5, dataup5 = wav.read('./shazamData/uptown4050.wav')  # add track
rateup6, dataup6 = wav.read('./shazamData/uptown5060.wav')  # add track


# check track
# ratesup, dataup = wav.read('./shazamData/uptownsample.wav')

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
       
    def getfourpoints(self,chunk,freq):
#         print("here")
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
            tf = self.getfourpoints(chunk,self.freq)
            tag=hash(sum(tf))
            if tag in self.db.keys():
#                 if name not in self.db[tag]:
                self.db[tag].append(name)
            else:
                self.db[tag]=[name]
            
        print("inserted in database")
#         print(self.db)

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
    
def most_frequent(List): 
    dict = {} 
    count, itm = 0, '' 
    for item in reversed(List): 
        dict[item] = dict.get(item, 0) + 1
        if dict[item] >= count : 
            count, itm = dict[item], item 
    return(itm) 
  
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
#             if tag not in existingtags:
              count=count+1
              existingtags.append(tag)
        for ia in library[tag]:
              tag_list.append(ia)
      
    print("TAG LIST")
#     print(tag_list)
    print("COUNT")
    print(count)
#     print("count")
#     print(count)
    if count>=240:    
#         temp_set=tag_list[0].intersection(tag_list[1])
#         for i in range(2,len(tag_list)):
#             temp_set=temp_set.intersection(tag_list[i])
        print("MATCH FOUND")
        return most_frequent(tag_list)
    else:
        print("MATCH NOT FOUND")
        return "Match Not Found"
        
bins = [[40, 80], [80, 120], [120, 180], [180, 300]]
name = "tumsehi"
db = musicsamplelibrary("Samplelibrary", bins, 1024)
# if type(datatum[0])!=int:
print(datatum)
datatum=datatum[:,0]
datatum1 = datatum1[:, 0]
datatum2 = datatum2[:, 0]
datatum3 = datatum3[:, 0]
datatum4 = datatum4[:, 0]
dataup1 = dataup1[:, 0]
dataup2 = dataup2[:, 0]
dataup3 = dataup3[:, 0]
dataup4 = dataup4[:, 0]
dataup5 = dataup5[:, 0]
dataup6 = dataup6[:, 0]
  
#     dataup=dataup[:,0]

db.addtrack("tumsehi", datatum)
db.addtrack("tumsehi", datatum1)
db.addtrack("tumsehi", datatum2)
db.addtrack("tumsehi", datatum3)
db.addtrack("tumsehi", datatum4)
# db.addtrack("uptown", dataup)

db.addtrack("uptown", dataup1)
db.addtrack("uptown", dataup2)
db.addtrack("uptown", dataup3)
db.addtrack("uptown", dataup4)
db.addtrack("uptown", dataup5)
db.addtrack("uptown", dataup6)


