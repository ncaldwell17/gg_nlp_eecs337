from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from statistics import mode
import scipy
from operator import itemgetter
from collections import Counter
import numpy

def delete_rows_csr(mat, indices):
    #taken from StackExchange
    """
        Remove the rows denoted by ``indices`` form the CSR sparse matrix ``mat``.
    """
    if not isinstance(mat, scipy.sparse.csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")
    indices = list(indices)
    mask = numpy.ones(mat.shape[0], dtype=bool)
    mask[indices] = False
    return mat[mask]

def customMode(l):
    if len(l) < 10:
        return []
    else:
        d = Counter(l)
        mode = d.most_common(1)
        if mode[0][1] >= 5:
            return mode[0][0]

def categoryCluster(data):
    cosine_similarity_threshold = .75

        #data = #something will need to be here
    tfidf = [TfidfVectorizer().fit_transform(data),data]
    result_dict = {}

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
        tfidf[0] = delete_rows_csr(tfidf[0],toDelete)
        tfidf[1] = list(numpy.delete(tfidf[1],[toDelete]))
    modelist = []
    for i in list(result_dict.keys()):
        m = customMode(result_dict[i])
        if m != []:
            modelist.append((m,len(result_dict[i])))
    orderedList = sorted(modelist,key=itemgetter(1),reverse=True)
    return orderedList

#filter the following: case sensitivity, word 'wins', word 'golden globes', 'golden globe', generic stop words
#remove hyphens (a space before or after taken with them) i.e. ('- '), commas,