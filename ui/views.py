from django.http import HttpResponse
from django.template import Context, loader

from ui.models import Flowdata

def index(request):
    all_flows = Flowdata.objects.order_by('-start_time')[:5]
    template = loader.get_template('ui/index.html')
    context = Context({
        'all_flows': all_flows,
    })
    return HttpResponse(template.render(context))
