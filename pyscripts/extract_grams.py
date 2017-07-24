#!/usr/bin/env python
__author__ = 'arenduchintala'
import sys
import codecs
import argparse
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

BOW = '<'
EOW = '>'

if __name__ == '__main__':
    opt= argparse.ArgumentParser(description="write ngrams from a corpus to stdout")
    #insert options here
    opt.add_argument('--vec', action='store', dest='word_vec_file', required = True)
    opt.add_argument('--ming', action='store', dest='ming', default=1, type = int, required = True)
    opt.add_argument('--maxg', action='store', dest='maxg', default=2, type = int, required = True)
    options = opt.parse_args()
    if options.ming <= 0:
        raise BaseException('ming should be at least 1')

    grams = set([])
    for line in codecs.open(options.word_vec_file, 'r', 'utf8').readlines()[1:]:
        word = line.strip().split()[0]
        word = BOW + word + EOW
        word_grams = [word[i:i + n] for n in xrange(options.ming, options.maxg + 1) for i in xrange(len(word))]
        grams.update(word_grams)

    if options.ming == 1:
        grams.remove(BOW)
        grams.remove(EOW)
    else:
        pass
    for g in grams:
        print g
