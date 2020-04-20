# Reddit Flair Detector
---
- [About](#about)

- [Local Installation](#local-installation)

- [Data Collection](#data-collection)

- [Exploratory Data Analysis](#exploratory-data-analysis)

- [Flair Detection Results](#flair-detection-results)
  
- [Web App Deployment](#web-app-deployment)

- [Flair Prediction](#flair-prediction)

- [References](#references)




## About

A web application built using [Flask](https://flask.palletsprojects.com/en/1.1.x/) which can predict the *flair* of a given URL of a [r/india](https://new.reddit.com/r/india/) post using **Natural Language Processing** and **Machine Learning.** 

Flairs are nothing but the different categories a Reddit post in a particular subreddit is classified into. Only the title of the given post is used for prediction. The final **Multichannel Concolutional Neural Network** achieves a test accuracy of **~93%**.

The web app is deployed on Heroku at: https://reddit-flair-detection-app.herokuapp.com/

## Local Installation

**Note:** My installation is specific to Python 3.7 and TF 1.14

Clone the repository

```bash
git clone 
cd Reddit-Flair-Detector/
```

Install the virtualenv package and create a new env
```bash
pip3 install virtualenv
virtualenv -p python3 env
source env/bin/activate

#after finishing run:
deactivate
```

Install dependencies
```bash
pip3 -r requirements.txt 
```

Navigate to ```scripts``` directory and run ```server.py```
```bash
cd scripts/
python3 server.py

# Open browser and go to the following URL
http://127.0.0.1:5000/ 
```


## Data Collection

I've used the Python Reddit API Wrapper (PRAW) to scrape data from [r/india](https://new.reddit.com/r/india/). As of 10th April 2020, the subreddit had 11 flairs. We scrape multiple fields like ```title```, ```author```, ```body``` etc for each post in every flair. The dataset is very well balanced for each flair.

Link to notebook: [Reddit Data Collection.ipynb](notebooks/Reddit%20Data%20Collection.ipynb)


## Exploratory Data Analysis

Since raw data contains many unnecassary characters we pre-process the dataset before training models on it.

Link to notebook: [Exploratory Data Analysis.ipynb](notebooks/Exploratory%20Data%20Analysis.ipynb)


## Flair Detection Results

First we start training some baseline models and then move on to SoTA models like LSTMs and CNNs.

Link to notebook: [Flair Detector.ipynb](notebooks/Flair%20Detector.ipynb)

### **Results**

#### Title as Feature

| Machine Learning Algorithm | Test Accuracy     |
| -------------              |:-----------------:|
| Naive Bayes                | 0.64706           |
| Linear SVM                 | 0.68824           |
| Logistic Regression        | 0.6902            |
| Random Forest              | 0.67059           |
| MLP                        | 0.54706           |
| LSTM                       | 0.635             |
| **Multichannel CNN**       | **0.927**         |

#### Body as Feature

| Machine Learning Algorithm | Test Accuracy     |
| -------------              |:-----------------:|
| Naive Bayes                | 0.28627           |
| Linear SVM                 | 0.38235           |
| Logistic Regression        | 0.38235           |
| **Random Forest**          | **0.3902**        |
| MLP                        | 0.33529           |


## Web App Deployment

The model was deployed using Flask on Heroku. To test it out:

* Visit [New Reddit]("https://new.reddit.com/r/india/")
* Copy a post link. Make sure it's a Reddit post and not a redirect (the link should start with "..reddit.com/r/india/..")

The ```server.py``` file contains the following endpoints:

* */reqp* : After starting the server locally, use can run ```request.py``` in another terminal. Replace the ```input_url``` variable with another one if required. Response is the predicted flair for the URL given.
* */predict* : This is a POST endpoint called when you click on the "Predict" button on the website.
* */automated_testing* : This endpoint is used for testing performance of the classifier. We send an automated POST request to the endpoint with a .txt file which contains a link of a r/india post in every line. Response of the request should be a json file in which key is the link to the post and value should be predicted flair.

## Flair Prediction 

Using the saved model to predict flair's of current top 10 posts on [r/india](https://new.reddit.com/r/india/).

Link to notebook: [Flair Predictions.ipynb](notebooks/Flair%20Predictions.ipynb)


## References
1. https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
2. https://praw.readthedocs.io/en/latest/getting_started/authentication.html#script-application
3. https://www.storybench.org/how-to-scrape-reddit-with-python/
4. http://www.nltk.org/book_1ed/
5. https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a
6. https://machinelearningmastery.com/clean-text-machine-learning-python/
7. https://kanoki.org/2019/03/17/text-data-visualization-in-python/
8. https://towardsdatascience.com/multi-class-text-classification-model-comparison-and-selection-5eb066197568
9. https://machinelearningmastery.com/develop-n-gram-multichannel-convolutional-neural-network-sentiment-analysis/
10. https://colah.github.io/posts/2015-08-Understanding-LSTMs/
11. https://github.com/abhinavsagar/Machine-Learning-Deployment
