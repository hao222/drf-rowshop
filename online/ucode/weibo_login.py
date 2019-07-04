#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 16:39
# @Author  : wuhao

# 微博登录实现原理
def get_auth_url():
    weibo_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://47.92.87.172:8000/complete/weibo/"
    auth_url = weibo_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=3604588907, re_url=redirect_url)

    print(auth_url)


def get_access_token(code="160ef20f05c81b81a6b19751cb54374d"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url,data={
        "client_id":3604588907,
        "client_secret": "d4b6f86e71a9a960e48513e11a0c2352",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://47.92.87.172:8000/complete/weibo/"
    })
    pass
 # b'{"access_token":"2.00p5o1bGlOUwvDce0030eb50UvvwID","remind_in":"157679999","expires_in":157679999,"uid":"6048481723","isRealName":"true"}'

def get_user_fans(access_token="", uid=""):
    fans_url = "https://api.weibo.com/2/friendships/followers.json?access_token={access_token}&uid={uid}".format(access_token=access_token, uid=uid)
    print(fans_url)

if __name__ == "__main__":
    # get_auth_url()
    # get_access_token(code="fe6d01afe3379d4f8d0ea8ab1cf99416")
    get_user_fans(access_token="2.00p5o1bGlOUwvDce0030eb50UvvwID", uid="6048481723")