# Dream-T!

<details>
<summary>Word Embeddings</summary>
	
* [Lexicon Based](#lexicon-based)
* [BOW](#bow)
* [TF-IDF](#tf-idf)
* [Word2Vec](#word2vec)
* [GloVe](#glove)
* [ELMo](#elmo)
* [BERT](#bert)

</details>



### Lexicon Based

### BOW

### TF-IDF

### Word2Vec
import gensim
w2vmodel = gensim.models.KeyedVectors.load_word2vec_format('./te_w2v.vec', binary=False)

### GloVe
glove_model = gensim.models.KeyedVectors.load_word2vec_format('./te_glove_w2v.txt', binary=False)

### FastText
fastText_model = gensim.models.KeyedVectors.load_word2vec_format('./te_fasttext.vec', binary=False)

### Meta-Embeddings
MetaEmbeddings_model = gensim.models.KeyedVectors.load_word2vec_format('./result_metaEmbeddings.txt', binary=False)

### ELMo

### BERT
