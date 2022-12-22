import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
import json

x = []
y = []

"""
DiscordのWebhookURL
"""
webhook_uri = "https://discord.com/api/webhooks/にゃーんにゃーん" # 適宜何かしらでお埋めください
"""
DiscordのWebhook用Header
"""
headers = {'Content-Type': 'application/json'}

"""
現在、移動しているかのTFの値
"""
is_moving = False

"""
減速している回数のカウント 10点以上で動きが見られない場合、移動が終了したと考える
"""
slow_count  = 0

"""
加速度が高いときのカウント 5点連続で速度が2を上回ったときに、移動を開始したと考える
"""
active_count = 0


def init():
    """
    初期化処理
    """
    plt.ylim([0, 10])

def move_param_reset():
    """
    移動状態の監視で使ってるパラメータをリセット
    """
    global active_count,slow_count
    active_count = 0
    slow_count = 0


def data_update():
    """
    サーバーにGETして値を更新する
    """
    global x, y
    data_json = requests.get(
        "https://sensornetworkiot-iwi.onrender.com/get").json()

    formatted_dic = {float(data_str): mag for data_str,
                     mag in data_json.items()}
    formatted_dic = dict(((data, mag)
                         for data, mag in sorted(formatted_dic.items())))

    x = [datetime.datetime.fromtimestamp(unix_sec)
         for unix_sec in formatted_dic.keys()]

    y = list(formatted_dic.values())

    check_move()

def plot_update():
    """
    グラフのアップデート
    """
    global x, y
    plt.clf()
    plt.plot(x[len(x)-100:len(x)], list(y)[len(x)-100:len(x)])
    plt.yticks(np.arange(0, 11, 2))
    plt.draw()

def send_discord():
    """
    Discord のWebhookに送信する
    """
    global webhook_uri,headers
    
    send_message = ""
    
    if is_moving:
        send_message = "先生が動きだしたぞ！注意しろ！"
    else :
        send_message = "先生が止まりました！捕まえるなら今 :punch:"
    
    requests.post(
        webhook_uri, json.dumps({"content":send_message}), headers=headers)

def check_move():
    """
    移動しているかのチェック
    """
    global is_moving,active_count,slow_count
    
    # 動いていたら (動くのを辞めたか判定する)
    if is_moving:
        if y[-1] < 1.5:
            slow_count += 1
        if slow_count > 10:
            is_moving = False
            move_param_reset()
            send_discord()
    
    # 動いていなかったら (動きはじめたかを判定)
    else :
        if y[-1] > 1.5:
            active_count += 1
        if active_count > 3:
            is_moving = True
            move_param_reset()
            send_discord()
            
def main():
    """
    メイン 全体のやつを色々
    """
    init()
    while True:
        data_update()
        plot_update()
        plt.pause(5)

if __name__ == "__main__":
    main()