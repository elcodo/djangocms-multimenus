from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from .models import MenuItem


class MenuItemAdminForm(TranslatableModelForm, MoveNodeForm):
    pass


MenuItemAdminForm = movenodeform_factory(MenuItem, form=MenuItemAdminForm)
