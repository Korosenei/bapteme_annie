from django.db import models


class Invitation(models.Model):
    """Réponse RSVP d'un invité."""
    PRESENCE_CHOICES = [('oui', 'Présent(e)'), ('non', 'Absent(e)')]

    prenom       = models.CharField(max_length=100)
    nom          = models.CharField(max_length=100)
    telephone    = models.CharField(max_length=30, blank=True, default='')
    email        = models.EmailField(blank=True, default='')
    presence     = models.CharField(max_length=3, choices=PRESENCE_CHOICES, default='oui')
    message      = models.TextField(blank=True, default='')
    date_reponse = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_reponse']

    @property
    def nb_total(self):
        """Nombre total de personnes : l'invité + ses accompagnateurs."""
        if self.presence == 'non':
            return 0
        return 1 + self.accompagnateurs.count()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.presence})"


class Accompagnateur(models.Model):
    """Accompagnateur lié à une invitation."""
    invitation = models.ForeignKey(
        Invitation, on_delete=models.CASCADE, related_name='accompagnateurs'
    )
    prenom = models.CharField(max_length=100, blank=True, default='')
    nom    = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Don(models.Model):
    """
    Cadeau ou don enregistré pour Annie Charlen.
    Peut être lié à un invité existant ou renseigné manuellement.
    """
    TYPE_CHOICES = [
        ('argent', 'Argent'),
        ('cadeau', 'Cadeau'),
        ('autre',  'Autre'),
    ]

    donateur_nom          = models.CharField(max_length=200, verbose_name="Nom du donateur")
    donateur_tel          = models.CharField(max_length=30, blank=True, default='', verbose_name="Téléphone")
    type_don              = models.CharField(max_length=10, choices=TYPE_CHOICES, default='argent')
    montant               = models.DecimalField(
        max_digits=12, decimal_places=0,
        null=True, blank=True,
        verbose_name="Montant (FCFA)"
    )
    description           = models.CharField(max_length=300, blank=True, default='', verbose_name="Description")
    note                  = models.TextField(blank=True, default='', verbose_name="Note interne")
    invitation            = models.ForeignKey(
        Invitation, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='dons',
        verbose_name="Invité lié"
    )
    date_enregistrement   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_enregistrement']
        verbose_name = "Don / Cadeau"
        verbose_name_plural = "Dons / Cadeaux"

    def __str__(self):
        if self.type_don == 'argent':
            return f"{self.donateur_nom} — {self.montant} FCFA"
        return f"{self.donateur_nom} — {self.get_type_don_display()}: {self.description}"
        