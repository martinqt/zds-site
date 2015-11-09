# coding: utf-8

from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from oauth2_provider.models import Application, AccessToken
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from zds.stats.factories import LogFactory
from zds.member.factories import ProfileFactory, StaffProfileFactory
from zds.gallery.factories import UserGalleryFactory, ImageFactory, GalleryFactory
from zds.tutorial.factories import BigTutorialFactory, MiniTutorialFactory, PartFactory, \
    ChapterFactory, NoteFactory, SubCategoryFactory, LicenceFactory
from zds.tutorial.models import Note, Tutorial, Validation, Extract, Part, Chapter
import tempfile


def create_public_big_tutorial(client):
    licence = LicenceFactory()
    user_author = ProfileFactory().user
    bigtuto = BigTutorialFactory(light=True)
    bigtuto.authors.add(user_author)
    bigtuto.gallery = GalleryFactory()
    bigtuto.licence = licence
    bigtuto.save()

    part1 = PartFactory(tutorial=bigtuto, position_in_tutorial=1, light=True)
    part2 = PartFactory(tutorial=bigtuto, position_in_tutorial=2, light=True)
    part3 = PartFactory(tutorial=bigtuto, position_in_tutorial=3, light=True)

    chapter1_1 = ChapterFactory(
        part=part1,
        position_in_part=1,
        position_in_tutorial=1,
        light=True)
    chapter1_2 = ChapterFactory(
        part=part1,
        position_in_part=2,
        position_in_tutorial=2,
        light=True)
    chapter1_3 = ChapterFactory(
        part=part1,
        position_in_part=3,
        position_in_tutorial=3,
        light=True)

    chapter2_1 = ChapterFactory(
        part=part2,
        position_in_part=1,
        position_in_tutorial=4,
        light=True)
    chapter2_2 = ChapterFactory(
        part=part2,
        position_in_part=2,
        position_in_tutorial=5,
        light=True)

    user = ProfileFactory().user
    staff = StaffProfileFactory().user

    login_check = client.login(
        username=staff.username,
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
    first_validator = staff

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
    print("====> TUTO PUBLIC {}".format(bigtuto))

def generate_log_content(content_type, number):
    f = tempfile.NamedTemporaryFile()
    for i in range(number):
        log = LogFactory(content=content_type)
        f.write("{}\n".format(log))
        # print(log)
    f.seek(0)
    print("====> NOM : {}".format(f.name))
    s = open(f.name, "r")
    for line in s:
        print(line)
    args = [f.name]
    opts = {}
    call_command('parse_logs', *args, **opts)
    f.close()


class TutorialListAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        create_public_big_tutorial(self.client)

    def test_list_of_tutorials_empty(self):
        response = self.client.get(reverse('api-stats-list-content-visits', args=["tutoriel"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(response.data.get('results'), [])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))

    def test_list_of_tutorials(self):
        generate_log_content("tutorial", settings.REST_FRAMEWORK['PAGINATE_BY'])
        response = self.client.get(reverse('api-stats-list-content-visits', args=["tutoriel"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertEqual(len(response.data.get('results')), settings.REST_FRAMEWORK['PAGINATE_BY'])
        self.assertIsNone(response.data.get('next'))
        self.assertIsNone(response.data.get('previous'))