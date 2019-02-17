# Golden Globes Project
Team Members: Harper Pack, Brandon Harris, Michael Cantu, Noah Caldwell-Gatsos

To implement the code, include a target .json file with the tweet corpus and run the ? command of the ? file to begin.

## Packages Used
* json
* spacy [did a better job at named-entity recognition and was faster] 
* collections
* en_core_web_sm

## nominees, presenters, and winners
  Our methodology to obtain the nominees, presenters, and winners is mostly the same - the only difference being the words that we used to identity which is which in the initial run-through. The results (a boolean for each filter) are then sorted using the following four functions to match them to their respective awards and other values. Think of it like a cascade - a single tweet is pushed through filter after filter to pair it with its respective attributes. 

## categorize_tweet

## top_ten_ents

## top_ten_dict

## top_ten_noms

## get_sentiment
  To get sentiment analysis, we used a publicly available dictionary provided by the University of Pittsburgh with over 7,000 words and their associated negativity or positivity. Function get_sentiment intakes a corpus of tweets selected about the nominees, winners, and presenters, runs them against the UPITT list of words to see how many negative/positive words come up, and reports back the percentages in a human-readable format. Function get_sentiment will be run when the ? command of the ? file is run. 

## get_best_dressed
  To find the 'best dressed' at the Golden Globes, we input the corpus of tweets related to the nominees, use our function get_sentiment to find the nominees associated with positive words, and then filter using keywords such as 'red carpet, variations of the word look, custom, dress/shoes/gown, and associated complimenting words.' We then take the top ten of the analysis and place them in a human-readable list matching with 'best-dressed.' Function get_best_dressed will be run when the ? command of the ? file is run.  

## get_parties
  To find who was throwing parties after the Golden Globes, we input the corpus of tweets related to the nominees and filter using a regEx * after party to figure out cased names associated with the parties. Function get_parties will be run when the ?command of the ? file is run. 
  
## spanish_functionality 
  

