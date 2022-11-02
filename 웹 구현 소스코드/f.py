from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
# from konlpy.tag import Okt
import pickle
import numpy as np
import pandas as pd
from nltk import ConditionalFreqDist, ConditionalProbDist, MLEProbDist
from nltk.util import ngrams

with open('static\data\PKDFFinal.p', 'rb') as f1:
    df = pickle.load(f1)

stopwords = ['가', '예', '이', '리가', '하', '오', '지', '도', 
             '마치', '와', '우', '거야', '그', '끼', '번','으로','로'
             '에서', '걸','해','고','얄라리','줘요내']

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


with open('static\data\KLyricGenre.p', 'rb') as f2:
    df_genre = pickle.load(f2)


m = load_model('static\model\LSTM8p.h5')

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
# 현재 단어(문장), 반복할 횟수, 모델, 토크나이저
# def sentence_generation(current_word, n, model = m, cpd = cpd, tokenizer = tokenizer):  
#     words = current_word.split()
#     words_len = len(words)
#     sentence = ''
#     for i in range(words_len):
#         # 단어마다 매번 새로운 결과를 내기 위해 Conditional Probability Distribution 모델 적용
#         # 새 단어 생성 (바이그램으로 연관성이 있을 수 있는 단어이다.)
#         try:
#             current_word = cpd[words[i]].generate()
#         # 사용자 입력값이 없는 단어라면 가장 많이 등장하는 '내'에서 generate     
#         except:
#             current_word = cpd['내'].generate() 
#         sentence = sentence + ' ' + current_word
#         # n-1번 반복 (문장의 길이가 결정됨)
#         for _ in range(n-1):
#             encoded = tokenizer.texts_to_sequences([current_word])[0]
#             encoded = pad_sequences([encoded], maxlen=6-1, padding='pre')
#             # 입력한 X(현재 단어)에 대해서 y를 예측하고 y(예측한 단어)를 result에 저장.
#             result = model.predict(encoded, verbose=0)
#             result = np.argmax(result, axis=1)
#             for word, index in tokenizer.word_index.items(): 
#                 # 만약 예측한 단어와 인덱스와 동일한 단어가 있다면
#                 if index == result:
#                     break
#             # 현재 단어 + ' ' + 예측 단어를 현재 단어로 변경
#             current_word = current_word + ' '  + word
#             # 예측 단어를 문장에 저장    
#             sentence = sentence + ' ' + word
#         sentence += '\n'
#         # sentence = init_word + ' ' + sentence
#     return sentence

# 단어, 반복할 횟수, 모델, 토크나이저 
def sentence_generation(input_word, n, model = m, cpd = cpd, tokenizer = tokenizer):
    import re
    input_word_ = ''
    for w in input_word.split():
        w = re.sub('[^가-힣]', '', w) # 단어가 될 수 있는 글자만 남김
        input_word_ = input_word_ + ' ' + w
    sentence = ''
    try:
        words = input_word_.strip().split()[-1]  # 외쪽 공백 지우기고 맨 마지막 단어 꺼내기
    except: # 모든 문자가 가-힣이 아니라 아예 빈 문자열이 된다면
        sentence = '"죄송합니다. 문장(단어)을 이해하지 못하겠어요. 대신 특정 문장을 소개해드릴게요."\n'   
    try:
        current_word = cpd[words].generate()
    except:
        current_word = cpd['내'].generate() # 없는 단어라면 가장 많이 등장하는 '내'에서 generate
        sentence = '"죄송합니다. 문장(단어)을 이해하지 못하겠어요. 대신 특정 문장을 소개해드릴게요."\n'
    current_word = input_word_ + ' ' + current_word
        # n번 반복
    for _ in range(n):
        encoded = tokenizer.texts_to_sequences([current_word])[0]
        encoded = pad_sequences([encoded], maxlen=6-1, padding='pre')
        # 입력한 X(현재 단어)에 대해서 y를 예측하고 y(예측한 단어)를 result에 저장.
        result = model.predict(encoded, verbose=0)
        result = np.argmax(result, axis=1)
        word = tokenizer.index_word[result[0]]
        # 현재 단어 + ' ' + 예측 단어를 현재 단어로 변경
        current_word = current_word + ' '  + word
        # 예측 단어를 문장에 저장    
        sentence = sentence + ' ' + word
    return sentence.strip()