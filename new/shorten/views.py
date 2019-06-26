from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import bitly
from .forms import bitlyform, editBitly
# Create your views here.

def index(request):
    objects = bitly.objects.all()
    print(objects)

    context = {'objs' : objects}
    return render(request, "index.html", context)

def create(request):
    from .utils import create_shortcode
    form = bitlyform(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.shortcode = create_shortcode()
        instance.datewise = "{}"
        instance.save()

        return HttpResponseRedirect("http://127.0.0.1:8000/home/")

    context = {"urlform": form}
    return render(request, "create.html", context)

def goto(request, shortcode=None):
    qs = get_object_or_404(bitly, shortcode__iexact=shortcode)
    import json
    if qs:
        from .utils import current_day
        instance = json.loads(qs.datewise)
        crt_date = current_day()
        if crt_date in instance:
            instance[crt_date]+= 1
        else:
            instance[crt_date] = 1
        qs.datewise = json.dumps(instance)
        qs.save()
    return HttpResponseRedirect(qs.long_url)

def update(request, pk=None):
    qs = get_object_or_404(bitly, id=pk)
    form = editBitly(request.POST or None, instance=qs)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("http://127.0.0.1:8000/home")

    context = {'urlform': form}
    return render(request, 'create.html', context)

def delete(request, pk=None):
    qs = get_object_or_404(bitly, id=pk)
    qs.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/home")

