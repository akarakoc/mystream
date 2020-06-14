from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import connection
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UsersLoginForm, UsersRegisterForm
from .forms import UsersRegisterForm
from .forms import AddCommunity
from .forms import AddPosttype
from .forms import SendPrimitives
from .forms import AddTextEntry, AddTextEntryEnum, AddTagPost, AddTextPost, AddTextAreaPost, AddImagePost, AddAudioPost, AddVideoPost, AddBooleanPost, AddEmailPost, AddIpAddressPost, AddUrlPost, AddDatePost, AddTimePost, AddDateTimePost, AddIntegerPost, AddDecimalPost, AddFloatPost, AddEnumaratedPost, AddLocationPost, textComment, ReportPost, EditCommunity
from .forms import AddTextEntry, AddTextEntryEnum, AddTagSearch, AddTextSearch, AddTextAreaSearch, AddImageSearch, AddAudioSearch, AddVideoSearch, AddBooleanSearch, AddEmailSearch, AddIpAddressSearch, AddUrlSearch, AddDateSearch, AddTimeSearch, AddDateTimeSearch, AddIntegerSearch, AddDecimalSearch, AddFloatSearch, AddEnumaratedSearch, AddLocationSearch
from .forms import posttypeList, searchList, freeSearchField, EditUser
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string, get_template
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import json
import requests
import uuid
import hashlib
from datetime import datetime
from streampage.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,PostsMetaHash,Posts,PostComments,CommunityTags,DatatTypeTags,PostTags,UserTags,ActivityStreams,ReportedPosts,UserCircle
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from countryinfo import CountryInfo
from unicode_tr import unicode_tr

def saveTagSearch_view(src):
    SEARCHPAGE = src	
    PARAMS = {
		"action":"wbsearchentities",
		"format": "json",
		"limit": "50",
        "language":"en",
		"search": SEARCHPAGE
    }
    Srch = requests.Session()
    URL = "https://wikidata.org/w/api.php"
    Res = Srch.get(url=URL, params=PARAMS)
    DATA = Res.json()['search']
    titles = ""
    items = ""
    for tt in DATA:
        titles = titles + tt['label']+","
        items = items + tt['id']+","
    return {'TITLE' : titles, "ITEM" : items}

def saveTag_view(returneditems):
    looping = returneditems.replace("#",",").split(",")
    titles=""
    items=""		
    for iter in looping:
        if iter != '':
            resp=saveTagSearch_view(iter)
            try:
                titles = titles + resp["TITLE"]
                items = items + resp["ITEM"]
            except:
                print("!")
    print({'TITLE' : titles, "ITEM" : items})	
    return {'TITLE' : titles, "ITEM" : items}
	
def LoginPage(request):
    return render(request, 'login.html', {'community_resp': 'test'}) 

def index(request):
    if request.user.is_authenticated:
        user = request.user    
        userModel = communityUsers.objects.filter(nickName=user)[0]
        userphoto = userModel.userPhoto
        PosttypeList = Datatypes.objects.filter(subscribers=userModel)
        followingList = []
        subscriptionList  = []
        for i in PosttypeList:
            subscriptionList.append(i.name)
        if len(UserCircle.objects.filter(circleOwner=userModel)) > 0:
            for i in UserCircle.objects.get(circleOwner=userModel).circleUsers.all():
                followingList.append(i.nickName)
            queriesUser = [Q(detail__actor__name=following) for following in followingList]
            queries = queriesUser + [Q(detail__object__name=posttypename) for posttypename in subscriptionList]
        else:
            queries = [Q(detail__object__name=posttypename) for posttypename in subscriptionList]
        if len(queries) > 0:
            query = queries.pop()
            for item in queries:
                query |= item
            activityDetailList = ActivityStreams.objects.filter(query).order_by('-id')
            paginator = Paginator(activityDetailList, 10)
            page = request.GET.get('page')
            index_resp = paginator.get_page(page)
            return render(request, 'index.html', {'activities': activityDetailList, 'index_resp': index_resp, 'userPhoto':userphoto})
        else:
            return render(request, 'index.html', {})
    else:
        return HttpResponseRedirect("/streampage/login")

def browsePage(request):
    if Communities.objects.all():
        Community_List = Communities.objects.filter(communityPrv=False).order_by('-communityCreationDate')
        paginator = Paginator(Community_List, 3)
        page = request.GET.get('page')
        community_resp = paginator.get_page(page)
        return render(request, 'browse.html', {'community_resp': community_resp})
    else:
        return render(request, 'login.html', {})

def PosttypePageBrowse(request):
    try:
        CommunityHash = request.GET.get('showDataTypes')
        Community_List = Communities.objects.filter(communityHash=CommunityHash)
        currentCommunity = Community_List[0]
        postEntries={}
        c = connection.cursor()
        postHashQuery='select "entryHash" from streampage_posts where "relatedCommunityforPost_id" ='+str(currentCommunity.id)+' group by "entryHash"'
        c.execute(postHashQuery)
        posts=c.fetchall()
        postInstance=[]
        for hashes in posts:
            currentObject={}
            postInfo = PostsMetaHash.objects.filter(postMetaHash=hashes[0])[0]
            currentObject['postList']=Posts.objects.filter(entryHash=hashes[0])
            currentObject['posttype']=Posts.objects.filter(entryHash=hashes[0])[0].relatedDatatypes.datatypefields_set.all()
            currentObject['comments']=postInfo.postcomments_set.all().order_by('-id')
            postInstance.append(currentObject)
        postEntries['postInstances']=postInstance
        print(postEntries)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page)
        comment=textComment()
        return render(request, 'browseDatatypes.html', {'postEntries':postEntries, 'comment': comment, 'post_resp': post_resp, 'community_Hash':CommunityHash, 'community':Community_List[0]})
    except:
        return HttpResponseRedirect("/streampage/login")

def showPostDetailsBrowse_view(request):
    try:
        EntryHash = request.GET.get('postHash')
        queryPost = Posts.objects.filter(entryHash=EntryHash)
        currentPost = queryPost[0]
        relatedCommunity = currentPost.relatedCommunityforPost
        relatedPosttype = currentPost.relatedDatatypes
        postEntries={}
        postInstance=[]
        currentObject={}
        postInfo = PostsMetaHash.objects.filter(postMetaHash=EntryHash)[0]
        currentObject['postList']=Posts.objects.filter(entryHash=EntryHash)
        currentObject['posttype']=Posts.objects.filter(entryHash=EntryHash)[0].relatedDatatypes.datatypefields_set.all()
        currentObject['comments']=postInfo.postcomments_set.all().order_by('-id')
        postInstance.append(currentObject)
        postEntries['postInstances']=postInstance
        comment=textComment()
        return render(request, 'postDetailsBrowse.html', {'postEntries':postEntries, 'comment': comment, 'community':relatedCommunity, 'posttype': relatedPosttype })
    except:
        return HttpResponseRedirect("/streampage/login")

def communityPage(request):
    if request.user.is_authenticated:
        if Communities.objects.all():
            Community_List = Communities.objects.all().order_by('-communityCreationDate')
            Cuser = request.user
            UserList = communityUsers.objects.filter(nickName=Cuser)[0]
            userphoto = UserList.userPhoto
            User_communities = UserList.members.all().order_by('-id')
            paginator = Paginator(Community_List, 3)
            page = request.GET.get('page')
            community_resp = paginator.get_page(page)
            return render(request, 'community.html', {'community_resp': community_resp, 'User_communities': User_communities, 'userPhoto':userphoto})
        else:
            return render(request, 'community.html', {})
    else:
        return HttpResponseRedirect("/streampage/login")
		
	
def communityForm(request):
    form = AddCommunity()
    return render(request, 'modal.html', {'form': form})

