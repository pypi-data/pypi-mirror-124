# Утилитарный пакет для работы с django

## Добавление бекенда аутентификации через Keycloak

В настройки django добавьте переменную AUTHENTICATION_BACKENDS с указанием класса 'KeycloakBackend'

```
AUTHENTICATION_BACKENDS = (
    'vtb_django_utils.backends.KeycloakBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

## Добавление возможности аутентификации с токеном Keycloak
Обратите внимание, что если токен "протух", то выдается ошибка 403. 
Если вы используете пакет межсервисного взаимодействия vtb-http-interaction, 
то в нем не предусмотрено получение нового токена при ошибке 403, только 401. Неправильно делать вызовы сервис->сервис. 
Запрос должен идти через Kong с использованием плагина jwt-keycloak.
```
authentication_classes = (SessionAuthentication, KeycloakAuthentication)
```

## Для добавления функционала версий для сущности нужно:
#### 1. Добавить модель версий в БД:
```python
ActionVersion = create_version_model_class(__name__, 'Action', VersionModel)
```

#### 2. Добавить миксин VersionedModelMixin к основной модели:
```python
class Action(VersionedModelMixin, RelObjVersionMixin, LifecycleModelMixin, models.Model):
```

#### 3. Добавить миксин VersionMixin в админку:
```python
class ActionAdmin(ImportExportMixin, CopyMixin, VersionMixin, admin.ModelAdmin):
```

#### 4. Сериализатор отнаследовать от LastVersionSerializer:
```python
class ActionSerializer(LastVersionSerializer):
```

#### 5. Добавить миксин VersionMixin во вьюсет:
```python
class ActionViewSet(SearchMixin, ContextMixin, RetrieveJsonMixin, FilterArrayMixin, ImportExportMixin,
                    InstanceCopyMixin, VersionMixin, viewsets.ModelViewSet):
```
