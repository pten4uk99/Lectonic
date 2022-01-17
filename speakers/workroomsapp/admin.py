from django.contrib import admin

from workroomsapp.models import *


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Projects)
# class ProjectsAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(ProjectAdmin)
# class ProjectAdminAdmin(admin.ModelAdmin):
#     pass


@admin.register(ProjectLecturer)
class ProjectLecturerAdmin(admin.ModelAdmin):
    pass

