import svar
import numpy

m=svar.load('/data/zhaoyong/Desktop/svar_buffer/build/libsvar_buffer.so')
m3d=m.Matrix3d([1,2,3,4,5,6,7,8,9])
a=numpy.frombuffer(m3d)

print(a.strides,a.shape)

print(m3d,m3d.__buffer__().__str__())

mem=memoryview(a)

m3d1=m.Matrix3d(mem)

print(m3d1)
