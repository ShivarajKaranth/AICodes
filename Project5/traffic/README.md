WHAT I TRIED:

* Initially I started with 1 convolution and 1 maxpooling and then used dropout rate of 0.5 to avoid overfitting and this model yielded in a accuracy of 90% and loss of 1.98% 

* Then I used 2 convolution and 2 maxpooling along with drop out rate of 0.5 and output layer with activation function "sigmoid" and got accuracy of 95% and loss of 1.07%

* Then changed 60 units in hidden layer to 120 units and used 1 convolution and 1 maxpooling along with dropout rate of 0.5 .This yielded good accuracy for epoch1 but model had some overfitting problem.

* I increased filter number in convolution layer to see the change in accuracy and found that the model yielded a accuracy of 97% but had overfitting problem.

* Then used 3X3 matrix for max pooling but resulted in low accuracy of 77%

* Then with 2 convoltion,2 maxpooling with dropout rate 0.5 and 2x2 maxpooling used output layer with activation function "softmax" to get accuracy of 98% and loss of 0.59%


Observations:

* What I observed is that when we add more hidden layers the accuracy increases but need to consider proper value for drop out rate to prevent over fitting of model.Also we need to choose proper matrix for maxpooling to get good accuracy.

* If we add more units to hidden layer it yielded good accuracy for epoch1 but did not yield good overall accuracy and also had overfitting problem


