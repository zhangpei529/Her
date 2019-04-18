from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Customer(models.Model):
    class Meta:
        verbose_name_plural = '客户资料'
        verbose_name = '客户资料'

    SEX_CHOICE = (
        ('男', '男'),
        ('女', '女'),
    )
    STATUS_CHOICE = (
        ('未填报', '未填报'),
        ('已填报', '已填报')
    )
    name = models.CharField(max_length=20, verbose_name='姓名')
    id_number = models.CharField(max_length=18, verbose_name='身份证号')
    age = models.IntegerField(verbose_name='年龄')
    sex = models.CharField(max_length=1, verbose_name='性别', choices=SEX_CHOICE)
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    birthday = models.DateField()
    card_number = models.CharField(max_length=30, verbose_name='银行卡卡号')
    id_picture_positive = models.ImageField(verbose_name='身份证正面图片', upload_to='id_card_positive')
    id_picture_negative = models.ImageField(verbose_name='身份证反面图片', upload_to='id_card_negative')
    card_picture_positive = models.ImageField(verbose_name='银行卡正面图片', upload_to='bank_card_positive')
    card_picture_negative = models.ImageField(verbose_name='银行卡反面图片', upload_to='bank_card_negative')
    status = models.CharField(max_length=5, verbose_name='状态', default="未填报", choices=STATUS_CHOICE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    def id_picture_positive_show(self):
        return mark_safe(u'<img src="%s" width="100px" />' % self.id_picture_positive.url)

    id_picture_positive_show.short_description = u'身份证正面图片'

    def id_picture_negative_show(self):
        return mark_safe(u'<img src="%s" width="100px" />' % self.id_picture_negative.url)

    id_picture_negative_show.short_description = u'身份证正面图片'

    def card_picture_positive_show(self):
        return mark_safe(u'<img src="%s" width="100px" />' % self.card_picture_positive.url)

    card_picture_positive_show.short_description = u'身份证正面图片'

    def card_picture_negative_show(self):
        return mark_safe(u'<img src="%s" width="100px" />' % self.card_picture_negative.url)

    card_picture_negative_show.short_description = u'身份证正面图片'

    def color_status(self):
        if self.status == '已填报':
            color = 'green'
        else:
            color = 'red'
        return format_html(
            '<span style="color: %s;">%s</span>' % (color, self.status)
        )
    color_status.short_description = "填报状态"
