from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.utils.translation import get_language

from multimenus.models import MenuItem

register = template.Library()


@register.tag
class ShowMultiMenu(InclusionTag):
    DEFAULT_TEMPLATE_NAME = "multimenus/menu.html"
    name = 'show_multi_menu'
    push_context = True
    options = Options(
        Argument('menu_id', required=True),
        Argument('template', required=False),
        MultiKeywordArgument('params', required=False)
    )

    def get_template(self, context, **kwargs):
        template_name = kwargs.get('template')
        if not template_name:
            template_name = ShowMultiMenu.DEFAULT_TEMPLATE_NAME
        return template_name

    def get_context(self, context, menu_id, template=None, params={}):
        current_site = get_current_site(context['request'])
        cache_key = 'multimenus-{}-{}-{}'.format(menu_id, current_site.pk, get_language())
        menu_items = cache.get(cache_key)
        if menu_items is None:
            try:
                menu = MenuItem.objects.get(site=current_site, menu_id=menu_id)
                if 'include_self' in params and params['include_self']:
                    menu_items = [menu, ]
                else:
                    menu_items = menu.get_children()
            except MenuItem.DoesNotExist:
                menu_items = []
            cache.set(cache_key, menu_items, 60 * 60 * 24)

        activated_menu_items = []
        for item in menu_items:
            activated_menu_items.append(ActivatedMenuItem(context['request'], item))

        return {
            'items': activated_menu_items,
            'template': template or ShowMultiMenu.DEFAULT_TEMPLATE_NAME,
        }

class ActivatedMenuItem:
    def __init__(self, request, menu_item):
        self._request = request
        self.menu_item = menu_item
        self.title = menu_item.title
        self.target = menu_item.target
        children = menu_item.get_children();
        activated_children = []
        for child in children:
            activated_children.append(ActivatedMenuItem(request, child))
        self.children = activated_children

    def get_children(self):
        return self.children

    def get_url(self):
        return self.menu_item.get_url()

    def is_active(self):
        return self.menu_item.get_url() == self._request.get_full_path()

    def is_has_active_children(self):
        childrens = self.get_children()
        for children in childrens:
            if children.is_active():
                return True
        return False

