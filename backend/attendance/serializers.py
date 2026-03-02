from rest_framework import serializers
from .models import AttendanceRecord, Excursion, RegistroExcursion
from core.serializers import BeneficiarySerializer, EventSerializer

class AttendanceRecordSerializer(serializers.ModelSerializer):
    beneficiary_details = BeneficiarySerializer(source='beneficiary', read_only=True)
    event_details = EventSerializer(source='event', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'beneficiary', 'event', 'date', 'recorded_by', 'beneficiary_details', 'event_details']
        read_only_fields = ['recorded_by', 'date']

class RegistroExcursionSerializer(serializers.ModelSerializer):
    beneficiary_details = BeneficiarySerializer(source='usuario', read_only=True)

    class Meta:
        model = RegistroExcursion
        fields = ['id', 'excursion', 'usuario', 'asistio', 'fecha_registro', 'beneficiary_details']
        read_only_fields = ['fecha_registro']

class ExcursionSerializer(serializers.ModelSerializer):
    registros = RegistroExcursionSerializer(many=True, read_only=True)
    inscritos_count = serializers.SerializerMethodField()

    class Meta:
        model = Excursion
        fields = [
            'id', 'nombre', 'descripcion', 'fecha_evento', 
            'edad_min', 'edad_max', 'min_asistencias', 'estado', 
            'created_at', 'updated_at', 'registros', 'inscritos_count'
        ]
        read_only_fields = ['estado', 'created_at', 'updated_at']

    def get_inscritos_count(self, obj):
        return obj.registros.count()
