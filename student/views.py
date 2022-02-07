from datetime import datetime, timedelta

from django.http import HttpRequest

from django.db.models import Count, Avg, Case, When, Subquery, OuterRef, Max, Min
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import StudentSerializer, FacultySerializer, MarkSerializer, SubjectSerializer, \
    SecondStudentSerializer, HighScoreSerializer, StudentSmallSerializer, UserLevelSerializer, \
    StudentWithSubjectSerializer, TeacherSerializer
from .models import Student, Subject, StudentSubjects, Mark, Faculty, Teacher, HighScore, StudentLevel
from rest_framework import permissions


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()



class SecondStudentApiView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = SecondStudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, *args, **kwargs):
        now = datetime.now().date() - timedelta(days=3)

        number_students = Student.objects.aggregate(
            number=Count('pk')
        )
        student_with_avg_mark = Student.objects.annotate(
            avg_mark=Avg('student_marks__mark'))
        student_with_avg_mark = StudentSmallSerializer(student_with_avg_mark, many=True).data

        student_registerd_nowadays = Student.objects.filter(entry_date__gt=now, )

        payload = {
            'number_students': number_students,
            'students_with_marks': student_with_avg_mark
        }
        return Response(payload, status=status.HTTP_200_OK)


class StudentTeacherLevelsListView(generics.ListCreateAPIView):
    serializer_class = UserLevelSerializer
    queryset = StudentLevel

    # def get(self, *args, **kwargs):
    #     student_levels = StudentLevel.objects.update(
    #         level=Case(
    #             When(
    #                 Subquery(Student.objects.all().annotate(avg_mark=Avg('student_marks__mark')))
    #             )
    #         )
    #     )
    #
    #     Relation.objects.update(
    #         rating=Subquery(
    #             Relation.objects.filter(
    #                 id=OuterRef('id')
    #             ).annotate(
    #                 total_rating=Sum('sign_relations__rating')
    #             ).values('total_rating')[:1]
    #         )
    #     )


class SubjectstudentList(generics.ListCreateAPIView):
    serializer_class = SecondStudentSerializer
    queryset = Subject.objects.all()

    # def get(self, *args, **kwargs):
    #     subject_students = Subject.objects.annotate(number_students=Count())


class StudentSubjectsList(generics.ListCreateAPIView):
    serializer_class = StudentWithSubjectSerializer
    queryset = Student.objects.all()

    def get(self, *args, **kwargs):
        data = Student.objects.values('pk', 'first_name', 'last_name').annotate(
            mark=Subquery(
                Mark.objects.filter(student=OuterRef('pk')).values('mark')[:1]
            )
        )
        test = Mark.objects.filter(student=1).values('mark')

        teacher_students = Teacher.objects.annotate(students='students__student')
        print(teacher_students)

        min_mark_student = Student.objects.all().aggregate(
            min_mark_student=Min('student_marks__mark'))

        payload = {
            'data': data,
            'test': test,
            'min_mark_student': min_mark_student,
            'teacher_students': teacher_students
        }
        return Response(payload, status=status.HTTP_200_OK)


class StudentDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class FacultyListApiView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    lookup_field = 'pk'


class MarkListApiView(generics.ListCreateAPIView):
    # queryset = Mark.objects.all()
    serializer_class = MarkSerializer

    # permission_classes = [permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     pass

    # def get_view_name(self):
    #     pass

    def get_queryset(self):
        return Mark.objects.all()

    def get_parsers(self):
        parsers = super(MarkListApiView, self).get_parsers()
        # print(parsers)
        return parsers

    def get_permissions(self):
        permissions = super(MarkListApiView, self).get_permissions()
        # print(permissions)
        return permissions

    def get_content_negotiator(self):
        content_negotiation = super(MarkListApiView, self).get_content_negotiator()
        # print(content_negotiation)
        return content_negotiation

    def get_serializer_context(self):
        serializer_context = super(MarkListApiView, self).get_serializer_context()
        # print(serializer_context)
        request = serializer_context.get('request')
        # print(request.data)
        # print(request)
        view = serializer_context.get('view')
        # print(view.serializer_class(request.data))
        # print(view.get_queryset())
        return serializer_context

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        # print(args)
        # print(kwargs)
        return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # print(request.data)
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def get_paginated_response(self, data):
    #     pass

    def filter_queryset(self, queryset):
        return queryset.filter(mark__gt=3)


class MarkDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    lookup_field = 'pk'


class SubjectListApiView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    lookup_field = 'pk'


@api_view(['GET', 'POST'])
def high_score(request):
    if request.method == 'GET':
        instance = HighScore.objects.all()
        serializer = HighScoreSerializer(instance, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = HighScoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
