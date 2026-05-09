from django.db import models
from django.utils import timezone

class Invitation(models.Model):
    PRESENCE_CHOICES = [('oui', 'Présent(e)'), ('non', 'Absent(e)')]
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    presence = models.CharField(max_length=3, choices=PRESENCE_CHOICES, default='oui')
    message = models.TextField(blank=True)
    date_reponse = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_reponse']

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.get_presence_display()}"

    def nb_total(self):
        return 1 + self.accompagnateurs.count()

class Accompagnateur(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name='accompagnateurs')
    prenom = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}".strip() or "Accompagnateur"
