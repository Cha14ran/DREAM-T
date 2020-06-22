# Dream-T!

<details>
<summary>Word Embeddings</summary>
	
* [Lexicon Based](#lexicon-based)
* [BOW](#bow)
* [TF-IDF](#tf-idf)
* [Word2Vec](#word2vec)
* [GloVe](#glove)
* [FastText](#fasttext)
* [Meta-Embeddings](#meta-embeddings)
* [ELMo](#elmo)
* [BERT](#bert)
</details>

<details>
<summary>User Interface for Annotation</summary>

## How to run
* Download entire folder userinterface_annotation
* Go to /Website_with_user_login 
* "python3 app.py" command to run the file.

</details>


<details>
	<summary> Box-Plots </summary>
	
* Different cells has been created in "Boxplots.ipynb" file for Sentiment Analysis,Emotion-Identification,Hate-Speech Detection,Sarcasm Detection 

</details>
<details>
	<summary> P-values </summary>
	
* Different cells has been created in "p-values.ipynb" file for Sentiment Analysis,Emotion-Identification,Hate-Speech Detection,Sarcasm Detection
* Assumptions were also checked to perform ANOVA test. 

</details>

## Lexicon Based

## BOW

## TF-IDF

## Word2Vec
#### Code Snippet for Word2Vec Model
	import gensim
	w2vmodel = gensim.models.KeyedVectors.load_word2vec_format('./te_w2v.vec', binary=False)
* "tw_w2v.vec" file can be downloaded from "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/mounika_marreddy_research_iiit_ac_in/EYtd0as6XFZIlW-zH19YomABLvBAmrgLgc8bXv5rNOKzrw?e=4%3aRm5aaN&at=9"

## GloVe
#### Code Snippet for GloVe Model
	import gensim
	glove_model = gensim.models.KeyedVectors.load_word2vec_format('./te_glove_w2v.txt', binary=False)
* "te_glove_w2v.txt" file can be downloaded from "https://iiitaphyd-my.sharepoint.com/:t:/g/personal/mounika_marreddy_research_iiit_ac_in/EQGA3JvxTAtFpbF3CQEOI9wBDiBY6xCm3d6Q4Tk3ByZgmw?e=7JtrK1"

## FastText
#### Code Snippet for FastText Model
	import gensim
	fastText_model = gensim.models.KeyedVectors.load_word2vec_format('./te_fasttext.vec', binary=False)
* "te_fasttext.vec" file can be downloaded from "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/mounika_marreddy_research_iiit_ac_in/Ee6vQf9XLi9IroEpqaeqfbwB7_be-kS6nj69BTPhBu6LTw?e=udghNS"

## Meta-Embeddings
#### Code Snippet for Meta-Embeddings Model
	import gensim
	MetaEmbeddings_model = gensim.models.KeyedVectors.load_word2vec_format('./te_metaEmbeddings.txt', binary=False)
* "te_metaEmbeddings.txt" file can be downloaded from "https://iiitaphyd-my.sharepoint.com/:t:/g/personal/mounika_marreddy_research_iiit_ac_in/ERLGiaMiJiFDu3UwBD8YxUwBMB_aiGrRUHJXUrkKlN3Brw?e=BgocBA" 

## ELMo

#### Code-Snippet for Elmo Features:
	from allennlp.modules.elmo import Elmo, batch_to_ids  
	from allennlp.commands.elmo import ElmoEmbedder  
	from wxconv import WXC  
	from polyglot_tokenizer import Tokenizer  
	  
	options_file = "options.json"  

	weight_file = "elmo_weights.hdf5"  

	elmo = ElmoEmbedder(options_file, weight_file)  
	con = WXC(order='utf2wx',lang='tel')  
	tk = Tokenizer(lang='te', split_sen=False)  
	  
	sentence = ''  
	wx_sentence = con.convert(sentence)  

	elmo_features = np.mean(elmo.embed_sentence(tk.tokenize(wx_sentence))[2],axis=0)

* "allennlp" module can be downloaded from "https://github.com/allenai/allennlp"
* "elmo_weights.hdf5" file can be downloaded from "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/mounika_marreddy_research_iiit_ac_in/EXycd38SGhRLs5y8hBws9PMB9mvkCAzWhlwBo8k7LqbMUA?e=NbAfoc"
* "options.json" file can be downloaded from " "
* "wxconv" module can be downloaded from "https://github.com/irshadbhat/indic-wx-converter"
* "polyglot_tokenizer" module can be downloaded from "https://github.com/ltrc/polyglot-tokenizer"

## BERT
#### Code-Snippet for BERT Features:
	from bertviz import head_view  
	from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModel, BertConfig, BertForSequenceClassification, BertForNextSentencePrediction  
  
	def show_head_view(model, tokenizer, sentence_a, sentence_b=None):  

		inputs = tokenizer.encode_plus(sentence_a, sentence_b, return_tensors='pt', add_special_tokens=True)  

		input_ids = inputs['input_ids']  

		if sentence_b:  

			token_type_ids = inputs['token_type_ids']  

			attention = model(input_ids, token_type_ids=token_type_ids)[-1]  

			sentence_b_start = token_type_ids[0].tolist().index(1)  

		else:  

			attention = model(input_ids)[-1]  

			sentence_b_start = None  

		input_id_list = input_ids[0].tolist() # Batch index 0  

		tokens = tokenizer.convert_ids_to_tokens(input_id_list)  

		return attention  
  
	config = BertConfig.from_pretrained("subbareddyiiit/music_cog",output_attentions=True)  

	tokenizer = AutoTokenizer.from_pretrained("subbareddyiiit/music_cog")  

	model = AutoModel.from_pretrained("./pytorch_model_task.bin",config=config)  

	sentence_a = "pilli cApa mIxa kUrcuMxi"  
	sentence_b = "pilli raggu mIxa padukuMxi"  
	sen_vec = show_head_view(model, tokenizer, sentence_a, sentence_b)

* "transformers" module can be downloaded from "https://huggingface.co/transformers/"
* "bertviz" module can be downloaded from ""
