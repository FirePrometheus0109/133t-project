from rest_framework import serializers

from leet import serializers as base_serializers
from letter_template import models
from letter_template import validators
from letter_template import utils


class LetterTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LetterTemplate
        fields = (
            'id',
            'name',
            'subject',
            'body',
            'modified_at',
            'event_type'
        )

    def validate_name(self, name):
        validators.validate_name_letter_template(
            self.instance,
            self.context['company'],
            name)
        return name

    def validate(self, attrs):
        if self.instance is None:
            validators.validate_count_of_existing_templates(
                self.context['company'])
        return attrs

    def create(self, validated_data):
        validated_data['company'] = self.context['company']
        return super().create(validated_data)

    def save(self, **kwargs):
        event_type = self.validated_data.get('event_type')
        utils.delete_default_letter_template_for_event(
            self.context['company'], event_type)
        return super().save(**kwargs)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if result['event_type']:
            result['event_type'] = base_serializers.EventTypeSerializer(
                instance.event_type).data
        return result
