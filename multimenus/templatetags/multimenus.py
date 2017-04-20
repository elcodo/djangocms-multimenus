from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template

from multimenus.models import MenuItem

register = template.Library()


@register.tag
class ShowMultiMenu(InclusionTag):
    name = 'show_multi_menu'
    push_context = True
    options = Options(
        Argument('name', required=True),
        Argument('template', required=False),
    )

    def get_template(self, context, **kwargs):
        return kwargs.get('template')

    def get_context(self, context, name, template="multimenus/menu.html"):
        try:
            item = MenuItem.objects.get(title=name)
        except MenuItem.DoesNotExist:
            raise Exception("Menu item named '%s' not found." % name)

        lang = context['LANGUAGE_CODE']
        url = ''
        if item.url:
            url = item.url
        elif item.page:
            draft_url = item.page.get_draft_url(language=lang)
            public_url = item.page.get_public_url(language=lang)

            if context['request'].toolbar.edit_mode:
                if item.page.is_dirty(lang):
                    if draft_url:
                        url = draft_url
                else:
                    if public_url:
                        url = public_url
            else:
                if public_url:
                    url = public_url

        return {'url': url, 'item': item, 'template': template}
