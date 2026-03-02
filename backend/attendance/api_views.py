from datetime import date, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from core.models import Beneficiary, Activity
from .models import AttendanceRecord, Excursion

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    today = date.today()
    
    # Basic Stats
    attendances_today = AttendanceRecord.objects.filter(date=today).count()
    active_users = Beneficiary.objects.filter(is_active=True).count()
    
    # Top Activity
    top_activity = Activity.objects.annotate(attendance_count=Count('events__attendances')).order_by('-attendance_count').first()
    
    from django.db.models.functions import ExtractYear, ExtractMonth
    
    # Chart Data (Annual comparison, last 3 years)
    current_year = today.year
    years = [current_year, current_year - 1, current_year - 2]
    
    annual_data = {
        y: [0]*12 for y in years
    }
    
    qs = AttendanceRecord.objects.filter(date__year__in=years).annotate(
        year=ExtractYear('date'),
        month=ExtractMonth('date')
    ).values('year', 'month').annotate(count=Count('id'))
    
    for row in qs:
        annual_data[row['year']][row['month'] - 1] = row['count']
        
    chart_series = [
        {'name': str(y), 'data': annual_data[y]} for y in years
    ]

    # Top 5 Attendees
    top_attendees_qs = Beneficiary.objects.annotate(
        attendance_count=Count('attendances')
    ).filter(attendance_count__gt=0).order_by('-attendance_count')[:5]
    
    top_attendees = [
        {
            'id': b.id,
            'name': f"{b.first_name} {b.last_name}",
            'ci': b.ci,
            'attendance_count': b.attendance_count
        } for b in top_attendees_qs
    ]

    return Response({
        'attendances_today': attendances_today,
        'active_users': active_users,
        'top_activity_name': top_activity.name if top_activity else 'N/A',
        'chart_data': chart_series,
        'top_attendees': top_attendees
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_time = request.GET.get('start_time')  # format HH:MM
    end_time = request.GET.get('end_time')       # format HH:MM
    
    qs = AttendanceRecord.objects.select_related('beneficiary', 'event__activity').all()
    
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
    if start_time:
        qs = qs.filter(time__gte=start_time)
    if end_time:
        qs = qs.filter(time__lte=end_time)
        
    qs = qs.order_by('-date', '-time')
    
    data = []
    for r in qs:
        data.append({
            'id': r.id,
            'date': r.date.strftime('%Y-%m-%d'),
            'time': r.time.strftime('%H:%M') if r.time else '',
            'beneficiary_name': f"{r.beneficiary.first_name} {r.beneficiary.last_name}",
            'beneficiary_ci': r.beneficiary.ci,
            'activity_name': r.event.activity.name,
            'event_name': r.event.name,
        })
        
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_attendance_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    qs = AttendanceRecord.objects.select_related('event__activity').all()
    
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)
        
    # Group by Event (and Activity by string relation context in rendering)
    report_data = qs.values(
        'event__activity__name', 
        'event__name'
    ).annotate(
        attendees=Count('beneficiary', distinct=True)
    ).order_by('-attendees')
    
    data = []
    for r in report_data:
        data.append({
            'activity_name': r['event__activity__name'],
            'event_name': r['event__name'],
            'attendees': r['attendees']
        })
        
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_report(request):
    """
    Returns attendance count grouped by event (with event date), for the 'Por Evento' report.
    Query params: start_date, end_date
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    qs = AttendanceRecord.objects.select_related('event__activity').all()

    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    report_data = qs.values(
        'event__id',
        'event__name',
        'event__date',
        'event__activity__name',
    ).annotate(
        attendees=Count('beneficiary', distinct=True)
    ).order_by('-attendees', 'event__activity__name')

    data = []
    for r in report_data:
        data.append({
            'event_id': r['event__id'],
            'event_name': r['event__name'],
            'event_date': r['event__date'].strftime('%Y-%m-%d') if r['event__date'] else '-',
            'activity_name': r['event__activity__name'],
            'attendees': r['attendees'],
        })

    return Response(data)


from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def beneficiary_profile_report(request, pk):
    b = get_object_or_404(Beneficiary, pk=pk)
    
    total_attendance = AttendanceRecord.objects.filter(beneficiary=b).count()
    
    # Breakdown by activity/event
    activities_data = AttendanceRecord.objects.filter(beneficiary=b).values(
        'event__activity__name', 'event__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    recent_attendances = AttendanceRecord.objects.filter(beneficiary=b).select_related('event__activity').order_by('-date')[:5]
    
    recent_list = []
    for r in recent_attendances:
        recent_list.append({
            'date': r.date.strftime('%Y-%m-%d'),
            'activity': r.event.activity.name,
            'event': r.event.name
        })
        
    activity_list = []
    for a in activities_data:
        activity_list.append({
            'activity_name': a['event__activity__name'],
            'event_name': a['event__name'],
            'count': a['count']
        })
    
    profile_data = {
        'id': b.id,
        'first_name': b.first_name,
        'last_name': b.last_name,
        'ci': b.ci,
        'dob': b.dob.strftime('%Y-%m-%d') if b.dob else None,
        'sex': b.get_sex_display(),
        'sector': b.sector,
        'is_active': b.is_active,
        'created_at': b.created_at.strftime('%Y-%m-%d'),
        
        'stats': {
            'total_attendance': total_attendance,
            'top_activities': activity_list,
            'recent_history': recent_list
        }
    }
    
    return Response(profile_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_profile_report(request, pk):
    act = get_object_or_404(Activity, pk=pk)
    
    events_qs = act.events.annotate(attendance_count=Count('attendances')).order_by('-id')
    events_list = []
    
    total_attendance = 0
    for e in events_qs:
        events_list.append({
            'id': e.id,
            'name': e.name,
            'date': e.date.strftime('%Y-%m-%d') if e.date else None,
            'attendance_count': e.attendance_count
        })
        total_attendance += e.attendance_count

    profile_data = {
        'id': act.id,
        'name': act.name,
        'category': act.category,
        'deadline_date': act.deadline_date.strftime('%Y-%m-%d') if act.deadline_date else None,
        'description': act.description,
        'is_active': act.is_active,
        'image': act.image,
        'events': events_list,
        'total_attendance': total_attendance
    }
    
    return Response(profile_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_attendees_detail(request):
    """
    Returns the list of unique attendees for a given activity+event within a date range.
    Query params: activity_name, event_name, start_date, end_date
    """
    activity_name = request.GET.get('activity_name', '')
    event_name = request.GET.get('event_name', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    qs = AttendanceRecord.objects.select_related('beneficiary', 'event__activity').all()

    if activity_name:
        qs = qs.filter(event__activity__name=activity_name)
    if event_name:
        qs = qs.filter(event__name=event_name)
    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    qs = qs.order_by('beneficiary__first_name', 'beneficiary__last_name')

    # Unique attendees: one row per beneficiary (most recent attendance date shown)
    seen = {}
    for r in qs:
        bid = r.beneficiary.id
        if bid not in seen:
            seen[bid] = {
                'nombre': f"{r.beneficiary.first_name} {r.beneficiary.last_name}",
                'cedula': r.beneficiary.ci or '-',
                'sector': r.beneficiary.sector or '-',
                'ultima_asistencia': r.date.strftime('%Y-%m-%d'),
                'ultima_hora': r.time.strftime('%H:%M') if r.time else '',
                'total_visitas': 0,
            }
        seen[bid]['total_visitas'] += 1
        # keep the most recent date
        if r.date.strftime('%Y-%m-%d') > seen[bid]['ultima_asistencia']:
            seen[bid]['ultima_asistencia'] = r.date.strftime('%Y-%m-%d')
            seen[bid]['ultima_hora'] = r.time.strftime('%H:%M') if r.time else ''

    return Response(list(seen.values()))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_chart_data(request):
    """
    Returns daily attendance counts for the given date range.
    Query params: start_date, end_date
    """
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        # Default: last 7 days
        end_dt = date.today()
        start_dt = end_dt - timedelta(days=6)
    else:
        from datetime import datetime
        start_dt = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Build list of all days in range
    delta = (end_dt - start_dt).days + 1
    days = [start_dt + timedelta(days=i) for i in range(delta)]

    # Aggregate attendance per day
    qs = AttendanceRecord.objects.filter(
        date__gte=start_dt, date__lte=end_dt
    ).values('date').annotate(count=Count('id')).order_by('date')

    counts_by_date = {r['date']: r['count'] for r in qs}

    labels = [d.strftime('%d %b') for d in days]
    data = [counts_by_date.get(d, 0) for d in days]

    return Response({'labels': labels, 'data': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_notifications(request):
    """
    Returns a unified list of system alerts/notifications:
    - Birthdays (Today and next 7 days)
    - Activities close to deadline
    - Excursions that are past their date but not marked as finished
    """
    today = date.today()
    notifications = []
    
    # 1. Birthdays
    # Note: Extracting month/day cross-year is tricky in simple ORM without ExtractMonth etc, 
    # but for simplicity we'll pull all active users and filter in memory if the DB is small enough,
    # OR use ExtractMonth/Day. Given this is SQLite/small DB, we'll do extract.
    from django.db.models.functions import ExtractMonth, ExtractDay
    upcoming_limit = today + timedelta(days=7)
    
    # Easier approximation: just get those whose birthday is EXACTLY today or next days.
    # To handle wrap-around years, it's safer to just check month/day combinations.
    active_bens = Beneficiary.objects.filter(is_active=True, dob__isnull=False).annotate(
        birth_month=ExtractMonth('dob'),
        birth_day=ExtractDay('dob')
    )
    
    for b in active_bens:
        # Reconstruct their birthday for THIS year
        try:
            bday_this_year = date(today.year, b.birth_month, b.birth_day)
        except ValueError:
            # Leap year edge case (Feb 29 on a non-leap year)
            bday_this_year = date(today.year, 2, 28)
            
        if today <= bday_this_year <= upcoming_limit:
            if bday_this_year == today:
                msg = f"¡Hoy es el cumpleaños de {b.first_name} {b.last_name}!"
            else:
                msg = f"{b.first_name} {b.last_name} cumple años el {bday_this_year.strftime('%d/%m')}."
                
            notifications.append({
                'id': f'bday_{b.id}',
                'type': 'birthday',
                'title': 'Cumpleaños',
                'message': msg,
                'date': bday_this_year.strftime('%Y-%m-%d'),
                'is_urgent': bday_this_year == today
            })
            
    # 2. Expiring Activities
    expiring_acts = Activity.objects.filter(
        is_active=True, 
        deadline_date__isnull=False,
        deadline_date__gte=today,
        deadline_date__lte=upcoming_limit
    )
    for act in expiring_acts:
        notifications.append({
            'id': f'act_{act.id}',
            'type': 'activity',
            'title': 'Actividad por expirar',
            'message': f"La actividad '{act.name}' expira el {act.deadline_date.strftime('%d/%m')}.",
            'date': act.deadline_date.strftime('%Y-%m-%d'),
            'is_urgent': act.deadline_date == today
        })
        
    # 3. Expired Excursions (Not finalized)
    expired_excursions = Excursion.objects.filter(
        fecha_evento__lt=today
    ).exclude(estado='finalizado').exclude(estado='cancelado')
    
    for exc in expired_excursions:
        notifications.append({
            'id': f'exc_{exc.id}',
            'type': 'warning',
            'title': 'Excursión Pendiente',
            'message': f"La excursión '{exc.nombre}' ya pasó ({exc.fecha_evento.strftime('%d/%m')}) y sigue en estado '{exc.get_estado_display()}'.",
            'date': exc.fecha_evento.strftime('%Y-%m-%d'),
            'is_urgent': True
        })
        
    # Sort notifications by urgency and date
    notifications.sort(key=lambda x: (not x['is_urgent'], x['date']))
    
    return Response(notifications)
