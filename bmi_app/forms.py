from django import forms

class BMIForm(forms.Form):
    weight = forms.CharField(label='体重')
    height = forms.CharField(label='身長')