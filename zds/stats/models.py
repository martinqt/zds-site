# coding: utf-8

from django.db import models
from django.db.models import Avg, Min, Max, Count


class Logable:
    def get_total_visits(self):
        return Log.objects.filter(id_zds=self.pk).count()

    def get_unique_visits(self):
        return Log.objects.filter(id_zds=self.pk).values_list('remote_addr', flat=True).distinct().count()

    def get_avg_load_speed(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(avg_load_speed=Avg('request_time'))
        return req_result['avg_load_speed']

    def get_min_load_speed(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(avg_load_speed=Min('request_time'))
        return req_result['avg_load_speed']

    def get_max_load_speed(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(avg_load_speed=Max('request_time'))
        return req_result['avg_load_speed']

    def get_avg_size_page(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(avg_size_page=Max('body_bytes_sent'))
        return req_result['avg_size_page']

    def get_min_size_page(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(min_size_page=Max('body_bytes_sent'))
        return req_result['min_size_page']

    def get_max_size_page(self):
        req_result = Log.objects.filter(id_zds=self.pk).aggregate(max_size_page=Max('body_bytes_sent'))
        return req_result['max_size_page']

    def get_sources(self):
    	return list(Log.objects.filter(id_zds=self.pk).values('dns_referal').annotate(total_visits=Count('pk'), unique_visits=Count('remote_addr')))

    def get_countrys(self):
    	return list(Log.objects.filter(id_zds=self.pk).values('country').annotate(total_visits=Count('pk'), unique_visits=Count('remote_addr')))

    def get_cities(self):
    	return list(Log.objects.filter(id_zds=self.pk).values('city').annotate(total_visits=Count('pk'), unique_visits=Count('remote_addr')))


class Log(models.Model):
    class Meta:
        verbose_name = 'Log web'
        verbose_name_plural = 'Logs web'


    id_zds = models.IntegerField('Identifiant sur ZdS')
    content_type = models.CharField('Type de contenu', max_length=80)
    hash_code = models.CharField('Hash code de la ligne de log', max_length=80, null=True)
    timestamp = models.DateTimeField('Timestamp', db_index=True)
    remote_addr = models.CharField('Adresse IP', max_length=39, null=True, db_index=True)
    body_bytes_sent = models.IntegerField('Taille de la page')
    dns_referal = models.CharField('Source', max_length=80, null=True)
    os_family = models.CharField('Famille de systeme d\exploitation', max_length=40, null=True)
    os_version = models.CharField('Version du systeme d\exploitation', max_length=5, null=True)
    browser_family = models.CharField('Famille du navigateur', max_length=40, null=True)
    browser_version = models.CharField('Version du navigateur', max_length=5, null=True)
    device_family = models.CharField('Famille de device', max_length=20, null=True)
    request_time = models.IntegerField('Temps de chargement de la page')
    country = models.CharField('Pays', max_length=80, null=True)
    city = models.CharField('Ville', max_length=80, null=True)

    def get_total_visits(self):
        return Log.objects.filter(dns_referal=self.dns_referal).count()

    def get_unique_visits(self):
        return Log.objects.filter(dns_referal=self.dns_referal).values_list('remote_addr', flat=True).distinct().count()

    def get_avg_load_speed(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(avg_load_speed=Avg('request_time'))
        return req_result['avg_load_speed']

    def get_min_load_speed(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(avg_load_speed=Min('request_time'))
        return req_result['avg_load_speed']

    def get_max_load_speed(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(avg_load_speed=Max('request_time'))
        return req_result['avg_load_speed']

    def get_avg_size_page(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(avg_size_page=Max('body_bytes_sent'))
        return req_result['avg_size_page']

    def get_min_size_page(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(min_size_page=Max('body_bytes_sent'))
        return req_result['min_size_page']

    def get_max_size_page(self):
        req_result = Log.objects.filter(dns_referal=self.dns_referal).aggregate(max_size_page=Max('body_bytes_sent'))
        return req_result['max_size_page']