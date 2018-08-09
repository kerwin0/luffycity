from django.conf.urls import url
from api.views import course
from api.views import shoppingcar
urlpatterns = [
    url(r'^course/$', course.CoursesView.as_view()),
    url(r'^shoopingcar/$', shoppingcar.ShoopingCarView.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy', 'put': 'update'})),
    url(r'^course/(?P<pk>\d+)/$', course.CourseDetailView.as_view()),
    url(r'^degreeteacher/$', course.DegreeAndTeacherView.as_view()),  # a学位课名称以及授课老师api
    url(r'^coursesalry/$', course.CourseSalryView.as_view()),  # a学位课名称以及授课老师api
    url(r'^degreecourse/$', course.DegreeCourseView.as_view()),  # c所有的學位課的模塊api
    url(r'^coursemodel/(?P<pk>\d+)/$', course.CourseModelView.as_view()),  # d. 查看学位课id对应的所有模块名称api
    url(r'^courselist/(?P<pk>\d+)/$', course.CourseListView.as_view()),  # e.获取专题课id對應的并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_coursesapi
    url(r'^coursequestion/(?P<pk>\d+)/$', course.CourseQuestionView.as_view()),  # f.获取专题课對應的课程相关的所有常见问题
    url(r'^courseoutline/(?P<pk>\d+)/$', course.CourseOutlineView.as_view()),  # g.获取专题课對應的课程相关的课程大纲
    url(r'^courseoutline/(?P<pk>\d+)/$', course.CourseOutlineView.as_view()),  # h.获取专题课對應的课程相关的所有章节
    url(r'^coursechapter/(?P<pk>\d+)/$', course.CourseChapterView.as_view()),  # h.获取专题课對應的课程相关的所有章节
]


