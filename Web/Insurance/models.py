from django.db import models


class Customer(models.Model):
    SEX_CHOICE = (
        ('男', '男'),
        ('女', '女'),
    )
    name = models.CharField(max_length=20, verbose_name='姓名')
    age = models.IntegerField(max_length=2, verbose_name='年龄')
    sex = models.CharField(max_length=1, verbose_name='性别', choices=SEX_CHOICE)
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    id_number = models.CharField(max_length=18, verbose_name='身份证号')
    card_number = models.CharField(max_length=30, verbose_name='银行卡卡号')
    id_picture_positive = models.ImageField(verbose_name='身份证正面图片')
    id_picture_negative = models.ImageField(verbose_name='身份证反面图片')
    card_picture_positive = models.ImageField(verbose_name='银行卡正面图片')
    card_picture_negative = models.ImageField(verbose_name='银行卡反面图片')