def populateProvince(request):
    country = request.GET.__getitem__("country")
    provinceList = []

    if(str(country) == "Turkey"):
        provinceList = ['Adana', 'Adıyaman', 'Afyon', 'Ağrı', 'Aksaray', 'Amasya', 'Ankara', 'Antalya', 'Ardahan', 'Artvin', 'Aydın', 'Balıkesir', 'Bartın', 'Batman',
                        'Bayburt', 'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli', 'Diyarbakır', 'Düzce', 'Edirne',
                        'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkari', 'Hatay', 'Içel', 'Iğdır', 'Isparta', 'İstanbul',
                        'İzmir', 'Kahramanmaraş', 'Karabük', 'Karaman', 'Kars', 'Kastamonu', 'Kayseri', 'Kilis', 'Kırıkkale', 'Kırklareli', 'Kırşehir', 'Kocaeli', 'Konya',
                        'Kütahya', 'Malatya', 'Manisa', 'Mardin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Osmaniye', 'Rize', 'Sakarya', 'Samsun', 'Şanlıurfa', 'Siirt',
                        'Sinop', 'Şırnak', 'Sivas', 'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli', 'Uşak', 'Van', 'Yalova', 'Yozgat', 'Zonguldak']
    else:
        try:
            if CountryInfo(str(country)).provinces() != None:
                for province in CountryInfo(str(country)).provinces():
                    provinceList.append(province)
        except:
            print("exception")

    return JsonResponse({'provinceList': provinceList})

def handle_uploaded_file(f):
    filepath = 'streampage/static/uploads/communities/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"

def CreateCommunity_view(request):
    form = AddCommunity(request.POST, request.FILES)
    c_image=request.FILES.get("Community_Image")
    image_path=handle_uploaded_file(c_image)

    comm = Communities()
    comm.name = request.POST.get("Community_Name")
    comm.description = request.POST.get("Community_Description")
    salt = uuid.uuid4().hex
    commhash =  hashlib.sha256(salt.encode() + comm.name.encode()).hexdigest() + salt
    comm.communityHash = commhash
    if request.POST.get("Private_Community"):
        comm.communityPrv = True
    else:
        comm.communityPrv = False
    comm.communityPhoto = image_path
    comm.communityCountry = request.POST.get("Community_Country")
    comm.communityLocation = request.POST.get("Community_Location")
    comm.communityTags = request.POST.get("Community_Tags")
    comm.communityCreationDate = datetime.now()
    comm.communityCreator = communityUsers.objects.get(nickName=request.user)
    comm.save()
    comm.communityMembers.add(communityUsers.objects.get(nickName=request.user))
    comm.save()
    Tags = saveTag_view(request.POST.get("Community_Tags"))
    tagentry = CommunityTags()
    relatedComm = Communities.objects.filter(communityHash=commhash)[0]
    tagentry.communityTag = relatedComm
    tagentry.tagName = Tags["TITLE"]
    tagentry.tagItem = Tags["ITEM"]
    tagentry.save()

    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "created",
        "published": str(comm.communityCreationDate),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Community",
            "name": comm.name,
            "hash": comm.communityHash
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form' : "Community is created Successfully!"})


def EditCommunityModal_view(request):
    form = EditCommunity()
    return render(request, 'modal.html', {'form': form})
	
def EditCommunity_view(request):
    try:
        form = EditCommunity(request.POST, request.FILES)
        c_image=request.FILES.get("Community_Image")
        image_path=handle_uploaded_file(c_image)
        communityHash = request.POST.get("community_Hash")
        comm = Communities.objects.filter(communityHash=communityHash)[0]
        comm.description = request.POST.get("Community_Description")
        if request.POST.get("Private_Community"):
            comm.communityPrv = True
        else:
            comm.communityPrv = False
        comm.communityPhoto = image_path
        comm.communityTags = request.POST.get("Community_Tags")
        comm.communityCreationDate = datetime.now()
        comm.communityCreator = communityUsers.objects.get(nickName=request.user)
        comm.save()
        comm.communityMembers.add(communityUsers.objects.get(nickName=request.user))
        comm.save()
        Tags = saveTag_view(request.POST.get("Community_Tags"))
        tagentry = CommunityTags()
        relatedComm = comm
        tagentry.communityTag = relatedComm
        tagentry.tagName = Tags["TITLE"] 
        tagentry.tagItem = Tags["ITEM"]
        tagentry.save()
        activityStream = ActivityStreams()
        description = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "edited",
            "published": str(comm.communityCreationDate),
            "actor": {
                "id": "",
                "name": communityUsers.objects.get(nickName=request.user).nickName,
                "photo": communityUsers.objects.get(nickName=request.user).userPhoto
            },
            "object": {
                "id": "",
                "type": "Community",
                "name": comm.name,
                "hash": comm.communityHash
            }
        }
        ActivityStreams.objects.create(detail = description)
        return render(None, 'tagSearch.html', {'form' : "Community is Edited Successfully!"})
    except:
        return render(None, 'tagSearch.html', {'form' : "Community cannot be Edited Successfully!"})


def JoinCommunity_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Comm = Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    Comm.communityMembers.add(userModel)
    Comm.save()

    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "joined",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Community",
            "name": Comm.name,
            "hash": Comm.communityHash
        }
    }
    ActivityStreams.objects.create(detail = description)

    return render(None, 'tagSearch.html', {'form': "You joined to Community Successfully!"})
	
def LeaveCommunity_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Comm = Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    Comm.communityMembers.remove(userModel)
    Comm.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "left",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Community",
            "name": Comm.name,
            "hash": Comm.communityHash
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form': "You left from Community successfully!"})

def CheckMembership_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    if Communities.objects.filter(communityMembers=userModel,communityHash=request.POST.get("community_Hash")):
        return render(None, 'tagSearch.html', {'form': "Yes"})
    else:
        return render(None, 'tagSearch.html', {'form': "No"})
	
def VoteCommunity_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Comm = Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    Comm.communityPopularity.add(userModel)
    return render(request, 'tagSearch.html', {'form': form})

def DeleteCommunity_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Comm = Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    name = Comm.name
    comCreator = Comm.communityCreator
    if str(user) == str(comCreator):
        try:
            Comm.delete()
            activityStream = ActivityStreams()
            description = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "deleted",
                "published": str(datetime.now()),
                "actor": {
                    "id": "",
                    "name": communityUsers.objects.get(nickName=request.user).nickName,
                    "photo": communityUsers.objects.get(nickName=request.user).userPhoto
                },
                "object": {
                    "id": "",
                    "type": "Community",
                    "name": name,
                }
            }
            ActivityStreams.objects.create(detail = description)
            return render(None, 'tagSearch.html', {'form': name+" Community has been Deleted Successfully !"})
        except:
            return render(None, 'tagSearch.html', {'form': name+" Community cannot be Deleted!"})        

def posttypeForm(request):
    form = AddPosttype()
    return render(request, 'modal.html', {'form': form})


def searchTag_view(request):
    txtSRC = request.GET.get('search_text')
    SEARCHPAGE = txtSRC
    PARAMS = {
		"action":"wbsearchentities",
		"format": "json",
		"limit": "50",
        "language":"en",
		"search": SEARCHPAGE
    }
    Srch = requests.Session()
    URL = "https://wikidata.org/w/api.php"
    Res = Srch.get(url=URL, params=PARAMS)
    DATA = Res.json()['search']
    titles=""
    for tt in DATA:
        if tt['label'] not in titles:
            titles+="#"+tt['label']
    return render(None, 'tagSearch.html', {'form' : titles})


#TODO
def PosttypePageBCK(request):
    if request.user.is_authenticated:
        CommunityHash = request.GET.get('showDataTypes')
        Community_List = Communities.objects.filter(communityHash=CommunityHash)
        c = connection.cursor()
        execution_string = 'select "entryHash",json_object_agg("propertyName","propertyValue") from (select "entryHash","propertyName","propertyValue" from streampage_posts) S GROUP BY "entryHash"'
        c.execute(execution_string)
        posts=c.fetchall()
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page)
        comment=textComment()
        return render(request, 'datatypes.html', {'comment': comment, 'post_resp': post_resp, 'community_Hash':CommunityHash, 'community':Community_List[0]})
    else:
        return HttpResponseRedirect("/streampage/login")

