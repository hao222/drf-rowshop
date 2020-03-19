#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/3 16:39
# @Author  : wuhao

# 微博登录实现原理
def get_auth_url():
    weibo_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://111.229.129.44:8000/complete/weibo/"
    auth_url = weibo_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=3604588907, re_url=redirect_url)

    print(auth_url)


def get_access_token(code="fb4c657b8119511a258603193663cc2a"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url,data={
        "client_id": 'client_id',
        "client_secret": "d4b6f86e71a9a960e48513e11a0c2352",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://111.229.129.44:8000/complete/weibo/"
    })
    print(re_dict.json())

def get_user_fans(access_token="", uid=""):
    fans_url = "https://api.weibo.com/2/friendships/followers.json?access_token={access_token}&uid={uid}".format(access_token=access_token, uid=uid)
    print(fans_url)

if __name__ == "__main__":
    # get_auth_url()
    # get_access_token(code="9d84e7ddc017866bcac039b16fc91ec8")
    get_user_fans(access_token="2.1", uid="11")