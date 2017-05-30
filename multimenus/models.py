from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from cms.models.fields import PageField
from parler.models import TranslatableModel, TranslatedFields
from treebeard.mp_tree import MP_Node

from . import enums


class MenuItem(TranslatableModel, MP_Node):
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('Title'), max_length=255)
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    menu_id = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Template tags refers to Menu ID.'),
        verbose_name=_('Menu ID'))
    page = PageField(
        verbose_name=_('Page'),
        null=True,
        blank=True
    )
    url = models.URLField(null=True, blank=True)
    target = models.CharField(
        verbose_name=_('Target'),
        choices=enums.TARGET_CHOICES,
        blank=True,
        max_length=255
    )

    class Meta:
        ordering = ('path', )
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

    def __str__(self):
        return self.title

    def get_url(self):
        if self.page:
            return self.page.get_absolute_url()
        if self.url:
            return self.url
        return "#"

    def save(self, *args, **kwargs):
        current_site = Site.objects.get_current()
        self.site = current_site
        return super().save(*args, **kwargs)
