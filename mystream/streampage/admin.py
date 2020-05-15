from django.contrib import admin
from streampage.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts,PostComments,PostsMetaHash,ReportedPosts,CommunityTags,DatatTypeTags,PostTags,UserTags,UserCircle

admin.site.register(Primitives)
admin.site.register(communityUsers)
admin.site.register(Communities)
admin.site.register(Datatypes)
admin.site.register(DatatypeFields)
admin.site.register(Posts)
admin.site.register(PostComments)
admin.site.register(PostsMetaHash)
admin.site.register(ReportedPosts)
admin.site.register(CommunityTags)
admin.site.register(DatatTypeTags)
admin.site.register(PostTags)
admin.site.register(UserTags)
admin.site.register(UserCircle)


