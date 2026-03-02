from datetime import date, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Beneficiary, Activity, Event
from attendance.models import Excursion, RegistroExcursion, AttendanceRecord
from attendance.services import add_participant, change_state, mark_attendance

class ExcursionServicesTests(TestCase):
    def setUp(self):
        today = date.today()
        # Be exact about 20 years old
        exact_dob = date(today.year - 20, today.month, today.day)
        self.user = Beneficiary.objects.create(
            first_name="Test",
            last_name="User",
            dob=exact_dob, 
            sex=Beneficiary.Sex.MALE,
            ci="123456",
            sector="Sector Test"
        )
        self.excursion = Excursion.objects.create(
            nombre="Excursion 1",
            fecha_evento=date.today() + timedelta(days=5),
            edad_min=18,
            edad_max=25,
            min_asistencias=0
        )

    def test_add_participant_success(self):
        reg = add_participant(self.excursion, self.user)
        self.assertEqual(reg.usuario, self.user)
        self.assertEqual(reg.excursion, self.excursion)

    def test_add_participant_invalid_state(self):
        self.excursion.estado = Excursion.Estado.REGISTRO_CERRADO
        self.excursion.save()
        with self.assertRaises(ValidationError):
            add_participant(self.excursion, self.user)

    def test_add_participant_age_restriction(self):
        self.excursion.edad_max = 19
        self.excursion.save()
        with self.assertRaisesMessage(ValidationError, "rango permitido"):
            add_participant(self.excursion, self.user)

    def test_add_participant_min_asistencias(self):
        self.excursion.min_asistencias = 2
        self.excursion.save()
        with self.assertRaisesMessage(ValidationError, "se requieren al menos"):
            add_participant(self.excursion, self.user)
        
        # Add attendances
        act = Activity.objects.create(name="Act")
        ev1 = Event.objects.create(activity=act, name="Ev1", date=date.today())
        ev2 = Event.objects.create(activity=act, name="Ev2", date=date.today())
        AttendanceRecord.objects.create(beneficiary=self.user, event=ev1)
        AttendanceRecord.objects.create(beneficiary=self.user, event=ev2)
        
        # Should succeed now
        add_participant(self.excursion, self.user)

    def test_temporary_block_logic(self):
        # User registered to E1 but didn't attend
        self.excursion.fecha_evento = date.today() - timedelta(days=10)
        self.excursion.save()
        reg1 = add_participant(self.excursion, self.user)
        
        # Change state and mark attendance as False
        change_state(self.excursion, Excursion.Estado.REGISTRO_CERRADO)
        change_state(self.excursion, Excursion.Estado.DIA_EVENTO)
        mark_attendance(self.excursion, {self.user.id: False})
        
        # New excursion (E2) immediately after
        e2 = Excursion.objects.create(
            nombre="Excursion 2",
            fecha_evento=date.today() - timedelta(days=5)
        )
        with self.assertRaisesMessage(ValidationError, "bloqueado temporalmente"):
            add_participant(e2, self.user)
            
        # Third excursion (E3), user shouldn't be blocked anymore since they skipped E2
        e3 = Excursion.objects.create(
            nombre="Excursion 3",
            fecha_evento=date.today()
        )
        add_participant(e3, self.user) # Should succeed

    def test_change_state_forward_only(self):
        change_state(self.excursion, Excursion.Estado.REGISTRO_CERRADO)
        self.assertEqual(self.excursion.estado, Excursion.Estado.REGISTRO_CERRADO)
        
        with self.assertRaisesMessage(ValidationError, "hacia adelante"):
            change_state(self.excursion, Excursion.Estado.PENDIENTE_REGISTRO)

    def test_mark_attendance(self):
        add_participant(self.excursion, self.user)
        change_state(self.excursion, Excursion.Estado.REGISTRO_CERRADO)
        change_state(self.excursion, Excursion.Estado.DIA_EVENTO)
        
        mark_attendance(self.excursion, {self.user.id: True})
        reg = RegistroExcursion.objects.get(usuario=self.user, excursion=self.excursion)
        self.assertTrue(reg.asistio)
