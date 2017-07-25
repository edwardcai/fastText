# Demo:
```
$./demo.py  --word-vec $WORD_EMBEDDING_FILE --ngram-vec $NGRAM_EMBEDDING_FILE --minn 1 --maxn 4 --dim 50 --span_size 2
../models/fastext.full-simple-wiki.e.50.m.skipgram.ming.1.maxg.4.winsubs.1.vec
../models/fastext.full-simple-wiki.e.50.m.skipgram.ming.1.maxg.4.winsubs.1.ngrams
Enter chat options (comma seperated):I like to watch movies, I like to read books
Enter learner input:I love novels
Cosine Distance based:
0 i->i, love->like to, novels->watch movies cost: 1.3004
1 i->i, love->like to, novels->read books cost: 1.2098
------------------------------------------------
Levenshtein Distance based:
0 i->i, love->like, ->to, ->watch, novels->movies cost: 12.0
1 i->i, love->like, novels->to read, ->books cost: 11.0
------------------------------------------------
```

