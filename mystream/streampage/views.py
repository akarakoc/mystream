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
from .forms import AddTextEntry, AddTextEntryEnum, AddTagPost, AddTextPost, AddTextAreaPost, AddImagePost, AddAudioPost, AddVideoPost, AddBooleanPost, AddEmailPost, AddIpAddressPost, AddUrlPost, AddDatePost, AddTimePost, AddDateTimePost, AddIntegerPost, AddDecimalPost, AddFloatPost, AddEnumaratedPost, AddLocationPost
from .forms import AddTextEntry, AddTextEntryEnum, AddTagSearch, AddTextSearch, AddTextAreaSearch, AddImageSearch, AddAudioSearch, AddVideoSearch, AddBooleanSearch, AddEmailSearch, AddIpAddressSearch, AddUrlSearch, AddDateSearch, AddTimeSearch, AddDateTimeSearch, AddIntegerSearch, AddDecimalSearch, AddFloatSearch, AddEnumaratedSearch, AddLocationSearch
from .forms import posttypeList
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
from streampage.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts,CommunityTags,DatatTypeTags,PostTags,UserTags



def saveTagSearch_view(src):
    SEARCHPAGE = src	
    PARAMS = {
		"action":"wbsearchentities",
		"format": "json",
		"limit": "10",
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
        if iter is not '':
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
        return render(request, 'index.html', {})
    else:
        return HttpResponseRedirect("/streampage/login")

def communityPage(request):
    if request.user.is_authenticated:
        if Communities.objects.all():
            Community_List = Communities.objects.all().order_by('-communityCreationDate')
            Cuser = request.user
            UserList = communityUsers.objects.filter(nickName=Cuser)[0]
            User_communities = UserList.members.all()
            paginator = Paginator(Community_List, 3)
            page = request.GET.get('page')
            community_resp = paginator.get_page(page)
            return render(request, 'community.html', {'community_resp': community_resp, 'User_communities': User_communities})
        else:
            return render(request, 'community.html', {})
    else:
        return HttpResponseRedirect("/streampage/login")
		
	
def communityForm(request):
    form = AddCommunity()
    return render(request, 'modal.html', {'form': form})
	
def JoinCommunity_view(request):
    user = request.user
    userModel = communityUsers.objects.filter(nickName=user)[0]
    Comm = Communities.objects.get(communityHash=request.POST.get("community_Hash"))
    Comm.communityMembers.add(userModel)
    Comm.save()	
    return render(request, 'tagSearch.html', {'form': "You joined successfully!"})
	
def LeftCommunity_view(request):
    return render(request, 'tagSearch.html', {'form': form})

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
	
def posttypeForm(request):
    form = AddPosttype()
    return render(request, 'modal.html', {'form': form})

def searchTag_view(request):
    txtSRC = request.GET.get('search_text')
    SEARCHPAGE = txtSRC	
    PARAMS = {
		"action":"wbsearchentities",
		"format": "json",
		"limit": "10",
        "language":"en",
		"search": SEARCHPAGE
    }
    Srch = requests.Session()
    URL = "https://wikidata.org/w/api.php"
    Res = Srch.get(url=URL, params=PARAMS)
    DATA = Res.json()['search']
    titles=""
    for tt in DATA:
        titles+="#"+tt['label']
    return render(None, 'tagSearch.html', {'form' : titles})


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
    return render(None, 'tagSearch.html', {'form' : "Community is created Successfully!"})


def PosttypePage(request):
    if request.user.is_authenticated:
        CommunityHash = request.GET.get('showDataTypes')
        Community_List = Communities.objects.filter(communityHash=CommunityHash)
        dt = Community_List[0].datatypes_set.all()
        paginator = Paginator(dt, 5)
        page = request.GET.get('page')
        dt_resp = paginator.get_page(page)
        return render(request, 'datatypes.html', {'dt_resp': dt_resp, 'community_Hash':CommunityHash, 'community':Community_List[0]})
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
    d_image=request.FILES.get("Posttype_Image")
    image_path=handle_uploaded_datatypefile(d_image)
    dt = Datatypes()
    dt.name = request.POST.get("Posttype_Name")
    salt = uuid.uuid4().hex
    communityHash=request.POST.get("community_Hash")
    DtHash = hashlib.sha256(salt.encode() + dt.name.encode()).hexdigest() + salt
    dt.datatypeHash = DtHash
    dt.datatypePhoto = image_path
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
    return JsonResponse({'form' : "Posttype is created Successfully!",'communityHash' : communityHash, 'posttypeHash':DtHash}) 
	
def EditPosttypeMeta_view(request):
    dt_hash = request.POST.get("Posttype_Hash")
    d_image=request.FILES.get("Posttype_Image")
    image_path=handle_uploaded_datatypefile(d_image)
    dt = Datatypes.objects.filter(datatypeHash = dt_hash)[0]
    dt.name = request.POST.get("Posttype_Name")
    dt.datatypePhoto = image_path
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
    return JsonResponse({'form' : "Posttype is updated Successfully!",'posttypeHash':dt_hash})

def DeletePosttypeMeta_view(request):
    dt_hash = request.POST.get("Posttype_Hash")
    dt = Datatypes.objects.filter(datatypeHash = dt_hash)[0]
    dt.delete() 
    return JsonResponse({'form' : "Posttype is deleted Successfully!",'posttypeHash':dt_hash})
	
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
                    return render(None, 'tagSearch.html', {'form' : "Data is saved!"})

def DeleteDatatypeFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    Dt= Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
    name = request.POST.get("name")
    HiddenPosts= Posts.objects.filter(propertyName=name,relatedDatatypes=Dt).delete()
    DatatypeFields.objects.filter(name=name).delete()
    return render(None, 'tagSearch.html', {'form' : "Posttyype Field is Deleted Successfully!"})

def EditPosttypes_view(request):
    CommunityHash = request.GET.get("community_Hash")
    context={}
    form=posttypeList(cHash=CommunityHash)
    return render(request, 'modal.html', {'form': form})  

def EditDatatypeFields_view(request):
    name = request.POST.get("name")
    type = request.POST.get("Types")
    req = request.POST.get("Required")
    show = request.POST.get("ShowPage")
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    context[fields.name]=posttypeList(dtHash=DatatypeHash)
    Dt=Datatypes.objects.get(datatypeHash=DatatypeHash)
    Enumeration = request.POST.get("Enum")
    dtFields = DatatypeFields.objects.filter(name=name,relatedDatatype=Dt)[0]
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
                return render(None, 'tagSearch.html', {'form' : "Data is updated!"})

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
    return render(None, 'tagSearch.html', {'form':"Selected posttype is deleted succesfully!"})

def addPosttypeEditField_view(request):
    EnField = request.POST.get("Enumeration")
    if EnField == 'on':
        form = AddTextEntryEnum()
    else:
        form = AddTextEntry()
    return render(None, 'modalPostEdit.html', {'form' : form })

def ReturnPostFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
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
            if fields.relatedPrimitives.name == "Text":
                context[fields.name]=AddTextPost()
            elif fields.relatedPrimitives.name == "TextArea":
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
            context["Tags"]=AddTagPost()
        iter += 1
    return render(None, 'entryReturnFields.html', {'form' : context})

def handle_uploaded_postfile(f):
    filepath = 'streampage/static/uploads/posts/'+f.name
    with open(filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "/"+filepath.split("/")[1]+"/"+filepath.split("/")[2]+"/"+filepath.split("/")[3]+"/"+filepath.split("/")[4]+"/"
	
def CreatePost_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    Dt = Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
    PostFields = DatatypeFields.objects.filter(relatedDatatype=Dt)
    salt = uuid.uuid4().hex
    PostHash = hashlib.sha256(salt.encode() + request.POST.get(PostFields[0].name).encode()).hexdigest() + salt
    PostTime = datetime.now()         
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
            entry.postCreator = communityUsers.objects.get(nickName=request.user)
            entry.postCreationDate = PostTime
            entry.postTag = request.POST.get("Tags")
            entry.save()		
        elif request.POST.get(fields.name) != "":
            entry = Posts()
            entry.propertyName = fields.name
            entry.propertyValue = request.POST.get(fields.name)
            entry.relatedDatatypes = Datatypes.objects.get(datatypeHash=DatatypeHash)
            entry.relatedCommunityforPost = Communities.objects.get(communityHash=CommunityHash)
            entry.entryHash = PostHash
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
    return render(None, 'tagSearch.html', {'form' : "The Entry is Created Successfully"})
    
def DeletePost_view(request):
    PostHash = request.POST.get("PostHash")	
    Posts.objects.filter(entryHash=PostHash).delete()	
    return render(None, 'tagSearch.html', {'form' : "The Entry is deleted Successfully"})
	
	
def login_view(request):
    form = UsersLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        login(request, user)
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
    logout(request)
    return HttpResponseRedirect("/streampage/login")
	
def profilePage(request):
    if request.user.is_authenticated:
        username=request.user
        info = communityUsers.objects.filter(nickName=username)
        CUser = communityUsers.objects.filter(nickName=username)[0]
        Community_List = CUser.creator.all()
        Datatype_List = CUser.datatypecreator.all()
        Post_List = CUser.postcreator.all()
        joined_Communities = CUser.members.all()
        return render(request, "profile.html", {
	"user" : username,
	"additional" : info,
	"title" : "Login",
	"Communities" : Community_List,
	"Datatypes" : Datatype_List,
	"Posts" : Post_List,
	"Joined" : joined_Communities,	
	})
    else:
        return HttpResponseRedirect("/streampage/login")

def ReturnSearchFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    Dt = Datatypes.objects.filter(datatypeHash=DatatypeHash)[0]
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
            context[fields.name]=AddEnumaratedSearch(en=enumList,nm=name)			
        else:
            if fields.relatedPrimitives.name == "Text":
                context[fields.name]=AddTextSearch()
            elif fields.relatedPrimitives.name == "TextArea":
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
            context["Tags"]=AddTagSearch()
        iter += 1
    return render(None, 'entrySearchFields.html', {'form' : context})
	
def ReturnEntrySearchFields_view(request):
    CommunityHash = request.POST.get("CommunityHash")
    DatatypeHash = request.POST.get("DatatypeHash")
    DatatypeResult = Datatypes.objects.filter(datatypeHash=DatatypeHash)
    Dtfields = DatatypeFields.objects.filter(relatedDatatype=DatatypeResult[0])
    if request.user.is_authenticated:
        querylist=[]
        for fields in Dtfields:
            subquery=""
            if request.POST.get(fields.name+"_Value") != "":
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
        querystring = " and ".join(querylist)
        DatatypeId = DatatypeResult[0].id		
        RCommunity = Communities.objects.filter(communityHash=CommunityHash)
        Primitive_List = DatatypeResult[0].datatypefields_set.all()
        c = connection.cursor()
        execution_string = 'select "entryHash",json_object_agg("propertyName","propertyValue") from (select "entryHash","propertyName","propertyValue" from streampage_posts where "relatedDatatypes_id"='+str(DatatypeId)+' and '+querystring+') S GROUP BY "entryHash"'
        c.execute(execution_string)
        posts=c.fetchall()
        print(querystring)		
        paginator = Paginator(posts, 5)
        page = request.GET.get('page')
        post_resp = paginator.get_page(page) 
        return render(request, 'posts.html', {'post_resp': post_resp,'table_fields':Primitive_List,'Datatype_Id':DatatypeHash, 'Datatype_Name':DatatypeResult, 'Community_Name': RCommunity})
    else:
        return HttpResponseRedirect("/streampage/login")
