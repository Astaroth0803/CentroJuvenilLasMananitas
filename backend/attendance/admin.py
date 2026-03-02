from django.contrib import admin
from .models import AttendanceRecord, Excursion, RegistroExcursion

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('beneficiary', 'event', 'date', 'time', 'recorded_by')
    list_filter = ('date', 'event')
    search_fields = ('beneficiary__first_name', 'beneficiary__last_name', 'beneficiary__ci')

@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_evento', 'estado', 'min_asistencias')
    list_filter = ('estado', 'fecha_evento')
    search_fields = ('nombre',)

@admin.register(RegistroExcursion)
class RegistroExcursionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'excursion', 'asistio', 'fecha_registro')
    list_filter = ('excursion', 'asistio')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'usuario__ci')
