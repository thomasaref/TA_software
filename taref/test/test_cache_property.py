# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:10:35 2016

@author: thomasaref
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

#img=mpimg.imread(r'/Users/thomasaref/Dropbox/crypto.png')
img=mpimg.imread("/Users/thomasaref/Downloads/IMG_0881.jpg")
#img.transpose()
img=np.swapaxes(img, 0, 1)
img=img[:,::-1,:]
img=img[645:1450, :,0]
print img
plt.plot([x for x in np.diff([n for n, i in enumerate(img[100, :]) if i<100]) if x>1], 'o')
plt.plot([x for x in np.diff([n for n, i in enumerate(img[-100, :]) if i<100]) if x>1], 'o')

#plt.plot(np.diff(img[-100, :]))
#plt.ylim(40,100)
plt.figure()
#plt.hist(img.ravel(), bins=256) #, range=(0.0, 1.0), fc='k', ec='k')
plt.imshow(img, cmap="spectral", clim=(40,100))
plt.colorbar()
plt.show()

class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """  # noqa

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value

class Test(object):

    @cached_property
    def a(self):
        return 3

a=Test()

print dir(a)

print a.__dict__

print a.a

a.a=2
print a.a
print a.__dict__, a.__class__.a

del a.__class__.a

print a.__dict__

print a.a
