from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import Accompagnateur, Don, Invitation


class AccompagnateurInline(admin.TabularInline):
    model = Accompagnateur
    extra = 0
    fields = ('prenom', 'nom')


class DonInline(admin.TabularInline):
    model = Don
    extra = 0
    fields = ('type_don', 'montant', 'description', 'donateur_nom', 'date_enregistrement')
    readonly_fields = ('date_enregistrement',)
    show_change_link = True


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display  = ('prenom', 'nom', 'presence_badge', 'telephone', 'nb_total', 'nb_dons_cell', 'date_reponse')
    list_filter   = ('presence', 'date_reponse')
    search_fields = ('prenom', 'nom', 'telephone', 'email')
    ordering      = ('-date_reponse',)
    inlines       = [AccompagnateurInline, DonInline]
    readonly_fields = ('date_reponse', 'nb_total')

    @admin.display(description='Présence')
    def presence_badge(self, obj):
        if obj.presence == 'oui':
            return format_html('<span style="color:green;font-weight:bold;">✓ Présent(e)</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Absent(e)</span>')

    @admin.display(description='Dons')
    def nb_dons_cell(self, obj):
        n = obj.dons.count()
        return n if n else '—'


@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display  = ('donateur_nom', 'type_don_badge', 'montant_display', 'description', 'invitation', 'date_enregistrement')
    list_filter   = ('type_don', 'date_enregistrement')
    search_fields = ('donateur_nom', 'donateur_tel', 'description')
    ordering      = ('-date_enregistrement',)
    readonly_fields = ('date_enregistrement',)

    @admin.display(description='Type')
    def type_don_badge(self, obj):
        colors = {'argent': 'green', 'cadeau': 'steelblue', 'autre': 'darkorange'}
        labels = {'argent': '💵 Argent', 'cadeau': '🎁 Cadeau', 'autre': '✦ Autre'}
        color = colors.get(obj.type_don, 'gray')
        label = labels.get(obj.type_don, obj.type_don)
        return format_html(f'<span style="color:{color};font-weight:bold;">{label}</span>')

    @admin.display(description='Montant / Description')
    def montant_display(self, obj):
        if obj.type_don == 'argent' and obj.montant:
            return format_html(
                '<span style="color:green;font-weight:bold;">{} FCFA</span>',
                f"{int(obj.montant):,}".replace(',', ' ')
            )
        return obj.description or '—'

    def changelist_view(self, request, extra_context=None):
        """Ajouter le total des dons en argent dans le contexte."""
        extra_context = extra_context or {}
        total = Don.objects.filter(type_don='argent').aggregate(s=Sum('montant'))['s'] or 0
        extra_context['total_argent'] = f"{int(total):,} FCFA".replace(',', ' ')
        return super().changelist_view(request, extra_context=extra_context)