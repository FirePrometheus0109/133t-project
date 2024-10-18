from rest_framework import serializers

from geo import models
from geo import validators


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = (
            'id',
            'name'
        )


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = (
            'id',
            'name',
            'abbreviation'
        )


class CityAddressSerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = models.City
        fields = (
            'id',
            'name',
            'state'
        )


class CitySerializer(CityAddressSerializer):

    class Meta(CityAddressSerializer.Meta):
        fields = CityAddressSerializer.Meta.fields + (
            'timezone',
        )


class ZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zip
        fields = (
            'id',
            'code'
        )


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = (
            'id',
            'address',
            'country',
            'city',
            'zip',
        )

    def validate(self, attrs):
        zip_code = attrs.get('zip')
        city = attrs.get('city')
        validators.validate_zip_belongs_to_the_city(zip_code, city)
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['country'] = CountrySerializer(instance.country).data
        ret['city'] = CityAddressSerializer(instance.city).data
        ret['zip'] = ZipSerializer(instance.zip).data
        return ret


class AddressRequiredSerializer(AddressSerializer):

    """Because model 'Address' does not have required fields,
    Set all fields as required in serializer
    for creating company address and event location.
    NOTE (i.bogretsov): this does not work with method PATCH
    """

    address = serializers.CharField(required=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=models.Country.objects.all(),
        required=True
    )
    city = serializers.PrimaryKeyRelatedField(
        queryset=models.City.objects.all(),
        required=True
    )
    zip = serializers.PrimaryKeyRelatedField(
        queryset=models.Zip.objects.all(),
        required=True
    )

    class Meta:
        model = models.Address
        fields = (
            'id',
            'address',
            'country',
            'city',
            'zip'
        )


class AddressWithCityTimezoneSerializer(AddressRequiredSerializer):

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['city'] = CitySerializer(instance.city).data
        return ret
