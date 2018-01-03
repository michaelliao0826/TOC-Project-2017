# michaelliao_bot

## prerequirement
 - python3
 - telegram
 - network
 - ngrok (如果使用本機作為伺服器)

## setup
    pip3 install -r requirement.txt

## purpose
1. 讓人體會被女生敷衍的感覺
2. 搜尋表特板美圖><

## finite state machine
![](/img/show-fsm.png)

## usage
主要有二功能:
1. **無限敷衍女生**
不斷的發你洗澡卡，體會絕望的深淵
2. **表特板搜圖**
可以透過網路上學的爬蟲功能，找出每個圖片的連結再顯現

### how to use
1. state: intial
    - input: 任意非空字串
        - response: 
            會跳到start state
            開始事先載入表特板圖片

2. state: start
    - input: hi
        - response:
            輸入hi來開始chatbot
		

3. state: user
    - input: chat
        - response:
            會跳到chat state
            開始跟女生聊天

    - input: beauty
        - response:
            會跳到beauty state
            有兩種功能給使用者選擇，一張或多張圖片
4. state: chat
    - input: bath
        - response:
            會跳到bath state
            女生開始洗澡跳回user state

5. state: beauty
    - input: photo
        - response:
            會跳到photo state
            回應多張圖片跳回user state
    - input: one
        - response:
            會跳到one state
            回應一張圖片跳回user state

