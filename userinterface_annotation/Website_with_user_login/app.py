from flask import Flask, render_template, request, url_for, redirect, session, abort,flash,send_from_directory
# from wtforms import Form, BooleanField, PasswordField, validators, StringField
# from flask_table import Table,Col

import pandas as pd
import csv
import os
from functools import wraps



url_path = '../Project/'
app = Flask(__name__)
app.secret_key = "charan"
list_genres = []
user_dict = {'user1': '1001', 'user2':'2002', 'user3': '3003','user4':'4004','user5':'5005'}

# class results(Table):
#     id=Col('SENTENCE_ID')
#     sentence_str=Col('Sentence')
#     sentiment=Col('Sentiment')
#     emotion=Col('Emotion')
#     hatespeech=Col('Hate speech')
#     clickbait=Col('clickbait')
#     sarcasm=Col('Sarcasm')
#     text_box=Col('Text')

# class Data():
#     def __init__(self):
#         self.num_global=0
#         self.sentences=[]

# item=Data()
user_logins = []
user_data = []


def check_userlogins(username, passwd):
    for l in user_dict:
        if l == username and user_dict[l] == passwd:
            return 'correct'
    return 'incorrect'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('args,kwargs',args,kwargs)
        print(f)
        # if session['login'] and session['username']==kwargs['username']:
        if session['login']:

            if session['username']==kwargs['username']:
                return f(*args, **kwargs)
        else:

            flash("You need to login first")
            return redirect((url_for("index")))
    return wrap

def logout_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if 'login' not in session  :
                return f(*args, **kwargs)
        if 'login' in session and not session['login']:
                return f(*args, **kwargs)
        else:
            # flash("You need to logout first")
            return redirect(url_for('genre',username=session['username']))
    return wrap


@app.route('/', methods=['POST', 'GET'])
@logout_required
def index():
    error = None
    # session['login']=False
    # session['username']=""
    if "login" in session and session['login']:
        redirect(url_for('genre',username=session['username']))

    if request.method == "POST":
        if check_userlogins(request.form['username'], request.form['password']) == 'incorrect':
            error = 'Invalid Credentials,Please try again.'
        else:
            session['login'] = True
            session['username'] = request.form['username']
            return redirect(url_for('genre', username=request.form['username']))
    return render_template('main.html', error=error)

@app.route('/favicon.ico/')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')



@app.route('/logout/')
def logout():
    try:
        if session['login'] and session['username'] != "":
            session['login']=False
            session['username']=''
            # session.clear()
            # session.pop('username',None)
        return  redirect(url_for('index'))
    except Exception as e:
        print(e)
        return 'hello'


@app.route('/<username>/', methods=['GET', 'POST'])
@login_required
def genre(username):
    try:
        if username == "favicon.ico":
            return "favi"
        error=None
        if session['login'] and session['username']==username:
            GenreList = []
            GenreList.append(str(username))
            GenreList.append(next(os.walk(url_path + str(username)))[1])
            # print(GenreList)
            return render_template('Genre.html', genre_folders=GenreList,error=error)
    except Exception as e:
        print(e)
        return "Please login agian,some error has happened"
    # return redirect(url_for('index'))


@app.route('/<username>/<genre>/')
@login_required
def file(username, genre):
    try:
        if session['login'] and session['username']==username:
            folder = username
            Files_list = []
            Files_list.append(folder)
            Files_list.append(genre)
            Files_list.append(next(os.walk(url_path + str(folder) + '/' + str(genre)))[2])
            return render_template('Files.html', listoffiles=Files_list)
    except Exception as e:
        print(e)
    return "herl"


