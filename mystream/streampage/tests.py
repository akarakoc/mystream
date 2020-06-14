from django.test import TestCase
from streampage.models import Communities, communityUsers, Datatypes, Posts, Primitives, PostComments
from .forms import AddCommunity, UsersRegisterForm, AddPosttype, AddTextEntry
from datetime import datetime
from django_countries import countries
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)
        community = Communities.objects.get(name='Shopping for Who Cannot Go Out')
        self.assertTrue(isinstance(community, Communities))

    def test_edit_community(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'user': userCommunity.nickName, 'community_Hash': hash[0].communityHash, 'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Select from the shopping lists to grab the items in the list.",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"}
        requestDelete = client.post("/streampage/EditCommunity/", data=data)
        self.assertEqual(requestDelete.status_code, 200)

    def test_delete_community(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'user': userCommunity.nickName, 'community_Hash': hash[0].communityHash}
        requestDelete = client.post("/streampage/DeleteCommunity/", data=data)
        self.assertEqual(requestDelete.status_code, 200)

    def test_leave_community(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']
        data={'user': userCommunity.nickName, 'community_Hash': hash[0].communityHash}

        request = client.post("/streampage/LeaveCommunity/", data=data)
        self.assertEqual(request.status_code, 200)

    def test_register_form_validity(self):
        form = UsersRegisterForm(data={'username':'sevgitutkubayri', 'email':'tutku.bayri@boun.edu.tr', 'confirm_email':'tutku.bayri@boun.edu.tr', 'password':'2345678901'})
        self.assertTrue(form.is_valid())

    def test_login_page(self):
        user = User.objects.create(username='johnlennon')
        user.set_password('johnpassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='johnlennon')
        userCommunity.save()
        request = self.client.post("/streampage/login/", data={"username":'johnlennon', "password":'johnpassword'}, follow=True)
        self.assertEqual(request.status_code, 200)

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

    def test_user_page(self):
        user = User.objects.create(username='stutku')
        user.set_password('stutkupassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='stutku')
        userCommunity.save()
        client = Client()
        client.login(username='stutku', password='stutkupassword')
        response = client.get("/streampage/UserPage/", data={'user':userCommunity.nickName}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_user(self):
        user = User.objects.create(username='stutku')
        user.set_password('stutkupassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='stutku')
        userCommunity.save()
        client = Client()
        client.login(username='stutku', password='stutkupassword')

        data={"name":'Tutku', "surname":'BAYRI', "birth":"15/10/1995", "email":'tutkubayri@gmail.com', "bio":'Bio of Tutku'}
        response = client.get("/streampage/EditUser/", data=data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_follow_user(self):
        user = User.objects.create(username='johnlennon')
        user.set_password('johnpassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='johnlennon')
        userCommunity.save()
        userFollower = User.objects.create(username='sevgitutku')
        userFollower.set_password('tutkupassword')
        userFollower.save()
        follower = communityUsers.objects.create(nickName='sevgitutku')
        follower.save()
        client = Client()
        client.login(username='sevgitutku', password='tutkupassword')

        data = {'user': userCommunity.nickName}
        request = client.post("/streampage/FollowUser/", data=data)
        self.assertEqual(request.status_code, 200)

    def test_unfollow_user(self):
        user = User.objects.create(username='johnlennon')
        user.set_password('johnpassword')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='johnlennon')
        userCommunity.save()
        userFollower = User.objects.create(username='sevgitutku')
        userFollower.set_password('tutkupassword')
        userFollower.save()
        follower = communityUsers.objects.create(nickName='sevgitutku')
        follower.save()
        client = Client()
        client.login(username='sevgitutku', password='tutkupassword')

        data = {'user': userCommunity.nickName}
        request = client.post("/streampage/FollowUser/", data=data)
        requestUnfollow = client.post("/streampage/UnFollowUser/", data=data)
        self.assertEqual(requestUnfollow.status_code, 200)

    def test_community_description_length(self):
        community = Communities.objects.get(description='About epidemic that is occured in 2020')
        max_length = community._meta.get_field('description').max_length
        self.assertLessEqual(len(community.description), max_length)

    def test_community_creator(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')
        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Covid",
                                  'Community_Description': "Covid",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        community = Communities.objects.get(name="Covid")
        self.assertEqual(community.communityCreator, communityUsers.objects.get(nickName='Derya'))

    def test_community_search(self):
        data={'keyword':"Covid"}
        response = self.client.get('streampage/communityPageSearch/', data=data)
        self.assertNotEqual(response, None)

    def test_location_search(self):
        data = {'keyword': "İstanbul"}
        response = self.client.get('streampage/communityLocationPageSearch/', data=data)
        self.assertNotEqual(response, None)

    def test_choose_search_view_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        response = self.client.post('/streampage/chooseSearch/', data={'community_Hash': hash[0].communityHash})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modal.html')

    def test_free_search_field_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        response = self.client.post('/streampage/ReturnFreeSearchFields/', data={'community_Hash': hash[0].communityHash})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrySearchFields.html')

    def test_community_form_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        response = self.client.post('/streampage/sendCommunityForm/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modal.html')

    def test_posttype_form_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        response = self.client.post('/streampage/sendPosttypeForm/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modal.html')

    def test_edit_user_modal_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        response = self.client.post('/streampage/EditUserModal/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'modal.html')

    def test_upload_photo_uses_correct_template(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        response = self.client.post('/streampage/uploadPhotoForm/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tagSearch.html')

    #browse communities page
    def test_communities_view_uses_correct_template(self):
        response = self.client.get('/streampage/browse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse.html')

    #browse posttypes
    def test_posttypes_view_uses_correct_template(self):
        response = self.client.get('/streampage/sendPosttypePageBrowse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browseDatatypes.html')

    def test_add_post_modal(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)
        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        response = self.client.post('/streampage/AddPostModal/', data = {'community_Hash': hash[0].communityHash})
        self.assertEqual(response.status_code, 200)

    def test_send_posttypes(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)
        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)
        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}
        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)
        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]
        dataShow = {'postHash': post.entryHash, 'user': userCommunity.nickName}
        requestShow = client.get("/streampage/showPostDetails/", data=dataShow)
        self.assertEqual(requestShow.status_code, 200)

    def test_join_community(self):
        user = User.objects.create(username='deniz')
        user.set_password('78945612301')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='deniz')
        userCommunity.save()

        client = Client()
        client.login(username='deniz', password='78945612301')

        communityImage = SimpleUploadedFile(name='nedir.jpg', content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out", 'Community_Description': "Shopping for people who cannot go out",
                                   'Community_Image': communityImage , 'Private_Community': True, 'Community_Country':"Turkey", 'Community_Location':"İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)
        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']
        response = client.post("/streampage/JoinCommunity/", data={'community_Hash': hash[0].communityHash}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_posttype(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                           content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                           content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data={'Posttype_Name':"Shopping List", 'Posttype_Tags':"#shopping", 'community_Hash':hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        self.assertEqual(requestPosttype.status_code, 200)

    def test_edit_posttype(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                           content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                           content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data={'Posttype_Name':"Shopping List", 'Posttype_Tags':"#shopping", 'community_Hash':hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)
        posttype=Datatypes.objects.get(name='Shopping List')
        posttypeNewData={'Posttype_Hash': posttype.datatypeHash, 'Posttype_Name':posttype.name, 'Posttype_Tags':"#xyz12345"}
        requestEditPosttype = client.post("/streampage/EditPosttypeMeta/", data=posttypeNewData)

        self.assertEqual(requestEditPosttype.status_code, 200)

    def test_delete_posttype(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                           content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                           content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data={'Posttype_Name':"Shopping List", 'Posttype_Tags':"#shopping", 'community_Hash':hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)
        posttype=Datatypes.objects.get(name='Shopping List')
        requestDeletePosttype = client.post("/streampage/DeletePosttypeMeta/", data={'Posttype_Hash': posttype.datatypeHash})

        self.assertEqual(requestDeletePosttype.status_code, 200)

    def test_open_posttype_fields(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                           content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                           content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        community = Communities.objects.get(name="Shopping for Who Cannot Go Out")
        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data={'Posttype_Name':"Shopping List", 'Posttype_Tags':"#shopping", 'community_Hash':hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        data2={'Enumeration':"off"}
        requestAddPosttypeField = client.post("/streampage/addPosttypeField/", data=data2)
        self.assertEqual(requestAddPosttypeField.status_code, 200)

    def test_open_save_primitives_view(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True, 'CommunityHash':hash[0].communityHash,
                                  'PosttypeHash':datatypeHash, 'Enum':"off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        self.assertEqual(requestPosttypeField.status_code, 200)

    def test_create_post(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost={'community_Hash': hash[0].communityHash,'PosttypeHash': datatypeHash, 'user':userCommunity.nickName,
                  'For Who':"Deniz Yıldırım", 'List':"1kg potatoes, 1kg apples", 'Tags':"#xyz1234"}
        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)

        self.assertEqual(requestPost.status_code, 200)

    def test_search_results_view(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost={'community_Hash': hash[0].communityHash,'PosttypeHash': datatypeHash, 'user':userCommunity.nickName,
                  'For Who':"Deniz Yıldırım", 'List':"1kg potatoes, 1kg apples", 'Tags':"#xyz1234"}
        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)

        dataSearch={'CommunityHash': hash[0].communityHash, 'user':userCommunity.nickName, 'For Who_Value':"Deniz Yıldırım", 'For Who_Condition':"equals", "page":1}
        requestSearch = client.post("/streampage/ReturnEntrySearchResults/", data=dataSearch, follow=True)
        self.assertEqual(requestSearch.status_code, 200)

    def test_delete_post(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)
        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)
        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}
        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost={'community_Hash': hash[0].communityHash,'PosttypeHash': datatypeHash, 'user':userCommunity.nickName,
                  'For Who':"Deniz Yıldırım", 'List':"1kg potatoes, 1kg apples", 'Tags':"#xyz1234"}
        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)
        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]
        requestDelete = client.post("/streampage/DeletePost/", data={'PostHash':post.entryHash}, follow=True)
        self.assertEqual(requestDelete.status_code, 200)

    def test_report_post(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)
        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        requestReport = client.post("/streampage/reportPost/", data={'post_Hash':post.entryHash}, follow=True)
        self.assertEqual(requestReport.status_code, 200)

    def test_report_delete_post(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)
        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        requestReport = client.post("/streampage/reportPostDelete/", data={'post_Hash':post.entryHash}, follow=True)
        self.assertEqual(requestReport.status_code, 200)

    def test_subscribe_posttype(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)

        post=Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        datasubscription = {'post_Hash': post.entryHash,'user': userCommunity.nickName}

        requestSubscription = client.post("/streampage/subscribePosttype/", data=datasubscription, follow=True)

        self.assertEqual(requestSubscription.status_code, 200)

    def test_unsubscribe_posttype(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)

        post=Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        datasubscription = {'post_Hash': post.entryHash,'user': userCommunity.nickName}

        requestSubscription = client.post("/streampage/subscribePosttype/", data=datasubscription, follow=True)

        requestUnsubscription = client.post("/streampage/unsubscribePosttype/", data=datasubscription, follow=True)

        self.assertEqual(requestUnsubscription.status_code, 200)

    def test_populate_province(self):
        data = {'country':"Turkey"}
        response = self.client.get("/streampage/populateProvince/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_search_tag(self):
        data={"search_text":'covid'}
        request = self.client.get("/streampage/searchTag/", data=data, follow=True)
        self.assertEqual(request.status_code, 200)

    def test_create_comment(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)

        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        datacomment = {'community_Hash':hash[0].communityHash, 'post_Hash': post.entryHash, 'user': userCommunity.nickName,
                       'Comment':"I can buy these items."}

        requestComment = client.post("/streampage/CreatePostComment/", data=datacomment, follow=True)

        self.assertEqual(requestComment.status_code, 200)

    def test_delete_comment(self):
        user = User.objects.create(username='ahmet')
        user.set_password('9638527410')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='ahmet')
        userCommunity.save()

        client = Client()
        client.login(username='ahmet', password='9638527410')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'Posttype_Name': "Shopping List", 'Posttype_Tags': "#shopping", 'community_Hash': hash[0].communityHash}
        requestPosttype = client.post("/streampage/CreatePosttype/", data=data)

        datatypeHash = Datatypes.objects.get(name="Shopping List").datatypeHash

        primitive = Primitives.objects.create(id=1, name="Text")
        primitive.save()

        dataPosttypeField = {'name': "For Who", "Types": primitive.name, "Required": True, "ShowPage": True,
                             'CommunityHash': hash[0].communityHash,
                             'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField = client.post("/streampage/SavePrimitives/", data=dataPosttypeField)

        dataPosttypeField2 = {'name': "List", "Types": primitive.name, "Required": True, "ShowPage": True,
                              'CommunityHash': hash[0].communityHash,
                              'PosttypeHash': datatypeHash, 'Enum': "off"}

        requestPosttypeField2 = client.post("/streampage/SavePrimitives/", data=dataPosttypeField2)

        dataPost = {'community_Hash': hash[0].communityHash, 'PosttypeHash': datatypeHash,
                    'user': userCommunity.nickName,
                    'For Who': "Deniz Yıldırım", 'List': "1kg potatoes, 1kg apples", 'Tags': "#xyz1234"}

        requestPost = client.post("/streampage/CreatePost/", data=dataPost, follow=True)
        post = Posts.objects.filter(relatedDatatypes=Datatypes.objects.get(name="Shopping List"))[0]

        datacomment = {'community_Hash':hash[0].communityHash, 'post_Hash': post.entryHash, 'user': userCommunity.nickName,
                       'Comment':"I can buy these items."}
        requestComment = client.post("/streampage/CreatePostComment/", data=datacomment, follow=True)

        comment = PostComments.objects.get(commentText="I can buy these items.")
        requestDeleteComment = client.post("/streampage/deletePostComment/", data={'comment_Hash':comment.commentHash}, follow=True)

        self.assertEqual(requestDeleteComment.status_code, 200)

    def test_check_membership(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')

        form = AddCommunity(data={'Community_Name': "Shopping for Who Cannot Go Out",
                                  'Community_Description': "Shopping for people who cannot go out",
                                  'Community_Image': communityImage, 'Private_Community': True,
                                  'Community_Country': "Turkey", 'Community_Location': "İstanbul",
                                  'Community_Tags': "#xyz12345"})
        request = client.post("/streampage/CreateCommunity/", data=form.data)

        firstResponse = client.post(reverse("streampage:Communities"))
        hash = firstResponse.context['User_communities']

        data = {'user': userCommunity.nickName, 'community_Hash': hash[0].communityHash}
        requestCheck = client.post("/streampage/CheckMembership/", data=data)
        self.assertEqual(requestCheck.status_code, 200)

    def test_upload_photo(self):
        user = User.objects.create(username='Derya')
        user.set_password('5978614230')
        user.save()
        userCommunity = communityUsers.objects.create(nickName='Derya')
        userCommunity.save()

        client = Client()
        client.login(username='Derya', password='5978614230')

        communityImage = SimpleUploadedFile(name='nedir.jpg',
                                            content=open("C:\\Users\\Tutku\\Desktop\\nedir.jpg", 'rb').read(),
                                            content_type='image/jpg')
        data={'ImageEntry':communityImage}

        request = client.post("/streampage/uploadPhoto/", data=data)
        self.assertEqual(request.status_code, 200)

