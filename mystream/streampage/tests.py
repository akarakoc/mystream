from django.test import TestCase
from streampage.models import Communities, communityUsers, Datatypes, Posts
from .forms import AddCommunity, UsersRegisterForm
from datetime import datetime
from django_countries import countries
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse

class UnitTestClass(TestCase):
    @classmethod
    def setUpTestData(self):
        user = communityUsers.objects.create(nickName='ayseyilmaz', userName='Ayşe', userSurname='Yılmaz', userPassword='234567891')
        community = Communities.objects.create(name='Covid-19 Preventions in İstanbul', description='Preventions that are taken in İstanbul for Covid-19',
                                   communityCreator=communityUsers.objects.get(nickName='ayseyilmaz'),communityCountry='Turkey', communityLocation='İstanbul',
                                   communityTags="#covid19#corona#preventions")
        community2 = Communities.objects.create(name='Epidemic', description='About epidemic that is occured in 2020',
                                               communityCreator=communityUsers.objects.get(nickName='ayseyilmaz'), communityCountry='Turkey',
                                               communityLocation='İstanbul', communityTags="#covid19#corona#preventions")
        community3 = Communities.objects.create(name='Recycling bins in Beşiktaş',
                                               communityCreator=communityUsers.objects.get(nickName='ayseyilmaz'),
                                               communityCountry='Turkey', communityLocation='İstanbul',
                                               communityTags="#recycling#world")
        community.save()
        user.save()
        community3.save()
        community2.save()

    def test_community_creation(self):
        community = Communities.objects.get(name='Covid-19 Preventions in İstanbul')
        self.assertTrue(isinstance(community, Communities))

    def test_null_community_name_in_form(self):
        country = dict(countries)['TR']
        form = AddCommunity(data={'Community_Name': "", 'Community_Description': "About epidemic that is occured in 2020", 'Community_Image': None, 'Private_Community': None,
                                  'Community_Country':country, 'Community_Location':"İstanbul", 'Community_Tags': "#epidemic#2020"})
        self.assertEqual(form.data['Community_Name'], "")

    def test_register_form_validity(self):
        form = UsersRegisterForm(data={'username':'sevgitutkubayri', 'email':'tutku.bayri@boun.edu.tr', 'confirm_email':'tutku.bayri@boun.edu.tr', 'password':'2345678901'})
        self.assertTrue(form.is_valid())

    def test_community_page(self):
        user = User.objects.create(username='johnlennon')
        user.set_password('johnpassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='johnlennon')
        userCommunity.save()
        client = Client()
        client.login(username='johnlennon', password='johnpassword')
        response = client.get("/streampage/communities/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_community_count(self):
        user = User.objects.create(username='johnlennon')
        user.set_password('johnpassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='johnlennon')
        userCommunity.save()
        client = Client()
        client.login(username='johnlennon', password='johnpassword')
        response = client.get("/streampage/communities/", follow=True)
        self.assertEqual(len(response.context['User_communities']), 0)

    def test_posttype_page(self):
        user = User.objects.create(username='tutkubayri')
        user.set_password('987654321')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='tutkubayri')
        userCommunity.save()
        community = Communities.objects.create(name='Epidemics through the world', communityCreator=communityUsers.objects.get(nickName='ayseyilmaz'),
                                               communityCountry='Turkey', communityLocation='İstanbul', communityTags="#epidemics#world")
        community.save()
        client = Client()
        client.login(username='tutkubayri', password='987654321')
        firstResponse = client.post(reverse("streampage:PosttypePage"))
        hash = firstResponse.context['community_Hash']
        response = client.get("/streampage/sendPosttypePage/", data = hash, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        user = User.objects.create(username='stutku')
        user.set_password('stutkupassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='stutku')
        userCommunity.save()
        client = Client()
        client.login(username='stutku', password='stutkupassword')
        response = client.get("/streampage/profile/", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_subscription_list(self):
        user = User.objects.create(username='stutku')
        user.set_password('stutkupassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='stutku')
        userCommunity.save()
        client = Client()
        client.login(username='stutku', password='stutkupassword')
        response = client.get("/streampage/profile/", follow=True)
        self.assertEqual(len(response.context['subscriptionList']), 0)

    def test_community_description_length(self):
        community = Communities.objects.get(description='About epidemic that is occured in 2020')
        max_length = community._meta.get_field('description').max_length
        self.assertLessEqual(len(community.description), max_length)

    def test_community_creator(self):
        community = Communities.objects.get(name='Covid-19 Preventions in İstanbul')
        self.assertEqual(community.communityCreator, communityUsers.objects.get(nickName='ayseyilmaz'))

    def test_community_search(self):
        response = self.client.get('streampage/communityPageSearch?keyword=Covid-19')
        self.assertNotEqual(response, None)

    def test_communities_view_uses_correct_template(self):
        response = self.client.get('/streampage/browse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse.html')

    def test_posttypes_view_uses_correct_template(self):
        response = self.client.get('/streampage/sendPosttypePageBrowse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browseDatatypes.html')

    def test_trial(self):
        user = User.objects.create(username='deniz')
        user.set_password('78945612301')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='deniz')
        userCommunity.save()
        Communities.objects.get(name='Recycling bins in Beşiktaş')

        client = Client()
        client.login(username='deniz', password='78945612301')
        firstResponse = client.post(reverse("streampage:PosttypePage"))
        # hash = firstResponse.context['community_Hash']
        # print(hash)
        print(firstResponse)
        print(firstResponse.context)

        # response = client.get("/streampage/JoinCommunity/", data=commhash, follow=True)
        # self.assertEqual(response.status_code, 200)

    # def test_post_details_view_uses_correct_template(self):
    #     community = Communities.objects.create(name='Shopping for Who Cannot Go Out',
    #                                            communityCreator=communityUsers.objects.get(nickName='ayseyilmaz'),
    #                                            communityCountry='Turkey', communityLocation='İstanbul',
    #                                            communityTags="#epidemic#shopping")
    #     community.save()
    #     name = 'Shopping List'
    #     postType = Datatypes.objects.create(name='Shopping List', datatypeCreator=communityUsers.objects.get(nickName='ayseyilmaz'),
    #                                         relatedCommunity=Communities.objects.get(name='Covid-19 Preventions in İstanbul'))
    #     postType.save()
    #     post = Posts.objects.create(
    #         relatedCommunityforPost=Communities.objects.get(name='Covid-19 Preventions in İstanbul'),
    #         relatedDatatypes=Datatypes.objects.get(name='Shopping List'), postCreator=communityUsers.objects.get(nickName='ayseyilmaz'))
    #     post.save()
    #
    #     firstResponse = self.client.post(reverse("streampage:showPostDetailsBrowse"), follow=True)
    #     print(firstResponse)
    #     hash = firstResponse.context['postEntries.postInstances.0.postList.0.entryHash']
    #     print(hash)

        # response = self.client.get('/streampage/showPostDetailsBrowse/', follow=True)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'postDetailsBrowse.html')


