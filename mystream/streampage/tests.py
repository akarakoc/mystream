from django.test import TestCase
from streampage.models import Communities, communityUsers, Datatypes, DatatypeFields
from datetime import datetime

class UnitTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        communityUsers.objects.create(nickName = 'tutkubayri', userName = 'Tutku', userSurname = 'Bayrı',
                                      userMail='tutkubayri@gmail.com', userPassword = '987654321', userBirthDay = '15/10/1995')
        communityUsers.objects.create(nickName = 'ayseyilmaz', userName = 'Ayşe', userSurname = 'Yılmaz', userPassword = '234567891')
        Communities.objects.create(name='Covid-19 Preventions in İstanbul', description='Preventions that are taken in İstanbul for Covid-19',
                                   communityCreator= communityUsers.objects.get(nickname='tutkubayri'),communityCountry='Turkey', communityLocation='İstanbul',
                                   communityTags ="#covid19#corona#preventions", communityCreationDate = datetime.now())
        Communities.objects.create(description='About epidemic that is occured in 2020',
                                   communityCreator= communityUsers.objects.get(nickname='tutkubayri'),communityCountry='Turkey', communityLocation='İstanbul',
                                   communityTags ="#epidemic#2020", communityCreationDate = datetime.now())
        Datatypes.objects.create(name ='Preventions for Epidemic', datatypeCreator = communityUsers.objects.get(nickname='ayseyilmaz'),
                                 relatedCommunity = Communities.objects.get(name='Covid-19 Preventions in İstanbul'), datatypeCreationDate=datetime.now(),
                                 datatypeTags="#covid#vacination")


    def test_community_creation(self):
        community = Communities.objects.get(name='Covid-19 Preventions in İstanbul')
        self.assertTrue(isinstance(community, Communities))

    def test_community_name(self):
        community = Communities.objects.get(description='About epidemic that is occured in 2020')
        self.assertNotEqual(community.name, None)

    def test_community_creator(self):
        community = Communities.objects.get(name='Covid-19 Preventions in İstanbul')
        self.assertEqual(community.communityCreator, communityUsers.objects.get(nickname='tutkubayri'))

    def test_community_search(self):
        response = self.client.get('communityPageSearch/?keyword=Covid-19')
        self.assertNotEqual(response, None)

    def test_posttype_subscribtion(self):
        user = communityUsers.objects.get(nickname='tutkubayri')
        datatype = Datatypes.objects.get(name ='Preventions for Epidemic')
        data = {
            'Posttype_Hash': datatype.datatypeHash,
            'user': user
        }
        response = self.client.post('/streampage/subscribePosttype/', data)
        self.assertContains(response,"You Subscribed to the Community Successfully!")


    def test_delete_posttype(self):
        datatype = Datatypes.objects.get(name='Preventions for Epidemic')
        data = {
            'Posttype_Hash': datatype.datatypeHash,
            'community_Hash': datatype.relatedCommunity.communityHash
        }
        self.client.post('/streampage/DeletePosttypeMeta/', data)
        deleted = Datatypes.objects.get(name='Preventions for Epidemic')
        self.assertNotEqual(deleted, None)




