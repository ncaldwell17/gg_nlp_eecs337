#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 23:57:54 2019

@author: harper
"""

import requests
import helper

queryForMovies = '''SELECT ?movies ?moviesLabel
   WHERE
   {
   ?movies wdt:P31 wd:Q11424.
   ?movies wdt:P577 ?date.
   FILTER("2011-01-01"^^xsd:dateTime <= ?date && ?date < "2019-01-01"^^xsd:dateTime)
   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
   }'''

queryForStopMotionMovies = '''SELECT DISTINCT ?stopmotion ?stopmotionLabel WHERE {
  ?stopmotion wdt:P31 wd:Q18089587.
  #?televisionSeries wdt:P166 ?date.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''

queryForAnimatedFeature = '''SELECT DISTINCT ?animatedfeature ?animatedfeatureLabel WHERE {
  ?animatedfeature wdt:P31 wd:Q29168811.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}'''

queryForTvShows = '''SELECT ?televisionSeries ?televisionSeriesLabel WHERE {
  ?televisionSeries wdt:P31 wd:Q5398426.

  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

}'''

queryForMini = ''' SELECT DISTINCT ?mini ?miniLabel WHERE {
  ?mini wdt:P31 wd:Q1259759.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}'''

queryForTvSeason = '''SELECT DISTINCT ?tvseason ?tvseasonLabel WHERE {
  ?tvseason wdt:P31 wd:Q3464665.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
'''
queryForActors = '''SELECT DISTINCT ?movie ?nameLabel WHERE {
  ?movie wdt:P31 wd:Q11424.
  ?movie wdt:P161 ?cast.
  ?cast wdt:P373 ?name.
  ?movie wdt:P577 ?date.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  FILTER(("2011-01-01"^^xsd:dateTime <= ?date) && (?date < "2019-01-01"^^xsd:dateTime))
}'''

queryForDirectors = '''SELECT DISTINCT ?director ?directorLabel WHERE {
  ?director wdt:P106 wd:Q2526255.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}'''




def listInMedia():
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    MovieNamesInjson = requests.get(url, params={'query': queryForMovies, 'format': 'json'}).json()
    StopMotionMovieNamesInjson = requests.get(url, params={'query': queryForStopMotionMovies, 'format': 'json'}).json()
    TvShowsNamesInjson = requests.get(url, params={'query': queryForTvShows, 'format': 'json'}).json()
    ActorsNamesInjson = requests.get(url, params={'query': queryForActors, 'format': 'json'}).json()
    DirectorsNamesInjson = requests.get(url, params={'query': queryForDirectors, 'format': 'json'}).json()
    AnimatedFeatureNamesInjson = requests.get(url, params={'query': queryForAnimatedFeature, 'format': 'json'}).json()
    MiniNamesInjson = requests.get(url, params={'query': queryForMini, 'format': 'json'}).json()
    TvseasonNamesInjson = requests.get(url, params={'query': queryForTvSeason, 'format': 'json'}).json()

    result_dict = {}


    actor_names = []
    for i in ActorsNamesInjson['results']['bindings']:
        actor_names.append(i['nameLabel']['value'].lower())
    result_dict['actor'] = actor_names

    movie_titles = []
    for m in MovieNamesInjson['results']['bindings']:
        movie_titles.append(m['moviesLabel']['value'].lower())
    result_dict['movie'] = movie_titles


    for m in StopMotionMovieNamesInjson['results']['bindings']:
        movie_titles.append(m['stopmotionLabel']['value'].lower())
    result_dict['movie'] = movie_titles

    for m in AnimatedFeatureNamesInjson['results']['bindings']:
        movie_titles.append(m['animatedfeatureLabel']['value'].lower())
    result_dict['movie'] = movie_titles

    tvShows_titles = []
    for t in TvShowsNamesInjson['results']['bindings']:
        tvShows_titles.append(t['televisionSeriesLabel']['value'].lower())
    result_dict['tv'] = tvShows_titles

    for t in MiniNamesInjson['results']['bindings']:
        tvShows_titles.append(t['miniLabel']['value'].lower())
    result_dict['tv'] = tvShows_titles

    for t in TvseasonNamesInjson['results']['bindings']:
        tvShows_titles.append(t['tvseasonLabel']['value'].lower())
    result_dict['tv'] = tvShows_titles

    director_names = []
    for d in DirectorsNamesInjson['results']['bindings']:
        director_names.append(d['directorLabel']['value'].lower())
    result_dict['director'] = director_names

    return result_dict

r = listInMedia()
#if 'true detective' in r["tv"]:
#    print('yes!!!')


