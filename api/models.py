from django.db import models
from django.contrib import admin


class BroadcastGroup(models.Model):
    name = models.CharField(max_length=20, verbose_name="群組名")

    class Meta:
        verbose_name, verbose_name_plural = '推播群組', '推播群組'

    def __str__(self):
        return self.name


class Message(models.Model):
    message = models.TextField(verbose_name="推播內容")
    stopID = models.IntegerField(verbose_name="目前發送至此")
    created_at = models.DateTimeField(verbose_name="發送日期", auto_now=True)

    class Meta:
        verbose_name, verbose_name_plural = '歷史紀錄', '歷史紀錄'
    
    def __str__(self):
        return self.created_at.strftime("%x-%X") + " id:" + str(self.stopID)


class AccessToken(models.Model):
    token = models.TextField()
    groups = models.ManyToManyField(BroadcastGroup, verbose_name='群組', blank=True)
    username = models.CharField(max_length=2048, verbose_name="用戶名", default="unknow")
    userType = models.CharField(max_length=20, verbose_name="種類", default="unknow")

    class Meta:
        verbose_name, verbose_name_plural = '推播用戶', '推播用戶'
    
    def __str__(self):
        return self.username + "-" + self.userType


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', "stopID", "created_at"]

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ["username", "userType"]
    readonly_fields = ('token',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(BroadcastGroup)
class BroadcastGroupAdmin(admin.ModelAdmin):
    list_display = ["name"]
