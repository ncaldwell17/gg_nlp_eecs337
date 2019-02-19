# Golden Globes Project
Team Members: Harper Pack, Brandon Harris, Michael Cantu, Noah Caldwell-Gatsos

To implement the code, specify paths for both a "load_path" and a "results_path" on lines 8 and 9 of master_vf.py (corresponding to the location of the data file to be loaded, and the location of the results json, respectively).  Then, run master_vf.py. The output is .json-readable, and includes sections for the name of the award, winner, nominees, presenters, the hosts of the awards, and the favorites to win. The same is also printed to the console.

Please note that while tweet corpi of the size of gg2015.json take a while to run, corpi of of the size of gg2013.json run within just a few minutes.

Finally, please be advised that to run the code on your machine you must:
> Run master_vf.py
> Have test.py and listInMedia.py in the same directory as master_vf.py

You may additionally need to install "helper", "requests", and SpaCy.  

If you have any questions or concerns, please do not hesitate to reach out to our team.

## Packages Used
* json
* spacy [did a better job at named-entity recognition than NLTK and was faster] 
* collections
* en_core_web_sm
* helper
* sklearn

## nominees, presenters, favorites, and winners
  Our methodology to obtain the nominees, presenters, favorites, and winners is mostly the same - we attempt to categorize each tweet into sub-corpi which correspond to each award, as well as additional corpi for nominees, hosts, and award names. We utilize a series of filters (a boolean for each filter) to achieve this categorizationThink of it like a cascade - a single tweet is pushed through filter after filter to pair it with its respective attributes.  Having curated these sub-corpi, we utilize SpaCy's named entity recognition to identify entities, prune the list to remove inappropriate entity types (for example, the winner of 'Best Performance in a Motion Picture - Drama - Actor' must be a person), and then select the most frequently occuring one.
  We focused less on 'cleaning' the tweets and more simply pulling the relevant entities out of the tweet corpus, just because finding tweets that even mentioned nominees or presenters was already difficult and having retweets in the corpus was more helpful in pulling out the most relevant winners than harmful. 
  

  

