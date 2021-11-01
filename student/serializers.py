from collections import OrderedDict

from rest_framework import serializers
from .models import Student, Teacher, Mark, Faculty, StudentSubjects, Subject, StudentProfile, HighScore, Skills


class SKillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('name',)


class StudentProfileSerializer(serializers.ModelSerializer):
    skills = SKillSerializer()

    class Meta:
        model = StudentProfile
        fields = ('image', 'skills')

    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    # faculty = serializers.SlugRelatedField(queryset=Faculty.objects.all(), slug_field='name')
    # url = serializers.HyperlinkedIdentityField(view_name="student-detail")
    # faculty = serializers.HyperlinkedRelatedField(view_name='faculty-detail', lookup_field='pk')
    faculty = serializers.SlugRelatedField(queryset=Faculty.objects.all(), slug_field='name')
    studentprofile = StudentProfileSerializer()

    class Meta:
        model = Student
        fields = (
            'id', 'url', 'email', 'first_name', 'last_name', 'faculty', 'student_id', 'interests', 'studentprofile')

    def create(self, validated_data):
        print(validated_data)
        student_profile = validated_data.pop('studentprofile')
        print(student_profile)
        skills = student_profile.pop('skills')
        print(student_profile)
        skills = Skills.objects.create(category=skills['category'], name=skills['name'])
        request = self.context.get('request')
        student = Student.objects.create(**validated_data)
        student_profile = StudentProfile.objects.create(image=student_profile['image'], student=student, skills=skills)
        return student

    def update(self, instance, validated_data):
        # print(self.context.get_request())
        new_student_profile = validated_data.pop('studentprofile')
        print(new_student_profile)
        student_profile = StudentProfile.objects.get(student=instance)
        print(student_profile)
        student_profile.image = new_student_profile['image']
        student_profile.save()
        return super(StudentSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(StudentSerializer, self).to_representation(instance)
        # data = {
        #     # 'id': instance['id'],
        #     'email': instance['email'],
        #     'student_profile': instance['studentprofile']
        # }
        # print(data)
        return data

class StudentListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        students = [Student(**item) for item in validated_data]
        return Student.objects.bulk_create(students)


class SecondStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ('email', 'first_name', 'last_name', 'faculty')
        fields = '__all__'
        list_serializer_class = StudentListSerializer


class MarkSerializer(serializers.ModelSerializer):
    # this default for url
    url = serializers.HyperlinkedIdentityField(view_name='mark-detail', lookup_field='pk')

    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # student = serializers.RelatedField(source='student.first_name', read_only=True)
    # student = serializers.HyperlinkedRelatedField(view_name='student-detail', queryset=Student.objects.all())
    # This field is read_only
    # subject = serializers.HyperlinkedRelatedField(view_name='subject-detail', queryset=Subject.objects.all())
    #  this field is write-read field
    subject = serializers.SlugRelatedField(queryset=Subject.objects.all(), slug_field='name')
    # student = serializers.SlugRelatedField(queryset=Student.objects.all(), slug_field='full_name')
    student = serializers.HyperlinkedRelatedField(view_name='student-detail', queryset=Student.objects.all(),
                                                  default=serializers.CurrentUserDefault())

    class Meta:
        model = Mark
        fields = ('url', 'student', 'subject', 'mark')
        # read_only_fields = ('url',) this for read only fields
        extra_kwargs = {
            'url': {'view_name': 'mark-detail', 'lookup_field': 'pk'},
        }

    def to_representation(self, instance):
        data = super(MarkSerializer, self).to_representation(instance)
        # self.fields['subjects'] = SubjectSerializer()
        # # data = {
        # #     'data': data,
        # # }
        return data


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    # modeldagi name nomini subject nomiga o'zgartirish mumkin
    subject = serializers.CharField(source='name')

    class Meta:
        model = Subject
        # fields = '__all__'
        fields = ('url', 'subject',)


class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }

    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')

        # Perform the data validation.
        if not score:
            raise serializers.ValidationError({
                'score': 'This field is required.'
            })
        if not player_name:
            raise serializers.ValidationError({
                'player_name': 'This field is required.'
            })
        if len(player_name) > 10:
            raise serializers.ValidationError({
                'player_name': 'May not be more than 10 characters.'
            })

        # Return the validated values. This will be available as
        # the `.validated_data` property.
        return {
            'score': int(score),
            'player_name': player_name
        }

    def create(self, validated_data):
        return HighScore.objects.create(**validated_data)
