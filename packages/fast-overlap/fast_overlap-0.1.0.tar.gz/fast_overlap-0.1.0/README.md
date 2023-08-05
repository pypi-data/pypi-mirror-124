# Fast Overlap

A tiny cython library to calculate the pairwise overlap of all cell
masks between two time points. Created for use in https://github.com/Hekstra-Lab/microutil/

## Install

```
pip install fast-overlap
```


## Development

### Installation
```
python setup.py build_ext -i
```

To really remove stuff and build + test:
```
rm *.so build/ fast_overlap.cpp -rf && python setup.py build_ext -i && python test_speedup.py
```