def PosttypePage(request):
    if request.user.is_authenticated:
        CommunityHash = request.GET.get('showDataTypes')
        Community_List = Communities.objects.filter(communityHash=CommunityHash)
        User = communityUsers.objects.filter(nickName=request.user)[0]
        userphoto = User.userPhoto
        currentCommunity = Community_List[0]
        postEntries={}
        c = connection.cursor()
        postHashQuery='select "entryHash", "postCreationDate" from streampage_posts where "relatedCommunityforPost_id" ='+str(currentCommunity.id)+' group by "entryHash","postCreationDate" order by "postCreationDate" desc '
        c.execute(postHashQuery)
        posts=c.fetchall()
        hashList=[]
        for tuples in posts:
            hashList.append(tuples[0])
        cleanPosts = list(dict.fromkeys(hashList))
        postInstance=[]
        for hashes in cleanPosts:
            currentObject={}
            postInfo = PostsMetaHash.objects.filter(postMetaHash=hashes)[0]
            currentObject['postList']=Posts.objects.filter(entryHash=hashes).order_by('-id')
            currentObject['posttype']=Posts.objects.filter(entryHash=hashes)[0].relatedDatatypes.datatypefields_set.all().order_by('-id')
            currentObject['comments']=postInfo.postcomments_set.all().order_by('-id')
            postInstance.append(currentObject)
        postEntries['postInstances']=postInstance
        print(postEntries)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page)
        comment=textComment()
        return render(request, 'datatypes.html', {'postEntries':postEntries, 'comment': comment, 'post_resp': post_resp, 'community_Hash':CommunityHash, 'community':Community_List[0], 'userPhoto':userphoto})
    else:
        return HttpResponseRedirect("/streampage/login")

def showPostDetails_view(request):
    if request.user.is_authenticated:
        EntryHash = request.GET.get('postHash')
        User = communityUsers.objects.filter(nickName=request.user)[0]
        userphoto = User.userPhoto
        queryPost = Posts.objects.filter(entryHash=EntryHash)
        currentPost = queryPost[0]
        relatedCommunity = currentPost.relatedCommunityforPost
        relatedPosttype = currentPost.relatedDatatypes
        postEntries={}
        postInstance=[]
        currentObject={}
        postInfo = PostsMetaHash.objects.filter(postMetaHash=EntryHash)[0]
        currentObject['postList']=Posts.objects.filter(entryHash=EntryHash)
        currentObject['posttype']=Posts.objects.filter(entryHash=EntryHash)[0].relatedDatatypes.datatypefields_set.all()
        currentObject['comments']=postInfo.postcomments_set.all().order_by('-id')
        postInstance.append(currentObject)
        postEntries['postInstances']=postInstance
        comment=textComment()
        return render(request, 'postDetails.html', {'postEntries':postEntries, 'comment': comment, 'community':relatedCommunity, 'posttype': relatedPosttype, 'userPhoto':userphoto })
    else:
        return HttpResponseRedirect("/streampage/login")
    
def PostPage(request):
    if request.user.is_authenticated:
        DatatypeResult = Datatypes.objects.filter(datatypeHash=request.GET.get('showPosts'))
        DatatypeHash = DatatypeResult[0].datatypeHash
        DatatypeId = DatatypeResult[0].id		
        RCommunityFilter = DatatypeResult[0].relatedCommunity
        RCommunity = Communities.objects.filter(name=RCommunityFilter.name)
        Primitive_List = DatatypeResult[0].datatypefields_set.all()
        c = connection.cursor()
        execution_string = 'select "entryHash",json_object_agg("propertyName","propertyValue") from (select "entryHash","propertyName","propertyValue" from streampage_posts where "relatedDatatypes_id"='+str(DatatypeId)+') S GROUP BY "entryHash"'
        c.execute(execution_string)
        posts=c.fetchall()
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page)
        return render(request, 'posts.html', {'post_resp': post_resp,'table_fields':Primitive_List,'Datatype_Id':DatatypeHash, 'Datatype_Name':DatatypeResult, 'Community_Name': RCommunity})
    else:
        return HttpResponseRedirect("/streampage/login")


def handle_uploaded_datatypefile(f):
    filepath = 'streampage/static/uploads/datatypes/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"

def CreatePosttype_view(request):
    form = AddPosttype(request.POST, request.FILES)
    dt = Datatypes()
    dt.name = request.POST.get("Posttype_Name")
    salt = uuid.uuid4().hex
    communityHash=request.POST.get("community_Hash")
    DtHash = hashlib.sha256(salt.encode() + dt.name.encode()).hexdigest() + salt
    dt.datatypeHash = DtHash
    dt.relatedCommunity=Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    dt.datatypeTags = request.POST.get("Posttype_Tags")
    dt.datatypeCreationDate = datetime.now()
    dt.datatypeCreator = communityUsers.objects.get(nickName=request.user)
    dt.save()
    Tags = saveTag_view(request.POST.get("Posttype_Tags"))
    tagentry = DatatTypeTags()
    relatedDt = Datatypes.objects.filter(datatypeHash=DtHash)[0] 
    tagentry.datatypeTag = relatedDt
    tagentry.tagName = Tags["TITLE"] 
    tagentry.tagItem = Tags["ITEM"]
    tagentry.save()

    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "created",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": dt.name,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": dt.relatedCommunity.name,
            "hash": dt.relatedCommunity.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return JsonResponse({'form' : "Posttype is created Successfully!",'communityHash' : communityHash, 'posttypeHash':DtHash}) 

def EditPosttypeMeta_view(request):
    dt_hash = request.POST.get("Posttype_Hash")
    dt = Datatypes.objects.filter(datatypeHash = dt_hash)[0]
    dt.name = request.POST.get("Posttype_Name")
    dt.datatypeTags = request.POST.get("Posttype_Tags")
    dt.datatypeCreationDate = datetime.now()
    dt.datatypeCreator = communityUsers.objects.get(nickName=request.user)
    dt.save()
    Tags = saveTag_view(request.POST.get("Posttype_Tags"))
    tagentry = DatatTypeTags()
    relatedDt = Datatypes.objects.filter(datatypeHash=dt_hash)[0] 
    tagentry.datatypeTag = relatedDt
    tagentry.tagName = Tags["TITLE"] 
    tagentry.tagItem = Tags["ITEM"]
    tagentry.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "edited",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": dt.name,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": dt.relatedCommunity.name,
            "hash": dt.relatedCommunity.communityHash
        }
    }
    ActivityStreams.objects.create(detail = description)
    return JsonResponse({'form' : "Posttype is updated Successfully!",'posttypeHash':dt_hash})

def DeletePosttypeMeta_view(request):
    dt_hash = request.POST.get("Posttype_Hash")
    dt = Datatypes.objects.filter(datatypeHash = dt_hash)[0]
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "deleted",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": dt.name,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": dt.relatedCommunity.name,
            "hash": dt.relatedCommunity.communityHash
        }
    }
    ActivityStreams.objects.create(detail = description)
    dt.delete()
    return JsonResponse({'form' : "Posttype is deleted Successfully!",'posttypeHash':dt_hash})
	

def addPosttypeField_view(request):
    EnField = request.POST.get("Enumeration")
    if EnField == 'on':
        form = AddTextEntryEnum()
    else:
        form = AddTextEntry()
    return render(None, 'modalPost.html', {'form' : form })


