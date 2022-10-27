from django.urls import path
from . import views

app_name = "reviews"


urlpatterns = [
    path('', views.index, name='index'),
    path("<int:review_pk>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/comment_delete/', views.comment_delete, name='comment_delete'),
]
