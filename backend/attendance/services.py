from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError
from attendance.models import Excursion, RegistroExcursion, AttendanceRecord

@transaction.atomic
def add_participant(excursion, user):
    """
    Registra un beneficiario (usuario) en la excursión aplicando reglas de negocio.
    """
    if excursion.estado != Excursion.Estado.PENDIENTE_REGISTRO:
        raise ValidationError("La excursión no está en estado pendiente de registro.")

    # 1. Age validation
    if user.dob:
        today = date.today()
        age = today.year - user.dob.year - ((today.month, today.day) < (user.dob.month, user.dob.day))
        if not (excursion.edad_min <= age <= excursion.edad_max):
            raise ValidationError(f"La edad del usuario ({age}) no cumple el rango permitido ({excursion.edad_min} - {excursion.edad_max}).")
    else:
        raise ValidationError("El usuario no tiene fecha de nacimiento registrada.")

    # 2. Min asistencias
    if excursion.min_asistencias > 0:
        asistencias_count = AttendanceRecord.objects.filter(beneficiary=user).count()
        if asistencias_count < excursion.min_asistencias:
            raise ValidationError(
                f"El usuario tiene {asistencias_count} asistencias, pero se requieren al menos {excursion.min_asistencias}."
            )

    # 3. Temporary block logic (Cronológico)
    last_registration = RegistroExcursion.objects.filter(
        usuario=user,
        excursion__fecha_evento__lt=excursion.fecha_evento
    ).select_related('excursion').order_by('-excursion__fecha_evento').first()

    if last_registration and last_registration.asistio is False:
        # Check if there was any excursion in between the missed one and the target one
        excursiones_intermedias = Excursion.objects.filter(
            fecha_evento__gt=last_registration.excursion.fecha_evento,
            fecha_evento__lt=excursion.fecha_evento
        ).count()

        if excursiones_intermedias == 0:
            raise ValidationError("El usuario está bloqueado temporalmente por no asistir a la última excursión a la que se registró.")

    if RegistroExcursion.objects.filter(excursion=excursion, usuario=user).exists():
        raise ValidationError("El usuario ya está registrado en esta excursión.")

    return RegistroExcursion.objects.create(excursion=excursion, usuario=user)


@transaction.atomic
def change_state(excursion, new_estado):
    """
    Avanza el estado de una excursión. Solo permite transiciones hacia adelante.
    pendiente_registro -> registro_cerrado -> dia_evento -> finalizado
    """
    states = [
        Excursion.Estado.PENDIENTE_REGISTRO,
        Excursion.Estado.REGISTRO_CERRADO,
        Excursion.Estado.DIA_EVENTO,
        Excursion.Estado.FINALIZADO
    ]

    if new_estado == Excursion.Estado.CANCELADO:
        if excursion.estado in [Excursion.Estado.FINALIZADO, Excursion.Estado.CANCELADO]:
            raise ValidationError("No se puede cancelar una excursión que ya ha finalizado o está cancelada.")
        # Proceed to cancel
    else:
        if new_estado not in states:
            raise ValidationError("Estado de excursión inválido.")

        if excursion.estado == Excursion.Estado.CANCELADO:
            raise ValidationError("Una excursión cancelada no puede cambiar de estado.")

        try:
            current_idx = states.index(excursion.estado)
            new_idx = states.index(new_estado)
        except ValueError:
            raise ValidationError("Estado actual o nuevo inválido.")

        if new_idx <= current_idx:
            raise ValidationError("Solo se permiten transiciones hacia adelante. No se puede regresar a un estado anterior o mantener el actual mediante esta función.")

        if new_estado in [Excursion.Estado.REGISTRO_CERRADO, Excursion.Estado.DIA_EVENTO, Excursion.Estado.FINALIZADO]:
            inscritos = RegistroExcursion.objects.filter(excursion=excursion).count()
            if inscritos < 2:
                raise ValidationError("La excursión debe tener al menos 2 participantes registrados antes de cambiar de estado.")

    excursion.estado = new_estado
    excursion.save(update_fields=['estado', 'updated_at'])
    return excursion


@transaction.atomic
def mark_attendance(excursion, attendance_dict):
    """
    Marca la asistencia de los participantes.
    attendance_dict formato esperado: { user_id (int o str): True | False }
    """
    if excursion.estado != Excursion.Estado.DIA_EVENTO:
        raise ValidationError("Solo se puede marcar asistencia cuando la excursión está en estado 'Día del Evento'.")

    registros = RegistroExcursion.objects.filter(excursion=excursion).select_related('usuario')
    registros_to_update = []

    for registro in registros:
        uid_str = str(registro.usuario.id)
        uid_int = int(registro.usuario.id)
        
        if uid_str in attendance_dict:
            registro.asistio = bool(attendance_dict[uid_str])
            registros_to_update.append(registro)
        elif uid_int in attendance_dict:
            registro.asistio = bool(attendance_dict[uid_int])
            registros_to_update.append(registro)

    if registros_to_update:
        RegistroExcursion.objects.bulk_update(registros_to_update, ['asistio'])

    return len(registros_to_update)
