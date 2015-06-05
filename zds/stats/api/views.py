# -*- coding: utf-8 -*-

from rest_framework import status, exceptions, filters
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListCreateAPIView, \
    get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.etag.decorators import etag
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

from zds.stats.models import Log
from zds.tutorial.models import Tutorial, Chapter, Part
from zds.article.models import Article
from zds.stats.api.serializers import StatTutorialSerializer, StatPartSerializer, StatChapterSerializer, StatArticleSerializer, StatSourceContentSerializer

class PagingStatContentListKeyConstructor(DefaultKeyConstructor):
    pagination = bits.PaginationKeyBit()
    search = bits.QueryParamsKeyBit(['search', 'ordering'])
    list_sql_query = bits.ListSqlQueryKeyBit()
    unique_view_id = bits.UniqueViewIdKeyBit()

class DetailKeyConstructor(DefaultKeyConstructor):
    format = bits.FormatKeyBit()
    language = bits.LanguageKeyBit()
    retrieve_sql_query = bits.RetrieveSqlQueryKeyBit()
    unique_view_id = bits.UniqueViewIdKeyBit()


def get_content_serialiser(content_type):
    if content_type == 'tutoriel':
        return StatTutorialSerializer
    elif content_type == 'partie':
        return StatPartSerializer
    elif content_type == 'chapitre':
        return StatChapterSerializer
    elif content_type == 'article':
        return StatArticleSerializer
    else:
        raise exceptions.NotFound()


class StatContentListAPI(ListCreateAPIView):
    filter_backends = (filters.OrderingFilter, filters.OrderingFilter)
    list_key_func = PagingStatContentListKeyConstructor()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return get_content_serialiser(self.kwargs.get("content_type"))

    def get_queryset(self):
        if self.kwargs.get("content_type") == 'tutoriel':
            return Tutorial.objects.all().filter(sha_public__isnull=False)
        elif self.kwargs.get("content_type") == 'partie':
            return Part.objects.all().filter(tutorial__sha_public__isnull=False)
        elif self.kwargs.get("content_type") == 'chapitre':
            return Chapter.objects.all().filter(part__tutorial__sha_public__isnull=False)
        elif self.kwargs.get("content_type") == 'article':
            return Article.objects.all().filter(sha_public__isnull=False)
        else:
            raise exceptions.NotFound()

class StatContentDetailAPI(RetrieveAPIView):
    obj_key_func = DetailKeyConstructor()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return get_content_serialiser(self.kwargs.get("content_type"))

    def get_object(self):

        if self.kwargs.get("content_type") == 'tutoriel':
            return Tutorial.objects.all().filter(id=self.kwargs.get("content_id"), sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'partie':
            return Part.objects.all().filter(id=self.kwargs.get("content_id"), tutorial__sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'chapitre':
            return Chapter.objects.all().filter(id=self.kwargs.get("content_id"), part__tutorial__sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'article':
            return Article.objects.all().filter(id=self.kwargs.get("content_id"), sha_public__isnull=False).first()
        else:
            raise exceptions.NotFound()

def get_app_from_content_type(content_type):
	if content_type=="tutoriel":
		return "tutorial"
	elif content_type=="article":
		return "article"
	elif content_type=="chapitre":
		return "chapter"
	elif content_type=="partie":
		return "part"
	else:
		return None

class StatSourceContentListAPI(ListCreateAPIView):
    filter_backends = (filters.OrderingFilter, filters.OrderingFilter)
    list_key_func = PagingStatContentListKeyConstructor()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StatSourceContentSerializer

    def get_queryset(self):
    	app_name = get_app_from_content_type(self.kwargs.get("content_type"))
        return Log.objects.all().filter(content_type=app_name).distinct()

class StatSourceContentDetailAPI(RetrieveAPIView):
    obj_key_func = DetailKeyConstructor()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StatSourceContentSerializer

    def get_object(self):

        if self.kwargs.get("content_type") == 'tutoriel':
            return Tutorial.objects.all().filter(id=self.kwargs.get("content_id"), sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'partie':
            return Part.objects.all().filter(id=self.kwargs.get("content_id"), tutorial__sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'chapitre':
            return Chapter.objects.all().filter(id=self.kwargs.get("content_id"), part__tutorial__sha_public__isnull=False).first()
        elif self.kwargs.get("content_type") == 'article':
            return Article.objects.all().filter(id=self.kwargs.get("content_id"), sha_public__isnull=False).first()
        else:
            raise exceptions.NotFound()