# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from zds.tutorial.models import Tutorial, Chapter, Part
from zds.article.models import Article
from zds.stats.models import Log


class StatContentSerializer(serializers.ModelSerializer):

    total_visits = serializers.IntegerField(source='get_total_visits')
    unique_visits = serializers.IntegerField(source='get_unique_visits')
    avg_load_speed = serializers.IntegerField(source='get_avg_load_speed')
    min_load_speed = serializers.IntegerField(source='get_min_load_speed')
    max_load_speed = serializers.IntegerField(source='get_max_load_speed')
    avg_size_page = serializers.IntegerField(source='get_avg_size_page')
    min_size_page = serializers.IntegerField(source='get_min_size_page')
    max_size_page = serializers.IntegerField(source='get_max_size_page')
    sources = serializers.ListField(source='get_sources', child=serializers.DictField(child=serializers.CharField()))
    countrys = serializers.ListField(source='get_countrys', child=serializers.DictField(child=serializers.CharField()))
    cities = serializers.ListField(source='get_cities', child=serializers.DictField(child=serializers.CharField()))


class StatTutorialSerializer(StatContentSerializer):
    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'slug', 'total_visits', 'unique_visits', 'avg_load_speed', 'min_load_speed', 'max_load_speed', 'avg_size_page', 'min_size_page', 'max_size_page', 'description', 'pubdate', 'update', 'sources', 'countrys', 'cities')


class StatChapterSerializer(StatContentSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'title', 'slug', 'total_visits', 'unique_visits', 'avg_load_speed', 'min_load_speed', 'max_load_speed', 'avg_size_page', 'min_size_page', 'max_size_page', 'sources', 'countrys', 'cities')


class StatPartSerializer(StatContentSerializer):
    class Meta:
        model = Part
        fields = ('id', 'title', 'slug', 'total_visits', 'unique_visits', 'avg_load_speed', 'min_load_speed', 'max_load_speed', 'avg_size_page', 'min_size_page', 'max_size_page', 'sources', 'countrys', 'cities')


class StatArticleSerializer(StatContentSerializer):
    class Meta:
        model = Tutorial
        fields = ('id', 'title', 'slug', 'total_visits', 'unique_visits', 'avg_load_speed', 'min_load_speed', 'max_load_speed', 'avg_size_page', 'min_size_page', 'max_size_page', 'description', 'pubdate', 'update', 'sources', 'countrys', 'cities')


class StatSourceContentSerializer(serializers.ModelSerializer):

    total_visits = serializers.IntegerField(source='get_total_visits')
    unique_visits = serializers.IntegerField(source='get_unique_visits')
    avg_load_speed = serializers.IntegerField(source='get_avg_load_speed')
    avg_size_page = serializers.IntegerField(source='get_avg_size_page')
    sources = serializers.ListField(source='get_sources', child=serializers.DictField(child=serializers.CharField()))

    class Meta:
        model = Log
        fields = ('dns_referal', 'total_visits', 'unique_visits', 'avg_load_speed', 'avg_size_page', 'sources')