def SavePrimitives_view(request):
    name = request.POST.get("name")
    type = request.POST.get("Types")
    req = request.POST.get("Required")
    show = request.POST.get("ShowPage")
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("PosttypeHash")
    postType = Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
    try:
        checkName = postType.datatypefields_set.filter(name=name)[0].name
        if  checkName == name:
            Enumeration = request.POST.get("Enum")
            dtFields = DatatypeFields.objects.filter(name=name,relatedDatatype=postType)[0]
            dtFields.fieldCreationDate = datetime.now()
            dtFields.fieldCreator = communityUsers.objects.get(nickName=request.user)
            if req == 'on':
                dtFields.fieldRequired = True
            else:
                dtFields.fieldRequired = False
            if show == 'on':
                dtFields.fronttableShow = True
            else:
                dtFields.fronttableShow = False	
            if name == '':
                return render(None, 'tagSearch.html', {'form' : "Please Enter The Name!!"})
            elif type == '':
                return render(None, 'tagSearch.html', {'form' : "Please Choose The Type!!"})
            else:
                if Enumeration is None:
                    typefield = Primitives.objects.get(name=type)
                    dtFields.name = name
                    dtFields.relatedDatatype = Datatypes.objects.get(datatypeHash=DatatypeHash)
                    dtFields.relatedComm = Communities.objects.get(communityHash=CommunityHash)
                    dtFields.relatedPrimitives = typefield
                    dtFields.save()
                    activityStream = ActivityStreams()
                    description = {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "updated",
                        "published": str(datetime.now()),
                        "actor": {
                            "id": "",
                            "name": communityUsers.objects.get(nickName=request.user).nickName,
                            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
                        },
                        "object": {
                            "id": "",
                            "type": "PosttypeField",
                            "name": Datatypes.objects.get(datatypeHash=DatatypeHash).name
                        },
                        "target": {
                            "id": "",
                            "type": "Community",
                            "name": Communities.objects.get(communityHash=CommunityHash).name,
                            "hash": Communities.objects.get(communityHash=CommunityHash).communityHash,
                        }
                    }
                    ActivityStreams.objects.create(detail = description)
                    return render(None, 'tagSearch.html', {'form' : "Data is updated!"})
                else:
                    if Enumeration == '':
                        return render(None, 'tagSearch.html', {'form' : "Please Enter the Enumeration Fields!"})
                    else:
                        typefield = Primitives.objects.get(name=type)
                        dtFields.name = name
                        dtFields.relatedDatatype = Datatypes.objects.get(datatypeHash=DatatypeHash)
                        dtFields.relatedComm = Communities.objects.get(communityHash=CommunityHash)
                        dtFields.relatedPrimitives = typefield
                        dtFields.enumerations = Enumeration
                        dtFields.save()
                        activityStream = ActivityStreams()
                        description = {
                            "@context": "https://www.w3.org/ns/activitystreams",
                            "type": "updated",
                            "published": str(datetime.now()),
                            "actor": {
                                "id": "",
                                "name": communityUsers.objects.get(nickName=request.user).nickName,
                                "photo": communityUsers.objects.get(nickName=request.user).userPhoto
                            },
                            "object": {
                                "id": "",
                                "type": "PosttypeField",
                                "name": Datatypes.objects.get(datatypeHash=DatatypeHash).name
                            },
                            "target": {
                                "id": "",
                                "type": "Community",
                                "name": Communities.objects.get(communityHash=CommunityHash).name,
                                "hash": Communities.objects.get(communityHash=CommunityHash).communityHash,
                            }
                        }
                        ActivityStreams.objects.create(detail = description)
                        return render(None, 'tagSearch.html', {'form' : "Data is updated!"})
    except:
        Enumeration = request.POST.get("Enum")
        dtFields = DatatypeFields()
        dtFields.fieldCreationDate = datetime.now()
        dtFields.fieldCreator = communityUsers.objects.get(nickName=request.user)
        if req == 'on':
            dtFields.fieldRequired = True
        else:
            dtFields.fieldRequired = False
        if show == 'on':
            dtFields.fronttableShow = True
        else:
            dtFields.fronttableShow = False	
        if name == '':
            return render(None, 'tagSearch.html', {'form' : "Please Enter The Name!!"})
        elif type == '':
            return render(None, 'tagSearch.html', {'form' : "Please Choose The Type!!"})
        else:
            if Enumeration is None:
                typefield = Primitives.objects.get(name=type)
                dtFields.name = name
                dtFields.relatedDatatype = Datatypes.objects.get(datatypeHash=DatatypeHash)
                dtFields.relatedComm = Communities.objects.get(communityHash=CommunityHash)
                dtFields.relatedPrimitives = typefield
                dtFields.save()
                activityStream = ActivityStreams()
                description = {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "type": "added",
                    "published": str(datetime.now()),
                    "actor": {
                        "id": "",
                        "name": communityUsers.objects.get(nickName=request.user).nickName,
                        "photo": communityUsers.objects.get(nickName=request.user).userPhoto
                    },
                    "object": {
                        "id": "",
                        "type": "PosttypeField",
                        "name": Datatypes.objects.get(datatypeHash=DatatypeHash).name
                    },
                    "target": {
                        "id": "",
                        "type": "Community",
                        "name": Communities.objects.get(communityHash=CommunityHash).name,
                        "hash": Communities.objects.get(communityHash=CommunityHash).communityHash,
                    }
                }
                ActivityStreams.objects.create(detail = description)
                return render(None, 'tagSearch.html', {'form' : "Data is saved!"})
            else:
                if Enumeration == '':
                    return render(None, 'tagSearch.html', {'form' : "Please Enter the Enumeration Fields!"})
                else:
                    typefield = Primitives.objects.get(name=type)
                    dtFields.name = name
                    dtFields.relatedDatatype = Datatypes.objects.get(datatypeHash=DatatypeHash)
                    dtFields.relatedComm = Communities.objects.get(communityHash=CommunityHash)
                    dtFields.relatedPrimitives = typefield
                    dtFields.enumerations = Enumeration
                    dtFields.save()
                    activityStream = ActivityStreams()
                    description = {
                        "@context": "https://www.w3.org/ns/activitystreams",
                        "type": "added",
                        "published": str(datetime.now()),
                        "actor": {
                            "id": "",
                            "name": communityUsers.objects.get(nickName=request.user).nickName,
                            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
                        },
                        "object": {
                            "id": "",
                            "type": "PosttypeField",
                            "name": Datatypes.objects.get(datatypeHash=DatatypeHash).name
                        },
                        "target": {
                            "id": "",
                            "type": "Community",
                            "name": Communities.objects.get(communityHash=CommunityHash).name,
                            "hash": Communities.objects.get(communityHash=CommunityHash).communityHash,
                        }
                    }
                    ActivityStreams.objects.create(detail = description)
                    return render(None, 'tagSearch.html', {'form' : "Data is saved!"})

def DeletePosttypeFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    Dt= Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
    name = request.POST.get("name")
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "deleted",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
            "object": {
            "id": "",
            "type": "PosttypeField",
            "name": Datatypes.objects.get(datatypeHash=DatatypeHash).name
        },
            "target": {
            "id": "",
            "type": "Community",
            "name": Communities.objects.get(communityHash=CommunityHash).name,
            "hash": Communities.objects.get(communityHash=CommunityHash).communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    HiddenPosts= Posts.objects.filter(propertyName=name,relatedDatatypes=Dt).delete()
    DatatypeFields.objects.filter(name=name,relatedDatatype=Dt).delete()
    return render(None, 'tagSearch.html', {'form' : "Posttyype Field is Deleted Successfully!"})

def EditPosttypes_view(request):
    CommunityHash = request.GET.get("community_Hash")
    context={}
    form=posttypeList(cHash=CommunityHash)
    return render(request, 'modal.html', {'form': form})  


def ShowPosttypeFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    PosttypeName = request.POST.get("PosttypeEntry")
    Cm = Communities.objects.filter(communityHash=CommunityHash)[0]
    Dt = Cm.datatypes_set.filter(name=PosttypeName)[0]
    PostFields = DatatypeFields.objects.filter(relatedDatatype=Dt)
    if DatatypeFields.objects.filter(relatedDatatype = Dt):
        PtFields = DatatypeFields.objects.filter(relatedDatatype = Dt)
        context = {}
        iter=0
        for fields in PtFields:
            name = fields.name
            Types = fields.relatedPrimitives
            Required = fields.fieldRequired
            Show = fields.fronttableShow
            if fields.enumerations:
                Enum = fields.enumerations
                form = AddTextEntryEnum(initial={'name': name, 'Types': Types, 'Required': Required, 'ShowPage': Show, 'Enum': Enum})
                context['form'+str(iter)]=form
            else:
                form = AddTextEntry(initial={'name': name, 'Types': Types, 'Required': Required, 'ShowPage': Show})
                context['form'+str(iter)]=form
            iter +=1
        return render(None, 'showDataTypeFields.html', {'form':context, 'posttypeHash':Dt.datatypeHash})
    else:
        return render(None, 'showDataTypeFields.html', {'form':"Yes", 'posttypeHash':Dt.datatypeHash})

def DeletePosttypes_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    PosttypeName = request.POST.get("PosttypeEntry")
    Cm = Communities.objects.filter(communityHash=CommunityHash)[0]
    Dt = Cm.datatypes_set.filter(name=PosttypeName)[0].delete()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "deleted",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": PosttypeName,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": Cm.name,
            "hash": Cm.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form':"Selected posttype is deleted succesfully!"})

def addPosttypeEditField_view(request):
    EnField = request.POST.get("Enumeration")
    if EnField == 'on':
        form = AddTextEntryEnum()
    else:
        form = AddTextEntry()
    return render(None, 'modalPostEdit.html', {'form' : form })

def subscribePosttype_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Posttype = Posts.objects.filter(entryHash=request.POST.get("post_Hash"))[0].relatedDatatypes
    Posttype.subscribers.add(userModel)
    Posttype.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "subscribed",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": Posttype.name,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": Posttype.relatedCommunity.name,
            "hash": Posttype.relatedCommunity.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form': "You Subscribed to the Community Successfully!"})

def unsubscribePosttype_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Posttype = Posts.objects.filter(entryHash=request.POST.get("post_Hash"))[0].relatedDatatypes
    Posttype.subscribers.remove(userModel)
    Posttype.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "unsubscribed",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Posttype",
            "name": Posttype.name,
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": Posttype.relatedCommunity.name,
            "hash": Posttype.relatedCommunity.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form': "You Unsubscribed from the Community Successfully!"})

def reportPostModal_view(request):
    form = ReportPost()
    return render(None, 'tagSearch.html', {'form' : form })

def reportPost_view(request):
    PostHash = request.POST.get("post_Hash")
    try:
        PosttypeMeta = PostsMetaHash.objects.filter(postMetaHash=PostHash)[0]
        Cm = PosttypeMeta.relatedCommunity
        user = request.user
        userModel = communityUsers.objects.filter(nickName=user)[0]
        salt = uuid.uuid4().hex
        reportHash = hashlib.sha256(salt.encode() + request.POST.get("Report_Reason").encode()).hexdigest() + salt
        reportEntry = ReportedPosts()
        reportEntry.relatedCommunity = Cm
        reportEntry.relatedMeta = PosttypeMeta
        reportEntry.reportHash = reportHash
        reportEntry.reason = request.POST.get("Report_Reason")
        reportEntry.description = request.POST.get("Description")
        reportEntry.reportPostCreator = userModel
        reportEntry.reportPostCreationDate = datetime.now()
        reportEntry.save()
        return render(None, 'tagSearch.html', {'form' : 'You successfully reported the post!' })
    except:
        return render(None, 'tagSearch.html', {'form' : 'Reporting is unsuccessfull!' })

def reportPostDelete_view(request):
    PostHash = request.POST.get("post_Hash")
    try:
        user = request.user
        userModel = communityUsers.objects.filter(nickName=user)[0]
        reportEntry = ReportedPosts.objects.get(reportHash=PostHash)
        reportEntry.delete()
        return render(None, 'tagSearch.html', {'form' : 'The Report is Removed!' })
    except:
        return render(None, 'tagSearch.html', {'form' : 'The Report cannot be Removed!' })

def ReturnPostFields_view(request):
    CommunityHash = request.POST.get("community_Hash")
    PosttypeName = request.POST.get("PosttypeEntry")
    Cm = Communities.objects.filter(communityHash=CommunityHash)[0]
    Dt = Cm.datatypes_set.filter(name=PosttypeName)[0]
    PostFields = DatatypeFields.objects.filter(relatedDatatype=Dt)
    iter=0
    context={}
    for fields in PostFields:
        if fields.enumerations is not None:
            name = fields.name
            types = fields.relatedPrimitives.name
            req = fields.fieldRequired
            show = fields.fronttableShow
            enum = fields.enumerations
            enumList = enum.split(",")				
            context[fields.name]=AddEnumaratedPost(en=enumList,nm=name)			
        else:
            print(fields.relatedPrimitives.name)
            if fields.relatedPrimitives.name == "Text":
                context[fields.name]=AddTextPost()
            elif fields.relatedPrimitives.name == "Text Area":
                context[fields.name]=AddTextAreaPost()
            elif fields.relatedPrimitives.name == "Audio":
                context[fields.name]=AddAudioPost(request.POST, request.FILES)
            elif fields.relatedPrimitives.name == "Boolean":
                context[fields.name]=AddBooleanPost()
            elif fields.relatedPrimitives.name == "Date":
                context[fields.name]=AddDatePost()
            elif fields.relatedPrimitives.name == "DateTime":
                context[fields.name]=AddDateTimePost()
            elif fields.relatedPrimitives.name == "Decimal":
                context[fields.name]=AddDecimalPost()
            elif fields.relatedPrimitives.name == "E-mail":
                context[fields.name]=AddEmailPost()
            elif fields.relatedPrimitives.name == "Float":
                context[fields.name]=AddFloatPost()
            elif fields.relatedPrimitives.name == "IP Address":
                context[fields.name]=AddIpAddressPost()
            elif fields.relatedPrimitives.name == "Image":
                context[fields.name]=AddImagePost(request.POST, request.FILES)
            elif fields.relatedPrimitives.name == "Integer":
                context[fields.name]=AddIntegerPost()
            elif fields.relatedPrimitives.name == "Location":
                context[fields.name]=AddLocationPost()
            elif fields.relatedPrimitives.name == "Time":
                context[fields.name]=AddTimePost()
            elif fields.relatedPrimitives.name == "URL":
                context[fields.name]=AddUrlPost()
            elif fields.relatedPrimitives.name == "Video":
                context[fields.name]=AddVideoPost(request.POST, request.FILES)
            name = fields.name
            types = fields.relatedPrimitives.name
            req = fields.fieldRequired
            show = fields.fronttableShow
        iter += 1
    print(context)
    context["Tags"]=AddTagPost()
    return render(None, 'entryReturnFields.html', {'form' : context, 'posttypeHash':Dt.datatypeHash})


def AddPostModal_view(request):
    CommunityHash = request.POST.get("community_Hash")
    context={}
    form=posttypeList(cHash=CommunityHash)
    return render(request, 'modal.html', {'form': form})  


def handle_uploaded_postfile(f):
    filepath = 'streampage/static/uploads/posts/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"

def CreatePost_view(request):
    CommunityHash = request.POST.get("community_Hash")
    DatatypeHash = request.POST.get("PosttypeHash")
    Dt = Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
    PostFields = DatatypeFields.objects.filter(relatedDatatype=Dt)
    print(PostFields[0].name)
    salt = uuid.uuid4().hex
    try:
        PostHash = hashlib.sha256(salt.encode() + request.POST.get(PostFields[0].name).encode()).hexdigest() + salt
    except:
        PostHash = hashlib.sha256(salt.encode() + uuid.uuid4().hex.upper()[0:9].encode()).hexdigest() + salt
    PostTime = datetime.now()
    metaPost = PostsMetaHash()
    metaPost.relatedCommunity = Communities.objects.get(communityHash=CommunityHash)
    metaPost.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
    metaPost.postCreator = communityUsers.objects.get(nickName=request.user)
    metaPost.postCreationDate = PostTime
    metaPost.postMetaHash = PostHash
    metaPost.save()
    for fields in PostFields:
        if (fields.relatedPrimitives.name == "Image" or fields.relatedPrimitives.name == "Audio" or fields.relatedPrimitives.name == "Video") and request.POST.get(fields.name) != "":
            p_image=request.FILES.get(fields.name)
            file_path=handle_uploaded_postfile(p_image)
            entry = Posts()
            entry.propertyName = fields.name
            entry.propertyValue = file_path
            entry.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
            entry.relatedCommunityforPost = Communities.objects.get(communityHash=CommunityHash)
            entry.entryHash = PostHash
            entry.relatedMeta = PostsMetaHash.objects.get(postMetaHash = PostHash)
            entry.postCreator = communityUsers.objects.get(nickName=request.user)
            entry.postCreationDate = PostTime
            entry.postTag = request.POST.get("Tags")
            entry.save()		
        elif request.POST.get(fields.name) != "" and fields.relatedPrimitives.name != "Boolean":
            entry = Posts()
            entry.propertyName = fields.name
            entry.propertyValue = request.POST.get(fields.name)
            entry.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
            entry.relatedCommunityforPost = Communities.objects.get(communityHash=CommunityHash)
            entry.entryHash = PostHash
            entry.relatedMeta = PostsMetaHash.objects.get(postMetaHash = PostHash)
            entry.postCreator = communityUsers.objects.get(nickName=request.user)
            entry.postCreationDate = PostTime
            entry.postTag = request.POST.get("Tags")
            entry.save()
        elif fields.relatedPrimitives.name == "Boolean" and request.POST.get(fields.name) != "":
            entry = Posts()
            entry.propertyName = fields.name
            if entry.propertyValue == "on":
                entry.propertyValue = "Yes"
                entry.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
                entry.relatedCommunityforPost = Communities.objects.get(communityHash=CommunityHash)
                entry.entryHash = PostHash
                entry.relatedMeta = PostsMetaHash.objects.get(postMetaHash = PostHash)
                entry.postCreator = communityUsers.objects.get(nickName=request.user)
                entry.postCreationDate = PostTime
                entry.postTag = request.POST.get("Tags")
                entry.save()
            else:
                entry.propertyValue = "No"
                entry.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
                entry.relatedCommunityforPost = Communities.objects.get(communityHash=CommunityHash)
                entry.entryHash = PostHash
                entry.relatedMeta = PostsMetaHash.objects.get(postMetaHash = PostHash)
                entry.postCreator = communityUsers.objects.get(nickName=request.user)
                entry.postCreationDate = PostTime
                entry.postTag = request.POST.get("Tags")
                entry.save()
        else:
            if fields.fieldRequired == True:
                return render(None, 'tagSearch.html', {'form' : fields.name+" is required!"})
    Tags = saveTag_view(request.POST.get("Tags"))
    tagentry = PostTags()
    relatedPost = Posts.objects.filter(entryHash=PostHash)[0] 
    tagentry.relatedPostTag = relatedPost
    tagentry.tagName = Tags["TITLE"] 
    tagentry.tagItem = Tags["ITEM"]
    tagentry.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "created",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
        },
        "object": {
            "id": "",
            "type": "Post",
            "hash": entry.relatedMeta.postMetaHash,
            "posttype": Dt.name
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": entry.relatedCommunityforPost.name,
            "hash": entry.relatedCommunityforPost.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form' : "The Entry is Created Successfully"})
    
def DeletePost_view(request):
    PostHash = request.POST.get("PostHash")
    activityStream = ActivityStreams()
    entry = Posts.objects.filter(entryHash=PostHash)[0]
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "deleted",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
        },
        "object": {
            "id": "",
            "type": "Post",
            "posttype": entry.relatedDatatypes.name
        },
        "target": {
            "id": "",
            "type": "Community",
            "name": entry.relatedCommunityforPost.name,
            "hash": entry.relatedCommunityforPost.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    Posts.objects.filter(entryHash=PostHash).delete()
    return render(None, 'tagSearch.html', {'form' : "The Entry is deleted Successfully"})

def CreatePostComment_view(request):
    CommunityHash = request.POST.get("community_Hash")
    postHash = request.POST.get("post_Hash")
    salt = uuid.uuid4().hex
    commentHash = hashlib.sha256(salt.encode() + request.POST.get("Comment").encode()).hexdigest() + salt
    commentTime = datetime.now()
    test = Posts.objects.filter(entryHash = postHash)[0]
    entryComment = PostComments()
    entryComment.relatedCommunityforComment = Communities.objects.get(communityHash=CommunityHash)
    entryComment.relatedMeta = PostsMetaHash.objects.get(postMetaHash = postHash)
    entryComment.commentHash = commentHash
    entryComment.commentText = request.POST.get("Comment")
    entryComment.postCommentCreator = communityUsers.objects.get(nickName=request.user)
    entryComment.postCommentCreationDate = commentTime
    entryComment.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "commented",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
        },
        "object": {
            "id": "",
            "type": "Comment",
            "hash": entryComment.relatedMeta.postMetaHash,
            "name": entryComment.commentText,
            "posttype": entryComment.relatedMeta.relatedDatatypes.name,
        },
        "target": {
            "id": "",
            "name": entryComment.relatedCommunityforComment.name,
            "hash": entryComment.relatedCommunityforComment.communityHash,
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form' : "Successfully Commented on the Post!"})

def deletePostComment_view(request):
    commentHash = request.POST.get("comment_Hash")
    comment = PostComments.objects.filter(commentHash=commentHash)[0]
    try:
        activityStream = ActivityStreams()
        description = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "deleted",
            "published": str(datetime.now()),
            "actor": {
                "id": "",
                "name": communityUsers.objects.get(nickName=request.user).nickName,
                "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
            },
            "object": {
                "id": "",
                "type": "Comment",
                "hash": comment.relatedMeta.postMetaHash,
                "name": comment.commentText,
                "posttype": comment.relatedMeta.relatedDatatypes.name
            },
            "target": {
                "id": "",
                "type": "Post",
                "name": comment.relatedCommunityforComment.name,
                "hash": comment.relatedCommunityforComment.communityHash,
            }
        }
        comment.delete()
        ActivityStreams.objects.create(detail = description)
        return render(None, 'tagSearch.html', {'form' : "The Comment is Deleted Successfully!"})
    except:
        return render(None, 'tagSearch.html', {'form' : "The Comment cannot be deleted!"})


