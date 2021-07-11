from django import forms

class EntryForm(forms.Form):
    content = forms.CharField(
        label="", 
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'placeholder':'Enter Markdown Content Here...'
    }))

class NewEntryForm(EntryForm):
    title = forms.CharField(
    label="",
    widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Title Here...'
    }))