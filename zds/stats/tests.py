# coding: utf-8

from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from oauth2_provider.models import Application, AccessToken
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from zds.stats.factories import LogFactory
from zds.stats.models import Log
from zds.member.factories import ProfileFactory, StaffProfileFactory
from zds.gallery.factories import UserGalleryFactory, ImageFactory, GalleryFactory
from zds.tutorial.factories import BigTutorialFactory, MiniTutorialFactory, PartFactory, \
    ChapterFactory, NoteFactory, SubCategoryFactory, LicenceFactory
from zds.tutorial.models import Note, Tutorial, Validation, Extract, Part, Chapter
import tempfile
import os
import shutil
from zds.settings import BASE_DIR


overrided_drf = settings.REST_FRAMEWORK
overrided_zds_app = settings.ZDS_APP
overrided_drf["PAGINATE_BY"] = 3
overrided_zds_app['tutorial']['repo_path'] = os.path.join(BASE_DIR, 'tutoriels-private-test')
overrided_zds_app['tutorial']['repo_public_path'] = os.path.join(BASE_DIR, 'tutoriels-public-test')
overrided_zds_app['article']['repo_path'] = os.path.join(BASE_DIR, 'article-data-test')


def create_public_big_tutorial(client, author, licence, validator):
    bigtuto = BigTutorialFactory(light=True)
    bigtuto.authors.add(author)
    bigtuto.gallery = GalleryFactory()
    bigtuto.licence = licence
    bigtuto.save()

    part1 = PartFactory(tutorial=bigtuto, position_in_tutorial=1, light=True)

    chapter1_1 = ChapterFactory(
        part=part1,
        position_in_part=1,
        position_in_tutorial=1,
        light=True)

    client.login(
        username=validator.username,
        password='hostel77')

    # ask public tutorial
    pub = client.post(
        reverse('zds.tutorial.views.ask_validation'),
        {
            'tutorial': bigtuto.pk,
            'text': u'Ce tuto est excellent',
            'version': bigtuto.sha_draft,
            'source': 'http://zestedesavoir.com',
        },
        follow=False)

    # reserve tutorial
    validation = Validation.objects.get(
        tutorial__pk=bigtuto.pk)
    pub = client.post(
        reverse('zds.tutorial.views.reservation', args=[validation.pk]),
        follow=False)

    # publish tutorial
    pub = client.post(
        reverse('zds.tutorial.views.valid_tutorial'),
        {
            'tutorial': bigtuto.pk,
            'text': u'Ce tuto est excellent',
            'is_major': True,
            'source': 'http://zestedesavoir.com',
        },
        follow=True)
    return bigtuto


def generate_public_content(client, number, author, licence, validator):
    f = tempfile.NamedTemporaryFile()
    #f = open("logexample.log", "w")
    for i in range(number):
        bigtuto = create_public_big_tutorial(client=client, author=author, licence=licence, validator=validator)
        log = LogFactory(content="tutorial", pk=bigtuto.pk)
        f.write("{}\n".format(log))
        log = LogFactory(content="part", pk=Part.objects.get(tutorial__pk=bigtuto.pk).pk)
        f.write("{}\n".format(log))
        log = LogFactory(content="chapter", pk=Chapter.objects.get(part__tutorial__pk=bigtuto.pk).pk)
        f.write("{}\n".format(log))
    #f.seek(0)
    f.close()
    #s = open(f.name, "r")
    #args = [f.name]
    args = ["logexample.log"]
    opts = {}
    call_command('parse_logs', *args, **opts)
    f.close()



@override_settings(REST_FRAMEWORK=overrided_drf)
@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'media-test'))
@override_settings(ZDS_APP=overrided_zds_app)
class ContentEmptyListAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_of_tutorials_empty(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["tutoriel"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_list_of_articles_empty(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["article"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_list_of_chapters_empty(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["chapitre"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_list_of_parts_empty(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["partie"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def tearDown(self):
        if os.path.isdir(settings.ZDS_APP['tutorial']['repo_path']):
            shutil.rmtree(settings.ZDS_APP['tutorial']['repo_path'])
        if os.path.isdir(settings.ZDS_APP['tutorial']['repo_public_path']):
            shutil.rmtree(settings.ZDS_APP['tutorial']['repo_public_path'])
        if os.path.isdir(settings.ZDS_APP['article']['repo_path']):
            shutil.rmtree(settings.ZDS_APP['article']['repo_path'])
        if os.path.isdir(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

@override_settings(REST_FRAMEWORK=overrided_drf)
@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'media-test'))
@override_settings(ZDS_APP=overrided_zds_app)
class ContentListAPITest(APITestCase):

    data_generate = False

    def setUp(self):
        self.client = APIClient()
        print(self.data_generate)
        if not self.data_generate:
	        self.licence = LicenceFactory()
	        self.author = ProfileFactory().user
	        self.validator = StaffProfileFactory().user
	        generate_public_content(client=self.client, licence=self.licence, author=self.author, validator=self.validator, number = settings.REST_FRAMEWORK['PAGINATE_BY'])
	        self.data_generate = True
        

    def test_list_of_tutorials(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["tutoriel"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertEqual(len(response.data.get('results')), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    """
    def test_list_of_articles(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["article"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertEqual(len(response.data.get('results')), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))
    """
    def test_list_of_parts(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["partie"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertEqual(len(response.data.get('results')), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_list_of_chapters(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["chapitre"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertEqual(len(response.data.get('results')), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def tearDown(self):
        if os.path.isdir(settings.ZDS_APP['tutorial']['repo_path']):
            shutil.rmtree(settings.ZDS_APP['tutorial']['repo_path'])
        if os.path.isdir(settings.ZDS_APP['tutorial']['repo_public_path']):
            shutil.rmtree(settings.ZDS_APP['tutorial']['repo_public_path'])
        if os.path.isdir(settings.ZDS_APP['article']['repo_path']):
            shutil.rmtree(settings.ZDS_APP['article']['repo_path'])
        if os.path.isdir(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)