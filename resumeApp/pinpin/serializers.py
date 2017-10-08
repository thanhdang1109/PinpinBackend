from rest_framework import serializers
from resumeApp.pinpin.models import Country, State, City, UserProfile


class CountrySerializer(serializers.Serializer):
    def __init__(self):
        pass
