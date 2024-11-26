from src.init import *
from src.landing import *
from io import BytesIO
from django.core.files.base import ContentFile
from django.templatetags.static import static
import base64
from django.contrib.staticfiles import finders
from decimal import Decimal

def generate_train_code():
    train_obj = Train.objects.all()
    
    if train_obj:
        numeric_ids = [int(train.TrainCode.split('-')[-1]) for train in train_obj if train.TrainCode.startswith('TRN-')]
        current_id = max(numeric_ids) if numeric_ids else 0
    else:
        current_id = 0  # Start from 0 if no trains exist
    
    new_trainid = current_id + 1
    return f"TRN-{new_trainid:03d}"

@login_required
@admin_only
def adminhome(request):
    context = initialization(request)
    train_obj = Train.objects.all()
    
    context['train_obj'] = train_obj
    return render(request,'backend/adminhome.html', context)

@login_required
@admin_only
def journey_create(request):
    context = initialization(request)
    
    state = State.objects.all()
    
    if request.method == "POST" and "create_btn" in request.POST:
        depart_station = Station.objects.create(
            Name = request.POST.get("DepartLocation"),
            State = State.objects.get(pk=request.POST.get("Depart")),
        )
        
        arrive_station = Station.objects.create(
            Name = request.POST.get("ArriveLocation"),
            State = State.objects.get(pk=request.POST.get("Arrive")),
        )
        
        departdate_str = request.POST.get("DepartDateTime")
        arrivedate_str = request.POST.get("ArriveDateTime")
        depart_time = datetime.strptime(departdate_str, "%Y-%m-%dT%H:%M")
        arrive_time = datetime.strptime(arrivedate_str, "%Y-%m-%dT%H:%M")

        
        train_obj = Train.objects.create(
            TrainCode = generate_train_code(),
            DepartDateTime = depart_time,
            ArriveDateTime = arrive_time,
            TotalPassenger = 120,
            Price = request.POST.get("Price"),
            DepartLocation = depart_station,
            ArriveLocation = arrive_station,
            DepartState = depart_station.State.Name,
            ArriveState = arrive_station.State.Name,
        )
        
        coach_type = ['A', 'B', 'C', 'D', 'E', 'F']
        
        for i in range(1, 7):
            type = coach_type[i % len(coach_type)]
            coach_obj = Coach.objects.create(
                Train = train_obj,
                CoachType = type,
            )
            
            for j in range(1, 21):
                seat_obj = Seat.objects.create(
                    Coach = coach_obj,
                    Train = train_obj,
                    CoachType = coach_obj.CoachType,
                    SeatNo = f"{j:02}",
                    SeatStatus = "AVAILABLE",
                )
        
        return redirect("adminhome")
    
    context['state'] = state
    return render(request, 'backend/journey_create.html', context)
