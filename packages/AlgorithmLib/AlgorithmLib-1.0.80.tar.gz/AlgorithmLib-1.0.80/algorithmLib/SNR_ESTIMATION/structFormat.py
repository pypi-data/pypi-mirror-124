# -*- coding: UTF-8 -*-
import sys
sys.path.append('../')
from ctypes import *
import wave
import numpy as np


class emxArray_real_T(Structure):
 _fields_ = [
          ("pdata", POINTER(c_double)),  # c_byte
          ("psize", POINTER(c_int)),  # c_byte
          ("allocSize", c_int),  #  c_byte
          ("NumDimensions", c_int),  # c_byte
          ("canFreeData", c_uint),
]

def get_data_of_ctypes_(inWaveFile=None):
    wavf = wave.open(inWaveFile, 'rb')
    refChannel,refsamWidth,refsamplerate,refframeCount = wavf.getnchannels(),wavf.getsampwidth(),wavf.getframerate(),wavf.getnframes()

    if (refChannel,refsamWidth) != (1,2):
        raise TypeError('Different format of ref and test files!')
    pcmdata = wavf.readframes(refframeCount)

    ref = np.frombuffer(pcmdata,dtype=np.int16)

    ref = ref.astype(np.float64)



    datastruct = emxArray_real_T()

    datastruct.pdata = (c_double * refframeCount)(*ref)
    datastruct.psize = (c_int * 1)(*[refframeCount])
    wavf.close()
    return  datastruct,refsamplerate,refframeCount


# struct emxArray_real_T
# {
#   double *data;
#   int *size;
#   int allocatedSize;
#   int numDimensions;
#   boolean_T canFreeData;
# };
