from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all().select_related('beneficiary', 'event')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(recorded_by=self.request.user)
        except IntegrityError:
            raise ValidationError({'detail': 'El usuario ya tiene asistencia registrada para este evento hoy.'})

class PublicAttendanceViewSet(viewsets.ModelViewSet):
    """ Allows anyone to register attendance on the public form """
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'options']

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({'detail': 'Ya has registrado tu asistencia para este evento hoy.'})
