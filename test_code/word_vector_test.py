# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 12:40:18 2016

@author: thomasaref
"""
import codecs
import numpy

def build_word_vector_matrix(vector_file, n_words):
        '''Iterate over the GloVe array read from sys.argv[1] and return its vectors and labels as arrays'''
        numpy_arrays = []
        labels_array = []
        with codecs.open(vector_file, 'r', 'utf-8') as f:
                for c, r in enumerate(f):
                    if c!=0:
                        sr = r.split()
                        labels_array.append(sr[0])
                        numpy_arrays.append([float(i) for i in sr[1:]])
                        print len(sr[1:])

                        if c == n_words:
                                return numpy.array( numpy_arrays ), labels_array

        return numpy.array( numpy_arrays ), labels_array
        
if __name__=="__main__":
    a, b=build_word_vector_matrix("/Users/thomasaref/Downloads/5maa", 800)
    print a.dtype
    print type(a), a.shape
    a.reshape(800, 200)