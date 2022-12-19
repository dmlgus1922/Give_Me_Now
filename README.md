# Give_Me_Now!
광주인공지능사관학교 첫 번째 프로젝트.

### 노래 가사를 뽑아주는 프로그램
  김이나처럼 유명 작사가가 되고픈 이들을 위해 도움을 주는 프로그램을 만든다.
  
     - 각 기능을 가진 모델, 함수를 구현한다.
     - 서비스를 이용할 수 있는 웹 페이지를 구현한다.
     - 플라스크를 이용해 웹과 프로그램을 연결한다.
  
  

#### :notebook: 크롤링 
  - 멜론 장르별 스테디 셀러: 약 200여 곡씩
  - 멜론 장르별 최신곡: 약 500여 곡씩
  - 한국 노래 총 5000여 곡을 크롤링
  - 시 크롤링
    - e-book은 이미지로 제공되어서 크롤링하기가 힘들었다.
    - 운이 좋게도 한 다음 블로그(무자천서)에서 시 모음집을 발견할 수 있었다.
    - 멜론의 가사처럼 정형화된 방식으로 구절이 나눠져 있지 않았으므로 전처리 과정에서 애를 먹었다.
    - 그냥 구절마다 4 단어씩 묶어 리스트로 저장하고 그보다 짧은 것들은 내버려둠. 
    - 문장이 적절하지 못한 곳에서 끊기면 문맥이 이상해질 수도 있지만 데이터셋을 늘리기 위해 일단 사용했다.


#### :cloud: 워드 클라우드를 통한 키워드별 시각화 
  - 봄, 여름, 가을, 겨울에 관련한 노래 가사를 시각화 한다.
  - 장르별(발라드, 댄스, 힙합, 알앤비 등) 노래 가사를 시각화 한다.
  
  
#### :pencil2:  장르별 랜덤 문장 출력하기
  - 전처리 과정이 있기 전의 노래 가사 데이터셋을 랜덤하게 출력해주는 프로그램을 만든다.
  - 간단한 파이썬 함수로 구현.
  - 사용자가 장르, 출력할 문장의 수, 문장의 길이를 설정하면 그에 맞게 출력.
  
  
####  :pencil2:  자신만의 문장 만들기 
  - 크롤링한 가사를 기반으로 랜덤 문장을 생성해낸다.
    ##### 데이터셋
        - 각 문장마다 3 이상의 단어를 가지도록 문장 샘플 생성.
        - 43만여 개의 문장 샘플 각 길이 확인 결과 대부분 6 이하의 길이를 가짐.
        - 6으로 패딩.
        - 가장 마지막 단어가 y, 그 앞의 단어들은 x로 설정.
    ##### LSTM, 확률적 언어 모델 응용
        1. 사용자 입력값에 확률적 언어 모델을 적용해 새로운 단어 하나를 추가하여 인풋을 바꿔줌.
        2. LSTM이 바뀐 인풋으로 예측값 생성.
        3. 그 예측값을 앞선 인풋에 다시 더해줌.
        4. 또다시 예측을 하고 사용자가 설정한 길이만큼 반복.

<hr>

### **실행**



<p align="center">

#### 1. 메인 페이지

<img src="https://user-images.githubusercontent.com/103303021/208462879-8320dfe2-78f1-45c8-b492-2ec9ead9bcdc.gif" width="80%">

</p>


<p align="center">

#### 2. 워드 클라우드

<img src="https://user-images.githubusercontent.com/103303021/208465722-2a1268f6-fe74-46d9-b13c-90a280fe9472.gif" width="80%">

</p>

<p align="center">

#### 3. 장르별 가사 추천

<img src="https://user-images.githubusercontent.com/103303021/208467003-746e76c2-e61c-48fb-bb2d-412d5071c1b6.gif" width="80%">

</p>

<p align="center">

#### 4. 가사 생성

<img src="https://user-images.githubusercontent.com/103303021/208468880-5f8a3293-445f-4c89-947a-a8bbcb22dd13.gif" width="80%">

</p>

<hr>

#### Team Happy Goose
  ###### 김의현 dmlgus1922@naver.com
  ###### 최희주 chj12365@gmail.com
  ###### 하영진 hay8268@gmail.com
  ###### 창연준 silvsk42@gmail.com
