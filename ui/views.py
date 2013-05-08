from django.http import HttpResponse
from django.db import connection
from django.template import Context, loader
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta

from ui.models import Flowdata

def index(request):
    # Set up initial values
    all_flows = Flowdata.objects.all()
    delta = timedelta(minutes=20)
    right_now = timezone.now()
    num_slices = 12

    # Create the initial time slices
    slices = []
    slices.append(right_now - delta)
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

    # Work out the top X (10?) busiest filenames for each time slice
    # Note - This is PostgreSQL specific syntax as it's MUCH faster than
    # using Django syntax (for me, with limited Django knowledge so far)
    cursor = connection.cursor()
    cursor.execute("select distinct (filename) filename, count(*) OVER (PARTITION by filename) from ui_flowdata where start_time > %s order by count desc limit 10", [right_now - delta])
    busiest_files = cursor.fetchall()

    # Work out the length of time taken to create this view
    end_now = timezone.now()
    processing_time = timedelta.total_seconds(end_now - right_now)

    # Render and return the view
    template = loader.get_template('ui/index.html')
    context = Context({
        'right_now': right_now, # Timestamp of when this data is from
        'delta': delta, # The number of minutes per time slice
        'num_slices': num_slices, # The number of time slices in the data array
        'processing_time': processing_time, # The length of time taken to create this view
        'counts': counts, # Array holding the flow totals per time slice
        'highest_count': highest_count_value, # The highest flow value found.  Used to highlight the busiest time slice
        'busiest_files': busiest_files, # The busiest files in the first time slice (should be expanded to do each time slice)
    })
    return HttpResponse(template.render(context))
