from classytags.arguments import Argument, MultiKeywordArgument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template

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
        try:
            menu = MenuItem.objects.get(menu_id=menu_id)
            if 'include_self' in params and params['include_self']:
                menu_items = [menu, ]
            else:
                menu_items = menu.get_children()
        except MenuItem.DoesNotExist:
            menu_items = []
        return {
            'items': menu_items,
            'template': template or ShowMultiMenu.DEFAULT_TEMPLATE_NAME,
        }
