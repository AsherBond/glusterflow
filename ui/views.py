from django.http import HttpResponse
from django.template import Context, loader
from django.utils import timezone
from datetime import timedelta

from ui.models import Flowdata

def index(request):
    # Set up initial values
    all_flows = Flowdata.objects.all()
    delta = timedelta(minutes=20)
    rightnow = timezone.now()
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
    highest_count_value = 0 # Holds the highest flow value found in a time slice
    for x in range(num_slices):
        new_count = flows[x].count()
        if new_count > highest_count_value:
            highest_count_value = new_count # Keep track of the highest flow count value
        counts.append(new_count)

    # Render and return the view
    template = loader.get_template('ui/index.html')
    context = Context({
        'rightnow': rightnow, # Timestamp of when this data is from
        'delta': delta, # The number of minutes per time slice
        'num_slices': num_slices, # The number of time slices in the data array
        'counts': counts, # Array holding the flow totals per time slice
        'highest_count': highest_count_value, # The highest flow value found.  Used to highlight the busiest time slice
    })
    return HttpResponse(template.render(context))
