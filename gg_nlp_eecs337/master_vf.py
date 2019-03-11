#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 20:33:25 2019

@author: harper
"""

load_path = "./gg2013.json"
results_path = "./results.json"

import json
import spacy
from collections import Counter
from spacy.lang.en import English
import en_core_web_sm

from difflib import SequenceMatcher

import listInMedia
from test import *

def theBigOne():

    def substantial_similarity(one_str, two_str, threshold=.5):
        if isinstance(one_str, str):
            one_l = one_str.lower()
            two_l = two_str.lower()
            similarity = SequenceMatcher(None, one_l, two_l).ratio()
            return similarity > threshold
        elif isinstance(one_str, list):
            two_l = two_str.lower()
            for i in one_str:
                i_l = i.lower()
                similarity = SequenceMatcher(None, i_l, two_l).ratio()
                if similarity > threshold:
                    return True
        return False


    tweets = ''
    tweet_load = []
    count = 0
    host = {'tweets': ''}
    hst = "host"

    nlp = en_core_web_sm.load()

    awards = { 
            'Golden Globe Award for Best Motion Picture – Drama': 
                    {'medium': 'movie',
                    'genre': ['drama', 'Drama'],
                    'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Motion Picture – Musical or Comedy': 
                    {'medium': 'movie',
                    'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                    'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Motion Picture – Foreign Language': 
                    {'medium': ['movie', 'film', 'Movie', 'Film'],
                    'genre': ['foreign', 'Foreign'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Motion Picture – Animated': 
                    {'medium': ['movie', 'film', 'Movie', 'Film'],
                    'genre': ['animated', 'Animated'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Director – Motion Picture': 
                    {'medium': 'movie',
                    'genre': ['director', 'Director'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Actor – Motion Picture Drama': 
                    {'medium': 'movie',
                    'genre': ['drama', 'Drama'],
                    'required': ['actor', 'Actor'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Actress – Motion Picture Drama': 
                    {'medium': ['actress', 'Actress'], 
                    'genre': ['drama', 'Drama'],
                    'prohibited': ['tv', 'TV', 'television', 'Television'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Screenplay – Motion Picture': 
                    {'medium': 'movie',
                    'genre': ['screenplay', 'Screenplay'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Original Score – Motion Picture': 
                    {'medium': 'movie',
                    'genre': ['score', 'Score'],
                    'required': ['original', 'Original'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Original Song – Motion Picture': 
                    {'medium': 'movie',
                    'genre': ['song', 'Song'],
                    'required': ['original', 'Original'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Television Series – Drama': 
                    {'medium': 'tv',
                    'genre': ['drama', 'Drama'],
                    'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Television Series – Musical or Comedy': 
                    {'medium': 'tv',
                    'genre': ['comedy', 'musical', 'Comedy', 'Musical'],
                    'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Miniseries or Television Film': 
                    {'medium': 'tv',
                    'genre': ['film', 'Film', 'mini', 'Mini'],
                    'prohibited': ['actor', 'Actor', 'actress', 'Actress'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Actor – Miniseries or Television Film': 
                    {'medium': 'tv',
                    'genre': ['actor', 'Actor'],
                    'prohibited': ['supporting', 'Supporting'],
                    'required': ['film', 'Film', 'mini', 'Mini'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
                    'nom_list': [],
                    'nom_tweets': '',
                    'pres_tweets': ''},
                'Golden Globe Award for Best Actress – Miniseries or Television Film': 
                    {'medium': 'tv',
                    'genre': ['actress', 'Actress'],
                    'required': ['film', 'Film', 'mini', 'Mini'],
                    'tweets': '',
                    'winners': '',
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
                    'favorite': '',
                    'surprise': False,
                    'repeat': False,
                    'nominees': [],
                    'presenters': [],
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
        if criteria:
            return any(word in tweet for word in criteria)
        else:
            return True

    def is_host(tweet):
        return any(word in tweet for word in ['host', 'Host', 'hosts', 'Hosts', 
                                                'hosting', 'Hosting', 'hosted',
                                                'Hosted'])

    def is_presenter(tweet):
        return any(word in tweet for word in ['presente', 'Presente', 'presenta', 
                                                'Presenta', 'presenting', 'Presenting',
                                             'annou', 'Annou', 'introd', 'Introd'])

    def is_winner(tweet):
        return any(word in tweet for word in ['win', 'won', 'Win', 'WIN', 'Won', 'WON'])

    def is_required(tweet, criteria):
        return any(word in tweet for word in criteria)

    def is_prohibited(tweet, criteria):
        return not any(word in tweet for word in criteria)

    def is_nominees(tweet):
        return any(word in tweet for word in ['nomin', 'Nomin'])

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
                    'ewglobes', 'goldenglobe', 'thing', ' yes ', '#', '@', ' at ',
                    'http', 'https', 'tryna', 'Golden Globes', 'RT ', 'RT', ' as ',
                    ' my ', ' in ', ' as ', ' ever ', ' no ', ' one ', 'WIN',
                    ' win ', ' wins ', 'ongrat', 'ONGRAT', ' has ', ' top ',
                    ' may ', ' so ', ' aren ', ' us ', ' than ', 'NBC', 'AP',
                    'Win', 'CNN']

    go_words = ['a', 'i', 'go', 're', 'he', 'be', 'how', 'is', 'to', 'it', 'on',
                'our', 'am', 'me', 'or', 'ca', 'an', 'if', 'at', 'the', 'my', 'in',
                'as', 'ever', 'no', 'one', 'has', 'top', 'may', 'so', 'and', 'all',
                'are', 'aren', 'than', 'us', 'via', ' ', 'your', 'our', 'of']

    for w in missing_words:
        if w not in spacy_stopwords:
            spacy_stopwords.append(w)

    for w in go_words:
        while w in spacy_stopwords:
            spacy_stopwords.remove(w)

    award_reader = {'tweets':''}

    def categorize_tweet(atweet):
        if is_award(atweet):
            award_reader['tweets'] += atweet + '. '
            for award in awards.keys():
                temp = None
                if is_nominees(atweet):
                    awards[award]['nom_list'].append(atweet)
                if is_medium(atweet, medium=awards[award]['medium']):
                    if is_genre(atweet, awards[award]['genre']):
                        if 'prohibited' in awards[award].keys():
                            temp = 'prohibited'
                        if 'required' in awards[award].keys():
                            if temp == 'prohibited':
                                temp = 'both'
                            else:
                                temp = 'required'
                        if temp == 'both':
                            if is_required(atweet, awards[award]['required']) and is_prohibited(atweet, awards[award]['prohibited']):
                                awards[award]['tweets'] += atweet + ' . '
                                if is_presenter(atweet):
                                    awards[award]['pres_tweets'] += atweet + '. '
                        elif temp == 'prohibited':
                            if is_prohibited(atweet, awards[award]['prohibited']):
                                awards[award]['tweets'] += atweet + ' | '
                                if is_presenter(atweet):
                                    awards[award]['pres_tweets'] += atweet + '. '
                        elif temp == 'required':
                            if is_required(atweet, awards[award]['required']):
                                awards[award]['tweets'] += atweet + ' | '
                                if is_presenter(atweet):
                                    awards[award]['pres_tweets'] += atweet + '. '
                        elif temp == None:
                            awards[award]['tweets'] += atweet + ' | '
                            if is_presenter(atweet):
                                    awards[award]['pres_tweets'] += atweet + '. '
        if is_host(atweet):
            if not is_presenter(atweet) and not is_award(atweet):
                host['tweets'] += atweet + '. '

    def make_awards_data(award_tweets):
        data = []
        if len(award_tweets) > 999999:
            tweets = award_tweets
            while len(tweets) > 999999:
                doc = nlp(tweets[:999999])
                items = [x.text for x in doc.ents if "best" in x.text or "Best" in x.text]
                for item in items:
                    data.append(item)
                tweets = tweets[999999:]
            doc = nlp(tweets)
            items = [x.text for x in doc.ents if "best" in x.text or "Best" in x.text]
            for item in items:
                data.append(item)
        else:
            doc = nlp(award_tweets)
            items = [x.text for x in doc.ents if "best" in x.text or "Best" in x.text]
            for item in items:
                data.append(item)
        kb = listInMedia()
        categoryDataCleaner(data, spacy_stopwords, kb)
        clust = categoryCluster(data)
        print("The awards are: ")
        for i in clust:
            print("Award: " + str(i))
        return clust

    def make_hosts(host_tweets, max_hosts=10, limit=0.7):
        data = []
        if len(host_tweets) > 999999:
            tweets = host_tweets
            while len(tweets) > 999999:
                doc = nlp(tweets[:999999])
                items = [(x.text, x.label_) for x in doc.ents if x.label_ == 'PERSON']
                for item in items:
                    data.append(item)
                tweets = tweets[999999:]
            doc = nlp(tweets)
            items = [x.text for x in doc.ents if x.label_ == 'PERSON']
            for item in items:
                data.append(item)
        else:
            doc = nlp(host_tweets)
            items = [(x.text, x.label_) for x in doc.ents if x.label_ == 'PERSON']
            for item in items:
                data.append(item)
        common_list = Counter(data).most_common(max_hosts)
        host_list = [common_list[0][0][0]]
        for i in common_list:
            ratio = i[1] / common_list[0][1]
            if ratio <= limit:
                break
            else:
                if not substantial_similarity(host_list, i[0][0]):
                    host_list.append(i[0][0])
        if len(host_list) == 1:
            print("The host is: \n" + str(host_list))
            return host_list
        else:
            print("The hosts are: ")
            for i in host_list:
                print("\n" + str(i))
            return host_list

    def top_ten_ents(tweets, award_name, addlstop=['#', '@', 'http'], pres=False, winner=''):
        doc = nlp(award_name)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct and not token.like_url]
        if addlstop:
            for item in addlstop:
                tokens.append(item)
        doc = nlp(tweets)
        items = [(x.text, x.label_) for x in doc.ents if not any(word in x.text for word in tokens)]
        count_items = Counter(items).most_common()
        uniques = {}
        top_ten = [[0,'entity','label']] * 10
        for i in range(len(count_items)):
            if count_items[i][0][0] not in uniques.keys():
                uniques[count_items[i][0][0]] = {count_items[i][0][1]: count_items[i][1]}
            else:
                if count_items[i][0][1] not in uniques[count_items[i][0][0]].keys():
                    uniques[count_items[i][0][0]][count_items[i][0][1]] = count_items[i][1]
                else:
                    uniques[count_items[i][0][0]][count_items[i][0][1]] += count_items[i][1]
        count = 0
        for key in uniques.keys():
            simil_flag = False
            if not any(word in key for word in spacy_stopwords) and key != ' ' and key != '' and key != "\n":
                most = [0, '']
                total = 0
                for sub_key in uniques[key].keys():
                    total += uniques[key][sub_key]
                    if uniques[key][sub_key] > most[0]:
                        most[0] = uniques[key][sub_key]
                        most[1] = sub_key
                if most[1] == 'CARDINAL' or most[1] == 'ORDINAL' or most[1] == 'DATE' or most[1] == 'TIME':
                    continue
                if pres:
                    if most[1] == 'PERSON':
                        doc = nlp(key)
                        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
                        if not len(tokens) < 2 or 'ong' in award_name:
                            for i in range(10):
                                if total > top_ten[i][0]:
                                    top_ten.insert(i, [total, key, most[1]])
                                    count += 1
                                    break
                    else:
                        continue
                if not any(word in award_name for word in ['Actor', 'Actress', 'Director', 'Score', 'Screenplay']):
                    if most[1] != 'PERSON':
                        for i in range(10):
                            if total > top_ten[i][0]:
                                if not winner and count > 0:
                                    for indx in range(count):
                                        if substantial_similarity(top_ten[indx][1], key):
                                            simil_flag = True
                                            break
                                if simil_flag:
                                    break
                                top_ten.insert(i, [total, key, most[1]])
                                count += 1
                                break
                else:
                    if most[1] == 'PERSON':
                        doc = nlp(key)
                        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
                        if not len(tokens) < 2 or 'ong' in award_name:
                            for i in range(10):
                                if total > top_ten[i][0]:
                                    if not winner and count > 0: 
                                        for indx in range(count):
                                            if substantial_similarity(top_ten[indx][1], key):
                                                simil_flag = True
                                                break
                                    if simil_flag:
                                        break
                                    top_ten.insert(i, [total, key, most[1]])
                                    count += 1
                                    break
        return top_ten

    with open(load_path, "r") as file:
        print("Here is start count: " + str(count))
        tweet_load = json.load(file)
        for line in tweet_load:
            categorize_tweet(line['text'])
            count += 1
            if count > 9999999:
                break
        print("Here is end count: " + str(count))


    for key in awards:
        print(key)
        if len(awards[key]['tweets']) > 0:
            if "surprise" in awards[key]['tweets']:
                awards[key]['surprise'] = True
            if "repeat" in awards[key]['tweets']:
                awards[key]['repeat'] = True
            if len(awards[key]['tweets']) < 1000000:
                noms = top_ten_ents(awards[key]['tweets'], key)
                awards[key]['winners'] = noms[0][1]
                awards[key]['favorite'] = noms[0][1]
                awards[key]['nominees'].append(noms[0][1])
                for nom in noms[1:]:
                    if substantial_similarity(awards[key]['nominees'], nom[1]):
                        continue
                    else:
                        if nom[1] != 'entity':
                            awards[key]['nominees'].append(nom[1])
                            check = nom[1]
                        else:
                            break
            else:
                #print("This string was too big!")
                noms = top_ten_ents(awards[key]['tweets'][:999999], key)
                awards[key]['winners'] = noms[0][1]
                awards[key]['favorite'] = noms[0][1]
                awards[key]['nominees'].append(noms[0][1])
                for nom in noms[1:]:
                    if substantial_similarity(awards[key]['nominees'], nom[1]):
                        continue
                    else:
                        if nom[1] != 'entity':
                            awards[key]['nominees'].append(nom[1])
                        else:
                            break
            won = awards[key]['winners']
            lwon = won.lower()
            if len(awards[key]['pres_tweets']) > 1000000:
                presenters = top_ten_ents(awards[key]['pres_tweets'][:999999], key, pres=True, winner=won)
                for presenter in presenters:
                    if substantial_similarity(awards[key]['winners'], presenter[1]):
                        continue
                    else:
                        if presenter[1] != 'entity':
                            if awards[key]['presenters']:
                                if not substantial_similarity(awards[key]['presenters'], presenter[1]):
                                    awards[key]['presenters'].append(presenter[1])
                            else:
                                awards[key]['presenters'].append(presenter[1])
                        else:
                            break
            elif len(awards[key]['pres_tweets']) > 0:
                presenters = top_ten_ents(awards[key]['pres_tweets'], key, pres=True, winner=won)
                for presenter in presenters:
                    if substantial_similarity(awards[key]['winners'], presenter[1]):
                        continue
                    else:
                        if presenter[1] != 'entity':
                            if awards[key]['presenters']:
                                if not substantial_similarity(awards[key]['presenters'], presenter[1]):
                                    awards[key]['presenters'].append(presenter[1])
                            else:
                                awards[key]['presenters'].append(presenter[1])
                        else:
                            break
            for tweet in awards[key]['nom_list']:
                if is_required(tweet, [won, lwon]):
                    awards[key]['nom_tweets'] += tweet + '. '
            if len(awards[key]['nom_tweets']) > 1000000:
                nominees = top_ten_ents(awards[key]['nom_tweets'][:999999], key)
                for nominee in nominees:
                    if substantial_similarity(awards[key]['nominees'], nominee[1]):
                        continue
                    else:
                        if nominee[1] != 'entity':
                            awards[key]['nominees'].append(nominee[1])
                        else:
                            break
            elif len(awards[key]['nom_tweets']) > 0:
                nominees = top_ten_ents(awards[key]['nom_tweets'][:999999], key)
                for nominee in nominees:
                    if substantial_similarity(awards[key]['nominees'], nominee[1]): 
                        continue
                    else:
                        if nominee[1] != 'entity':
                            awards[key]['nominees'].append(nominee[1])
                        else:
                            break
            print("Winner:")
            print(awards[key]['winners'])
            if awards[key]['surprise']:
                print("This seems to be a surprise win!")
            if awards[key]['repeat']:
                print("This seems to be a repeat win!")
            print("\n")
            print("Nominees:")
            print(awards[key]['nominees'])
            print("\n")
            print("Favorite:")
            print(awards[key]['favorite'])
            print("\n")
            print("Presenters:")
            print(awards[key]['presenters'])
            print("\n")
        else:
            pass
    list_of_awards = make_awards_data(award_reader['tweets'])
    list_of_hosts = make_hosts(host['tweets'])

    with open('./host_results.json', 'w') as fp:
        json.dump(list_of_hosts, fp)

    with open('./awards_results.json', 'w') as fp:
        json.dump(list_of_awards, fp)

    nom = {}
    for i in awards.keys():
        nom[i] = awards[i]['nominees']

    with open('./nominees_results.json', 'w') as fp:
        json.dump(nom, fp)

    win = {}
    for i in awards.keys():
        win[i] = awards[i]['winners']

    with open('./winner_results.json', 'w') as fp:
        json.dump(win, fp)

    pres = {}
    for i in awards.keys():
        pres[i] = awards[i]['presenters']

    with open('./presenters_results.json', 'w') as fp:
        json.dump(pres, fp)

    '''
    dump_json = {}
    dump_json['host'] = []
    dump_json['host'].extend(list_of_hosts)
    dump_json['awards'] = awards

    
    real_json = {}
    real_json['Host'] = dump_json['host']

    for i in dump_json['awards'].keys():
        real_json[i] = {}
        real_json[i]['Presenters'] = dump_json['awards'][i]['presenters']
        real_json[i]['Nominees'] = dump_json['awards'][i]['nominees']
        real_json[i]['Winner'] = dump_json['awards'][i]['winners']

    with open(results_path, 'w') as fp:
        json.dump(real_json, fp)
        '''

if __name__ == '__main__':
    theBigOne()