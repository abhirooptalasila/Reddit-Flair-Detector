# Web App Scripts
---

The web app is deployed on Heroku and built using the microframework Flask. I'll exlpain some of the files and how to use them after cloning the repo.


```request.py``` : It is a sample testing endpoint (*/reqp*). It contains a pre-defined variable for the URL (can be changed). We extract the ```id``` of the post in the URL and send it via the ```requests``` API to ```server.py```. Which then returns the predicted flair of the submitted post


```server.py``` : This script contains multiple endpoints and functions:

* */reqp* recieves an ID value via POST. We then use the ```submission``` attribute of the PRAW API to get the post corresponding to the given ID. Title of the post is retrieved from the response and passed to ```nltk_clean()``` to perform pre-processing steps. The cleaned title is tokenized and converted to sequences using the loaded [Tokenizer](../models/tokenizer.pickle). Then we perform prediction on the sequence using the loaded [model](../models/model.h5). We then get the flair name from the ```dict``` dictionary corresponding to the predicted key. A dictionary containing the flair name is returned.
*  */predict* works almost similarly to */reqp* instead it takes it's input from the text field in [```index.html```](templates/index.html) and updates the predicted flair name on the website.
*  */automated_testing* is used for testing performance of the classifier. We send an automated POST request to the endpoint with a .txt file which contains a link of a r/india post in every line. Response of the request should be a json file in which key is the link to the post and value should be predicted flair.


```testing.py``` : This script submits ```sample.txt``` to */automated_testing* endpoint and expects a JSON dictionary containing key-value pairs where each key is an URL in a line of the text file and it's corresponding value is it's predicted flair.