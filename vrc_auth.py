import configparser
import requests




def readConf(key:str=None):
    conf = configparser.ConfigParser()
    conf.read(("./vrc_credential_info.ini"), encoding="utf-8")

    if key in ["username", "password", "apikey"]:
        return conf["auth"][key]
    elif key in ["authcookie"]:
        return conf["cache"]["authcookie"]
    else:
        return conf["auth"]["username"], conf["auth"]["password"], conf["auth"]["apikey"], conf["cache"]["authcookie"]


def writeConf(username=None, password=None):
    conf = configparser.ConfigParser()
    conf.read((confpath:="./vrc_credential_info.ini"), encoding="utf-8")

    if username:
        conf.set("auth", "username", username)

    if password:
        conf.set("auth", "password", password)

    with open(confpath, "w", encoding="utf-8") as c:
        conf.write(c)




def _setConfCookie(authcookie:str):
    conf = configparser.ConfigParser()
    conf.read((confpath:="./vrc_credential_info.ini"), encoding="utf-8")

    conf.set("cache", "authcookie", authcookie)

    with open(confpath, "w", encoding="utf-8") as c:
        conf.write(c)


def _getAuthCookie(username, password):
    APIKEY = readConf("apikey")

    if not username:
        username = readConf("username")
    if not password:
        password = readConf("password")

    r = requests.get(
        "https://api.vrchat.cloud/api/1/auth/user",
        headers = {"User-Agent": username},
        data = {"apiKey": APIKEY},
        auth = (username,password)
    )

    cookie = r.cookies["auth"]
    return cookie


def _repStatus(cookie, status_code):
    match status_code:
        case 200:
            _setConfCookie(cookie)
            return cookie
        case 400:
            return "[400] Verify code is different."
        case 401:
            return "[401] Username and password, one or both are incorrect."
        case _:
            return "An unexpected error has occurred."


def mailAuth(username:str=None, password:str=None):
    cookie = (_getAuthCookie(username=username, password=password))

    f2acode = input("2facode: ")

    r = requests.post(
        "https://api.vrchat.cloud/api/1/auth/twofactorauth/emailotp/verify",
        headers={"User-Agent": "uirou_machine", "Content-Type": "application/json"},
        cookies={"auth": cookie},
        json={"code": f2acode}
    )

    return _repStatus(cookie=cookie, status_code=r.status_code)


def codeAuth(username:str=None, password:str=None):
    cookie = (_getAuthCookie(username=username, password=password))

    f2acode = input("2facode: ")

    r = requests.post(
        "https://api.vrchat.cloud/api/1/auth/twofactorauth/totp/verify",
        headers={"User-Agent": "uirou_machine", "Content-Type": "application/json"},
        cookies={"auth": cookie},
        json={"code": f2acode}
    )

    return _repStatus(cookie=cookie, status_code=r.status_code)




if __name__ == "__main__":
    username = input("username: ")
    password = input("password: ")

    writeConf(username=username, password=password)
    result = mailAuth()

    print("Authenticated cookie:", result)