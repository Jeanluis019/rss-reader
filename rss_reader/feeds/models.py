from django.db import models # noqa
from django.utils.translation import gettext_lazy as _ # noqa
from django.contrib.auth import get_user_model

User = get_user_model()


class FeedCategory(models.Model):
    user = models.ForeignKey(
                            User,
                            verbose_name=_('Owner'),
                            related_name='feed_categories',
                            on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=50)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Feed(models.Model):
    user = models.ForeignKey(
                            User,
                            verbose_name=_('Owner'),
                            related_name='feeds',
                            on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    category = models.ForeignKey(
                                FeedCategory,
                                verbose_name=_('Category'), 
                                blank=True, null=True,
                                related_name='feeds', 
                                on_delete=models.SET_NULL)
    url = models.URLField(verbose_name=_('URL'), max_length=200)


    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.name
