from rest_framework import serializers

from workroomsapp.models import Domain, Lecture, User


# class LectureHallSerializer(serializers.ModelSerializer):
#     hall_id = serializers.IntegerField(source='id')
#
#     class Meta:
#         model = LectureHall
#         fields = '__all__'


class DomainModelSerializerBase(serializers.ModelSerializer):
    """DomainSerializerBase - для сохранения данных сферы деятельности"""

    # domain_id = serializers.IntegerField(source='id')

    class Meta:
        model = Domain
        fields = '__all__'


class DomainModelSerializer(serializers.ModelSerializer):
    """DomainSerializer - для вывода данных сферы деятельности"""
    domain_id = serializers.IntegerField(source='id')

    class Meta:
        model = Domain
        # fields = '__all__'
        # fields = ('id', 'name', 'code',)
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id')

    class Meta:
        model = User
        fields = (
            'user_id',
            'email',
        )


class LectureSerializer(serializers.ModelSerializer):
    lecturers = UserSerializer(many=True, required=False)
    # hall = LectureHallSerializer(required=False)
    # domain = DomainSerializer(many=True, required = False)
    domain = DomainModelSerializer(many=True, required=False)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Lecture
        fields = '__all__'

    def create(self, validated_data):
        lecture = Lecture.objects.create(**validated_data)
        lecture.lecturers.add(User.objects.get(id=self.context.user.pk))
        return lecture


class LectorLecturesSerializer(serializers.ModelSerializer):
    lecture_id = serializers.IntegerField(source='id')

    class Meta:
        model = Lecture
        fields = ['lecture_id', 'name']
