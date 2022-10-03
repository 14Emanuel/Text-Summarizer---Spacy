#Import dependencies
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from flask import Flask , render_template , request
from collections import Counter

#Initialize Flask and set the template folder to "template"
app = Flask(__name__, template_folder = 'template')

#create our "home" route using the "housingprice.html" page
@app.route('/')
def home():
    
    context={
        'sentences': 5, 
        'summary':2,
    }
    return render_template('base.html',context=context)

#Set a post method to yield predictions on page
@app.route('/predict', methods = ['POST'])

def predict():
    document =request.form["content"]  #fetching text from html form
    num = request.form["sentences"]  #fetching text from html form
    #Load English into Spacy
    nlp = spacy.load("en_core_web_sm")
    document = nlp(document)
    
    len(list(document.sents))
    #filtering tokens
    
    keyword= []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in document:
        if( token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
            
    freq_word = Counter(keyword)
    freq_word.most_common(10)
    
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word]=(freq_word[word]/max_freq)
        freq_word.most_common(10)
    
    sent_strength= {}
    for sent in document.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys() :
                    sent_strength[sent]+=freq_word[word.text]
                else:
                    sent_strength[sent]=freq_word[word.text]
  
    #Summarizing sentences
    summarized_sentences = nlargest(int(num) if num else 4, sent_strength, key=sent_strength.get)
     
    #final sentence
    final_sentences= [w.text for w in summarized_sentences]
    summary= ''.join(final_sentences)
    
    # return summary
    return summary
    # print(summarise(text))

#Run app
if __name__ == "__main__":
    app.run(debug=False)