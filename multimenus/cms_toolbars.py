# coding: utf-8

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class MultimenusModifier(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'multimenus-app',
            _(u'Multimenu'),
        )
        menu.add_modal_item(
            _(u'Manage menus'),
            url=reverse('admin:multimenus_menuitem_changelist'),
        )
