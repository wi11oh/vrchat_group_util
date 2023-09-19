import json
import requests

import vrc_auth



def send(groupId:str, title:str, text:str):
    def _postAnnounce(groupId, title, text):
        r = requests.post(
            f"https://api.vrchat.cloud/api/1/groups/{groupId}/announcement",
            json.dumps({"title": title, "text": text, "sendNotification": True}),
            headers = {"User-Agent": vrc_auth.readConf("username"), "Content-Type": "application/json"},
            cookies={"auth": vrc_auth.readConf("authcookie")}
        )
        return r.status_code

    if (statuscode := _postAnnounce(groupId=groupId, title=title, text=text)) != 200:
        print(f"[{statuscode}] エラーが発生しました。再認証します、コードを入力してください: ")
        vrc_auth.mailAuth()
        statuscode = _postAnnounce(groupId=groupId, title=title, text=text)
        if statuscode == 200:
            print("送信完了")
        else:
            print("エラーで終了しました。vrc_credential_infoの編集またはvrc_auth.writeConf(~)の実行で治る可能性があります")
    else:
        print("送信完了")


if __name__ == "__main__":
    gid = input("grouoid: ")
    title = input("title: ")
    text = input("text: ")

    send(groupId=gid, title=title, text=text)