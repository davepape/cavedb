from django.db import models


class EntityCategory(models.Model):
    name = models.CharField(max_length=256)


class Entity(models.Model):
    name = models.TextField(default='')
    sortkey = models.CharField(max_length=256, default='')
    category = models.ForeignKey(EntityCategory, on_delete=models.PROTECT)
    url = models.CharField(max_length=1024,default='')
    description = models.TextField(default='')


class LinkCategory(models.Model):
    name = models.CharField(max_length=256)
    entity1Category = models.ForeignKey(EntityCategory, blank=True, null=True, on_delete=models.PROTECT, related_name='entity1Category')
    entity2Category = models.ForeignKey(EntityCategory, blank=True, null=True, on_delete=models.PROTECT, related_name='entity2Category')


class Link(models.Model):
    category = models.ForeignKey(LinkCategory, on_delete=models.PROTECT)
    entity1 = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name='entity1')
    entity2 = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name='entity2')


