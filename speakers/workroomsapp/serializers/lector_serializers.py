from rest_framework import serializers

from workroomsapp.models import Domain, Lecture, User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = User
      fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
  # user = UserSerializer(many=True)
  class Meta:
      model = Lecture
      fields = '__all__'

  def create(self, validated_data):
    # Lecture.lecturers.add(user_id=User.objects.get(id = request.user.pk), lecture_id=lec) # Записываем связь лектора и лекции в бд
    user_data = validated_data.pop('user')
    lecture_data = Lecture.objects.create(**validated_data)
    Lecture.objects.create(user=user_data, **lecture_data)
    return lecture_data
    
    return Lecture.objects.create(**validated_data)

  def update(self, instance, validated_data):
    instance.id = validated_data.get('id', instance.id)
    instance.name = validated_data.get('name', instance.name)
    instance.hall = validated_data.get('hall', instance.hall)
    instance.date = validated_data.get('date', instance.date)
    instance.duration = validated_data.get('duration', instance.duration)
    instance.description = validated_data.get('description', instance.description)
    instance.lecturer_name = validated_data.get('lecturer_name', instance.lecturer_name)
    instance.domain = validated_data.get('domain', instance.domain)
    instance.save()
    return instance

class LecturesDataSerializer(serializers.ModelSerializer):
  class Meta:
      model = Lecture
      fields = ['id','name']

class LectorLecturesCommunicationSerializer(serializers.ModelSerializer):
  lecture = LecturesDataSerializer(source='lecturers')
  class Meta:
    model = Lecture
    fields = ['lecture']