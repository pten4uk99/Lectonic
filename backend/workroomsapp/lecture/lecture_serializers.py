from rest_framework import serializers

from config.settings import DEFAULT_HOST
from workroomsapp.calendar.utils import get_model_from_attrs
from workroomsapp.lecture.validators import LectureDatetimeValidator
from workroomsapp.models import Lecture, Respondent


class LectureAsLecturerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    svg = serializers.IntegerField(min_value=1)
    domain = serializers.ListField()
    datetime = serializers.ListField()
    hall_address = serializers.CharField(required=False)
    equipment = serializers.CharField(required=False)
    type = serializers.CharField()
    cost = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = [
            'name',
            'svg',
            'domain',
            'hall_address',
            'equipment',
            'type',
            'cost',
            'description',
        ]

    def get_creator_obj(self):
        lecturer = self.context['request'].user.person.lecturer
        if not lecturer:
            raise serializers.ValidationError('Пользователь не является лектором')
        return lecturer

    def validate_datetime(self, datetime_list):
        lecture_id = self.context['request'].data.get('id')
        validator = LectureDatetimeValidator(self.get_creator_obj(), edit=bool(lecture_id))
        return validator.validate(datetime_list)

    def create(self, validated_data):
        return Lecture.objects.create_lecture(
            lecturer=self.get_creator_obj(),
            name=validated_data.get('name'),
            svg=validated_data.get('svg'),
            domain=validated_data.get('domain'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            type=validated_data.get('type'),
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )

    def update(self, lecture, validated_data):
        return Lecture.objects.update_lecture(
            lecture=lecture,
            name=validated_data.get('name'),
            datetime=validated_data.get('datetime'),
            domain=validated_data.get('domain'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            type=validated_data.get('type'),
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )


class LectureAsCustomerSerializer(LectureAsLecturerSerializer):
    listeners = serializers.IntegerField()

    def get_creator_obj(self):
        customer = self.context['request'].user.person.customer
        if not customer:
            raise serializers.ValidationError('Пользователь не является заказчиком')
        return customer

    def create(self, validated_data):
        return Lecture.objects.create_lecture(
            customer=self.get_creator_obj(),
            name=validated_data.get('name'),
            svg=validated_data.get('svg'),
            domain=validated_data.get('domain'),
            datetime=validated_data.get('datetime'),
            hall_address=validated_data.get('hall_address'),
            equipment=validated_data.get('equipment'),
            listeners=validated_data.get('listeners'),
            type=validated_data.get('type'),
            cost=validated_data.get('cost', 0),
            description=validated_data.get('description'),
        )


class LecturesGetSerializer(serializers.ModelSerializer):
    lecture_type = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    hall_address = serializers.StringRelatedField(source='optional.hall_address')
    equipment = serializers.StringRelatedField(source='optional.equipment')
    creator_is_lecturer = serializers.SerializerMethodField()
    creator_user_id = serializers.SerializerMethodField()
    creator_id = serializers.SerializerMethodField()
    creator_first_name = serializers.SerializerMethodField()
    creator_photo = serializers.SerializerMethodField()
    creator_last_name = serializers.SerializerMethodField()
    creator_middle_name = serializers.SerializerMethodField()
    creator_bgc_number = serializers.SerializerMethodField()
    can_response = serializers.SerializerMethodField()
    response_dates = serializers.SerializerMethodField()
    related_person = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            'id',
            'svg',
            'name',
            'lecture_type',
            'dates',
            'domain',
            'hall_address',
            'listeners',
            'description',
            'equipment',
            'cost',
            'can_response',
            'response_dates',
            'related_person',
            'creator_user_id',
            'creator_is_lecturer',
            'creator_id',
            'creator_photo',
            'creator_first_name',
            'creator_last_name',
            'creator_middle_name',
            'creator_bgc_number',
            'can_edit',
        ]

    def get_lecture_type(self, obj):
        return obj.get_type_display()

    def get_domain(self, obj):
        return obj.lecture_domains.all().values_list('domain__name', flat=True).distinct()

    def get_dates(self, obj):
        dates = []
        lecture_requests = obj.lecture_requests.order_by('event__datetime_start').all()
        user = self.context['user']
        lecture_creator = get_model_from_attrs(
            lecture_requests.first().lecture, ['lecturer', 'customer']).person

        for lecture_request in lecture_requests:
            respondents = lecture_request.respondent_obj.filter(confirmed=True)

            if (not respondents.exists() or  # если дата лекции не подтверждена
                    respondents.filter(person=user.person).exists() or  # если пользователь является подтвержденным
                    lecture_creator == user.person):  # если пользователь является создателем лекции

                dates.append({
                    'start': lecture_request.event.datetime_start,
                    'end': lecture_request.event.datetime_end,
                })

        return dates

    def get_creator_is_lecturer(self, obj):
        return bool(obj.lecturer)

    def get_related_person(self, obj):
        query_from = self.context.get('query_from')

        if not query_from:
            return

        person = None

        if get_model_from_attrs(obj, [query_from]):  # проверяем является ли запрашивающий создателем лекции
            lecture_request = obj.lecture_requests.filter(respondent_obj__confirmed=True).first()
            person = lecture_request.respondent_obj.get(confirmed=True).person
        else:
            if obj.lecturer:
                person = obj.lecturer.person
            else:
                person = obj.customer.person

        return {
            'user_id': person.user.pk,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'middle_name': person.middle_name
        }

    def get_creator_id(self, obj):
        if obj.lecturer:
            return obj.lecturer.pk
        else:
            return obj.customer.pk

    def get_creator_first_name(self, obj):
        if obj.customer:
            return obj.customer.person.first_name
        return obj.lecturer.person.first_name

    def get_creator_user_id(self, obj):
        if obj.customer:
            return obj.customer.person.user.pk
        return obj.lecturer.person.user.pk

    def get_creator_photo(self, obj):
        if obj.customer:
            if obj.customer.person.photo:
                return DEFAULT_HOST + obj.customer.person.photo.url
            return ''
        if obj.lecturer.person.photo:
            return DEFAULT_HOST + obj.lecturer.person.photo.url
        return ''

    def get_creator_last_name(self, obj):
        if obj.customer:
            return obj.customer.person.last_name
        return obj.lecturer.person.last_name

    def get_creator_middle_name(self, obj):
        if obj.customer:
            return obj.customer.person.middle_name
        return obj.lecturer.person.middle_name

    def get_creator_bgc_number(self, obj):
        if obj.customer:
            return obj.customer.person.bgc_number
        return obj.lecturer.person.bgc_number

    def get_can_response(self, obj):
        person = self.context['user'].person
        for lecture_request in obj.lecture_requests.all():
            respondent = Respondent.objects.filter(person=person, lecture_request=lecture_request).first()
            if respondent and not (respondent.rejected or respondent.confirmed):
                return False
        return True

    def get_response_dates(self, obj):
        person = self.context['user'].person
        data = []

        for lecture_request in person.responses.filter(lecture=obj):
            respondent = Respondent.objects.get(person=person, lecture_request=lecture_request)
            data.append({
                'date': lecture_request.event.datetime_start,
                'rejected': respondent.rejected,
                'confirmed': respondent.confirmed
            })

        return data

    def get_can_edit(self, lecture):
        if self.get_creator_user_id(lecture) == self.context['user']:
            return lecture.lecture_requests.filter(respondent__obj__confirmed=True).exists()

        return False

