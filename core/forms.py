import requests

from django import forms

from core.models import Corp


class CorpAddForm(forms.ModelForm):
    class Meta:
        model = Corp
        fields = ["corp_id"]

    def clean_corp_id(self):
        corp_id = self.cleaned_data['corp_id']

        # Check it doesn't already exist
        corp = Corp.objects.filter(corp_id=corp_id)
        if corp.exists():
            raise forms.ValidationError("%s is already in the database" % corp.first().name)

        # Test fetch the corp id
        r = requests.get("https://esi.evetech.net/latest/corporations/%s/?datasource=tranquility" % corp_id)
        if r.status_code != 200:
            raise forms.ValidationError("Failed to fetch corp from ESI")

        return corp_id

    def save_m2m(self):
        pass

    def save(self, commit=True):
        """
        Ignore our internal model instance and return a newly fetched object.
        """
        return Corp.fetch(self.cleaned_data['corp_id'], active=True)
