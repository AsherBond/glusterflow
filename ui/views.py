from django.http import HttpResponse
from django.db import connection
from django.template import Context, loader
from django.utils import timezone
from django.utils.timesince import timesince
from datetime import timedelta
from ui.models import Filename_Summaries
from ui.models import Fop_Summaries

def index(request):
    # Set up initial values
    all_busiest_files = Filename_Summaries.objects.all()
    all_summaries = Fop_Summaries.objects.all()
    delta = timedelta(minutes=1)
    right_now = timezone.now()
    num_slices = 12
    num_busiest_files = 10

    # Create the initial time slices
    slices = []
    slices.append(right_now - delta)
    for x in range(1, num_slices):
        slices.append(slices[x-1] - delta)

    # Slice the summary data into time slices
    operations = []
    operations.append(all_summaries.filter(summary_time__gte=slices[0]))
    for x in range(1, num_slices):
        operations.append(all_summaries.filter(summary_time__gte =slices[x])
                                       .filter(summary_time__lt=slices[x-1]))

    # Create an array holding the # of file operations per time slice
    counts = []
    highest_count_value = 0 # Holds the highest operation value found in a
                            # time slice
    for x in range(num_slices):
        new_count = 0
        for fop_summary in operations[x].all():
            new_count += fop_summary.count

        if new_count > highest_count_value:
            highest_count_value = new_count # Keep track of the highest
                                            # operation count value

        counts.append(new_count)

    # Work out the top X busiest files for each time slice
    busiest_files = []
    this_set = []
    query_set = all_busiest_files.filter(summary_time__gte=slices[0]).order_by('-count')[:num_busiest_files]
    for x in query_set:
        this_set.append({'filename': x.filename, 'count': x.count})
    busiest_files.append(this_set)

    for x in range(1, num_slices):
        this_set = []
        query_set = all_busiest_files.filter(summary_time__gte=slices[x]).filter(summary_time__lt=slices[x-1]).order_by('-count')[:num_busiest_files]
        for y in query_set:
            this_set.append({'filename': y.filename, 'count': y.count})
        busiest_files.append(this_set)

    # Work out the length of time taken to create this view
    time_delta = timezone.now() - right_now
    processing_time = time_delta.seconds + (time_delta.days * 24 * 3600)

    # Render and return the view
    template = loader.get_template('ui/index.html')
    context = Context({
        'right_now': right_now, # Timestamp of when this data is from
        'delta': delta, # The number of minutes per time slice
        'num_slices': num_slices, # The number of time slices in the data array
        'processing_time': processing_time, # The length of time taken to create this view
        'counts': counts, # Array holding the flow totals per time slice
        'highest_count': highest_count_value, # The highest flow value found.  Used to highlight the busiest time slice
        'busiest_files': busiest_files, # The busiest files for each time slice
    })
    return HttpResponse(template.render(context))
