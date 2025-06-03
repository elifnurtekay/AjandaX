from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(attendee=request.user)
    return render(request, 'randevu/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.attendee = request.user
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'randevu/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, attendee=request.user)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'randevu/appointment_confirm_delete.html', {'appointment': appointment})
