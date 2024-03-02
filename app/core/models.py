from django.db import models
from django.db.models.query import QuerySet
from django.db.models import ProtectedError


class BaseModelQuerySet(QuerySet):

    def delete(self):
        [x.delete() for x in self]

    def hard_delete(self):
        [x.hard_delete() for x in self]

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class BaseModelManager(models.Manager):

    use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(BaseModelManager, self).__init__(*args, **kwargs)

    def all_objects(self):
        return BaseModelQuerySet(self.model)

    def get_queryset(self):
        if self.active_only:
            return BaseModelQuerySet(self.model).filter(is_active=True)
        return BaseModelQuerySet(self.model)

    def hard_delete(self):
        self.get_queryset().hard_delete()


class BaseModel(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = BaseModelManager(active_only=True)
    all_objects = BaseModelManager(active_only=False)

    def _on_delete(self):
        for relation in self._meta._relation_tree:
            on_delete = getattr(relation.remote_field, 'on_delete')

            if on_delete in [None, models.DO_NOTHING]:
                continue
            filter = {relation.name: self}
            related_queryset = relation.model.objects.filter(**filter)

            if on_delete == models.CASCADE:
                relation.models.objects.filter(**filter).delete()
            elif on_delete == models.SET_NULL:
                for r in related_queryset.all():
                    related_queryset.update(**{relation.name: None})
            elif on_delete == models.PROTECT:
                if related_queryset.count() > 0:
                    raise ProtectedError(
                        'Cannot remove this instances', related_queryset.all())
                else:
                    raise NotImplementedError()

    def delete(self):
        self.is_active = False
        self.save()
        self._on_delete()

    def hard_delete(self):
        super(BaseModel, self).delete()

    class Meta:
        abstract = True