def login_view(request):
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request, user)
        activityStream = ActivityStreams()
        description = {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "login",
            "published": str(datetime.now()),
            "actor": {
                "id": "",
                "name": communityUsers.objects.get(nickName=request.user).nickName,
                "photo": communityUsers.objects.get(nickName=request.user).userPhoto
            }
        }
        ActivityStreams.objects.create(detail = description)
        return redirect("/streampage")
    return render(request, "login.html", {
		"form" : form,
		"title" : "Login",})


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        comUsers = communityUsers()
        comUsers.userMail = user.email
        comUsers.nickName = user.username
        comUsers.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect("/streampage/login")
    return render(request, "login.html", {
	    "title" : "Register",
	    "form" : form,
    })
 
def logout_view(request):
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "logged out",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        }
    }
    logout(request)
    ActivityStreams.objects.create(detail = description)
    return HttpResponseRedirect("/streampage/login")
	
def profilePage(request):
    if request.user.is_authenticated:
        username=request.user
        CUser = communityUsers.objects.filter(nickName=username)[0]
        userphoto = CUser.userPhoto
        Community_List = CUser.creator.all()
        reportList = []
        for comm in Community_List:
            reports = comm.reportedposts_set.all()
            for rp in reports:
                reportList.append(rp)
        Datatype_List = CUser.datatypecreator.all()
        Post_List = CUser.postcreator.all()
        joined_Communities = CUser.members.all()
        activityDetailList = ActivityStreams.objects.filter(detail__actor__name = str(username)).order_by('-id')
        subscriptionList = Datatypes.objects.filter(subscribers = CUser)
        followingList = []
        if len(UserCircle.objects.filter(circleOwner=CUser)) > 0:
            for i in UserCircle.objects.get(circleOwner=CUser).circleUsers.all():
                followingList.append(i.nickName)
        followerList = []
        for i in communityUsers.objects.get(nickName=username).Followers.all():
            followerList.append(i.circleOwner.nickName)
        return render(request, "profile.html", {
			"Communities" : Community_List,
			"Datatypes" : Datatype_List,
			"Posts" : Post_List,
			"Joined" : joined_Communities,
			"UserInfo" : CUser,
			"ReportList": reportList,
			"activities":activityDetailList,
			"followers" : followerList,
			"following" : followingList,
			"subscriptionList": subscriptionList,
			"userPhoto":userphoto
	})
    else:
        return HttpResponseRedirect("/streampage/login")
		
