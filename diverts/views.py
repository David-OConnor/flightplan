from django.http import HttpResponse
from django.shortcuts import render

from diverts import diverts_code
from diverts.forms import DivertForm


def index(request):
    if request.method == 'POST':
        form = DivertForm(request.POST)
        if not form.is_valid():
            return HttpResponse("<h2>Something went wrong - try again.</h2>")

        flight_path = form.cleaned_data['flight_path']
        max_dist = form.cleaned_data['max_dist']
        min_rwy_len = form.cleaned_data['min_rwy_len']
        min_rwy_width = form.cleaned_data['min_rwy_width']
        paved_only = form.cleaned_data['paved_only']
        pickyness = form.cleaned_data['pickyness']

        flight_path = flight_path.split(' ')
        divert_fields = diverts_code.find_diverts(flight_path, max_dist,
                                                  min_rwy_len, min_rwy_width, paved_only)

        if not divert_fields:
            return HttpResponse("<h2>One of the flight plan points was invalid - try again.</h2>")

        flight_path_js = diverts_code.flight_path_js(flight_path)

        divert_fields_js = []
        for divert in divert_fields:
            ident = divert.icao if divert.icao else divert.ident
            divert_fields_js.append([divert.lat, divert.lon, ident])

        center = [flight_path_js[0][0], flight_path_js[0][1]]

        context = {
            'flight_path': flight_path_js,
            'divert_fields_js': divert_fields_js,
            'divert_fields': divert_fields,

            'center': center,  #todo find a smart algorithm/copy from royals
            'chart_type': 'TERRAIN',
            'zoom': 14,
            'width': '100%',
            'height': '100%',

        }

        # return render(request, 'diverts/diverts_results.html', context)
        return render(request, 'diverts/gmaps.html', context)

    else:
        form = DivertForm()
        context = {'form': form}

        return render(request, 'diverts/index.html', context)


from django.views.generic.edit import FormView


class DivertsView(FormView):
# class index(FormView):
    template_name = 'diverts/index.html'
    form_class = DivertForm
    success_url = '/diverts/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        # return super(index, self).form_valid(form)
        return super(DivertsView, self).form_valid(form)