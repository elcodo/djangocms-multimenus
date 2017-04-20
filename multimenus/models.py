from django.db import models
from django.utils.translation import ugettext as _

from treebeard.mp_tree import MP_Node
from cms.models.fields import PageField

from . import enums

from cms.models import Page


class MenuItem(MP_Node):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255
    )
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

    node_order_by = ['title', ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

    def get_url(self):
        if self.page:
            return self.page.get_absolute_url()
        if self.url:
            return self.url
