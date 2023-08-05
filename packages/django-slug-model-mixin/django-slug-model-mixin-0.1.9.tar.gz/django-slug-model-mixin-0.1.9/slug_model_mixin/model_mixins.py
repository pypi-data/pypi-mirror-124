import logging

from django.db import models
from django.utils.text import slugify
from uuslug import uuslug

logger = logging.getLogger('django-slug-model-mixin')


class SlugModelMixin(models.Model):
    slugged_field = 'title'
    slug_unique = True
    force_slugify = False

    slug = models.SlugField()

    class Meta:
        abstract = True
        # unique_together = ('slug',)

    def _slug_is_unique(self, slug: str, object_id: int = None) -> bool:
        try:
            if object_id:
                self.__class__._default_manager.exclude(id=self.id).get(slug=slug)
            else:
                self.__class__._default_manager.get(slug=slug)
            return False
        except self.__class__.DoesNotExist:
            return True

    def save(self, *args, **kwargs):
        _slugged_field = getattr(self, self.slugged_field)
        if not self.slug:
            if self.force_slugify:
                if not self.slug_unique or (self.id and self._slug_is_unique(_slugged_field, self.id)):
                    self.slug = slugify(_slugged_field)[:50]
                elif self.slug_unique:
                    self.slug = uuslug(_slugged_field, instance=self)
        else:
            if self.slug_unique:
                slug = self.slug
                if (
                    (self.id and self._slug_is_unique(slug, self.id))
                    or (not self.id and self._slug_is_unique(slug))
                ):
                    self.slug = slug
                else:
                    self.slug = uuslug(slug, instance=self)
        super(SlugModelMixin, self).save(*args, **kwargs)
