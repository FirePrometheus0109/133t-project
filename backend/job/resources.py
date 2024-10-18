from import_export import resources
from import_export import fields

from job import models


class SkillResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='skill')

    class Meta:
        model = models.Skill
        import_id_fields = ['name']
        fields = ('name', 'description', 'type')