@app.route('/<username>/<genre>/<file>/',methods=['GET','POST'])
@login_required
def sentences(username,genre,file):
    try:
        if not session['login']:
            return redirect(url_for('index'))
        if request.method=='GET':
            if 'Annotated' in file:
                file_path = url_path + str(username) + '/' + str(genre) + '/' + str(file)
                title_list=['Sentence','Sentiment','Emotion','Hatespeech','Clickbait','Sarcasm','TextBox']
                df = pd.read_csv(file_path, delimiter=',',names=title_list, header=None)
                pd.set_option('max_colwidth', -1)
                df['Sentence']=df['Sentence'].str.strip()
                return render_template('results.html',tables=[df.to_html(classes='data')],titles=df.columns.values)

            session['item'] = 0
            lis=[]
            file_path=url_path+str(username)+'/'+str(genre)+'/'+str(file)
            df = pd.read_csv(file_path, delimiter=',')
            sentences = df['Sentence']
            keys=df['key']
            for i in range(0,len(sentences)):
                if(df.at[i,'checked']==0):
                    session['item']=i
                    break
                elif i==len(sentences)-1:
                    return "sentences are completed"
            # print(session['item'], 'GET Request', username)
            num_rem_sentences=len(sentences)-session['item']
            if not session['item']<len(sentences):
                return "sentences are completed"
            else:
                for k in range(session['item'], session['item'] + 5):
                    options={'Sentiment':['pos','neg','neutral','comp'],'Emotion':['happy','sad','anger','fear','no'],'Hatespeech':['yes','no'],'Clickbait':['yes','no'],'Sarcasm':['yes','no'],'sentence':''}
                    if k==len(sentences):
                        break
                    row=sentences.loc[k]
                    key=keys.loc[k]
                    options.update({'sentence':row})
                    options.update({'key_value':key})
                    lis.append(options)
                return render_template('Viewsentences.html',list_sentences=lis,username=username,num_rem=num_rem_sentences)

        lis_sentences = []
        sentiment_response = []
        emotion_response = []
        hatespeech_response = []
        clickbait_response = []
        sarcasm_response = []
        text_response = []
        length=int(request.form['length_sentences'])
        for k in range(1,length+1):
            try:
                lis_sentences.append((request.form.getlist("sentence_name"+str(k)))[0])
                sentiment_response.append((request.form.getlist("sentiment_option"+str(k)))[0])
                emotion_response.append((request.form.getlist("emotion_option"+str(k)))[0])
                hatespeech_response.append((request.form.getlist("hatespeech_option"+str(k)))[0])
                clickbait_response.append((request.form.getlist("clickbait_option"+str(k)))[0])
                sarcasm_response.append((request.form.getlist("sarcasm_option"+str(k)))[0])
                text_response.append((request.form.getlist("text_data"+str(k)))[0])
            except Exception as e:
                print(e)

        file_path=url_path+str(username)+'/'+str(genre)+'/'+str(file)
        new_file_path=url_path+str(username)+'/'+str(genre)+'/'+str('Annotated_'+file)
        df = pd.read_csv(file_path, delimiter=',')
        sentences=df['Sentence']
        keys=df['key']
        p=0
        # print(session['item'], 'POST Request', username)
        lis_id=[]
        for k in range(session['item'],session['item']+length):
            if k==len(sentences):
                break
            if(sentiment_response[p]=='None'):
                df.at[k,'checked']=2
            else:
                df.at[k,'checked']=1
            p=p+1
            lis_id.append(k)

        record={
            'Id':lis_id,
            'Sentence':lis_sentences,
            'sentiment':sentiment_response,
            'emotion':emotion_response,
            'hatespeech':hatespeech_response,
            'clickbait':clickbait_response,
            'sarcasm':sarcasm_response,
            'textbox':text_response
        }
        dataframe=pd.DataFrame(record,columns=['Id','Sentence','sentiment','emotion','hatespeech','clickbait','sarcasm','textbox'])

        with open(new_file_path,'a') as f:
            dataframe.to_csv(f,header=False,index=False)

        df.to_csv(file_path,index=False)
        lis=[]
        for i in range(0, len(sentences)):
            if (df.at[i, 'checked'] == 0):
                session['item']=i
                break
            elif i==len(sentences)-1:
                return "sentences are completed"
        num_rem_sentences = len(sentences) - session['item']
        if (session['item'] < len(sentences)):
            for k in range(session['item'],session['item'] + 5):
                options = {'Sentiment': ['pos', 'neg', 'neutral','comp'],
                           'Emotion': ['happy', 'sad', 'anger', 'fear', 'no'],
                           'Hatespeech': ['yes', 'no'], 'Clickbait': ['yes', 'no'],
                           'Sarcasm': ['yes', 'no'], 'sentence': ''}
                if k==len(sentences):
                    break
                row = sentences.loc[k]
                key=keys.loc[k]
                options.update({'sentence': row})
                options.update({'key_value':key})
                lis.append(options)
            return render_template('Viewsentences.html', list_sentences=lis,username=username,num_rem=num_rem_sentences)
        else:
            return "Sentences are completed"
    except Exception as e:
        print(e)
        GenreList = []
        GenreList.append(username)
        GenreList.append(next(os.walk(url_path + username))[1])
        return redirect(url_for('genre', username=session['username']))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')