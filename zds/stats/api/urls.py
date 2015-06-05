# coding: utf-8

from django.conf.urls import patterns, url

from zds.stats.api.views import StatContentListAPI, StatContentDetailAPI, StatSourceContentListAPI, StatSourceContentDetailAPI

urlpatterns = patterns('',
                        url(r'^(?P<content_type>.+)/(?P<content_id>[0-9]+)/visites/$', StatContentDetailAPI.as_view(), name='api-stats-details-content-visits'),
                        url(r'^(?P<content_type>.+)/visites/$', StatContentListAPI.as_view(), name='api-stats-list-content-visits'),
                        url(r'^(?P<content_type>.+)/(?P<content_id>[0-9]+)/visites/sources/$', StatSourceContentDetailAPI.as_view(), name='api-stats-details-source-content-visits'),
                        url(r'^(?P<content_type>.+)/visites/sources/$', StatSourceContentListAPI.as_view(), name='api-stats-list-source-content-visits'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/plateformes$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/continents$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/continents/pays$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/continents/pays/villes$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/pays$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/pays/villes$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/villes$', StatContentDetailAPI.as_view(), name='api-member-profile'),
                        #url(r'^contenus/(?P<content_type>.+)/(?P<content_id>[0-9]+)/stats/visites/geo/continents$', StatContentDetailAPI.as_view(), name='api-member-profile'),
)