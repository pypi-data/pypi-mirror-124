# distutils: language=c++

import numpy as np

cimport cython
cimport numpy as np

__all__ = [
    "__version__",
    "overlap",
    "overlap_parallel",
]
cimport numpy as np


cdef extern from "parallel_overlap.cpp":
    cdef void overlap_parallel_cpp(int *, int *, Py_ssize_t[2], int *, Py_ssize_t) nogil

@cython.wraparound(False)
@cython.nonecheck(False)
cpdef overlap_parallel(int [:,::1] prev, int[:,::1] curr, shape):
    prev = np.ascontiguousarray(prev)
    curr = np.ascontiguousarray(curr)

    cdef np.ndarray[int, ndim=2, mode="c"] output = np.zeros(shape, dtype=np.dtype("i"))
    cdef Py_ssize_t ncols = shape[1]

    with nogil:
        overlap_parallel_cpp(&prev[0,0], &curr[0,0], prev.shape, &output[0,0], ncols)
    return output


# @cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cpdef overlap(int[:, :] prev, int[:,:] curr, shape):
    """
    Calculate the pairwise overlap the labels for two arrays.

    Parameters
    ----------
    prev, curr : 2D array-like of int
        curr will have at least as many unique labels as prev

    Returns
    -------
    arr : (N, M) array of int
        N is the number of unique labels in prev and M the number of unique in curr.
        The ijth entry in the array gives the number of pixels for which label *i* in prev
        overlaps with *j* in curr.
    """
    prev = np.ascontiguousarray(prev)
    curr = np.ascontiguousarray(curr)
    cdef int [:, :] arr
    arr = np.zeros(shape, dtype=np.dtype("i"))
    cdef size_t I, J, i, j
    for i in range(prev.shape[0]):
        for j in range(prev.shape[1]):
            p = prev[i,j]
            c = curr[i,j]
            if p and c:
                arr[p, c] += 1
    return np.asarray(arr)
