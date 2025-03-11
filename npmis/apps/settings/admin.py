from django.contrib import admin

from .models import *


@admin.register(Sdg)
class SdgAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']



class TdvTargetInlineAdmin(admin.TabularInline):
    model = TdvTarget


@admin.register(Tdv)
class TdvAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    inlines = [TdvTargetInlineAdmin]


@admin.register(Fydp)
class FydpAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Subsector)
class SubSectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'sector', 'name']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'vote_no', 'name']


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'vote']

@admin.register(ProjectNature)
class ProjectNatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
