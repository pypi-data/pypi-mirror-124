from __future__ import annotations

from copy import copy
from typing import Optional, List, Tuple, Type

from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.db.models import JSONField, Func, F, Value

from vtb_django_utils.user_info.info import get_user_info
from vtb_django_utils.utils.class_factory import class_factory
from vtb_django_utils.utils.db import CreatedMixin
from vtb_django_utils.utils.diff import get_objs_diff
from vtb_django_utils.utils.jsons import get_json_hash
from .utils.consts import START_VERSION, THERE_IS_NO_VERSION_DATA, DOES_NOT_EXIST_VERSION
from .utils.regex import version_regex
from .utils.strings import int_arr_to_str, str_to_int_arr


class VersionModel(CreatedMixin, models.Model):
    """ Базовый класс для версий какой-либо модели """
    user = JSONField(default=dict, blank=True)
    json = JSONField(default=dict, blank=True)
    hash = models.TextField()
    version_arr = ArrayField(models.PositiveSmallIntegerField(), max_length=3, default=list, blank=True)

    class Meta:
        abstract = True

    @property
    def version(self) -> str:
        """ Возвращает версию в виде строки """
        return int_arr_to_str(self.version_arr)

    @property
    def changed_by_user(self) -> str:
        # noinspection PyUnresolvedReferences
        return self.user.get('username', '')


class VersionRawJsonModel(VersionModel):
    """ Базовый класс для версий какой-либо модели с raw_json """
    raw_json = JSONField(default=dict, blank=True)
    raw_hash = models.TextField(default='', blank=True)

    class Meta:
        abstract = True


class VersionedModelMixin:
    """ Добавляет методы для работы с версиями модели """
    @property
    def json(self) -> dict:
        return {}

    @property
    def _versions_set(self):
        """ Возвращает set связанной модели по related_name """
        return getattr(self, 'versions')

    @property
    def hash(self) -> str:
        """ Возвращает хеш json  """
        return get_json_hash(self.json)

    def get_version_by_pattern(
            self, version: Optional[VersionModel], version_pattern_attr: Optional[str] = None) -> VersionModel:
        """ Возврашает инстанс версии модели по шаблону """
        if version:
            return version
        if not version_pattern_attr:
            return self.last_version
        return self._versions_set.annotate(
            exact_version=Func(F('version_arr'), Value('.'), function='array_to_string')
        ).filter(
            exact_version__regex=version_regex(version_pattern_attr)
        ).order_by('-version_arr').first()

    @property
    def version_list(self) -> List[str]:
        """ Возвращает список версий в виде строк """
        return [v.version for v in self._versions_set.all()]

    @property
    def last_version(self) -> Optional[VersionModel]:
        """ Возвращает инстанс последней версии """
        versions = self._versions_set.all()
        return max(versions, key=lambda x: x.version_arr) if versions else None

    @property
    def is_version_changed(self) -> bool:
        """ Возвращает признак изменения json модели по сравнению с посделней сохраненной версией """
        if self.last_version and self.hash == self.last_version.hash:
            return False
        return True

    @property
    def next_version_str(self) -> str:
        """ Возвращает строку со следующей версией, инкрементированной по минору """
        last_version = self.last_version
        if last_version and last_version.version_arr:
            # noinspection PyUnresolvedReferences
            last_version.version_arr[-1] += 1
            return int_arr_to_str(last_version.version_arr)
        else:
            return START_VERSION

    def get_json_by_version(self, version: Optional[str] = None, json_field_name: str = 'json',
                            compare_with_version: str = None) -> dict:
        """ Возвращает json версии по строке версии """
        if version:
            try:
                version_instance = self._versions_set.get(version_arr=str_to_int_arr(version))
            except self._versions_set.model.DoesNotExist:
                version_instance = None
        else:
            version_instance = self.last_version

        if version_instance:
            model_version_json = copy(getattr(version_instance, json_field_name, {}))
            if not model_version_json:
                model_version_json['error'] = THERE_IS_NO_VERSION_DATA
            model_version_json['version'] = version_instance.version
            model_version_json['version_create_dt'] = version_instance.create_dt
            model_version_json['version_changed_by_user'] = version_instance.changed_by_user
            if compare_with_version:
                json_diff = {'compare_with_version': compare_with_version}
                try:
                    compare_version_instance = self._versions_set.get(version_arr=str_to_int_arr(compare_with_version))
                except self._versions_set.model.DoesNotExist:
                    json_diff['err'] = DOES_NOT_EXIST_VERSION.format(compare_with_version)
                else:
                    origin_version_json = getattr(version_instance, json_field_name)
                    compare_version_json = getattr(compare_version_instance, json_field_name)
                    json_diff['diff'] = get_objs_diff(compare_version_json or {}, origin_version_json)
                    json_diff['changed_by_user'] = compare_version_instance.changed_by_user
                model_version_json['version_diff'] = json_diff
        else:
            model_version_json = {}

        return model_version_json

    @transaction.atomic
    def create_or_update_version(self, version_str: str = None) -> Tuple[bool, VersionModel]:
        """ Создает или обновляет версию """
        model_version, is_created = self._versions_set.get_or_create(
            version_arr=str_to_int_arr(version_str or self.next_version_str),
        )
        model_version.user = get_user_info()
        model_version = self._patch_model_version(model_version)
        model_version.save()

        return is_created, model_version

    def _patch_model_version(self, model_version: VersionModel) -> VersionModel:
        """ Модификация полей версии """
        model_version.json = self.json
        model_version.hash = self.hash
        return model_version


