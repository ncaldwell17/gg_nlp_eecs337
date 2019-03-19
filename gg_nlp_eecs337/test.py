#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 22:23:00 2019

@author: harper
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from statistics import mode
import scipy
from operator import itemgetter
from collections import Counter
import numpy
import re
from listInMedia import listInMedia

from difflib import SequenceMatcher

def substantial_similarity(one_str, two_str, threshold=.5):
    if isinstance(one_str, str):
        similarity = SequenceMatcher(None, one_str, two_str).ratio()
        return similarity > threshold
    elif isinstance(one_str, list):
        two_str_l = two_str.lower()
        for i in one_str:
            similarity = SequenceMatcher(None, one_str, two_str_l).ratio()
            if similarity > threshold:
                return True
    return False

def delete_rows_csr(mat, indices):
    # taken from StackExchange
    """
        Remove the rows denoted by ``indices`` form the CSR sparse matrix ``mat``.
    """
    if not isinstance(mat, scipy.sparse.csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")
    indices = list(indices)
    mask = numpy.ones(mat.shape[0], dtype=bool)
    mask[indices] = False
    return mat[mask]


def customMode(l,lenD):
    if float(len(l)) < .005 * float(lenD):
        return []
    else:
        d = Counter(l)
        mode = d.most_common(1)
        if mode[0][1] >= 5:
            return mode[0][0]


def categoryDataCleaner(data, stopwords, kb):
    for i in range(len(data) - 1, -1, -1):
        data[i] = data[i].lower()
        for j in stopwords:
            data[i] = data[i].replace(' ' + j + ' ', ' ')
        data[i] = re.sub('.*w[oi]ns? ', '', data[i])
        data[i] = re.sub(r'(#\w* | #\w*)', '', data[i])
        data[i] = data[i].replace('golden', '')
        data[i] = data[i].replace('globes', '')
        data[i] = data[i].replace('globe', '')
        data[i] = data[i].replace('  ', ' ')
        spl = data[i].split(' - ')
        data[i] = spl[0]
        for j in range(1, len(spl)):
            if spl[j] not in kb['actor'] and spl[j] not in kb['movie'] and spl[j] not in kb['tv']: 
                data[i] = data[i] + ' - '
                data[i] = data[i] + spl[j]
        if ' ' not in data[i] or len(data[i]) <= 7:
            del data[i]


def categoryCluster(data):
    cosine_similarity_threshold = .75

    tfidf = [TfidfVectorizer().fit_transform(data), data]
    result_dict = {}

    lenData = len(data)
    while tfidf[0].shape[0] > 1:
        cosine_similarities = linear_kernel(tfidf[0][0:1], tfidf[0]).flatten()
        related_docs_ix = cosine_similarities.argsort()[::-1]
        loop = True
        toDelete = []
        nested_ix = 0
        linked_list = []
        while loop:
            nested_ix += 1
            if nested_ix >= len(related_docs_ix):
                break
            ix = related_docs_ix[nested_ix]
            if cosine_similarities[ix] > cosine_similarity_threshold:
                linked_list.append(tfidf[1][ix])
                toDelete.append(ix)
            else:
                loop = False
        result_dict[tfidf[1][0]] = linked_list
        toDelete.append(0)
        tfidf[0] = delete_rows_csr(tfidf[0], toDelete)
        tfidf[1] = list(numpy.delete(tfidf[1], [toDelete]))
    modelist = []
    for i in list(result_dict.keys()):
        m = customMode(result_dict[i],len(data))
        if m != []:
            modelist.append((m, len(result_dict[i])))
    orderedList = sorted(modelist, key=itemgetter(1), reverse=True)
    return orderedList

# filter the following: case sensitivity, word 'wins', word 'golden globes', 'golden globe', generic stop words
# remove hyphens (a space before or after taken with them) i.e. ('- '), commas,