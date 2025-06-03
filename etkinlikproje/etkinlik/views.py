from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm
from datetime import date
from etkinlik.models import Event
from randevu.models import Appointment
import calendar
from datetime import date, timedelta

from datetime import date, timedelta
import calendar


def event_list(request):
    today = date.today()
    if request.user.is_authenticated:
        user = request.user
        # Etkinlik ve randevuları kullanıcıya göre çek
        events = Event.objects.filter(user=user)
        appointments = Appointment.objects.filter(attendee=user)

        # Bugünkü etkinlikler ve randevular
        today_events = [event for event in events if event.start_time.date() == today]
        today_appointments = [a for a in appointments if a.start_time.date() == today]

        # Takvim için ayın tüm günlerini dolduran matris
        month_start = today.replace(day=1)
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdatescalendar(today.year, today.month)
        calendar_matrix = []
        for week in month_days:
            week_cells = []
            for d in week:
                day_events = [event for event in events if event.start_time.date() == d]
                day_appointments = [a for a in appointments if a.start_time.date() == d]
                week_cells.append({
                    'date': d,
                    'today': d == today,
                    'events': day_events,
                    'appointments': day_appointments
                })
            calendar_matrix.append(week_cells)

        # Yaklaşan Etkinlikler (bu haftadan bugünden sonrası, max 5 adet)
        week_start = today - timedelta(days=today.weekday())  # Pazartesi
        week_end = week_start + timedelta(days=6)             # Pazar
        upcoming_events = [event for event in events if today < event.start_time.date() <= week_end]
        upcoming_events = sorted(upcoming_events, key=lambda x: x.start_time)[:5]

        # Yaklaşan Randevular (istersen ekleyebilirsin)
        # upcoming_appointments = [a for a in appointments if today < a.start_time.date() <= week_end]

        # İstatistikler
        this_month_events = [event for event in events if event.start_time.month == today.month]
        this_month_appointments = [a for a in appointments if a.start_time.month == today.month]
        finished_events = [event for event in events if event.end_time.date() < today]
        pending_events = [event for event in events if event.start_time.date() >= today]
    else:
        events = Event.objects.none()
        appointments = Appointment.objects.none()
        today_events = []
        today_appointments = []
        calendar_matrix = []
        upcoming_events = []
        this_month_events = []
        this_month_appointments = []
        finished_events = []
        pending_events = []

    context = {
        "today_event_count": len(today_events),
        "today_appointment_count": len(today_appointments),
        "events": events,
        "appointments": appointments,
        "calendar_matrix": calendar_matrix,
        "upcoming_events": upcoming_events,
        "month_event_count": len(this_month_events),
        "month_appointment_count": len(this_month_appointments),
        "finished_event_count": len(finished_events),
        "pending_event_count": len(pending_events),
    }
    return render(request, 'etkinlik/event_list.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # OTOMATİK OLARAK user ATA
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, "etkinlik/event_form.html", {"form": form})


def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'etkinlik/event_form.html', {'form': form})

def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'etkinlik/event_confirm_delete.html', {'event': event})

def event_listele(request):
    # Basitçe tüm etkinlikler
    from .models import Event
    events = Event.objects.all()
    return render(request, 'etkinlik/event_listele.html', {'events': events, 'active_tab': 'listele'})


def event_istatistik(request):
    from datetime import date
    user = request.user
    today = date.today()
    ay_baslangic = today.replace(day=1)

    if request.user.is_authenticated:
        # Kullanıcıya ait bu ayki etkinlikler
        ay_etkinlik = Event.objects.filter(
            user=user, start_time__gte=ay_baslangic, start_time__lte=today
        ).count()
        # Kullanıcıya ait bu ayki randevular (katılımcı)
        ay_randevu = Appointment.objects.filter(
            attendee=user, start_time__gte=ay_baslangic, start_time__lte=today
        ).count()
        # Tamamlanan etkinlikler
        tamamlanan = Event.objects.filter(
            user=user, end_time__lt=today
        ).count()
        # Bugünden sonra olanlar bekleyen kabul edilsin
        bekleyen = Event.objects.filter(
            user=user, start_time__gte=today
        ).count()
    else:
        ay_etkinlik = ay_randevu = tamamlanan = bekleyen = 0

    stats = {
        'ay_etkinlik': ay_etkinlik,
        'ay_randevu': ay_randevu,
        'tamamlanan': tamamlanan,
        'bekleyen': bekleyen,
    }
    return render(request, 'etkinlik/event_istatistik.html', {'stats': stats, 'active_tab': 'istatistik'})
