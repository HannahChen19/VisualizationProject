# analytics/urls.py
from django.urls import path
#from .views import upload_csv
from .views import default_view
from .views import player_performance_view
from .views import shooting_performance_view
#from .views import career_length_distribution
#from .views import data_story
#from .views import player_list
#from .views import player_detail
#from .views import chart_data

urlpatterns = [
    #path('upload/', upload_csv, name='upload_csv'),
    path('', default_view, name='default_view'),
    path('default', default_view, name='default_view'),
    path('player_performance', player_performance_view, name='player_performance_view'),
    path('shooting_performance', shooting_performance_view, name='shooting_performance_view'),
    #path('career_length_distribution/', career_length_distribution, name='career_length_distribution'),
    #path('data_story/', data_story, name='data_story'),
    #path('players/', player_list, name='player_list'),
    #path('players/<int:player_id>/', player_detail, name='player_detail'),
    #path('chart-data/', chart_data, name='chart_data'),
    # Define more URLs for analytics and visualization as needed
]


