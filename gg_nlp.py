import spacy
import json
from collections import Counter
from spacy.lang.en import English
import en_core_web_sm

tweets = ' '
tweet_load = []
count = 0

nlp = en_core_web_sm.load()

awards = { 'Golden Globe Award for Best Motion Picture – Drama':
                {'medium': 'movie',
                 'genre': ['drama', 'Drama'],
                 'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Motion Picture – Musical or Comedy':
                {'medium': 'movie',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Motion Picture – Foreign Language':
                {'medium': ['foreign', 'Foreign'],
                 'genre': ['win', 'won', 'Win', 'WIN', 'Won', 'WON'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Motion Picture – Animated':
                {'medium': ['animated', 'Animated'],
                 'genre': ['win', 'won', 'Win', 'WIN', 'Won', 'WON'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Director – Motion Picture':
                 {'medium': 'movie',
                 'genre': ['director', 'Director'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actor – Motion Picture Drama':
                {'medium': 'movie',
                 'genre': ['drama', 'Drama'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actor – Motion Picture Musical or Comedy':
                {'medium': 'movie',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['supporting', 'Supporting'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actress – Motion Picture Drama':
                {'medium': 'movie',
                 'genre': ['drama', 'Drama'],
                 'prohibited': ['supporting', 'Supporting'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actress – Motion Picture Musical or Comedy':
                {'medium': 'movie',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['supporting', 'Supporting'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Supporting Actor – Motion Picture':
                {'medium': 'movie',
                 'genre': ['supporting', 'Supporting'],
                 'prohibited': ['tv', 'TV', 'television', 'Television'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Supporting Actress – Motion Picture':
                {'medium': 'movie',
                 'genre': ['supporting', 'Supporting'],
                 'prohibited': ['tv', 'TV', 'television', 'Television'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Screenplay – Motion Picture':
                {'medium': 'movie',
                 'genre': ['screenplay', 'Screenplay'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Original Score – Motion Picture':
                {'medium': 'movie',
                 'genre': ['score', 'Score'],
                 'required': ['original', 'Original'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Original Song – Motion Picture':
                {'medium': 'movie',
                 'genre': ['song', 'Song'],
                 'required': ['original', 'Original'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Television Series – Drama':
                {'medium': 'tv',
                 'genre': ['drama', 'Drama'],
                 'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Television Series – Musical or Comedy':
                {'medium': 'tv',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Miniseries or Television Film':
                {'medium': 'tv',
                 'genre': ['film', 'Film', 'mini', 'Mini'],
                 'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actor – Television Series Drama':
                {'medium': 'tv',
                 'genre': ['drama', 'Drama'],
                 'prohibited': ['film', 'Film', 'mini', 'Mini'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actor – Television Series Musical or Comedy':
                {'medium': 'tv',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['film', 'Film', 'mini', 'Mini'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actor – Miniseries or Television Film':
                {'medium': 'tv',
                 'genre': ['actor', 'Actor'],
                 'required': ['film', 'Film', 'mini', 'Mini'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actress – Television Series Drama':
                {'medium': 'tv',
                 'genre': ['drama', 'Drama'],
                 'prohibited': ['film', 'Film', 'mini', 'Mini'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actress – Television Series Musical or Comedy':
                {'medium': 'tv',
                 'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                 'prohibited': ['film', 'Film', 'mini', 'Mini'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Actress – Miniseries or Television Film':
                {'medium': 'tv',
                 'genre': ['actress', 'Actress'],
                 'required': ['film', 'Film', 'mini', 'Mini'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Supporting Actor – Series, Miniseries or Television Film':
                {'medium': 'tv',
                 'genre': ['supporting', 'Supporting'],
                 'prohibited': ['movie', 'Movie', 'motion', 'Motion'],
                 'required': ['actor', 'Actor'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
            'Golden Globe Award for Best Supporting Actress – Series, Miniseries or Television Film':
                {'medium': 'tv',
                 'genre': ['supporting', 'Supporting'],
                 'prohibited': ['movie', 'Movie', 'motion', 'Motion'],
                 'required': ['actress', 'Actress'],
                 'tweets': '',
                 'winners': '',
                 'nominees': '',
                 'presenters': '',
                 'nom_list': [],
                 'nom_tweets': '',
                 'pres_tweets': ''},
                }

def is_award(tweet):
    return any(word in tweet for word in ['best', 'Best', 'category', 'Category'])

def is_medium(tweet, medium=None):
    if medium == "movie":
        return any(word in tweet for word in ['movie', 'Movie', 'motion', 'Motion', 'picture', 'Picture'])
    elif medium == "tv":
        return any(word in tweet for word in ['tv', 'TV', 'television', 'Television', 'series', 'Series'])
    elif medium:
        return any(word in tweet for word in medium)
    else:
        pass

def is_genre(tweet, criteria):
    return any(word in tweet for word in criteria)

def is_host(tweet):
    return any(word in tweet for word in ['host', 'Host', 'hosts', 'Hosts',
                                         'hosting', 'Hosting', 'hosted',
                                         'Hosted'])

def is_presenter(tweet):
    return any(word in tweet for word in ['presen', 'Presen', 'annou', 'Annou',
                                         'introd', 'Introd'])

def is_nominees(tweet):
    return any(word in tweet for word in ['nomin', 'Nomin'])

def is_required(tweet, criteria):
    return any(word in tweet for word in criteria)

def is_prohibited(tweet, criteria):
    return not any(word in tweet for word in criteria)

def is_winner(tweet):
    return any(word in tweet for word in ['win', 'won', 'Win', 'WIN', 'Won', 'WON'])

spacy_stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)

missing_words = ['able', 'dear', 'got', ' let ', 'like', 'likely', 'said', ' is ',
                 'says', 'twas', 'wants', 'goldenglobes', 'golden', ' ca ',
                 'globe', 'globes', "'s", "n't", '...', ' on ', ' our ', ' it ',
                 '``', 'haven', "couldn't", "isn't", ' am ', ' me ', ' or ',
                 "that'll", 'mustn', 'hadn', 'mightn', "you'd", "aren't",
                 'weren', "you're", 'theirs', "won't", "haven't", "it's",
                 ' ain ', "she's", "should've", 'doesn', "doesn't", "wasn't",
                 "you'll", 'couldn', "wouldn't", "shan't", 'having', 'shouldn',
                 'wouldn', 'aren', "hasn't", 'isn', "shouldn't", ' an ',
                 "weren't", 'don', "didn't", 'needn', 'wasn', 'didn', ' the ',
                 'shan', "don't", "hadn't", 'hasn', "mightn't", "you've",
                 "needn't", "mustn't", 'goldenglobes', 'GoldenGlobe', ' if ',
                 'ewglobes', 'goldenglobe', 'thing', 'yes', '#', '@', ' at ',
                 'http', 'https', 'tryna', 'Golden Globes', 'RT ', 'RT', ' as ',
                 ' my ', ' in ', ' as ', ' ever ', ' no ', ' one ',]

go_words = ['a', 'i', 'go', 're', 'he', 'be', 'how', 'is', 'to', 'it', 'on',
            'our', 'am', 'me', 'or', 'ca', 'an', 'if', 'at', 'the', 'my', 'in',
            'as', 'ever', 'no', 'one', ]

for w in missing_words:
    if w not in spacy_stopwords:
        spacy_stopwords.append(w)

for w in go_words:
    while w in spacy_stopwords:
        spacy_stopwords.remove(w)

def categorize_tweet(tweet):
    if is_award(tweet):
        for award in awards.keys():
            temp = None
            if is_nominees(tweet):
                awards[award]['nom_list'].append(tweet)
            if is_medium(tweet, medium=awards[award]['medium']):
                if is_genre(tweet, awards[award]['genre']):
                    if 'prohibited' in awards[award].keys():
                        temp == 'prohibited'
                    if 'required' in awards[award].keys():
                        if temp == 'prohibited':
                            temp = 'both'
                        else:
                            temp = 'required'
                    if temp == 'both':
                        if is_required(tweet, a.wards[award]['required']):
                            if is_winner(tweet):
                                awards[award]['tweets'] += tweet + ' | '
                            if is_presenter(tweet):
                                awards[award]['pres_tweets'] += tweet + ' .'
                    elif temp == 'prohibited':
                        if is_prohibited(tweet, awards[award]['prohibited']):
                            if is_winner(tweet):
                                awards[award]['tweets'] += tweet + ' | '
                            if is_presenter(tweet):
                                awards[award]['pres_tweets'] += tweet + ' . '
                    elif temp == 'required':
                        if is_required(tweet, awards[award]['required']):
                            if is_winner(tweet):
                                awards[award]['tweets'] += tweet + ' | '
                            if is_presenter(tweet):
                                awards[award]['pres_tweets'] += tweet + ' . '
                    elif temp == None:
                        if is_winner(tweet):
                            awards[award]['tweets'] += tweet + ' | '
                        if is_presenter(tweet):
                            awards[award]['pres_tweets'] += tweet + ' . '
    if is_host(tweet):
        pass
    if is_presenter():
        pass

def top_ten_ents(tweets, award_name, addlstop=['#', '@', 'http'], pres=False, winner=None):
    doc = nlp(award_name)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and not token.like_url]
    if addlstop:
        for item in addlstop:
            tokens.append(item)
    doc = nlp(tweets)
    items = [(x.text, x.label_) for x in doc.ents if not any(word in x.text for word in tokens)]
    count_items = Counter(items).most_common()
    uniques = {}
    top_ten = [[0, 'entity', 'label']] * 10
    for i in range(len(count_items)):
        if count_items[i][0][0] not in uniques.keys():
            uniques[count_items[i][0][0]] = {count_items[i][0][1]: count_items[i][1]}
        else:
            if count_items[i][0][1] not in uniques[count_items[i][0][0]].keys():
                uniques[count_items[i][0][0]][count_items[i][0][1]] = count_items[i][1]
            else:
                uniques[count_items[i][0][0]][count_items[i][0][1]] += count_items[i][1]
        # print("These are uniques: " + str(len(uniques.keys())))
    for key in uniques.keys():
        if not any(word in key for word in spacy_stopwords):
            most = [0, '']
            total = 0
            for sub_key in uniques[key].keys():
                total += uniques[key][sub_key]
                if uniques[key][sub_key] > most[0]:
                    most[0] = uniques[key][sub_key]
                    most[1] = sub_key
            # print(award_name)
            if pres:
                if most[1] == 'PERSON':
                    # print(most[1])
                    if winner not in key:
                        for i in range(10):
                            if total > top_ten[i][0]:
                                top_ten[i] = [total, key, most[1]]
                                # print(top_ten[i])
                                break
            if not any(word in award_name for word in ['Actor', 'Actress', 'Director', 'Score', 'Screenplay']):
                if most[1] != 'PERSON':
                    for i in range(10):
                        if total > top_ten[i][0]:
                            top_ten[i] = [total, key, most[1]]
                            break
            else:
                if most[1] == 'PERSON':
                    for i in range(10):
                        if total > top_ten[i][0]:
                            top_ten[i] = [total, key, most[1]]
                            break
    return top_ten

def top_ten_dict(dicct, key):
    top_10 = [[0,'entity']] * 10
    for subkey in dicct[key]['entities'].keys():
        for i in range(10):
            if dicct[key]['entities'][subkey] > top_10[i][0]:
                top_10[i] = [dicct[key]['entities'][subkey], subkey]
                break
    return top_10

people = ['PERSON']

drama_str = ''

#insert json file path here (after open)

with open("/Users/harper/Documents/19W/NLP/Project/gg2015.json", "r") as file:
   print("Here is start count: " + str(count))
   tweet_load = json.load(file)
   for line in tweet_load:
       categorize_tweet(line['text'])
       count += 1
       if count > 9999999:
           break
   print("Here is end count: " + str(count))

for key in awards.keys():
    #print(key)
    won = None
    if len(awards[key]['tweets']) > 0:
        #print("Here is the SpaCy top entities")
        if len(awards[key]['tweets']) < 1000000:
            #print("Winner:")
            #print(top_ten_ents(awards[key]['tweets'], key))
            awards[key]['winners'] = top_ten_ents(awards[key]['tweets'], key)
            won = awards[key]['winners'][0][1]
        else:
#            print("This string was too big!")
#            print("Winner:")
#            print(top_ten_ents(awards[key]['tweets'][:999999], key))
            awards[key]['winners'] = top_ten_ents(awards[key]['tweets'][:999999], key)
            won = awards[key]['winners'][0][1]
        if len(awards[key]['pres_tweets']) < 1000000:
#            print("Presenter:")
#            print(top_ten_ents(awards[key]['pres_tweets'], key, pres=True))
            awards[key]['presenters'] = top_ten_ents(awards[key]['pres_tweets'], key, pres=True, winner=won)
        else:
#            print("This string was too big!")
#            print("Presenter:")
            print(top_ten_ents(awards[key]['pres_tweets'][:999999], key, pres=True))
            awards[key]['presenters'] = top_ten_ents(awards[key]['pres_tweets'][:999999], key, pres=True, winner=won)
            #awards[key]['winners'] = top_ten_ents(awards[key]['tweets'], key)
#        print("Here is the NLTK top entities")
#        print(len(awards[key]['tweets']))
#        produce_nltk_chunks(awards[key]['tweets'], awards, key)
#        print(awards['Golden Globe Award for Best Motion Picture – Drama']['entities'])
#        print(top_ten_dict(awards, key))
    else:
        print("No string, need search better")
    #print("\n")

noms = ''

for key in awards.keys():
    count = 0
    print(len(awards[key]['nom_list']))
    for tweet in awards[key]['nom_list']:
        won = awards[key]['winners'][0][1]
        lwon = won.lower()
        if is_required(tweet, [won, lwon]):
            awards[key]['nom_tweets'] += tweet + ' . '
            count += 1
    #print("Finished " + str(key) + " with count " + str(count))

def top_ten_noms(noms, award_name, addlstop=['#', '@', 'http'], pres=False, winner=[]):
    limit = 999999
    new_limit = 0
    old_limit = 0
    while_count = 0
    ndoc = nlp(award_name)
    tokens = [token.text for token in ndoc if not token.is_stop and not token.is_punct and not token.like_url]
    if addlstop:
        for item in addlstop:
            tokens.append(item)
    if len(noms) > limit:
        ndoc = nlp(noms[0:limit])
        nitems = [(x.text, x.label_) for x in ndoc.ents if not any(word in x.text for word in tokens)]
        new_limit += limit
        while len(noms[new_limit:-1]) > limit:
            old_limit = new_limit
            new_limit += limit
            ndoc = nlp(awards[award_name]['nom_tweets'][old_limit:new_limit])
            nitems = [nitems.append((x.text, x.label_)) for x in ndoc.ents if not any(word in x.text for word in tokens)]
            print(while_count)
            while_count += 1
            if while_count > 9:
                break
    else:
        ndoc = nlp(noms)
        #nitems = [(x.text, x.label_) for x in ndoc.ents]
        nitems = [(x.text, x.label_) for x in ndoc.ents if not any(word in x.text for word in tokens)]
    ncount_items = Counter(nitems).most_common()
    nuniques = {}
    ntop_ten = [[0,'entity','label']] * 10
    for i in range(len(ncount_items)):
        if ncount_items[i][0][0] not in nuniques.keys():
            nuniques[ncount_items[i][0][0]] = {ncount_items[i][0][1]: ncount_items[i][1]}
        else:
            if ncount_items[i][0][1] not in nuniques[ncount_items[i][0][0]].keys():
                nuniques[ncount_items[i][0][0]][ncount_items[i][0][1]] = ncount_items[i][1]
            else:
                nuniques[ncount_items[i][0][0]][ncount_items[i][0][1]] += ncount_items[i][1]
    #print("These are uniques: " + str(len(uniques.keys())))
    for key in nuniques.keys():
        if not any(word in key for word in spacy_stopwords) and not any(word in key for word in winner):
            most = [0, '']
            total = 0
            for sub_key in nuniques[key].keys():
                total += nuniques[key][sub_key]
                if nuniques[key][sub_key] > most[0]:
                    most[0] = nuniques[key][sub_key]
                    most[1] = sub_key
            #print(award_name)
            if pres:
                if most[1] == 'PERSON':
                    #print(most[1])
                    for i in range(10):
                        if total > ntop_ten[i][0]:
                            ntop_ten[i] = [total, key, most[1]]
                            #print(top_ten[i])
                            break
            if not any(word in award_name for word in ['Actor', 'Actress', 'Director', 'Score', 'Screenplay']):
                if most[1] != 'PERSON':
                    for i in range(10):
                        if total > ntop_ten[i][0]:
                            ntop_ten[i] = [total, key, most[1]]
                            break
            else:
                if most[1] == 'PERSON':
                    for i in range(10):
                        if total > ntop_ten[i][0]:
                            ntop_ten[i] = [total, key, most[1]]
                            break
    #print(top_ten)
    #top_ten = [[0,'entity','label']] * 10
    #return top_ten[0][1:]
    return ntop_ten


#limit = 999999
#new_limit = 0
#old_limit = 0
#if len(awards[key]['nom_tweets']) > limit:
#    doc2 = nlp(awards[key]['nom_tweets'][0:limit])
#    items2 = [(x.text, x.label_) for x in doc2.ents]
#    new_limit += limit
#    while len(awards[key]['nom_tweets'][new_limit:]) > limit:
#        old_limit = new_limit
#        new_limit += limit
#        doc2 = nlp(awards[key]['nom_tweets'][old_limit:new_limit])
#        items2 = [items2.append((x.text, x.label_)) for x in doc2.ents]
#else:
#    doc2 = nlp(awards[key]['nom_tweets'])
#    items2 = [(x.text, x.label_) for x in doc2.ents]
##print("This is how long tweets is:" + str(len(awards[key]['nom_tweets'])))
#
#print("This is how long items is:" + str(len(items2)))
#
#nuniques = {}
#ntop_ten = [[0,'entity','label']] * 10
#
#count_items2 = Counter(items2).most_common()
#print("This is how long count is:" + str(len(count_items2)))
#
#for i in range(len(count_items2)):
#    if count_items2[i][0][0] not in nuniques.keys():
#        nuniques[count_items2[i][0][0]] = {count_items2[i][0][1]: count_items2[i][1]}
#    else:
#        if count_items2[i][0][1] not in nuniques[count_items2[i][0][0]].keys():
#            nuniques[count_items2[i][0][0]][count_items2[i][0][1]] = count_items2[i][1]
#        else:
#            nuniques[count_items2[i][0][0]][count_items2[i][0][1]] += count_items2[i][1]
#print("These are uniques: " + str(len(nuniques.keys())))
#for key in nuniques.keys():
#    if not any(word in key for word in spacy_stopwords):
#        most = [0, '']
#        total = 0
#        for sub_key in nuniques[key].keys():
#            total += nuniques[key][sub_key]
#            if nuniques[key][sub_key] > most[0]:
#                most[0] = nuniques[key][sub_key]
#                most[1] = sub_key
#        if most[1] not in people:
#            for i in range(10):
#                if total > ntop_ten[i][0]:
#                    ntop_ten[i] = [total, key, most[1]]
#                    break
#print(ntop_ten)

for key in awards:
    print(key)
    print("Winner:")
    print(awards[key]['winners'][0])
    won = awards[key]['winners'][0][1]
    lwon = won.lower()
    print("Presenter:")
    print(awards[key]['presenters'][0])
    print("Nominees:")
    print(top_ten_noms(awards[key]['nom_tweets'], key, winner=[won, lwon]))
    print("\n")

#with open("nom_tweets_2015.txt", "w") as file:
#    for key in awards:
#        file.write(key)
#        file.write("\n")
#        file.write(awards[key]['nom_tweets'])
#        file.write("\n")
#        file.write("\n")
#        file.write("\n")
#        file.write("\n")
#        file.write("\n")

#award_key = 'Best Motion Picture – Foreign Language'
#with open("cat_tweets_str.txt", "w") as file:
#    for key in awards:
#        file.write(key)
#        file.write("\n")
#        file.write(awards[key]['tweets'])
#        file.write("\n")
#print(awards[award_key]['tweets'][0:100])
#







