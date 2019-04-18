from django.contrib import admin

from Insurance.models import Customer

admin.site.site_header = '小不点的工作室'
admin.site.site_title = '小不点的工作室'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'age', 'sex', 'phone', 'birthday', 'id_number', 'card_number', 'id_picture_positive_show',
        'id_picture_negative_show',
        'card_picture_positive_show', 'card_picture_negative_show', 'create_time', 'color_status',)
    list_filter = ('status', 'sex',)
    search_fields = ('name', 'phone', 'id_number', 'card_number',)
    actions = ['make_finished']

    def make_finished(self, request, queryset):
        queryset.update(status='已填报')
    make_finished.short_description = "将客户标注为已填报"