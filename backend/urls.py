from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('question',views.ask_question,name='question'),
    path('save',views.question,name='save_question'),
    path('question/<int:id>', views.QuestionDetail, name='question_detail'),
    path('question/answer/<int:id>', views.Answer, name='ans'),
    path('fix',views.fixes,name='save_fix'),
    path('upvotes/<int:ans_id>',views.upvote,name='upvote')
]