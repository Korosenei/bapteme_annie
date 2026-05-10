import json
from decimal import Decimal

from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Accompagnateur, Don, Invitation


# ──────────────────────────────────────────────────
# Page invitation (accueil)
# ──────────────────────────────────────────────────
def invitation_view(request):
    return render(request, 'bapteme/invitation.html')


# ──────────────────────────────────────────────────
# Dashboard
# ──────────────────────────────────────────────────
def dashboard_view(request):
    invitations = Invitation.objects.prefetch_related('accompagnateurs', 'dons').all()
    dons        = Don.objects.select_related('invitation').all()

    total_confirmations = invitations.filter(presence='oui').count()
    total_absences      = invitations.filter(presence='non').count()
    total_reponses      = invitations.count()

    # Total personnes (invités présents + leurs accompagnateurs)
    total_personnes = sum(inv.nb_total for inv in invitations)

    # Stats dons
    dons_argent     = dons.filter(type_don='argent')
    total_argent    = dons_argent.aggregate(s=Sum('montant'))['s'] or Decimal('0')
    nb_dons_argent  = dons_argent.count()
    nb_cadeaux      = dons.count()
    nb_donateurs    = dons.values('donateur_nom').distinct().count()

    context = {
        'invitations':        invitations,
        'dons':               dons,
        'total_confirmations': total_confirmations,
        'total_absences':     total_absences,
        'total_reponses':     total_reponses,
        'total_personnes':    total_personnes,
        'total_argent':       total_argent,
        'nb_dons_argent':     nb_dons_argent,
        'nb_cadeaux':         nb_cadeaux,
        'nb_donateurs':       nb_donateurs,
    }
    return render(request, 'bapteme/dashboard.html', context)


# ──────────────────────────────────────────────────
# RSVP — création d'invitation
# ──────────────────────────────────────────────────
@require_POST
def rsvp_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)

    prenom   = data.get('prenom', '').strip()
    nom      = data.get('nom', '').strip()
    presence = data.get('presence', 'oui')

    if not prenom or not nom:
        return JsonResponse({'success': False, 'error': 'Prénom et nom requis'}, status=400)

    invitation = Invitation.objects.create(
        prenom    = prenom,
        nom       = nom,
        telephone = data.get('telephone', '').strip(),
        email     = data.get('email', '').strip(),
        presence  = presence,
        message   = data.get('message', '').strip(),
    )

    # Accompagnateurs (uniquement si présent)
    if presence == 'oui':
        for a in data.get('accompagnateurs', []):
            p = a.get('prenom', '').strip()
            n = a.get('nom', '').strip()
            if p or n:
                Accompagnateur.objects.create(invitation=invitation, prenom=p, nom=n)

    return JsonResponse({'success': True, 'id': invitation.id})


# ──────────────────────────────────────────────────
# Suppression d'invitation
# ──────────────────────────────────────────────────
@require_POST
def delete_invitation_view(request, invitation_id):
    try:
        inv = Invitation.objects.get(pk=invitation_id)
        inv.delete()
        return JsonResponse({'success': True})
    except Invitation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Introuvable'}, status=404)


# ──────────────────────────────────────────────────
# Enregistrement d'un don
# ──────────────────────────────────────────────────
@require_POST
def add_don_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON invalide'}, status=400)

    donateur_nom = data.get('donateur_nom', '').strip()
    type_don     = data.get('type_don', 'argent')

    if not donateur_nom:
        return JsonResponse({'success': False, 'error': 'Nom du donateur requis'}, status=400)

    if type_don == 'argent':
        try:
            montant = Decimal(str(data.get('montant') or 0))
            if montant <= 0:
                raise ValueError
        except (ValueError, Exception):
            return JsonResponse({'success': False, 'error': 'Montant invalide'}, status=400)
        description = ''
    else:
        montant     = None
        description = data.get('description', '').strip()
        if not description:
            return JsonResponse({'success': False, 'error': 'Description requise'}, status=400)

    # Lier à un invité si fourni
    invitation = None
    inv_id = data.get('invitation_id')
    if inv_id:
        try:
            invitation = Invitation.objects.get(pk=inv_id)
        except Invitation.DoesNotExist:
            pass

    don = Don.objects.create(
        donateur_nom  = donateur_nom,
        donateur_tel  = data.get('donateur_tel', '').strip(),
        type_don      = type_don,
        montant       = montant,
        description   = description,
        note          = data.get('note', '').strip(),
        invitation    = invitation,
    )

    return JsonResponse({
        'success':       True,
        'don': {
            'id':            don.id,
            'donateur_nom':  don.donateur_nom,
            'donateur_tel':  don.donateur_tel,
            'type_don':      don.type_don,
            'montant':       str(don.montant) if don.montant else None,
            'description':   don.description,
            'note':          don.note,
            'invitation_nom': f"{invitation.prenom} {invitation.nom}" if invitation else None,
        }
    })


# ──────────────────────────────────────────────────
# Suppression d'un don
# ──────────────────────────────────────────────────
@require_POST
def delete_don_view(request, don_id):
    try:
        don = Don.objects.get(pk=don_id)
        don.delete()
        return JsonResponse({'success': True})
    except Don.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Introuvable'}, status=404)


        