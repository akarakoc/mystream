from django.contrib import admin
from streampage.models import Primitives,communityUsers,Communities,Datatypes,DatatypeFields,Posts,CommunityTags,DatatTypeTags,PostTags,UserTags,UserCircle
from actstream import models

admin.site.register(Primitives)
admin.site.register(communityUsers)
admin.site.register(Communities)
admin.site.register(Datatypes)
admin.site.register(DatatypeFields)
admin.site.register(Posts)
admin.site.register(CommunityTags)
admin.site.register(DatatTypeTags)
admin.site.register(PostTags)
admin.site.register(UserTags)
admin.site.register(UserCircle)

try:
    from genericadmin.admin import GenericAdminModelAdmin as ModelAdmin
except ImportError:
    ModelAdmin = admin.ModelAdmin


class ActionAdmin(ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__str__', 'actor', 'verb', 'target', 'public')
    list_editable = ('verb',)
    list_filter = ('timestamp',)
    raw_id_fields = ('actor_content_type', 'target_content_type',
                     'action_object_content_type')


class FollowAdmin(ModelAdmin):
    list_display = ('__str__', 'user', 'follow_object', 'actor_only', 'started')
    list_editable = ('user',)
    list_filter = ('user', 'started',)
    raw_id_fields = ('user', 'content_type')


admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.Follow, FollowAdmin)