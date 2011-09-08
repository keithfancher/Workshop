from django.http import HttpResponseForbidden
from django.template import RequestContext, loader


# Because there's no fucking Http403 exception??? Seriously? At least in Django
# 1.1...
def error_403(request):
    t = loader.get_template('403.html')
    c = RequestContext(request)
    return HttpResponseForbidden(t.render(c))
