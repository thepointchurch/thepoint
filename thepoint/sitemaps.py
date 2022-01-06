from itertools import chain

from django.contrib import sitemaps
from django.urls import reverse

from upperroom.resources.models import get_featured_items


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):  # pylint: disable=no-self-use
        return list(chain(["home"], get_featured_items(), ["resources:index", "contact", "copyright"]))

    def location(self, item):  # pylint: disable=no-self-use
        if isinstance(item, str):
            return reverse(item)
        return item.get_absolute_url()
