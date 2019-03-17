#!/usr/bin/python
#-*- encoding: UTF-8 -*-

import time
start_time = time.time()

import ctypes, sys
import os

ckipws = None

class PyWordSeg(object):
    def __init__(self, Library, inifile):
        self.lib = ctypes.cdll.LoadLibrary(Library)
        self.lib.WordSeg_InitData.restype=ctypes.c_bool
        self.lib.WordSeg_ApplyList.restype=ctypes.c_bool
        self.lib.WordSeg_GetResultBegin.restype=ctypes.c_wchar_p
        self.lib.WordSeg_GetResultNext.restype=ctypes.c_wchar_p
        self.obj = self.lib.WordSeg_New()
        ret = self.lib.WordSeg_InitData(self.obj, inifile.encode('utf-8'))
        if not ret:
            raise IOError("Loading %s failed."%(inifile))

    def EnableLogger(self):
        self.lib.WordSeg_EnableConsoleLogger(self.obj)

    def ApplyList(self, inputList):
        if len(inputList)==0:
            return []
        inArr=(ctypes.c_wchar_p*len(inputList))()
        inArr[:]=inputList
        ret=self.lib.WordSeg_ApplyList(self.obj, len(inputList), inArr)
        if ret==None:
            return []

        outputList=[]
        out=self.lib.WordSeg_GetResultBegin(self.obj)
        while out!=None:
            outputList.append(out)
            out=self.lib.WordSeg_GetResultNext(self.obj)
            
        return outputList

    def Destroy(self):
        self.lib.WordSeg_Destroy(self.obj)

def initial(lib, inifile):
    global ckipws
    ckipws = PyWordSeg(lib, inifile)

def segment(Sent, mode = 0):
    global ckipws
    
    Result = ''
    try:
        oL = ckipws.ApplyList([Sent])
        Result = Result + oL[0]
        del oL
    except:
        pass
    finally:
        if mode == 0:
            WSResult = []
            Result = Result.split()
            for res in Result:
                re = res.strip()
                re = res[0:len(res)-1]
                temp = re.split(u'(')
                word = temp[0]
                pos = temp[1]
                WSResult.append((word,pos))
            # [('蔡英文', 'Nb'), ('是', 'SHI'), ...]
            return WSResult
        else:
            # 蔡英文(Nb)　是(SHI)　中華民國(Nc)...
            return Result


##################################
lib = 'libWordSeg.so'
# 指定 CKIPWS 的設定檔
inifile = 'ws.ini'
# 進行 CKIPWS 初始化的動作
initial(lib, inifile)


sep = ' '  # space as token separator

inputFile  = r'songshu.all.zht.txt'
#outputFile = r'songshu.s001-s010.pos.01.txt'
outputFile = r'songshu.s001-s100.pos.ckip.fixed.broken.passages.02.txt'

fo = open(outputFile, "w", encoding="utf-8", newline="\n")

i = 0
with open(inputFile, "r", encoding="utf-8", newline="\n") as fi:
    for line in fi:
        i += 1
        tok_pos = []
        res = segment(line.strip())
        for word, pos in res:
            if pos in ('name','office','place', 'era', 'ganzhi', 'Nb', 'Nc', 'Nd'):
                # nr=人名, ns=地名, nz=其它专名, t 时间词
                tok_pos.append(f"{word}_{pos}")
            else:
                tok_pos.append(word)
                #tok_pos.append(f"{word}_{pos}")
        fo.write(sep.join(tok_pos)+"\n")
        if i % 250 == 0:
            print(f"processed {i} lines...")
        #if line.startswith('v1p182'): break
fo.close()

elapsed_time = round(time.time() - start_time, 2)
print(f"Elapsed time: {elapsed_time} sec")
print(f"Your segmented file with POS tags is: '{outputFile}'")
