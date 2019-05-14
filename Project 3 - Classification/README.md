# Classification

## Introduction
In this project, we designed three classifiers: a perceptron classifier, a large-margin (MIRA) classifier and a slightly modified perceptron classifier for behavioral cloning. We tested the first two classifiers on a set of scanned handwritten digit images, and the last on sets of recorded pacman games from various agents. Even with simple features, your classifiers will be able to do quite well on these tasks when given enough training data.

Optical character recognition (OCR) is the task of extracting text from image sources. The data set on which we ran our classifiers is a collection of handwritten numerical digits (0-9). This is a very commercially useful technology, similar to the technique used by the US post office to route mail by zip codes. There are systems that can perform with over 99% classification accuracy (see LeNet-5 for an example system in action).

Behavioral cloning is the task of learning to copy a behavior simply by observing examples of that behavior. In this project, we used this idea to mimic various pacman agents by using recorded games as training examples. Our agent will then run the classifier at each action in order to try and determine which action would be taken by the observed agent.

## Perceptron
Unlike the naive Bayes classifier, a perceptron does not use probabilities to make its decisions. Instead it keeps a weight vector wy of each class y ( y is an identifier, not an exponent). Given a feature list f, the perceptron computes the class y whose weight vector is most similar to the input vector f. Formally, given a feature vector f (in our case, a map from pixel locations to indicators of whether they are on), we score each class with:

score(f,y)=∑ifiwyi
Then we choose the class with highest score as the predicted label for that data instance. In the code, we will represent wy as a Counter.

Learning weights
In the basic multi-class perceptron, we scan over the data, one instance at a time. When we come to an instance (f,y), we find the label with highest score:

y′=argmaxy″score(f,y″)
We compare y′ to the true label y. If y′=y, we've gotten the instance correct, and we do nothing. Otherwise, we guessed y′ but we should have guessed y. That means that wy should have scored f higher, and wy′ should have scored f lower, in order to prevent this error in the future. We update these two weight vectors accordingly:

wy=wy+f
wy′=wy′−f
Using the addition, subtraction, and multiplication functionality of the Counter class in util.py, the perceptron updates should be relatively easy to code. Each legal label needs its own Counter full of weights.

Run our code with:

* `python dataClassifier.py -c perceptron`

The command above should yield validation accuracies in the range between 40% to 70% and test accuracy between 40% and 70% (with the default 3 iterations). These ranges are wide because the perceptron is a lot more sensitive to the specific choice of tie-breaking than naive Bayes.
One of the problems with the perceptron is that its performance is sensitive to several practical details such as how many iterations you train it for, and the order you use for the training examples (in practice, using a randomized order works better than a fixed order). The current code uses a default value of 3 training iterations. You can change the number of iterations for the perceptron with the -i iterations option. Try different numbers of iterations and see how it influences the performance. In practice, you would use the performance on the validation set to figure out when to stop training, but we didn't need to implement this stopping criterion for this assignment.

## Perceptron Analysis
Perceptron classifiers, and other discriminative methods, are often criticized because the parameters they learn are hard to interpret. To see a demonstration of this issue, we can write a function to find features that are characteristic of one class. (Note that, because of the way perceptrons are trained, it is not as crucial to find odds ratios.)

We return a list of the 100 features with highest weight for that label. You can display the 100 pixels with the largest weights using the command:

* `python dataClassifier.py -c perceptron -w`
Use this command to look at the weights

## MIRA
MIRA is an online learner which is closely related to both the support vector machine and perceptron classifiers.

Similar to a multi-class perceptron classifier, multi-class MIRA classifier also keeps a weight vector wy of each label y. We also scan over the data, one instance at a time. When we come to an instance (f,y), we find the label with highest score:

y′=argmaxy″score(f,y″)
We compare y′ to the true label y. If y′=y, we've gotten the instance correct, and we do nothing. Otherwise, we guessed y′ but we should have guessed y. Unlike the perceptron, we update the weight vectors of these labels with a variable step size:

wy=wy+τf
wy′=wy′−τf
where τ≥0 is chosen such that it minimizes

minw′12∑c||(w′)c−wc||22
subject to the condition that (w′)yf≥(w′)y′f+1

which is equivalent to

minτ||τf||22 subject to τ≥(wy′−wy)f+12||f||22 and τ≥0
Note that, wy′f≥wyf, so the condition τ≥0 is always true given τ≥(wy′−wy)f+12||f||22 Solving this simple problem, we then have

τ=(wy′−wy)f+12||f||22
However, we would like to cap the maximum possible value of τ by a positive constant C, which leads us to

τ=min(C,(wy′−wy)f+12||f||22)

Implemented trainAndTune in mira.py. This method trains a MIRA classifier using each value of C in Cgrid. Evaluated accuracy on the held-out validation set for each C and choose the C with the highest validation accuracy. In case of ties, prefered the lowest value of C. Test our MIRA implementation with:

* `python dataClassifier.py -c mira --autotune`

The same code for returning high odds features in the perceptron implementation should also work for MIRA if you're curious what the classifier is learning.

## Behavioral Cloning
We have built two different types of classifiers, a perceptron classifier and mira. We now use a modified version of perceptron in order to learn from pacman agents.

For this application of classifiers, the data will be states, and the labels for a state will be all legal actions possible from that state. Unlike perceptron for digits, all of the labels share a single weight vector w, and the features extracted are a function of both the state and possible label.

For each action, calculated the score as follows:

score(s,a)=w∗f(s,a)
Then the classifier assigns whichever label receives the highest score:

a′=argmaxa″score(s,a″)
Training updates occur in much the same way that they do for the standard classifiers. Instead of modifying two separate weight vectors on each update, the weights for the actual and predicted labels, both updates occur on the shared weights as follows:

w=w+f(s,a) # Correct action

w=w−f(s,a′) # Guessed action

Run our code with:

* `python dataClassifier.py -c perceptron -d pacman`

This command should yield validation and test accuracy of over 70%.

## Pacman Feature Design
In this part you we wrote our own features in order to allow the classifier agent to clone the behavior of observed agents.

StopAgent: An agent that only stops
FoodAgent: An agent that only aims to eat the food, not caring about anything else in the environment.
SuicideAgent: An agent that only moves towards the closest ghost, regardless of whether it is scared or not scared.
ContestAgent: A staff agent from p2 that smartly avoids ghosts, eats power capsules and food.
Each agent has 15 games recorded and saved for training data, and 10 games for both validation and testing.

Added new features for behavioral cloning in the EnhancedPacmanFeatures function in dataClassifier.py.

Upon completing our features, we should get at least 90% accuracy on the ContestAgent, and 80% on each of the other 3 provided agents. You can directly test this using the `--agentToClone <Agent name>`, `-g <Agent name>` option for dataClassifier.py:

* `python dataClassifier.py -c perceptron -d pacman -f -g ContestAgent -t 1000 -s 1000`

A new ClassifierAgent, in pacmanAgents.py, uses our implementation of perceptron_pacman. This agent takes in training, and optionally validation, data and performs the training step of the classifier upon initialization. Then each time it makes an action it runs the trained classifier on the state and performs the returned action. You can run this agent with the following command:

* `python pacman.py -p ClassifierAgent --agentArgs trainingData=<path to training data>`

You can also use the `--agentToClone <Agent Name>` option to use one of the four agents specified above to train on:

* `python pacman.py -p ClassifierAgent --agentArgs agentToClone=<Agent Name>`

This project was completed with a partner, Joshua Herman (joshua9663)

[Link to official project description](http://ai.berkeley.edu/classification.html)
