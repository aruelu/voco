import subprocess
import json

def is_play():
    str_cmd = ["volumio","status"]
    result = subprocess.run(str_cmd,capture_output=True)
    ret_play = json.loads(result.stdout)
    print(ret_play)
    if ret_play['status'] == 'stop':
        print("stop")
        return False
    elif ret_play['status'] == 'play':
        print("play")
        return True
    elif ret_play['status'] == 'pause':
        print("pause")
        return False
    else:
        print("non")
        return False

def play():
    if is_play():
        str_cmd = ["volumio","pause"]
    else:
        str_cmd = ["volumio","play"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def prev():
    str_cmd = ["volumio","previous"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def next():
    str_cmd = ["volumio","next"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def volup():
    str_cmd = ["volumio","volume","plus"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def voldw():
    str_cmd = ["volumio","volume","minus"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def voltog():
    str_cmd = ["volumio","volume","toggle"]
    print(str_cmd)
    result = subprocess.run(str_cmd)
    print('')

def shutdown():
    str_cmd = ["shutdown","-h","now"]
    print(str_cmd)
    result = subprocess.run(str_cmd)

def main():
    print("1:prev")
    print("2:volup")
    print("3:play")
    print("4:voldw")
    print("5:next")
    print("6:voltog")
    print("7:shutdown")
    n = input("実行番号を入力してください：")
    if n == "1":
        prev()
    elif n == "2":
        volup()
    elif n == "3":
        play()
    elif n == "4":
        voldw()
    elif n == "5":
        next()
    elif n == "6":
        voltog()
    elif n == "7":
        shutdown()
    else:
        print("入力エラー")

if __name__ == '__main__':
    main()

