from django import forms
from .models import DeliverySchedule, Vehicle

class AssignVehicleForm(forms.ModelForm):
    class Meta:
        model = DeliverySchedule
        fields = ['vehicle', 'delivery_date']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'driver_name', 'capacity', 'is_active']
        widgets = {
            'vehicle': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
            