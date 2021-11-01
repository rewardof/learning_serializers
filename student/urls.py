from django.urls import path, include
from rest_framework.routers import DefaultRouter
from student import views

router = DefaultRouter()
router.register('student', views.StudentViewSet, basename='student')
# router.register('faculty', views.CustomerViewSet, basename='faculty')
# router.register('mark', views.PurchaseViewSet, basename='mark')
# router.register('subject', views.PurchaseViewSet, basename='subject')
# router.register('student_subjects', views.PurchaseViewSet, basename='student_subjects')
# router.register('teacher', views.PurchaseViewSet, basename='teacher')


urlpatterns = [
    path('', include(router.urls)),
    path('student/<int:id>/', views.StudentDetailApiView.as_view(), name='student-detail'),
    path('student2/', views.SecondStudentApiView.as_view(), name='student2-list'),
    path('faculty/', views.FacultyListApiView.as_view(), name='faculty-list'),
    path('faculty/<int:pk>/', views.FacultyDetailApiView.as_view(), name='faculty-detail'),
    path('marks/', views.MarkListApiView.as_view(), name='marks-list'),
    path('marks/<int:pk>/', views.MarkDetailApiView.as_view(), name='mark-detail'),
    path('subjects/', views.SubjectListApiView.as_view(), name='subjects-list'),
    path('subjects/<int:pk>/', views.SubjectDetailApiView.as_view(), name='subject-detail'),
    path('high_score/', views.high_score, name='high-score-list'),
]
