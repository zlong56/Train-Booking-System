from src.init import *
from src.landing import *
import json
from datetime import datetime, timedelta

def generate_booking_no():
    booking_obj = Booking.objects.all()
    
    if booking_obj:
        numeric_ids = [int(booking.BookingNo.split('-')[-1]) for booking in booking_obj if booking.BookingNo.startswith('TBS-')]
        current_id = max(numeric_ids) if numeric_ids else 0
    else:
        current_id = 0  # Start from 0 if no trains exist
    
    new_bookingid = current_id + 1
    return f"TBS-{new_bookingid:03d}"

def check_seat_status(request, coach_id):
    coach = Coach.objects.get(pk=coach_id)
    seats = Seat.objects.filter(Coach=coach)
    
    seat_status = {
        seat.pk: seat.SeatStatus for seat in seats
    }
    
    return JsonResponse(seat_status)

@login_required
@client_only
def clienthome(request):
    context = initialization(request)
    obj = Client.objects.get(pk=request.user.pk)
    context['obj'] = obj
    
    return render(request,'client/clienthome.html', context)

def userhome(request):
    context = initialization(request)
    state = State.objects.all()
    
    depart_state = None
    arrive_state = None
    date = None
    return_date = None
    
    if request.method == "POST" and "search_train" in request.POST:
        context['search_mode'] = True
        no_pax = request.POST.get("NoPax")
        request.session['no_pax'] = no_pax
        
        depart_state_obj = State.objects.get(pk=request.POST.get("Depart"))
        arrive_state_obj = State.objects.get(pk=request.POST.get("Arrive"))
        
        depart_state = depart_state_obj.Name
        arrive_state = arrive_state_obj.Name
        
        date_str = request.POST.get("Date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)
        
        if request.POST.get("ReturnDate"):
            returndate_str = request.POST.get("ReturnDate")
            return_date = datetime.strptime(returndate_str, "%Y-%m-%d").date() if returndate_str else None
            return_start_datetime = datetime.combine(return_date, datetime.min.time())
            return_end_datetime = return_start_datetime + timedelta(days=1)
        
        if depart_state and arrive_state and date:
            train_obj = Train.objects.filter(
                is_complete=False, 
                DepartState=depart_state, 
                ArriveState=arrive_state,   
                DepartDateTime__range=(start_datetime, end_datetime)
                ).order_by('DepartDateTime')
            
            train_seat_list = []
            
            for train in train_obj:
                available_seat = Seat.objects.filter(
                    Train=train, 
                    SeatStatus="AVAILABLE"
                    ).count()
                
                train_seat_list.append({
                    'train': train,
                    'available_seat': available_seat 
                })
                
            context['train_seat_list'] = train_seat_list
            context['train_obj'] = train_obj
            
    if request.method == "POST" and "view_train" in request.POST:
        request.session['train_pk'] = request.POST.get("view_train")
        request.session['no_pax'] = request.session.get("no_pax")
        return redirect('coach_select')
    
    context['state'] = state
    return render(request, 'client/userhome.html', context)

# region VIEW ===========================================

def coach_select(request):
    context = initialization(request)
    no_pax = request.session.get("no_pax")
    
    train_obj = Train.objects.get(pk=request.session.get("train_pk"))
    coach_obj = Coach.objects.filter(Train=train_obj).order_by('CoachType')
    
    coach_seat_list = []
    
    for coach in coach_obj:
        available_seat = Seat.objects.filter(
            Coach=coach,
            SeatStatus = "AVAILABLE"
        ).count()
        
        coach_seat_list.append({
            'coach': coach,
            'available_seat': available_seat
        })

    if request.method == "POST" and "view_seat" in request.POST:
        request.session['coach_pk'] = request.POST.get("view_seat")
        request.session['no_pax'] = no_pax
        request.session['train_pk'] = train_obj.pk
        return redirect('seat_select')

    context['coach_seat_list'] = coach_seat_list
    context['coach_obj'] = coach_obj
    context['train_obj'] = train_obj
    return render(request, 'client/coach_select.html', context) 

def seat_select(request):
    context = initialization(request)
    
    train_obj = Train.objects.get(pk=request.session.get("train_pk"))
    coach_obj = Coach.objects.get(pk=request.session.get("coach_pk"))
    no_pax = request.session.get("no_pax")
    
    col1_seat = Seat.objects.filter(Coach=coach_obj, SeatNo__in=["01", "03", "05", "07", "09"])
    col2_seat = Seat.objects.filter(Coach=coach_obj, SeatNo__in=["02", "04", "06", "08", "10"])
    col3_seat = Seat.objects.filter(Coach=coach_obj, SeatNo__in=["11", "13", "15", "17", "19"])
    col4_seat = Seat.objects.filter(Coach=coach_obj, SeatNo__in=["12", "14", "16", "18", "20"])
    
    if request.method == "POST" and "check_out" in request.POST:
        selected_seats_str = request.POST.getlist('selected_seats[]')[0]  # Take the first element, since it's a single string
        user_pk = request.user.pk
        price = Decimal(train_obj.Price) 
        pax = int(no_pax)
        total_price = price * pax

        # Parse the string into a list using json.loads
        selected_seats = json.loads(selected_seats_str)
        
        booking_obj = Booking.objects.create(
            BookingStatus = "PENDING PAYMENT",
            Price = total_price,
            NoPax = pax,
            BookingNo = generate_booking_no(),
            Client = Client.objects.get(pk=user_pk),
            Train = train_obj,
            Coach = coach_obj,
        )

        for seat_id in selected_seats:
            # Convert seat_id to an integer (it should already be a string, so this is fine)
            seat_id = int(seat_id)

            # Query the Seat object using the integer seat_id
            seat = Seat.objects.get(id=seat_id)
            
            # Update the seat's status
            seat.SeatStatus = "RESERVED"
            seat.last_locked_time = timezone.now()
            seat.save()
            
            booking_obj.Seat.add(seat)
            booking_obj.save()
            
        # Redirect to the booking summary page
        
        request.session['booking_pk'] = booking_obj.pk
        return redirect('booking_summary')
    
    context = {
        'coach_obj': coach_obj,
        'col1_seat': col1_seat,
        'col2_seat': col2_seat,
        'col3_seat': col3_seat,
        'col4_seat': col4_seat,
        'no_pax': no_pax,
    }
    return render(request, 'client/seat_select.html', context)

@login_required
@client_only
def booking_view(request):
    context = initialization(request)
    booking_obj = Booking.objects.filter(Client=request.user, BookingStatus="SUCCESS")
    pending_booking = Booking.objects.filter(Client=request.user, BookingStatus__in=["PENDING PAYMENT", "CANCEL"])
    
    if request.method == "POST" and "booking_view" in request.POST:
        request.session['booking_pk'] = request.POST.get("booking_view")
        return redirect('booking_select')
    
    context['pending_booking'] = pending_booking
    context['booking_obj'] = booking_obj
    return render(request, 'client/booking_view.html', context)

@login_required
@client_only
def booking_summary(request):
    context = initialization(request)
    booking_obj = Booking.objects.get(pk=request.session.get("booking_pk"))
    
    if request.method == "POST" and "make_payment" in request.POST:
        
        for seat in booking_obj.Seat.all():
            seat.SeatStatus = "LOCKED"
            seat.is_locked = True
            
            seat.save()
            
        booking_obj.BookingStatus = "SUCCESS"
        booking_obj.save()
        
        return redirect("booking_view")
    
    context['booking_obj'] = booking_obj
    return render(request, 'client/booking_summary.html', context)

@login_required
@client_only
def booking_select(request):
    context = initialization(request)
    booking_obj = Booking.objects.get(pk=request.session.get("booking_pk"))

    if request.method == "POST" and "make_payment" in request.POST:
        
        for seat in booking_obj.Seat.all():
            seat.SeatStatus = "LOCKED"
            seat.is_locked = True
            
            seat.save()
            
        booking_obj.BookingStatus = "SUCCESS"
        booking_obj.save()
        
        return redirect("booking_select")

    if request.method == "POST" and "cancel_booking" in request.POST:
        for seat in booking_obj.Seat.all():
            seat.is_locked = False
            seat.SeatStatus = "AVAILABLE"
            seat.last_lock_time = None
            
            seat.save() 
            
        booking_obj.BookingStatus = "CANCEL"
        booking_obj.save()
        return redirect('booking_view')
    
    if request.method == "POST" "delete_record" in request.POST:
        for seat in booking_obj.Seat.all():
            seat.is_locked = None
            seat.SeatStatus = "AVAILABLE"
            seat.last_lock_time = None
            
            seat.save() 
            
        booking_obj.delete()
        return redirect('booking_view')

    context['booking_obj'] = booking_obj
    return render(request, 'client/booking_select.html', context)