def chooseSearch_view(request):
    CommunityHash = request.POST.get("community_Hash")
    form=searchList(cHash=CommunityHash)
    return render(request, 'modal.html', {'form': form})

def ReturnSearchFields_view(request):
    CommunityHash = request.POST.get("community_Hash")
    DatatypeHash = request.POST.get("DatatypeHash")
    PostfieldName = request.POST.get("searchEntry")
    Cm = Communities.objects.filter(communityHash=CommunityHash)[0]
    PostFields = DatatypeFields.objects.filter(name=PostfieldName)
    fields=PostFields[0]
    context={}
    if fields.enumerations is not None:
        name = fields.name
        types = fields.relatedPrimitives.name
        req = fields.fieldRequired
        show = fields.fronttableShow
        enum = fields.enumerations
        enumList = enum.split(",")				
        context[fields.name]=AddEnumaratedSearch(en=enumList,nm=name)			
    else:
        if fields.relatedPrimitives.name == "Text":
            context[fields.name]=AddTextSearch()
        elif fields.relatedPrimitives.name == "Text Area":
            context[fields.name]=AddTextAreaSearch()
        elif fields.relatedPrimitives.name == "Audio":
            context[fields.name]=AddAudioSearch(request.POST, request.FILES)
        elif fields.relatedPrimitives.name == "Boolean":
            context[fields.name]=AddBooleanSearch()
        elif fields.relatedPrimitives.name == "Date":
            context[fields.name]=AddDateSearch()
        elif fields.relatedPrimitives.name == "DateTime":
            context[fields.name]=AddDateTimeSearch()
        elif fields.relatedPrimitives.name == "Decimal":
            context[fields.name]=AddDecimalSearch()
        elif fields.relatedPrimitives.name == "E-mail":
            context[fields.name]=AddEmailSearch()
        elif fields.relatedPrimitives.name == "Float":
            context[fields.name]=AddFloatSearch()
        elif fields.relatedPrimitives.name == "IP Address":
            context[fields.name]=AddIpAddressSearch()
        elif fields.relatedPrimitives.name == "Image":
            context[fields.name]=AddImageSearch(request.POST, request.FILES)
        elif fields.relatedPrimitives.name == "Integer":
            context[fields.name]=AddIntegerSearch()
        elif fields.relatedPrimitives.name == "Location":
            context[fields.name]=AddLocationSearch()
        elif fields.relatedPrimitives.name == "Time":
            context[fields.name]=AddTimeSearch()
        elif fields.relatedPrimitives.name == "URL":
            context[fields.name]=AddUrlSearch()
        elif fields.relatedPrimitives.name == "Video":
            context[fields.name]=AddVideoSearch(request.POST, request.FILES)
        name = fields.name
        types = fields.relatedPrimitives.name
        req = fields.fieldRequired
        show = fields.fronttableShow
        #context["Tags"]=AddTagSearch()
    return render(None, 'entrySearchFields.html', {'form' : context})
	
def ReturnFreeSearchFields_view(request):
    CommunityHash = request.POST.get("community_Hash")
    Cm = Communities.objects.filter(communityHash=CommunityHash)[0]
    context={}
    context["Free Search"]=freeSearchField()
    return render(None, 'entrySearchFields.html', {'form' : context})

def ReturnEntrySearchResults_view(request):
    CommunityHash = request.POST.get('CommunityHash')
    Community_List = Communities.objects.filter(communityHash=CommunityHash)
    User = communityUsers.objects.filter(nickName=request.user)[0]
    userphoto = User.userPhoto
    currentCommunity = Community_List[0]
    postEntries={}
    Dtfields = currentCommunity.datatypefields_set.all()
    if request.user.is_authenticated:
        querylist=[]
        querylistFree=[]
        for fields in Dtfields:
            print(request.POST.get("Free Search_Value"))
            subquery=""
            subqueryFree=""
            if request.POST.get(fields.name+"_Value"):
                if request.POST.get(fields.name+"_Condition") == "equals":
                    subquery = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" = "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "not equal":
                    subquery = "\"entryHash\" not in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" = "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "contains":
                    subquery = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" ~ "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "not contain":
                    subquery = "\"entryHash\" not in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" ~ "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "less than":
                    subquery = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND CAST(\"propertyValue\" as INTEGER)"+" < "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "more than":
                    subquery = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND CAST(\"propertyValue\" as INTEGER)"+" > "+"'"+request.POST.get(fields.name+"_Value")+"')"
                    querylist.append(subquery)
            elif request.POST.get(fields.name+"_Condition"):
                if request.POST.get(fields.name+"_Condition") == "equals":
                    subquery = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" = "+"'No')"
                    querylist.append(subquery)
                elif request.POST.get(fields.name+"_Condition") == "not equal":
                    subquery = "\"entryHash\" not in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" = "+"'No')"
                    querylist.append(subquery)
                
            if request.POST.get("Free Search_Value"):
                subqueryFree = "\"entryHash\" in (select \"entryHash\" from streampage_posts where \"propertyName\""+" = "+"'"+fields.name+"' AND \"propertyValue\""+" ~ "+"'"+request.POST.get("Free Search_Value")+"')"
                querylistFree.append(subqueryFree)
        querystring = " and ".join(querylist)
        querystringFree = " or ".join(querylistFree)
        RCommunity = Communities.objects.filter(communityHash=CommunityHash)
        c = connection.cursor()
        if querystring != "":
            execution_string = 'select "entryHash" from streampage_posts where '+querystring+' and "relatedCommunityforPost_id" ='+str(currentCommunity.id)+' GROUP BY "entryHash"'
        elif querystringFree != "":
            execution_string = 'select "entryHash" from streampage_posts where '+querystringFree+'  and "relatedCommunityforPost_id" ='+str(currentCommunity.id)+' GROUP BY "entryHash"'
        c.execute(execution_string)
        posts=c.fetchall()
        postInstance=[]
        for hashes in posts:
            currentObject={}
            postInfo = PostsMetaHash.objects.filter(postMetaHash=hashes[0])[0]
            currentObject['postList']=Posts.objects.filter(entryHash=hashes[0])
            currentObject['posttype']=Posts.objects.filter(entryHash=hashes[0])[0].relatedDatatypes.datatypefields_set.all()
            currentObject['comments']=postInfo.postcomments_set.all()
            postInstance.append(currentObject)
        postEntries['postInstances']=postInstance
        print(querystring)		
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page) 
        comment=textComment()
        return render(request, 'datatypes.html', {'postEntries':postEntries, 'comment': comment, 'post_resp': post_resp, 'community_Hash':CommunityHash, 'community':Community_List[0], 'userPhoto': userphoto})
    else:
        return HttpResponseRedirect("/streampage/login")


def uploadPhotoForm_view(request):
    form = AddImagePost()
    return render(request, 'tagSearch.html', {'form': form})

def handle_uploaded_profilefile(f):
    filepath = 'streampage/static/uploads/profiles/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"

def uploadPhoto_view(request):
    if request.user.is_authenticated:
        try:
            u_image = request.FILES.get("ImageEntry")
            userProfile = communityUsers.objects.get(nickName=request.user)
            image_path = handle_uploaded_profilefile(u_image)
            userProfile.userPhoto = image_path
            userProfile.save()
            activityStream = ActivityStreams()
            description = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "uploaded",
                "published": str(datetime.now()),
                "actor": {
                    "id": "",
                    "name": communityUsers.objects.get(nickName=request.user).nickName,
                    "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
                },
                "object": {
                    "id": "",
                    "type": "ProfilePhoto",
                    "name": image_path,
                },
                "target": {
                    "id": "",
                    "type": "Profile",
                }
            }
            ActivityStreams.objects.create(detail = description)
            return render(None, 'tagSearch.html', {'form' : 'The Photo is Saved Successfully!'})
        except:
            return render(None, 'tagSearch.html', {'form' : 'The Photo cannot be Saved!'})

