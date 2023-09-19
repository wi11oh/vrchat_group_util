import json, time
import requests

import vrc_auth




def get(groupId:str) -> list:
    def _get(groupId):
        online_list_r = requests.get(
            f"https://api.vrchat.cloud/api/1/auth/user/friends",
            headers = {"User-Agent": vrc_auth.readConf("username"), "Content-Type": "application/json"},
            cookies={"auth": vrc_auth.readConf("authcookie")}
        )

        time.sleep(1)
        groupmember_list_r = requests.get(
            f"https://api.vrchat.cloud/api/1/groups/{groupId}/members",
            headers = {"User-Agent": vrc_auth.readConf("username"), "Content-Type": "application/json"},
            cookies={"auth": vrc_auth.readConf("authcookie")}
        )

        if online_list_r.status_code == 200 and groupmember_list_r.status_code == 200:
            online_list = []
            groupmember = []

            for friend in json.loads(online_list_r.text):
                if friend["location"] == "offline":
                    pass
                else:
                    online_list.append(friend["displayName"])

            # for _ in json.loads(online_list_r.text):
            #     online_list.append(_["id"])

            for _ in json.loads(groupmember_list_r.text):
                groupmember.append(_["user"]["displayName"])


            online = list(set(groupmember).intersection(set(online_list)))

            if not online:
                online = []
            return online
        else:
            return False

    if (online:=_get(groupId=groupId)) == False:
        print(f"エラーが発生しました。再認証します,コードを入力してください")
        vrc_auth.mailAuth()
        _get(groupId=groupId)
        if _get(groupId=groupId) == False:
            print("エラーで終了しました。vrc_credential_infoの編集またはvrc_auth.writeConf(~)の実行で治る可能性があります")
            return False
        else:
            print("完了")
            return online
    else:
        print("完了")
        return online




if __name__ == "__main__":
    gid = input("grouoid: ")

    print(get(groupId=gid))