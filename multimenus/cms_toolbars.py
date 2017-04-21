# coding: utf-8

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar.items import Break
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class MultimenusToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)
        position = menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        menu.add_sideframe_item(
            _(u'Manage menus'),
            url=reverse('admin:multimenus_menuitem_changelist'),
            position=position
        )
