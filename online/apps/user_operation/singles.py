# 用户在创建之时，就让他加密
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user_operation.models import UserFav

# 需要在app下引入  才可以使用信号量   这样做不是很好
# post_save:接收信号的方式
# sender: 接收信号的model


# @receiver(post_save, sender=UserFav)
# def create_UserFav(sender, instance=None, created=False, **kwargs):
#     # 是否新建，因为update的时候也会进行post_save
#     if created:
#         goods = instance.goods
#         goods.fav_num += 1
#         goods.save()
#
#
# @receiver(post_delete, sender=UserFav)
# def delete_UserFav(sender, instance=None, created=False, **kwargs):
#         goods = instance.goods
#         goods.fav_num -= 1
#         goods.save()