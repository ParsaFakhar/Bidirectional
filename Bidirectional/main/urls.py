from django.urls import path, include
from . import views
import debug_toolbar

urlpatterns = [
    path('', views.Indexed.as_view(), name='index'),
    path('posted/', views.GetMyPost.as_view(), name='posted'),
    path('bfs/', views.BFS.as_view(), name='bfs'),
    # path('__debug__', include(debug_toolbar.urls)),

]