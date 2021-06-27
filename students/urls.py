from django.urls import path
from .views import *

urlpatterns = [
    #account
    path('info', StudentInfoView.as_view()),
    path('class', ClassroomInfoView.as_view()),
    path('achievements', AchievementListView.as_view()),

    #timetable1
    path('timetables', TimeTableView.as_view()),

    #grade
    path('grades', GradeListView.as_view()),

    #conduct
    path('conducts', ConductListView.as_view()),

    path('documents', StudyDocumentView.as_view()),
    path('download/<int:pk>', download),

]
