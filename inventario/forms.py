from django import forms
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['codigo_patrimonial', 'nombre', 'categoria', 'marca', 'modelo', 'numero_serie', 'stock', 'estado']
        widgets = {
            'codigo_patrimonial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: TI-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Laptop Dell Vostro'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dell'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Vostro 3400'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: SN-987654321'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }