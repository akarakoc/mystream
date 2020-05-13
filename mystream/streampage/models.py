from django.db import models
from django.contrib.postgres.fields import JSONField

class Primitives(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter your primitive data types')
    def __str__(self):
        return self.name

class communityUsers(models.Model):
    nickName = models.CharField(max_length=200, null=True, help_text='Enter your nickname')	
    userName = models.CharField(max_length=200, null=True, help_text='Enter your username')	
    userSurname = models.CharField(max_length=200, null=True, help_text='Enter your surname')		
    userMail = models.EmailField()	
    userPassword = models.CharField(max_length=200, null=True, help_text='Enter your password')	
    creationDate = models.DateTimeField(null=True)	
    communityPoint = models.CharField(max_length=200, null=True, help_text='Community Point')	
    userPhoto = models.CharField(max_length=200, null=True, help_text='Community Point')
    def __str__(self):        
        return self.nickName	

class Communities(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter community name')
    description = models.CharField(max_length=200, null=True, help_text='Enter community description')	
    communityHash = models.CharField(max_length=200, null=True, help_text='Enter community hash')	
    communityPrv = models.BooleanField(default=False)	
    communityPhoto = models.CharField(max_length=200, null=True, help_text='community photo')
    communityPopularity = models.ManyToManyField(communityUsers, related_name='votes', help_text='Vote')
    communityCreator = models.ForeignKey(communityUsers, related_name='creator',on_delete=models.SET_NULL, null=True)
    communityMembers = models.ManyToManyField(communityUsers, related_name='members', help_text='Select members')
    communityTags = models.CharField(max_length=2000, null=True, help_text='Enter community Tags')
    communityCreationDate= models.DateTimeField(null=True)	
    def __str__(self):
        return self.name

class Datatypes(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter ypur datatype') 
    datatypeCreator = models.ForeignKey(communityUsers, related_name='datatypecreator',on_delete=models.SET_NULL, null=True)
    datatypeEditor = models.ForeignKey(communityUsers, related_name='datatypeeditor',on_delete=models.SET_NULL, null=True)
    relatedCommunity = models.ForeignKey(Communities, help_text='Select related community',on_delete=models.SET_NULL, null=True)
    datatypeCreationDate= models.DateTimeField(null=True)
    datatypeEditionDate= models.DateTimeField(null=True)
    datatypeTags = models.CharField(max_length=2000, null=True, help_text='Enter datatype Tags')
    datatypeHash = models.CharField(max_length=200, null=True, help_text='Enter datatype hash')
    subscribers = models.ManyToManyField(communityUsers, related_name='subscribers', help_text='Select members')
    def __str__(self):
        return self.name
		
class DatatypeFields(models.Model):
    name = models.CharField(max_length=200, null=True, help_text='Enter your datatype')
    relatedDatatype = models.ForeignKey(Datatypes, help_text='Select related datatype', on_delete=models.SET_NULL, null=True)
    relatedComm = models.ForeignKey(Communities, help_text='Select related datatype', on_delete=models.SET_NULL, null=True)
    fieldCreator = models.ForeignKey(communityUsers, on_delete=models.SET_NULL, null=True)
    fieldCreationDate= models.DateTimeField(null=True)
    fieldRequired = models.BooleanField(default=False)
    fronttableShow = models.BooleanField(default=False)
    enumerations = models.CharField(max_length=200, null=True, help_text='Enter the Enumerations')
    relatedPrimitives = models.ForeignKey(Primitives, help_text='Select related primitive', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name  
    
class PostsMetaHash(models.Model):
    relatedCommunity = models.ForeignKey(Communities,on_delete=models.SET_NULL, null=True)
    relatedDatatypes = models.ForeignKey(Datatypes,on_delete=models.SET_NULL, null=True)
    postMetaHash = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    postCreator = models.ForeignKey(communityUsers, related_name='postmetacreator', on_delete=models.SET_NULL, null=True)
    postCreationDate= models.DateTimeField(null=True)
    def __str__(self):
        return self.postMetaHash
		
class Posts(models.Model):
    relatedCommunityforPost = models.ForeignKey(Communities,on_delete=models.SET_NULL, null=True)
    relatedDatatypes = models.ForeignKey(Datatypes,on_delete=models.SET_NULL, null=True)
    relatedMeta = models.ForeignKey(PostsMetaHash,on_delete=models.SET_NULL, null=True)
    entryHash = models.CharField(max_length=2000, null=True, help_text='Enter name of type')
    propertyName = models.CharField(max_length=2000, null=True, help_text='Enter name of type')
    propertyValue = models.CharField(max_length=2000, null=True, help_text='Enter name of type')
    postCreator = models.ForeignKey(communityUsers, related_name='postcreator', on_delete=models.SET_NULL, null=True)
    postCreationDate= models.DateTimeField(null=True)
    postTag= models.CharField(max_length=2000, null=True, help_text='Enter Post Tags')
    postTagItems= models.CharField(max_length=2000, null=True, help_text='Enter Post Tags Item')
    def __str__(self):
        return self.propertyValue
		
class PostComments(models.Model):
    relatedCommunityforComment = models.ForeignKey(Communities,on_delete=models.SET_NULL, null=True)
    relatedMeta = models.ForeignKey(PostsMetaHash,on_delete=models.SET_NULL, null=True)
    commentHash = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    commentText = models.CharField(max_length=200, null=True, help_text='Enter name of type')
    postCommentCreator = models.ForeignKey(communityUsers, related_name='commentcreator', on_delete=models.SET_NULL, null=True)
    postCommentCreationDate= models.DateTimeField(null=True)
    postCommentTag= models.CharField(max_length=2000, null=True, help_text='Enter Post Tags')
    def __str__(self):
        return self.commentText

class CommunityTags(models.Model):
    communityTag = models.ForeignKey(Communities, related_name='commTag',on_delete=models.SET_NULL, null=True)
    tagName = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag')
    tagItem = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag Item')
    def __str__(self):
        return self.tagName
		
class DatatTypeTags(models.Model):
    datatypeTag = models.ForeignKey(Datatypes, related_name='dataTag',on_delete=models.SET_NULL, null=True)
    tagName = models.CharField(max_length=2000, null=True, help_text='Enter Datatype Tag')
    tagItem = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag Item')
    def __str__(self):
        return self.tagName
		
class PostTags(models.Model):
    relatedPostTag = models.ForeignKey(Posts, related_name='postsTag',on_delete=models.SET_NULL, null=True)
    tagName = models.CharField(max_length=2000, null=True, help_text='Enter Post Tag')
    tagItem = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag Item')
    def __str__(self):
        return self.tagName
		
class UserTags(models.Model):
    userTag = models.ForeignKey(communityUsers, related_name='usersTag',on_delete=models.SET_NULL, null=True)
    tagName = models.CharField(max_length=2000, null=True, help_text='Enter Post Tag')
    tagItem = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag Item')
    def __str__(self):
        return self.tagName

class UserCircle(models.Model):
    circleOwner = models.OneToOneField(communityUsers, on_delete=models.SET_NULL, null=True)
    circleUsers = models.ManyToManyField(communityUsers, related_name='Followers', help_text='Select Members')
    tagItem = models.CharField(max_length=2000, null=True, help_text='Enter Community Tag Item')
    def __str__(self):
        return self.circleOwner
		
class ActivityStreams(models.Model):
    detail = JSONField()