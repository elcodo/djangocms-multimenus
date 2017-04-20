from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(TreeAdmin):
    form = movenodeform_factory(MenuItem)
