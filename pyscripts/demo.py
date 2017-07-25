__author__ = 'arenduchintala'
import itertools
import sys
import argparse
import codecs
from embed_utils import CombinedEmbeddings
from span_ed import SpanEditSearch
from pprint import pprint
import numpy as np
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def char_levenshetien_dist(a, b, h = 0):
    assert isinstance(a, list)
    assert isinstance(b, list)
    import editdistance as ed
    a = ''.join(a)
    b = ''.join(b)
    return int(ed.eval(a,b))  + h

def cosine_dist(a, b):
    dist = 0.
    a = ['<EPS>'] if len(a) == 0 else a
    b = ['<EPS>'] if len(b) == 0 else b
    for a_idx, b_idx in itertools.product(a, b):
        if a_idx.strip() == '<EPS>' or b_idx.strip() == '<EPS>':
            cs = 0.
        else:
            cs = ET.cosine_sim(a_idx, b_idx, full_word = 1)
        dist += (1. - cs)
    dist = np.around(dist, 4)
    assert dist >= 0.
    return dist


if __name__ == '__main__':
    opt= argparse.ArgumentParser(description="write ngrams from a corpus to stdout")
    opt.add_argument('--word-vec', action='store', dest='word_vec_file', required = True)
    opt.add_argument('--dim', action='store', dest='dim', required = True, type = int)
    opt.add_argument('--ngram-vec', action='store', dest='ngram_vec_file', required = True)
    opt.add_argument('--minn', action='store', dest='minn', type= int, required = True)
    opt.add_argument('--maxn', action='store', dest='maxn', type= int, required = True)
    options = opt.parse_args()
    ET = CombinedEmbeddings(options.word_vec_file, options.dim, options.ngram_vec_file, options.minn, options.maxn)
    ss = SpanEditSearch(0., 1, char_levenshetien_dist) 
    a = "i love to read books".split()
    b = "i like reading novels".split()
    table, path = ss.span_edit_dist(a,b)
    pprint(path)
    print '\n-------------------------------------------\n'
    ss = SpanEditSearch(0., 2, cosine_dist) 
    table, path = ss.span_edit_dist(a,b)
    pprint(path)
