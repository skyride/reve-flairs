import requests

from django import forms

from core.models import Corp


class CorpAddForm(forms.Form):
    id = forms.IntegerField(required=True)

    def clean_id(self):
        id = self.cleaned_data['id']

        # Check it doesn't already exist
        corp = Corp.objects.filter(corp_id=id)
        if corp.exists():
            raise forms.ValidationError("%s is already in the database" % corp.first().name)

        # Test fetch the corp id
        r = requests.get("https://esi.tech.ccp.is/latest/corporations/%s/?datasource=tranquility" % id)
        if r.status_code != 200:
            raise forms.ValidationError("Failed to fetch corp from ESI")

        return id