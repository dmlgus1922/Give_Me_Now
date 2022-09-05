import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # 텐서플로 경고문 무시
from flask import Flask, render_template, request, url_for
from f import show_sentence, sentence_generation


app = Flask(__name__)

# @app.before_first_request # 첫 요청 전에 실행
# def before_first_request():
#     # with open('static\data\KLyricGenre.p', 'rb') as f:
#     #     df_genre = pickle.load(f)
#     m = load_model('static\model\LSTM6.h5')

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/main")
def main():
    return render_template("index.html") 

@app.route("/intro")
def intro():
    return render_template('intro.html')

@app.route("/wordcloud")
def wordcloud():
    return render_template("wordcloud.html") 

@app.route("/wordcloud2")
def wordcloud2():
    return render_template("wordcloud2.html")
     
@app.route("/sentence", methods=['GET', 'POST'])
def sentence():
    genre = [
        {'disp':'모든 장르', 'val':'all'},
        {'disp':'발라드', 'val':'ballad'},
        {'disp':'댄스', 'val':'dance'},
        {'disp':'힙합', 'val':'hiphop'},
        {'disp':'인디', 'val':'inde'},
        {'disp':'포크', 'val':'folk'},
        {'disp':'알앤비', 'val':'rnb'},
        {'disp':'락', 'val':'rock'},
        {'disp':'트로트', 'val':'trot'},
        ]
    if request.method == 'GET':
        return render_template("sentence.html", genre = genre)
    else:
        g = request.form['genre']
        n = request.form['number']
        l = request.form['length']
        num = {'five':5, 'three':3, 'one':1}
        length = {'long':15, 'mid':10, 'short':5}
        n = num[n]
        l = length[l]
        result = show_sentence(g, n, l)
        import time
        time.sleep(0.3)
        return render_template("sentence_res.html", genre = genre, result=result)


@app.route("/makeLyric", methods=['GET', 'POST'])
def makeLyric():
    if request.method == 'GET':
        return render_template("makeLyric.html")
    else:
        sentence = request.form['sentence']
        l = request.form['length']
        length = {'long':20, 'mid':13, 'short':8}
        n = length[l]

        result = sentence_generation(sentence, n)
        return render_template("makeLyric_res.html", result = result)


if __name__ == "__main__":
    app.run(debug = True)