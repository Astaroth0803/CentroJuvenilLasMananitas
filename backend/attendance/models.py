from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import Beneficiary, Event

class AttendanceRecord(models.Model):
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE, related_name="attendances")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField("Fecha de Asistencia")
    time = models.TimeField("Hora de Registro", null=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="registered_attendances")

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo al crear, no al editar
            now_local = timezone.localtime(timezone.now())
            self.date = now_local.date()
            self.time = now_local.time()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('beneficiary', 'event', 'date')
        indexes = [
            models.Index(fields=['date'], name='idx_asistencia_fecha'),
            models.Index(fields=['event', 'date'], name='idx_evento_fecha'),
        ]

    def __str__(self):
        return f"{self.beneficiary} -> {self.event} ({self.date})"
