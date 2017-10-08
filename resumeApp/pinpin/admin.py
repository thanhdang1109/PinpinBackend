from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from resumeApp.pinpin.models import Country, State, City, \
    UserProfile, Video, Follower


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'country']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'get_followers', 'get_followings']


class FollowerAdmin(admin.ModelAdmin):
    list_display = ['user', 'follower', 'created']


class VideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created', 'date', 'description', 'link']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Video, VideoAdmin)
