#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import argparse
import numpy as np
import codecs

class Embeddings(object):
    def __init__(self, _file, _type):
        self.type = _type
        self.mat = None
        self.norms = None
        self.w2idx = None
        self.idx2w = {}
        self.load(_file)

    def load(self, v_file):
        for line_idx, line in enumerate(codecs.open(v_file).readlines()):
            if line_idx == 0:
                i_ = line.split()
                self.vocab_size = int(i_[0])
                self.dim = int(i_[1])
                self.mat = np.zeros((self.vocab_size, self.dim), dtype=np.float32)
                self.norms = np.zeros((self.vocab_size,), dtype=np.float32)
                self.w2idx = {}
                self.idx2w = {}
            else:
                i_ = line.split()
                w_ = i_[0]
                w_idx = self.add2w(w_)
                self.add2mat(i_[1:], w_idx)
    
    def getId(self, w):
        return  self.w2idx.get(w, -1)

    def add2w(self, w):
        w_idx = self.w2idx.get(w, len(self.w2idx))
        self.w2idx[w] = w_idx
        self.idx2w[w_idx] = w
        return w_idx

    def add2mat(self,v_str, v_idx):
        v_ = np.array(v_str, dtype=np.float32)
        self.norms[v_idx] = np.linalg.norm(v_)
        self.mat[v_idx, :] = v_

class EmbeddingTools(object):
    def __init__(self, w2v_file=None, ngram2v_file=None, ngram_confusion_file=None):
        if w2v_file is not None:
            self.word_vectors = Embeddings(w2v_file, 'words')
        else:
            self.word_vectors = None
        if ngram2v_file is not None:
            self.ngram_vectors = Embeddings(ngram2v_file, 'ngrams')
        else:
            self.ngram_vectors = None

    def compute_word_vector(self, w, minn, maxn):
        w_decorated = '<' + w + '>'
        grams = [w_decorated[i:i + n] for n in xrange(minn,maxn + 1) for i in xrange(len(w_decorated)) if w_decorated[i:i + n] not in ['<', '>']]
        gram_vec = np.zeros(self.ngram_vectors.dim, dtype=np.float32)
        for g in grams:
            gram_vec += self.ngram_vectors[self.ngram_vectors.w2idx[g],:]
        return gram_vec / len(grams)

    def get_vec(self, w, full_word):
        if full_word:
            w_idx = self.word_vectors.w2idx.get(w)
        else:
            w_idx = -1
        if w_idx >= 0:
            w_vec = self.word_vectors.mat[w_idx,:]
            w_norm = self.word_vectors.norms[w_idx]
        else:
            w_vec = self.compute_word_vector(w)
            w_norm = np.linalg.norm(w_vec)
        return w_vec, w_norm

    def cosine_sim(self, w1, w2, full_word = 1):
        w1_vec, w1_norm = self.get_vec(w1, full_word) 
        w2_vec, w2_norm = self.get_vec(w2, full_word) 
        return w1_vec.dot(w2_vec) / (w1_norm * w2_norm)


if __name__ == '__main__':
    opt= argparse.ArgumentParser(description="write ngrams from a corpus to stdout")
    opt.add_argument('--word-vec', action='store', dest='word_vec_file', required = True)
    opt.add_argument('--gram-vec', action='store', dest='gram_vec_file', required = True)
    options = opt.parse_args()
    ET = EmbeddingTools(options.word_vec_file, options.ngram_vec_file, None)
    print ET.cosine_sim('this', 'that')
    print ET.cosine_sim('this', 'that', full_word = 0)
