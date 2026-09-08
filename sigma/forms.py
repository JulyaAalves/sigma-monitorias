from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Quais campos o Pedagógico precisará preencher ao criar a conta
        fields = ('username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'cpf', 'telefone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica o visual do Bootstrap em todos os campos automaticamente
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # O campo de escolha (tipo_usuario) recebe uma classe um pouco diferente no Bootstrap
        self.fields['tipo_usuario'].widget.attrs['class'] = 'form-select'