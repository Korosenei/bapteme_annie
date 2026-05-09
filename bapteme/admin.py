from django.contrib import admin
from .models import Invitation, Accompagnateur

class AccompagnateurInline(admin.TabularInline):
    model = Accompagnateur
    extra = 0

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['prenom', 'nom', 'presence', 'telephone', 'nb_total', 'date_reponse']
    list_filter = ['presence', 'date_reponse']
    search_fields = ['prenom', 'nom', 'telephone']
    inlines = [AccompagnateurInline]
    readonly_fields = ['date_reponse']

@admin.register(Accompagnateur)
class AccompagnateurAdmin(admin.ModelAdmin):
    list_display = ['prenom', 'nom', 'invitation']
