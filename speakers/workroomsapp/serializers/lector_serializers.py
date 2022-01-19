from rest_framework import serializers

from workroomsapp.models import Domain, Lecture


class LectureSerializer(serializers.ModelSerializer):
  class Meta:
      model = Lecture
      fields = '__all__'

  def create(self, validated_data):
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
  lecture = LecturesDataSerializer(source='lectureId')
  class Meta:
    model = Lecture
    fields = ['lecture']