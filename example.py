import vrc_auth, vrc_group_announce, vrc_get_onlinemembers




# 認証 2回目はいらない
import vrc_auth

vrc_auth.writeConf(username="Mr_usernameisnotdisplayname", password="superstrongpwd")




# 指定のグループに通知を飛ばす
import vrc_group_announce

vrc_group_announce.send(
    "grp_********-********-********-****", #グルid
    "テステス",                            # title
    "ぉゎ～～～～～"                       # text
)




# 指定のグループのonlineの人のdisplaynameのリスト
import vrc_get_onlinemembers

onlinelist = vrc_get_onlinemembers.get("grp_********-********-********-****")

print(onlinelist)

