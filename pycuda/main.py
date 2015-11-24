#!/usr/bin/env python

import numpy

import pycuda.autoinit
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

# getting information about device

device = pycuda.autoinit.device
giga = 1073741824.0
print "Model: {0}".format(device.name())
print "Memory: {:.03} (in GigaBytes)".format(device.total_memory() / giga)

a = numpy.random.randn(4,4)
a = a.astype(numpy.float32) # if we need to work with single precision
# simple a
print a

mod = SourceModule("""
  __global__ void doublify(float *a)
  {
    int idx = threadIdx.x + threadIdx.y*4;
    a[idx] *= 2;
  }
  """)

a_gpu = cuda.mem_alloc(a.nbytes)
cuda.memcpy_htod(a_gpu, a) # transfer data to nvidia device
    
func = mod.get_function("doublify")
func(a_gpu, block=(4,4,1))

a_doubled = numpy.empty_like(a)
cuda.memcpy_dtoh(a_doubled, a_gpu)

# doubled a
print a_doubled
