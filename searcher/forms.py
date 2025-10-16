from django import forms
 
class MultiSearchForm(forms.Form):
    queries = forms.CharField(widget=forms.HiddenInput(), required=True)
 
    def clean_queries(self):
        raw = self.cleaned_data['queries']

        queries = [q.strip() for q in raw.split("\n") if q.strip()]
        if not queries:
            raise forms.ValidationError("At least one search query is required.")

        for q in queries:
            if len(q) < 2:
                raise forms.ValidationError("Each query must be at least 2 characters.")
        return queries