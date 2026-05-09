import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, Q
from .models import Invitation, Accompagnateur


def invitation_page(request):
    return render(request, 'bapteme/invitation.html')


def dashboard(request):
    invitations = Invitation.objects.all()
    total_confirmations = invitations.filter(presence='oui').count()
    total_absences = invitations.filter(presence='non').count()
    
    # Total personnes (invités + accompagnateurs)
    total_personnes = 0
    for inv in invitations.filter(presence='oui'):
        total_personnes += inv.nb_total()

    recent = invitations[:10]
    
    context = {
        'invitations': invitations,
        'total_confirmations': total_confirmations,
        'total_absences': total_absences,
        'total_personnes': total_personnes,
        'recent': recent,
    }
    return render(request, 'bapteme/dashboard.html', context)


@csrf_exempt
def rsvp_submit(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inv = Invitation.objects.create(
                prenom=data.get('prenom', '').strip(),
                nom=data.get('nom', '').strip(),
                telephone=data.get('telephone', '').strip(),
                email=data.get('email', '').strip(),
                presence=data.get('presence', 'oui'),
                message=data.get('message', '').strip(),
            )
            accompagnateurs = data.get('accompagnateurs', [])
            for a in accompagnateurs:
                Accompagnateur.objects.create(
                    invitation=inv,
                    prenom=a.get('prenom', '').strip(),
                    nom=a.get('nom', '').strip(),
                )
            return JsonResponse({'success': True, 'id': inv.id, 'message': 'Enregistré avec succès'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
