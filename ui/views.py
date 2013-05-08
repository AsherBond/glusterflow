from django.http import HttpResponse
from django.template import Context, loader
from datetime import datetime, timedelta

from ui.models import Flowdata

def index(request):
    all_flows = Flowdata.objects.all()

    # Create the initial time slices
    rightnow = datetime.now()
    slice1 = rightnow - timedelta(minutes=20)
    slice2 = slice1 - timedelta(minutes=20)
    slice3 = slice2 - timedelta(minutes=20)
    slice4 = slice3 - timedelta(minutes=20)
    slice5 = slice4 - timedelta(minutes=20)
    slice6 = slice5 - timedelta(minutes=20)

    # Slice the flow data into time slices
    flow1 = all_flows.filter(start_time__gte=slice1)
    flow2 = all_flows.filter(start_time__gte=slice2).filter(start_time__lt=slice1)
    flow3 = all_flows.filter(start_time__gte=slice3).filter(start_time__lt=slice2)
    flow4 = all_flows.filter(start_time__gte=slice4).filter(start_time__lt=slice3)
    flow5 = all_flows.filter(start_time__gte=slice5).filter(start_time__lt=slice4)
    flow6 = all_flows.filter(start_time__gte=slice6).filter(start_time__lt=slice5)

    # Count the number of flows in each time slice
    count1 = flow1.count()
    count2 = flow2.count()
    count3 = flow3.count()
    count4 = flow4.count()
    count5 = flow5.count()
    count6 = flow6.count()

    # Render and return the view
    template = loader.get_template('ui/index.html')
    context = Context({
        'all_flows': all_flows,
        'count1': count1,
        'count2': count2,
        'count3': count3,
        'count4': count4,
        'count5': count5,
        'count6': count6,
    })
    return HttpResponse(template.render(context))
