from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import MyUserCreationForm
from django.contrib.auth import logout
from .models import TableType, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'home')

def signup_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirigez vers la page que vous voulez après l'inscription
    else:
        form = MyUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirigez vers la page que vous voulez après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
        logout(request)
        return redirect('home')

@login_required(login_url='/login/') 
def reserve_table(request):
    # Définissez default_date ici pour qu'elle soit accessible pour les requêtes POST et GET.
    default_date = timezone.now().date()

    if request.method == 'POST':
        table_type_id = request.POST.get('table_type')
        # Assurez-vous de convertir la chaîne de la date postée en un objet date si elle existe
        date = request.POST.get('date') if 'date' in request.POST else default_date
        table_type = TableType.objects.get(id=table_type_id)

        # Vérifiez si l'utilisateur a déjà réservé une table de ce type pour la date choisie
        if Reservation.objects.filter(user=request.user, table_type=table_type, date=date).exists():
            messages.error(request, 'Vous avez déjà une réservation pour ce type de table à cette date.')
        else:
            Reservation.objects.create(user=request.user, table_type=table_type, date=date)
            messages.success(request, 'Votre réservation a été effectuée avec succès.')
        return redirect('reserve_table')

    # Si la requête est GET, affichez les types de tables disponibles
    tables = TableType.objects.all()
    return render(request, 'reserve_table.html', {'tables': tables, 'default_date': default_date})

@login_required
def account_view(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'account.html', {'reservations': reservations})

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        message = request.POST.get('message')

        # Préparer le contenu de l'email
        subject = f"Message de {first_name} {last_name}"
        email_message = f"Nom: {first_name} {last_name}\nEmail: {email}\nTéléphone: {contact_number}\n\nMessage:\n{message}"

        # Envoyer l'email
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['destinataire@example.com'],  # Remplacer par votre email de réception
            fail_silently=False,
        )
        messages.success(request, "Votre message a été envoyé avec succès.")
        return redirect('contact')

    return render(request, 'contact.html')

def foods(request):
    return render(request, 'foods.html')

def about(request):
    return render(request, 'about.html')