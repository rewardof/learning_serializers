from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import StudentSerializer, FacultySerializer, MarkSerializer, SubjectSerializer, \
    SecondStudentSerializer, HighScoreSerializer
from .models import Student, Subject, StudentSubjects, Mark, Faculty, Teacher, HighScore
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

    #
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
