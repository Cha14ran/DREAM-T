from flask import Flask, render_template,request,url_for,redirect
import  pandas as pd
import csv
import os
path_to_folders='/home/chinni/PycharmProjects/Honours/'
Folders_list=next(os.walk(path_to_folders))[1]
app = Flask(__name__)

class Data():
    def __init__(self):
        self.folder=''
        self.genre=''
        self.file=''
        self.sentences=[]
        self.num_global=0

item=Data()

@app.route('/')
def index():
    return render_template('main.html',folders=Folders_list)

@app.route('/select_genre',methods=['GET','POST'])
def select_genre():
    try:
        # if request.method == "POST":
        folder=request.form.get('folder_selection')
        item.folder=str(folder)
        Genre_list=[]
        Genre_list.append(str(folder))
        Genre_list.append(next(os.walk(path_to_folders+str(folder)))[1])
        # Genre_list=next(os.walk(path_to_folders+str(folder)))[1]
        return render_template('Genre.html',genre_folders=Genre_list)
    except Exception as e:
        print(e)

@app.route('/select_files',methods=['GET','POST'])
def select_files():
    try:
        genre = request.form.get('genre_selection')
        item.genre=str(genre)
        # print(item.genre)
        Files_list=[]
        Files_list.append(item.folder)
        Files_list.append(item.genre)
        Files_list.append(next(os.walk(path_to_folders + item.folder+'/'+item.genre))[2])
        return render_template('Files.html',listoffiles=Files_list)
    except Exception as e:
        print(e)

@app.route('/view_sentences',methods=['GET','POST'])
def view_sentences():
    try:
            file=request.form.get('file_selection')
            item.file=str(file)
            lis=[]
            file_path=path_to_folders+item.folder+'/'+item.genre+'/'+item.file
            df = pd.read_csv(file_path, delimiter=',')
            sentences = df['Sentence']
            for i in range(0,len(sentences)):
                if(df.at[i,'checked']==0):
                    item.num_global=i
                    break
                elif i==len(sentences)-1:
                    return "sentences are completed"

            if(item.num_global<len(sentences)):
                for k in range(item.num_global,item.num_global+5):
                    options={'Sentiment':['pos','neg','neutral'],'Emotion':['happy','sad','anger','fear','no'],'Hatespeech':['yes','no'],'Clickbait':['yes','no'],'Sarcasm':['yes','no'],'sentence':''}
                    if k==len(sentences):
                        break
                    row=sentences.loc[k]
                    item.sentences.append(row)
                    options.update({'sentence':row})
                    lis.append(options)
                # print(lis)
                return render_template('Viewsentences.html',list_sentences=lis)
            else:
                return "sentences are completed"
    except Exception as e:
        print(e)


@app.route('/final_results',methods=['GET','POST'])
def final_results():
    try:

        #
        # if stophere_response[0]=='stop':
        #     return render_template('main.html',folders=Folders_list)
        invalid_response=request.form.getlist("invalid_option")
        print(invalid_response)
        sentiment_response=request.form.getlist("sentiment_option")
        emotion_response=request.form.getlist("emotion_option")
        hatespeech_response=request.form.getlist("hatespeech_option")
        clickbait_response=request.form.getlist("clickbait_option")
        sarcasm_response=request.form.getlist("sarcasm_option")
        text_response=request.form.getlist("text_data")
        print(sentiment_response)
        print(emotion_response)
        print(sarcasm_response)
        file_path = path_to_folders + item.folder + '/' + item.genre + '/' + item.file
        new_file_path = path_to_folders + item.folder + '/' + item.genre + '/' + str('Annotated_'+item.file)
        df = pd.read_csv(file_path, delimiter=',')
        sentences=df['Sentence']
        lis_sentences=[]
        p=0
        for k in range(item.num_global,item.num_global+5):
            if k==len(sentences):
                break
            lis_sentences.append(sentences.loc[k])
            if(sentiment_response[p]=='None'):
                df.at[k,'checked']=2
            else:
                df.at[k,'checked']=1
            p=p+1

        record={
            'Sentence':lis_sentences,
            'sentiment':sentiment_response,
            'emotion':emotion_response,
            'hatespeech':hatespeech_response,
            'clickbait':clickbait_response,
            'sarcasm':sarcasm_response,
            'textbox':text_response
        }
        # with open(new_file_path,'a') as f:
        #     new_df=pd.read_csv(f,index=False)
        dataframe=pd.DataFrame(record,columns=['Sentence','sentiment','emotion','hatespeech','clickbait','sarcasm','textbox'])
        # final_dataframe=pd.concat([new_df,dataframe],ignore_index=True)
        # final_dataframe.to_csv(new_file_path,index=False)
        # print(final_dataframe)
        # new_df.insert(dataframe)
        # i=0
        # for j in range(item.num_global,item.num_global+5):
        #     if j == len(sentences):
        #         break
        #     new_df.at[j,'Sentence']=lis_sentences[i]
        #     new_df.at[j,'sentiment']=sentiment_response[i]
        #     new_df.at[j,'emotion']=emotion_response[i]
        #     new_df.at[j,'hatespeech']=hatespeech_response[i]
        #     new_df.at[j,'clickbait']=clickbait_response[i]
        #     new_df.at[j,'sarcasm']=sarcasm_response[i]
        #     new_df.at[j,'textbox']=text_response[i]
        #     i=i+1

        # for k in range(item.num_global,item.num_global+5):
        #     new_df.at[k,'Sentence']=sentences[k]
        #     new_df.at[k,'sentiment']=sentiment_response[k]
        #     new_df.at[k,'emotion']=emotion_response[k]
        #     new_df.at[k,'hatespeech']=hatspeech_response[k]
        #     new_df.at[k,'clickbait']=clickbait_response[k]
        #     new_df.at[k,'sarcasm']=sarcasm_response[k]
        #     if(emotion_response[k]!='no'):
        #         new_df.at[k,'textbox']=text_response[k]
        #     df.at[k,'checked']=1

        with open(new_file_path,'a') as f:
            dataframe.to_csv(f,header=False,index=False)

        df.to_csv(file_path,index=False)
        lis=[]
        for i in range(0, len(sentences)):
            if (df.at[i, 'checked'] == 0):
                item.num_global = i
                break
            elif i==len(sentences)-1:
                return "sentences are completed"
        if (item.num_global < len(sentences)):
            for k in range(item.num_global, item.num_global + 5):
                options = {'Sentiment': ['pos', 'neg', 'neutral'],
                           'Emotion': ['happy', 'sad', 'anger', 'fear', 'no'],
                           'Hatespeech': ['yes', 'no'], 'Clickbait': ['yes', 'no'],
                           'Sarcasm': ['yes', 'no'], 'sentence': ''}
                if k==len(sentences):
                    break
                row = sentences.loc[k]
                options.update({'sentence': row})
                lis.append(options)
                item.sentences.append(row)
            return render_template('Viewsentences.html', list_sentences=lis)
        else:
            return "Sentences are completed"
    except Exception as e:
        print(e)
        # stophere_response=request.form.getlist("stop_here")
        # if stophere_response[0]=='stop':
        #     return render_template('main.html',folders=Folders_list)
        # print("You haven't selected all options")
        return  render_template('main.html',folders=Folders_list,error="You haven't selected all options previously")
        # print(e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)