def EditUserModal_view(request):
    form = EditUser()
    return render(request, 'modal.html', {'form': form})

def EditUser_view(request):
    if request.user.is_authenticated:
        try:
            name = request.POST.get("name")
            surname = request.POST.get("surname")
            birthday= request.POST.get("birth")
            email = request.POST.get("email")
            bio = request.POST.get("bio")
            userProfile = communityUsers.objects.get(nickName=request.user)
            userProfile.userName = name
            userProfile.userSurname = surname
            userProfile.userBirthDay = birthday
            userProfile.userMail = email
            userProfile.userBio = bio
            userProfile.save()
            activityStream = ActivityStreams()
            description = {
                "@context": "https://www.w3.org/ns/activitystreams",
                "type": "updated",
                "published": str(datetime.now()),
                "actor": {
                    "id": "",
                    "name": communityUsers.objects.get(nickName=request.user).nickName,
                    "photo": communityUsers.objects.get(nickName=request.user).userPhoto,
                },
                "object": {
                    "id": "",
                    "type": "ProfileInformation",
                    "email": email,
                    "bio" : bio,
                },
                "target": {
                    "id": "",
                    "type": "Profile Information",
                }
            }
            ActivityStreams.objects.create(detail = description)
            return render(None, 'tagSearch.html', {'form' : 'The Information is Updated Successfully!'})
        except:
            return render(None, 'tagSearch.html', {'form' : 'The Information cannot be Updated!'})

def UserPage_view(request):
    if request.user.is_authenticated:
        Username = request.GET.get('user')
        CUser = communityUsers.objects.filter(nickName=Username)[0]
        userphoto = communityUsers.objects.filter(nickName=request.user)[0].userPhoto
        Community_List = CUser.creator.all()
        Datatype_List = CUser.datatypecreator.all()
        Post_List = CUser.postcreator.all()
        joined_Communities = CUser.members.all()
        activityDetailList = ActivityStreams.objects.filter(detail__actor__name = str(Username)).order_by('-id')
        subscriptionList = Datatypes.objects.filter(subscribers = CUser)
        followingList = []
        if len(UserCircle.objects.filter(circleOwner=CUser)) > 0:
            for i in UserCircle.objects.get(circleOwner=CUser).circleUsers.all():
                followingList.append(i.nickName)
        followerList = []
        for i in communityUsers.objects.get(nickName=Username).Followers.all():
            followerList.append(i.circleOwner.nickName)
        if str(request.user) == str(Username):
            return render(request, "profile.html", {
				"Communities" : Community_List,
				"Datatypes" : Datatype_List,
				"Posts" : Post_List,
				"Joined" : joined_Communities,
				"UserInfo" : CUser,
				"activities": activityDetailList,
				"followers" : followerList,
				"following" : followingList,
				"subscriptionList": subscriptionList,
				"userPhoto": userphoto
			})
        else:
            return render(request, "user.html", {
				"Communities" : Community_List,
				"Datatypes" : Datatype_List,
				"Posts" : Post_List,
				"Joined" : joined_Communities,
				"UserInfo" : CUser,
				"activities": activityDetailList,
				"followers" : followerList,
				"following" : followingList,
				"subscriptionList": subscriptionList,
				"userPhoto": userphoto
			})
    else:
        return HttpResponseRedirect("/streampage/login")

def FollowUser_view(request):
    user = request.user
    Username = request.POST.get('user')
    userModel = communityUsers.objects.filter(nickName=user)[0]
    followingUser = communityUsers.objects.filter(nickName=Username)[0]
    try:
        circUser = UserCircle.objects.get(circleOwner=userModel)
        circUser.circleUsers.add(followingUser)
        circUser.save()
    except:
        circUser = UserCircle()
        circUser.circleOwner = userModel
        circUser.save()
        addFollower = UserCircle.objects.get(circleOwner=userModel)
        addFollower.circleUsers.add(followingUser)
        addFollower.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "followed",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Username",
            "name": str(followingUser.nickName),
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form': "You are following the user!"})

def UnFollowUser_view(request):
    user = request.user
    Username = request.POST.get('user')
    userModel = communityUsers.objects.filter(nickName=user)[0]
    followingUser = communityUsers.objects.filter(nickName=Username)[0]
    circUser = UserCircle.objects.get(circleOwner=userModel)
    circUser.circleUsers.remove(followingUser)
    circUser.save()
    activityStream = ActivityStreams()
    description = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "unfollowed",
        "published": str(datetime.now()),
        "actor": {
            "id": "",
            "name": communityUsers.objects.get(nickName=request.user).nickName,
            "photo": communityUsers.objects.get(nickName=request.user).userPhoto
        },
        "object": {
            "id": "",
            "type": "Username",
            "name": str(followingUser.nickName),
        }
    }
    ActivityStreams.objects.create(detail = description)
    return render(None, 'tagSearch.html', {'form': "You are unfollowing the user!"})

def communityPageSearch_view(request):
    if request.user.is_authenticated:
        if request.GET.get('keyword'):
            if Communities.objects.all():
                searchString = request.GET.get('keyword')
                Community_List = Communities.objects.filter(description__contains=searchString).order_by('-communityCreationDate') | Communities.objects.filter(name__contains=searchString).order_by('-communityCreationDate')
                Cuser = request.user
                UserList = communityUsers.objects.filter(nickName=Cuser)[0]
                userphoto = UserList.userPhoto
                User_communities = UserList.members.all()
                paginator = Paginator(Community_List, 3)
                page = request.GET.get('page')
                community_resp = paginator.get_page(page)
                return render(request, 'community.html', {'community_resp': community_resp, 'User_communities': User_communities, 'userPhoto': userphoto })
            else:
                return render(request, 'community.html', {})
        else:
            if Communities.objects.all():
                Community_List = Communities.objects.all().order_by('-communityCreationDate')
                Cuser = request.user
                UserList = communityUsers.objects.filter(nickName=Cuser)[0]
                userphoto = UserList.userPhoto
                User_communities = UserList.members.all()
                paginator = Paginator(Community_List, 3)
                page = request.GET.get('page')
                community_resp = paginator.get_page(page)
                return render(request, 'community.html', {'community_resp': community_resp, 'User_communities': User_communities, 'userPhoto': userphoto })
            else:
                return render(request, 'community.html', {})
		
    else:
        return HttpResponseRedirect("/streampage/login")


def communityLocationPageSearch_view(request):
    if request.user.is_authenticated:
        if request.GET.get('keyword'):
            if Communities.objects.all():
                searchString = request.GET.get('keyword')
                text_true = unicode_tr(searchString)
                print(text_true.capitalize())
                Community_List = Communities.objects.filter(communityCountry__icontains = text_true.capitalize()).order_by(
                    '-communityCreationDate') | Communities.objects.filter(communityLocation__icontains=text_true.capitalize()).order_by(
                    '-communityCreationDate')
                Cuser = request.user
                UserList = communityUsers.objects.filter(nickName=Cuser)[0]
                userphoto = UserList.userPhoto
                User_communities = UserList.members.all()
                paginator = Paginator(Community_List, 3)
                page = request.GET.get('page')
                community_resp = paginator.get_page(page)
                return render(request, 'community.html',
                              {'community_resp': community_resp, 'User_communities': User_communities,
                               'userPhoto': userphoto})
            else:
                return render(request, 'community.html', {})
        else:
            if Communities.objects.all():
                Community_List = Communities.objects.all().order_by('-communityCreationDate')
                Cuser = request.user
                UserList = communityUsers.objects.filter(nickName=Cuser)[0]
                userphoto = UserList.userPhoto
                User_communities = UserList.members.all()
                paginator = Paginator(Community_List, 3)
                page = request.GET.get('page')
                community_resp = paginator.get_page(page)
                return render(request, 'community.html',
                              {'community_resp': community_resp, 'User_communities': User_communities,
                               'userPhoto': userphoto})
            else:
                return render(request, 'community.html', {})

    else:
        return HttpResponseRedirect("/streampage/login")