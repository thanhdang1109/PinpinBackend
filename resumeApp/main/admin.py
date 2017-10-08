from django.contrib import admin
from resumeApp.main.models import Country, State, City, Street, Address, \
    Organization, School, Degree, User, Education, Skill, User_Skill, \
    Experience, Video_Education, Video_Experience, Video_Skill


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']


class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'country', 'timezone', 'zipcode']


class StreetAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'suburb', 'state', 'country']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['number', 'street', 'zipcode']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


class DegreeAdmin(admin.ModelAdmin):
    list_display = ['name', 'school']


class UserAdmin(admin.ModelAdmin):
    list_display = ['created', 'username', 'firstname',
                    'middlename', 'lastname', 'email',
                    'street', 'city', 'country', 'facebook_token']


class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree', 'year']


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']


class User_SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'description']


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'organization',
                    'month_start', 'year_start',
                    'month_end', 'year_end',
                    'description']


class Video_ExperienceAdmin(admin.ModelAdmin):
    list_display = ['experience', 'storage_link', 'created']


class Video_SkillAdmin(admin.ModelAdmin):
    list_display = ['skill', 'storage_link', 'created']


class Video_EducationAdmin(admin.ModelAdmin):
    list_display = ['education', 'storage_link', 'created']


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Degree, DegreeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(User_Skill, User_SkillAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Video_Experience, Video_ExperienceAdmin)
admin.site.register(Video_Skill, Video_SkillAdmin)
admin.site.register(Video_Education, Video_EducationAdmin)
