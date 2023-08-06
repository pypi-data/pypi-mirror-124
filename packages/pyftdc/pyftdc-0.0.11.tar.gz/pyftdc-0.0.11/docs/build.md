You will need CMake and Boost to build the libraries. This steps also apply when installing with Pip, as the distribution is a source code bundle.


``` 
sudo apt-get install python3-dev python3-pip python-pybind11
sudo apt-get install cmake libboost-dev libboost-log-dev libboost-log-program-options-dev
```


Plus libbson

```
sudo apt-get install bson-1.0
```

Older versions of Bson need to be precompiled for now, as the repositories contain an ancient version of Bson (I'm looking at you, Debian Buster)


For OSX

```
brew install mongo-c-driver
brew install pybind11
```

Also, yaml-cpp

```
sudo apt install libyaml-cpp-dev
```

or built locally downloading and building
```
https://github.com/mongodb/mongo-c-driver/tree/master/src/libbson
https://github.com/jbeder/yaml-cpp/
```
