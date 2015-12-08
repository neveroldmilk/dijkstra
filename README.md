# dijkstra

## description
Implementing Dijkstra algorithm in python in sequential form
and using CUDA environment (with pycuda).

## Work with python sequential
You can run the following commands:
```
$ cd dijkstra/python
$ pip install -r requirements.txt
$ python src/main.py
```

## Work with pyCUDA
You need a `GPU device`, `Boost C++` libraries and `numpy` module. To start,
run the following commands:

```
$ sudo apt-get install libboost-all-dev -y
$ sudo apt-get install python-numpy -y
$ sudo apt-get install build-essential python-dev python-setuptools libboost-python-dev libboost-thread-dev -y
```
Now download pyCUDA from pypi. We are using pyCUDA version **2015.1.3**,
Ubuntu version is **14.04** and CUDA version is **7.5**.

```
$ VERSION=2015.1.3
$ wget https://pypi.python.org/packages/source/p/pycuda/pycuda-$VERSION.tar.gz
$ tar xvzf pycuda-$VERSION.tar.gz; cd pycuda-$VERSION
$ ./configure.py --cuda-root=/usr/local/cuda \\
  --cudadrv-lib-dir=/usr/lib/x86_64-linux-gnu \\
  --boost-inc-dir=/usr/include \\
  --boost-lib-dir=/usr/lib \\
  --boost-python-libname=boost_python \\
  --boost-thread-libname=boost_thread \\
  --no-use-shipped-boost
$ make [-j 4]
$ sudo python setup.py install
```

Instructions were retrieved from [pyCUDA Wiki](http://wiki.tiker.net/PyCuda/Installation/Linux/Ubuntu).
