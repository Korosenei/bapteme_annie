# Invitation Baptême & Première Communion
## Pare Annie Charlen — 23 Mai 2026

## Installation & Lancement

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 2. Installer Django
pip install django

# 3. Appliquer les migrations
python manage.py migrate

# 4. Créer un superutilisateur admin
python manage.py createsuperuser

# 5. Lancer le serveur
python manage.py runserver 0.0.0.0:8000
```

## Accès

| Page | URL |
|------|-----|
| 🎉 Invitation | http://localhost:8000/ |
| 📊 Dashboard | http://localhost:8000/dashboard/ |
| ⚙️ Admin Django | http://localhost:8000/admin/ |

Admin par défaut : **admin** / **admin2026**

## Ajouter la photo d'Annie Charlen

Modifiez la balise dans `templates/bapteme/invitation.html` :
```html
<div class="photo-inner">
  <img src="{% static 'images/annie.jpg' %}" alt="Pare Annie Charlen">
</div>
```
Placez la photo dans `static/images/annie.jpg`

## Ajouter la musique

Placez un fichier `static/audio/bapteme.mp3` et activez la balise audio dans le template.

## Structure du projet

```
bapteme_annie/
├── bapteme/          # App Django
│   ├── models.py     # Invitation + Accompagnateur
│   ├── views.py      # Pages + API RSVP
│   └── admin.py      # Interface admin
├── templates/
│   └── bapteme/
│       ├── invitation.html   # Page principale (enveloppe + carte)
│       └── dashboard.html    # Tableau de bord invités
├── static/
│   ├── audio/        # Musique de fond (bapteme.mp3)
│   └── images/       # Photo de Annie
└── db.sqlite3        # Base de données
```
