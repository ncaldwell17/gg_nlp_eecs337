# Golden Globes Project
Team Members: Harper Pack, Brandon Harris, Michael Cantu, Noah Caldwell-Gatsos

To implement the code, include a target .json file path in line 675 of gg_nlp.py. The output is .json-readable, and includes sections for the name of the award, winner, nominees, presenters, the hosts of the awards, and the favorites to win. 

## Packages Used
* json
* spacy [did a better job at named-entity recognition than NLTK and was faster] 
* collections
* en_core_web_sm
* helper
* sklearn

## nominees, presenters, favorites, and winners
  Our methodology to obtain the nominees, presenters, favorites, and winners is mostly the same - the only difference being the words that we used to identity which is which in the initial run-through. The results (a boolean for each filter) are then sorted using the following four functions to match them to their respective awards and other values. Think of it like a cascade - a single tweet is pushed through filter after filter to pair it with its respective attributes. 
  We focused less on 'cleaning' the tweets and more simply pulling the relevant entities out of the tweet corpus, just because finding tweets that even mentioned nominees or presenters was already difficult and having retweets in the corpus was more helpful in pulling out the most relevant winners than harmful. 
  

  

