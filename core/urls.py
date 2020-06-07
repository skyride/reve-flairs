from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [
    url(r'^$', views.all_top100_stats, name="home"),
    url(r'^alliances/$', views.alliance_stats, name="alliances"),
    url(r'^corps/$', views.corp_stats, name="corps"),
    url(r'^generics/$', views.generic_stats, name="generics"),

    #url(r'admin/$', views.admin, name="admin")
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
