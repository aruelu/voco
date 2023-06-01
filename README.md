# 作成中のため、まだきちんと動作しません

# voco

## volumio_contlrol
volumioのコントローラー。
色々なデバイスからvolumioのコントロールをするためのプログラムです。
キーボード、マウス、Bluetoothリモコン等からの操作が可能となります。

# 準備

## ダウンロード

```
git clone https://github.com/aruelu/covo.git
```

## セットアップ。

```
./setup.sh
```

## 設定ファイル。
```voco_init.py
voco_init.py
```

import evdev  

DEVICE = "/dev/input/event2"

[コマンド名,Type,Code,X移動量,Y移動量,H移動量,value]



## 設定内容

### DEVICE

デバイスファイル名を指定する（不要な物は記載しない）

指定したデバイスの準備が完了（/dev/以下のファイルが生成）するまで、プログラムは待機する。

### CTL

押されたボタンとコマンドの関連付け（必ず複数設定する）

[コマンド名,Type,Code,X移動量,Y移動量,H移動量,value]

### コマンド名

volumioのコマンドを指定

- play　　　：再生・停止
- prev　　    ：前へ　
- next　　　：次へ
- volup　　  ：音量大きく
- voldw　　 ：音量小さく
- voltog　　：消音・消音解除
- shutdown ：電源OFF
-  voltog　　：消音・消音解除

  

### Type
イベントのタイプを指定
例）

- evdev.ecodes.EV_KEY　：キーボードのボタン

- evdev.ecodes.EV_REL　：マウスのスクロール

  ※その他のタイプは、input-event-codes.h_excerpt.txtを参照

### Code

イベントのコードを指定

例）

evdev.ecodes.BTN_LEFT　：マウスの左ボタン

evdev.ecodes.BTN_RIGHT　：マウスの右ボタン

### X移動量、Y移動量、H移動量

各ボタンの判別のための移動量（イベント発生直前の状態）

指定なしの場合、""
BLE-M3の場合、直前のXY移動量によりボタンの判別が可能

### value

-   ボタンの場合

  - 1:down
  -  0:up

-  マウスイベントの場合

   - 移動量

  

### 定数は、include/uapi/linux/input-event-codes.hを参照

抜粋）input-event-codes.h_excerpt.txt



### 設定例

```
import evdev

# デバイスの指定
DEVICE = "/dev/input/event2"
#DEVICE = ('/dev/input/event3', '/dev/input/event2','/dev/input/event6')

#ボタンとコマンドの関連付け
CTL = (["prev",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,40,280,"",1],
        ["volup",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,60,200,"",1],
        ["play",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,160,-381,"",1],
        ["voldw",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,60,-316,"",1],
        ["next",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,-82,280,"",1],
        ["shutdown",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,10,-31,"",1],
        ["voltog",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_M,"","","",1],
        ["play",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_SPACE,"","","",1],
        ["play",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,"","","",1],
        ["volup",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_UP,"","","",1],
        ["voldw",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_DOWN,"","","",1],
        ["next",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_RIGHT,"","","",1],
        ["next",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_RIGHT,"","","",1],
        ["prev",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_LEFT,"","","",1],
        ["volup",evdev.ecodes.EV_REL,evdev.ecodes.REL_WHEEL,"","","",1],
        ["voldw",evdev.ecodes.EV_REL,evdev.ecodes.REL_WHEEL,"","","",-1])
```



キーボード、マウス、BLE-M3（bluetoothリモコン）を定義

移動量の判別が必要な場合、判別が不要なものよりも先に定義しておく。

