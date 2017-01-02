'''
Created on 9 juin 2016

@author: saldenisov
'''
import numpy as np
from utility import MyException, WrongArraySizes, IsnanInput


def remove_nan(a):
    try:
        out = np.array([value for value in a if not np.isnan(value)])
        return out
    except TypeError:
        raise IsnanInput


def array_correct_template(var_X, var_Y, correction_X, correction_Y):
    """
    Correct and return var_Y using corrections array
    comparing entries between var_X and
    corretion_X, growing arrays

    >>> X = list(range(1,11))
    >>> Y=list(range(10, 10+len(X)))
    >>> X_c = list(range(5,15))
    >>> Y_c=[2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    >>> array_correct_template(X, Y, X_c, Y_c)
    array([10, 11, 12, 13, 28, 30, 32, 34, 36, 38])
    """
    try:
        varX = np.array(var_X)
        corX = np.array(correction_X)
        varY = np.array(var_Y)
        corY = np.array(correction_Y)

        if varX.size != varY.size or corX.size != corY.size:
            raise WrongArraySizes()

        if (np.abs(var_X[1]-var_X[0])) ==\
                (np.abs(correction_X[1]-correction_X[0])):
            intersec = np.intersect1d(varX, corX)
            if intersec.size != 0:
                first = intersec[0]
                last = intersec[-1]
                from_varX_index = np.where(varX == first)[0][0]
                to_varX_index = np.where(varX == last)[0][0]
                var_indexes = list(range(from_varX_index, to_varX_index+1))

                from_corX_index = np.where(corX == first)[0][0]
                to_corX_index = np.where(corX == last)[0][0]
                cor_indexes = list(range(from_corX_index, to_corX_index+1))

                for i, j in zip(var_indexes, cor_indexes):
                    varY[i] = varY[i] * corY[j]

                return varY

            else:
                return np.array(var_Y)

        else:
            return np.array(var_Y)
    except (MyException, WrongArraySizes) as e:
        print(str(e))
        return np.array(var_Y)


def background_correct(var_Y):
    """
    Correct background of var_Y array

    Finds minimum in var_Y and subtract it
    >>> a = [1, 2, 3, 4, 5, 4, 3, 2.1, 2]
    >>> background_correct(a)
    array([ 0. ,  1. ,  2. ,  3. ,  4. ,  3. ,  2. ,  1.1,  1. ])
    """
    varY = np.array(var_Y)
    varY = varY - np.min(varY)
    return varY
