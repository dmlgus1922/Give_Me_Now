from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
# from konlpy.tag import Okt
import pickle
import numpy as np
import pandas as pd
from nltk import ConditionalFreqDist, ConditionalProbDist, MLEProbDist
from nltk.util import ngrams

with open('static\data\KLyricSentenceDFFinal.p', 'rb') as f1:
    df = pickle.load(f1)

stopwords = ['가', '예', '이', '리가', '하', '오', '지', '도', 
             '마치', '와', '우', '거야', '그', '끼', '번','으로','로'
             '에서']

# 토크나이저 생성
x_data = []
for i in range(len(df)):
    x = df.iloc[i,2]
    
    for line in x:
        xx = []
        for w in line.split():
            if w not in stopwords:
                xx.append(w)
        x_data.append(' '.join(xx))
tokenizer = Tokenizer()
tokenizer.fit_on_texts(x_data)

# cpd 생성
x_data = []
for i in range(len(df)):
    words = ' '.join(df.iloc[i,2]).split()
    x_data.append([w for w in words if w not in stopwords])

data_l = []
for lyric in x_data:
    data = ngrams(lyric, 2, pad_left=True, pad_right = True, 
            left_pad_symbol='SS', right_pad_symbol = 'SE')
    data_l += [l for l in data]

cfd = ConditionalFreqDist(data_l)
cpd = ConditionalProbDist(cfd, MLEProbDist)

# okt 생성
# okt = Okt()

with open('static\data\KLyricGenre.p', 'rb') as f2:
    df_genre = pickle.load(f2)

# with open('static\model\tokenizer6.p', 'rb') as f3:
#     tokenizer = pickle.load(f3)

m = load_model('static\model\LSTM6.h5')

# 가사 문장 랜덤으로 뽑는 함수
def show_sentence(genre, n, min_n, df = df_genre):
    gr = genre
    
    if not gr == 'all':
        temp_df = df[df.genre == gr]
    else:
        temp_df = df
        
    sentences = []
    print(len(sentences))
    import random
    while len(sentences) < n:
        song_num = random.randrange(len(temp_df))

        lyric = temp_df.iloc[song_num,2]
        sentence_num = random.randrange(len(lyric))
        
        sentence = lyric[sentence_num]

        while len(sentence.split()) < min_n:
            try:
                sentence_num += 1
                sentence = sentence + ' ' + lyric[sentence_num]
            except:
                break
        
        if len(sentence.split()) >= min_n:
            sentences.append(f"'{sentence}' - {temp_df.iloc[song_num,0]}, {temp_df.iloc[song_num,1]}")
    
    return '\n'.join(sentences)


# 명사만 뽑는 함수 근데 어떻게 써야할지 모르겠어서 미완
# def make_nouns(sentence, okt = okt):
#     p = okt.pos(sentence)
#     words = []
#     for i in range(len(p)):
#         if p[i][1] ==  'Noun':
#             words.append(p[i][0])
#     return words


# 문장 생성 함수
# 단어 여러개 넣어서 문맥이 있어보이는 척해보기
def sentence_generation(current_word, n, model = m, cpd = cpd, tokenizer = tokenizer): # 현재 단어, 반복할 횟수, 모델, 토크나이저 
    words = current_word.split()
    words_len = len(words)

    sentence = ''
    for i in range(words_len):
        # sentence = sentence + words[i]

        try:
            current_word = cpd[words[i]].generate()
        except:
            current_word = cpd['내'].generate() # 없는 단어라면 가장 많이 등장하는 '내'에서 generate
        
        sentence = sentence + ' ' + current_word

        # n번 반복
        for _ in range(n-1):
            encoded = tokenizer.texts_to_sequences([current_word])[0]
            encoded = pad_sequences([encoded], maxlen=10-1, padding='pre')

            # 입력한 X(현재 단어)에 대해서 y를 예측하고 y(예측한 단어)를 result에 저장.
            result = model.predict(encoded, verbose=0)
            result = np.argmax(result, axis=1)

            for word, index in tokenizer.word_index.items(): 
                # 만약 예측한 단어와 인덱스와 동일한 단어가 있다면
                if index == result:
                    break

            # 현재 단어 + ' ' + 예측 단어를 현재 단어로 변경
            current_word = current_word + ' '  + word

            # 예측 단어를 문장에 저장    
            sentence = sentence + ' ' + word
        
        sentence += '\n'
        # sentence = init_word + ' ' + sentence

    return sentence