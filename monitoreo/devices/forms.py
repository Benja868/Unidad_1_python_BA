from django import forms
from django.contrib.auth.models import User
from devices.models import Organization
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name','description', 'consumption', 'status', 'category', 'zone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'consumption': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # corregido a checkbox
            'category': forms.Select(attrs={'class': 'form-select'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        return name


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    organization_name = forms.CharField(label='Organization Name', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords don\'t match.')
        return cd.get('password2')

    def clean_organization_name(self):
        name = self.cleaned_data.get('organization_name')
        if Organization.objects.filter(name=name).exists():
            raise forms.ValidationError('Organization with this name already exists.')
        return name
