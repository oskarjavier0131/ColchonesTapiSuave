from django import forms
from .models import Contacto, Newsletter

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'telefono', 'ciudad', 'asunto', 'mensaje', 'acepto_terminos']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+57 300 123 4567'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu ciudad'
            }),
            'asunto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Cuéntanos cómo podemos ayudarte...'
            }),
            'acepto_terminos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
    def clean_acepto_terminos(self):
        acepto = self.cleaned_data.get('acepto_terminos')
        if not acepto:
            raise forms.ValidationError('Debes aceptar el tratamiento de datos personales.')
        return acepto

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email', 'nombre']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre (opcional)'
            })
        }