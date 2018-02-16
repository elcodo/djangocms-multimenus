djangocms-multimenus
====================

This plugin requires:
* django-cms: https://github.com/divio/django-cms
* django-treebeard
* django-parler
* aldryn-translation-tools

Multiple named menus support for DjangoCMS

Authors
-------

* Wojtek Kloc
* Grzegorz Biały

django-parler and django-treebeard integration based on code from:
https://github.com/aldryn/aldryn-categories/

Installation
------------

1. Add `'multimenus'` to INSTALLED_APPS in your Django project's
   settings file.
2. `python manage.py migrate multimenus`.

Usage
-----

First, create menu using panel in CMS main toolbar. See screenshots for details.

![django-multimenus1](https://cloud.githubusercontent.com/assets/186096/25271527/b5685f94-2684-11e7-9d5d-83c7a1a5046c.png)

![django-multimenus2](https://cloud.githubusercontent.com/assets/186096/25271528/b590fa26-2684-11e7-9881-e902ecbaaa36.png)


### Template

Display menu with Menu ID: NAVBAR_TOP

```html+django
{% load multimenus %}

<ul>
    {% show_multi_menu "NAVBAR_TOP" %}
</ul>
```

### Templatetag parameters

```html+django
{% show_multi_menu MENU_ID "template.html" include_self=True %}
```

* you can override menu template using path as second parameter. Basic template code:

```html+django
{% load multimenus %}

{% for item in items %}
<li>
    <a href="{{ item.get_url }}"{% if item.target %} target="{{ item.target }}"{% endif %}>{{ item.title }}</a>
    {% if item.get_children %}
    <ul>
        {% with items=item.get_children %}
            {% include template %}
        {% endwith %}
    </ul>
    {% endif %}
</li>
{% endfor %}
```

* include_self - boolean

By default, multimenus lists children of item matched by Menu ID. You can set include_self=True to include element.
