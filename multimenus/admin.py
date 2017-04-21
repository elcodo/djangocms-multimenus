from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _

from aldryn_translation_tools.admin import AllTranslationsMixin
from parler.admin import TranslatableAdmin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .forms import MenuItemAdminForm
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(AllTranslationsMixin, TranslatableAdmin, TreeAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'menu_id')}),
        (_('Link'), {'fields': ('page', 'url', 'target', )}),
        (_('Tree position'), {'fields': ('_position', '_ref_node_id')}),
    )
    form = MenuItemAdminForm
    list_display = ('title', 'menu_id', )
    ordering = ('path', )
    search_fields = ('translations__title', 'menu_id', )

    def get_form(self, request, obj=None, **kwargs):
        form_cls = super().get_form(request, obj, **kwargs)
        form_cls.base_fields['_position'].label = ugettext('Position')
        form_cls.base_fields['_ref_node_id'].label = ugettext('Relative to')
        return form_cls
