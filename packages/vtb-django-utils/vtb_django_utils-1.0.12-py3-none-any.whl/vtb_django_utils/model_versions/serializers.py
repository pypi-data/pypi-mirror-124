from abc import ABCMeta

from rest_framework import serializers


class LastVersionSerializer(serializers.ModelSerializer):
    __metaclass__ = ABCMeta
    last_version = serializers.SerializerMethodField()
    version_list = serializers.SerializerMethodField()

    class Meta:
        model = None

    @staticmethod
    def get_last_version(obj):
        return obj.last_version.version if obj.last_version else ''

    @staticmethod
    def get_version_list(obj):
        return obj.version_list
