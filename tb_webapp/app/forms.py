from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from datetime import date

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 
                'password2']

# def get_month_choices():
#     return [(i, date(2000, i, 1).strftime('%B')) for i in range(1, 13)]

def get_year_choices():
    current_year = date.today().year
    return [(year, year) for year in range(current_year, current_year + 5, 1)]

class MLForm(forms.Form):
    # month = forms.ChoiceField(choices=get_month_choices(), label="Month")
    year = forms.ChoiceField(choices=get_year_choices(), label="Year")

    def clean(self):
        # date = self.cleaned_data['date']
        # Set day to 1 to always use the first of the month
        cleaned_data = super().clean()
        # month = int(cleaned_data.get("month"))
        year = int(cleaned_data.get("year"))
        
        # Create a date with the day set to 1
        # cleaned_data["date"] = date(year, month, 1)
        cleaned_data['year']
        return cleaned_data