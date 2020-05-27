from django.urls import path
from . import views
urlpatterns = [
    path('', views.taskList, name='task-list'),
    path('task/<int:id>', views.taskView, name="task-view"),
    path('newtask/', views.newTask, name="new-task"),
    path('task/edit/<int:id>', views.editTask, name="edit-task"),
    path('task/delete/<int:id>', views.deleteTask, name="delete-task"),
    path('task/done/<int:id>', views.doneTask, name="done-task"),
]