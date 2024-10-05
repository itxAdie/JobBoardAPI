from datetime import datetime

from rest_framework.serializers import ModelSerializer, CharField, DateField, ImageField, ValidationError

from resume_control.models import PersonalModel


class PersonalModelSerializerMeta(ModelSerializer):
    class Meta:
        model = PersonalModel
        ref_name = 'PersonalModelSerializer'
        fields = [
            'first_name',
            'last_name',
            'about_me',
            'date_of_birth',
            'nationality',
            'city',
            'state',
            'country',
        ]


class PersonalModelSerializer:
    class List(PersonalModelSerializerMeta):
        class Meta(PersonalModelSerializerMeta.Meta):
            fields = PersonalModelSerializerMeta.Meta.fields + [
                'id',
                'resume',
                'resume_picture',
                'created_by',
                'created_at',
                'updated_by',
                'updated_at',
            ]

    class Write(PersonalModelSerializerMeta):
        about_me = CharField(allow_blank=True)
        nationality = CharField(allow_blank=True)
        city = CharField(allow_blank=True)
        state = CharField(allow_blank=True)
        country = CharField(allow_blank=True)

        class Meta(PersonalModelSerializerMeta.Meta):
            fields = PersonalModelSerializerMeta.Meta.fields

    class UpdateImage(PersonalModelSerializerMeta):
        resume_picture = ImageField(required=True)

        class Meta(PersonalModelSerializerMeta.Meta):
            fields = [
                'resume_picture',
            ]
