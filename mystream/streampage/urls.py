from django.urls import path
from django.conf.urls import include
from . import views


    
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name = "register"),
    path('logout/', views.logout_view, name = "logout"),
    path('profile/', views.profilePage, name = "profile"),
    path('communities/', views.communityPage, name='index'),
    path('sendCommunityForm/', views.communityForm, name='index'),
    path('CreateCommunity/', views.CreateCommunity_view, name = "CreateCommunity"),
    path('sendPosttypePage/', views.PosttypePage, name='index'),
    path('sendPostPage/', views.PostPage, name='index'),
	path('searchTag/', views.searchTag_view, name = "searchTag"),
	path('sendPosttypeForm/', views.posttypeForm, name = "Call datatype form"),
	path('CreatePosttype/', views.CreatePosttype_view, name = "CreatePosttype"),
	path('EditPosttypeMeta/', views.EditPosttypeMeta_view, name = "EditPosttypeMeta"),
	path('DeletePosttypeMeta/', views.DeletePosttypeMeta_view, name = "DeletePosttypeMeta"),
	path('addPosttypeField/', views.addPosttypeField_view, name = "addPosttypeField"),
	path('SavePrimitives/', views.SavePrimitives_view, name = "SavePrimitives"),
	path('ShowPosttypeFields/', views.ShowPosttypeFields_view, name = "ShowDatatypeFields"),
	path('DeletePosttypes/', views.DeletePosttypes_view, name = "DeletePosttypes"),
	path('DeletePosttypeFields/', views.DeletePosttypeFields_view, name = "DeletePosttypeFields"),
	path('EditPosttypes/', views.EditPosttypes_view, name = "EditPosttypeMeta"),
	path('addPosttypeEditField/', views.addPosttypeEditField_view, name = "addPosttypeEditField"),
	path('AddPostModal/', views.AddPostModal_view, name = "AddPostModal"),
	path('ReturnPostFields/', views.ReturnPostFields_view, name = "ReturnPostFields"),
	path('CreatePost/', views.CreatePost_view, name = "CreatePost"),
	path('CreatePostComment/', views.CreatePostComment_view, name = "CreatePostComment"),
	path('DeletePost/', views.DeletePost_view, name = "DeletePost"),
	path('JoinCommunity/', views.JoinCommunity_view, name = "JoinCommunity"),
	path('LeftCommunity/', views.LeftCommunity_view, name = "LeftCommunity"),
	path('VoteCommunity/', views.VoteCommunity_view, name = "VoteCommunity"),
	path('CheckMembership/', views.CheckMembership_view, name = "CheckMembership"),
	path('chooseSearch/', views.chooseSearch_view, name = "chooseSearch"),
	path('ReturnSearchFields/', views.ReturnSearchFields_view, name = "ReturnSearchFields"),
	path('ReturnEntrySearchResults/', views.ReturnEntrySearchResults_view, name = "ReturnEntrySearchResults"),
	path('ReturnFreeSearchFields/', views.ReturnFreeSearchFields_view, name = "ReturnFreeSearchFields"),
	path('showPostDetails/', views.showPostDetails_view, name = "showPostDetails"),
	path('subscribePosttype/', views.subscribePosttype_view, name = "subscribePosttype"),
	path('reportPostModal/', views.reportPostModal_view, name = "reportPostModal"),
	path('reportPost/', views.reportPost_view, name = "reportPost"),
	
]
