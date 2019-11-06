from django.contrib import admin
from . import models


@admin.register(models.Message)
class MassageAdmin(admin.ModelAdmin):

    """ MassageAdmin Definition """

    list_display = ("__str__", "created")


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ ConversationAdmin Definition """

    list_display = ("__str__", "count_messages", "count_participants")
