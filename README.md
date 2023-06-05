# voco

## volumio_contlrol
volumioのコントローラー。
色々なデバイスからvolumioのコントロールをするためのプログラムです。
キーボード、マウス、Bluetoothリモコン等からの操作が可能となります。



# 注意事項
起動直後にイベントを発生させると、異常終了する可能性があります。
logファイルを見ると原因がわかります。
その場合、root権限で下記を実行するか再起動して下さい。
```
./run_voco.sh
```


# 準備

## ダウンロード

```
git clone https://github.com/aruelu/covo.git
```

## セットアップ

```
./setup.sh
```

上記を実行後、再起動する。

## 設定ファイル

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
CTL = []
CTL.append(["prev",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,40,280,"",1]) #BLE-M3左ボタン
CTL.append(["volup",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,60,200,"",1]) #BLE-M3上ボタン
CTL.append(["play",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,160,-381,"",1])#BLE-M3真ん中ボタン
CTL.append(["voldw",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,60,-316,"",1])#BLE-M3下ボタン
CTL.append(["next",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,-82,280,"",1])#BLE-M3右ボタン
CTL.append(["shutdown",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,10,-31,"",1])#BLE-M3シャッターボタン
CTL.append(["voltog",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_M,"","","",1])#キーボード:m
CTL.append(["play",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_SPACE,"","","",1])#キーボード:スペース
CTL.append(["play",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_LEFT,"","","",1])#マウス:左ボタン
CTL.append(["volup",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_UP,"","","",1])#キーボード:上矢印
CTL.append(["voldw",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_DOWN,"","","",1])#キーボード:下矢印
CTL.append(["next",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_RIGHT,"","","",1])#キーボード:右矢印
CTL.append(["next",evdev.ecodes.EV_KEY,evdev.ecodes.BTN_RIGHT,"","","",1])#マウス:右ボタン
CTL.append(["prev",evdev.ecodes.EV_KEY,evdev.ecodes.KEY_LEFT,"","","",1])#キーボード:左矢印
CTL.append(["volup",evdev.ecodes.EV_REL,evdev.ecodes.REL_WHEEL,"","","",1])#マウスホイール:プラス
CTL.append(["voldw",evdev.ecodes.EV_REL,evdev.ecodes.REL_WHEEL,"","","",-1])#マウスホイール:マイナス
CTL.append(["play",1,115,"","","",0])#BT Shutter（ダイソー）:両方のボタン
CTL.append(["play",1,115,"","","",0])#CW Shutter（キャンドゥ）:両方のボタン
```



キーボード、マウス、BLE-M3（bluetoothリモコン）、１００均のリモコンシャッターを定義

移動量の判別が必要な場合、判別が不要なものよりも先に定義しておく。

１００均のリモコンシャッターは、２つのボタンが有るが、両方共に同じイベントのため判別は不可能。
販売の時期によっては判別可能かもしれません。
BT Shutter（ダイソー）とCW Shutter（キャンドゥ）は同じイベントのため、外観は違いますが製造元は一緒かもしれません。

CTLの設定をタプルからリストの配列に変更しました（コメントを記載できるようにするため）。



# イベントの調べ方
下記にてイベントを調べることが可能です。
実行する前に下記ファイルで指定しているデバイス名を変更して下さい。
複数のデバイスを同時に指定できますが、あまりおすすめしません。
個別に確認した方が確実です。
```
python3 ./multi_dev.py
```