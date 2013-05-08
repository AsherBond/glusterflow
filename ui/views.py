from django.http import HttpResponse
from django.template import Context, loader
from datetime import datetime, timedelta

from ui.models import Flowdata

def index(request):
    # Set up initial values
    all_flows = Flowdata.objects.all()
    delta = timedelta(minutes=20)
    rightnow = datetime.now()
    num_slices = 12

    # Create the initial time slices
    slices = []
    slices.append(rightnow - delta)
    for x in range(1, num_slices):
        slices.append(slices[x-1] - delta)

    # Slice the flow data into time slices
    flows = []
    flows.append(all_flows.filter(start_time__gte=slices[0]))
    for x in range(1, num_slices):
        flows.append(all_flows.filter(start_time__gte=slices[x]).filter(start_time__lt=slices[x-1]))

    # Count the number of flows in each time slice
    counts = []
    for x in range(num_slices):
      counts.append(flows[x].count())

    # Render and return the view
    template = loader.get_template('ui/index.html')
    context = Context({
        'all_flows': all_flows,
        'rightnow': rightnow,
        'num_slices': num_slices,
        'delta': delta,
        'slices': slices,
        'flows': flows,
        'counts': counts,
    })
    return HttpResponse(template.render(context))