class VersionedRawModelMixin(VersionedModelMixin):
    """ Добавляет методы для работы с версиями модели """
    versions = None

    @property
    def raw_json(self) -> dict:
        return {}

    @property
    def raw_hash(self) -> str:
        """ Возвращает хеш json отнаследованной модели """
        return get_json_hash(self.raw_json)

    def _patch_model_version(self, model_version: VersionRawJsonModel):
        """ Модификация полей версии """
        model_version = super(VersionedRawModelMixin, self)._patch_model_version(model_version)
        model_version.raw_json = self.raw_json
        model_version.raw_hash = self.raw_hash
        return model_version

    @property
    def is_raw_version_changed(self) -> bool:
        """ Возвращает признак изменения raw_json модели по сравнению с посделней сохраненной версией """
        last_version: Optional[VersionRawJsonModel] = self.last_version
        if last_version and self.raw_hash == last_version.raw_hash:
            return False
        return True


class RelObjVersionMixin:
    """
        Добавляет возможность получить версию у связанной модели
        Например: self._get_rel_obj_version('graph')
    """
    def _get_rel_obj_version(self, rel_obj_field_name: str):
        """ Возврашает инстанс версии указанной в моделе (фиксированную, последнюю или по шаблону) """
        rel_obj = getattr(self, rel_obj_field_name)
        obj_version = getattr(self, f'{rel_obj_field_name}_version')
        obj_version_pattern = getattr(self, f'{rel_obj_field_name}_version_pattern')
        return rel_obj.get_version_by_pattern(obj_version, obj_version_pattern) if rel_obj else None


def create_version_model_class(
        module_name: str, model_name: str, version_parent_model: Type[VersionModel]) -> VersionModel:
    lower_name = model_name.lower()
    capitalize_name = model_name.capitalize()
    meta_fields = dict(
        verbose_name=f'{lower_name} version',
        verbose_name_plural=f'{lower_name} versions',
        unique_together=(f'{lower_name}_id', 'version_arr'),
        indexes=[models.Index(fields=(f'{lower_name}_id', 'version_arr'))],
        ordering=(f'{lower_name}_id', 'version_arr'),
    )

    # create class Meta
    class_meta = class_factory(module_name, 'Meta', (version_parent_model.Meta,), {})
    for k, v in meta_fields.items():
        setattr(class_meta, k, v)

    # create class VersionModel
    class_version = class_factory(module_name, f'{capitalize_name}Version', (version_parent_model,), {
        lower_name: models.ForeignKey(capitalize_name, related_name='versions', on_delete=models.CASCADE),
        'Meta': class_meta,
    })
    class_version.__str__ = lambda self: f'{getattr(self, lower_name)}:{self.version}'

    return class_version
