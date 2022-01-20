from rest_framework import serializers

from workroomsapp.models import Domain, Lecture, User, LectureHall
      

class LectureHallSerializer(serializers.ModelSerializer):
  hall_id = serializers.IntegerField(source = 'id')
  class Meta:
      model = LectureHall
      fields = '__all__'

class DomainSerializer(serializers.ModelSerializer):
  domain_id = serializers.IntegerField(source = 'id')
  class Meta:
      model = Domain
      fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField(source = 'id')
  class Meta:
    model = User
    fields = (
      'user_id',
      'email',
    )

class LectureSerializer(serializers.ModelSerializer):
  lecturers = UserSerializer(many=True, required = False)
  hall = LectureHallSerializer(required = False)
  domain = DomainSerializer(many=True, required = False)
  class Meta:
      model = Lecture
      fields = '__all__'

  def create(self, validated_data):
      lecture = Lecture.objects.create(**validated_data)
      lecture.lecturers.add(User.objects.get(id=self.context.user.pk))
      return lecture

class LectorLecturesSerializer(serializers.ModelSerializer):
  lecture_id = serializers.IntegerField(source = 'id')
  class Meta:
    model = Lecture
    fields = ['lecture_id','name']