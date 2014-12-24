from django.conf.urls import *

from tilescache.views import TilescacheView


urlpatterns = patterns('',
    (r'', TilescacheView.as_view()),
)
