from django.urls import path
from django.conf.urls import include
from . import views


    
urlpatterns = [
    path('', views.index, name='index'),
    path('sendCommunityForm/', views.communityForm, name='index'),
    path('communities/', views.communityPage, name='index'),
    path('sendDatatypePage/', views.DatatypePage, name='index'),
    path('sendPostPage/', views.PostPage, name='index'),
	path('login/', views.login_view, name='login'),
	path('register/', views.register_view, name = "register"),
	path('logout/', views.logout_view, name = "logout"),
	path('profile/', views.profilePage, name = "profile"),
	path('searchTag/', views.searchTag_view, name = "searchTag"),
	path('CreateCommunity/', views.CreateCommunity_view, name = "CreateCommunity"),
	path('sendDatatypeForm/', views.datatypeForm, name = "Call datatype form"),
	path('CreateDatatype/', views.CreateDatatype_view, name = "CreateDatatype"),
	path('EditDataytpe/', views.EditDatatype_view, name = "EditDatatype"),
	path('SavePrimitives/', views.SavePrimitives_view, name = "SavePrimitives"),
	path('ShowDatatypeFields/', views.ShowDatatypeFields_view, name = "ShowDatatypeFields"),
	path('DeleteDatatypeFields/', views.DeleteDatatypeFields_view, name = "DeleteDatatypeFields"),
	path('EditDatatypeFields/', views.EditDatatypeFields_view, name = "EditDatatypeFields"),
	path('ReturnPostFields/', views.ReturnPostFields_view, name = "ReturnPostFields"),
	path('CreatePost/', views.CreatePost_view, name = "CreatePost"),
	path('DeletePost/', views.DeletePost_view, name = "DeletePost"),
	path('JoinCommunity/', views.JoinCommunity_view, name = "JoinCommunity"),
	path('LeftCommunity/', views.LeftCommunity_view, name = "LeftCommunity"),
	path('VoteCommunity/', views.VoteCommunity_view, name = "VoteCommunity"),		
	path('CheckMembership/', views.CheckMembership_view, name = "CheckMembership"),
	path('ReturnSearchFields/', views.ReturnSearchFields_view, name = "ReturnSearchFields"), 
	path('ReturnEntrySearchFields/', views.ReturnEntrySearchFields_view, name = "ReturnEntrySearchFields"),
]
