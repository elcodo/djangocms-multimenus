from django.utils.translation import get_language


def calculate_cache_key(menu_id, site_id):
    return 'multimenus-{}-{}-{}'.format(menu_id, site_id, get_language())
