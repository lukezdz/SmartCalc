# SmartCalc
Project for Artificial Intelligence course at Gdansk University of Technology.  

This application makes use of a neural network to recognize handwritten numbers and mathematical operators and carries out calculations.
Neural network is created, trained, loaded and later used with keras.

Neural network model is trained separately (in ModelTraining), saved and later loaded to the SmartCalc Desktop app.

## Note
Pulling master branch can take a very long time, because whole dataset is stored in this repo.
To make this process faster please use 'no_dataset' branch of this repository.
You will not be able to train a new model, but you will be able to see how the SmartCalc Desktop app works.

## Dependencies
* [keras](https://keras.io/)
* [tensorflow](https://www.tensorflow.org/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [pillow (PIL)](https://pypi.org/project/Pillow/)
* [sympy](https://www.sympy.org/en/index.html)
* [opencv](https://pypi.org/project/opencv-python/)


## Authors
* Paweł Leśniewski
* Łukasz Skołd
* Łukasz Zdziarski
