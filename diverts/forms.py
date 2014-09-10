from django import forms


pickyness_choices = [('all', "All"), ('best', "Best")]


class DivertForm(forms.Form):
    flight_path = forms.CharField(widget=forms.Textarea(attrs={
        'cols': 75, 'rows': 2}), max_length=1000)

    max_dist = forms.IntegerField(initial=30, help_text="Max distance from route")

    min_rwy_len = forms.IntegerField(initial=8000, help_text="Min rwy length")

    min_rwy_width = forms.IntegerField(initial=50, help_text="Min rwy width")

    paved_only = forms.BooleanField(initial=True, required=False, help_text="Paved runways only")

    pickyness = forms.ChoiceField(widget=forms.RadioSelect,
                                  choices=pickyness_choices, initial='all')


class CreatePlanForm(forms.Form):
    start_airfield = forms.CharField(max_length=6)
    end_airfield = forms.CharField(max_length=6)