from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Monitoria, PlanoTrabalhoMensal, AtendimentoDiario, EntregaMensal, AvaliacaoSemestral, AvaliacaoPrograma

class CustomUsuarioAdmin(UserAdmin):
    # Adiciona os campos personalizados na tela de edição do usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Sistema Sigma', {'fields': ('tipo_usuario', 'cpf', 'telefone')}),
    )
    # Adiciona os campos na tela de criação de um novo usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações do Sistema Sigma', {'fields': ('tipo_usuario', 'cpf', 'telefone')}),
    )
    # Cria colunas extras na lista geral de usuários para facilitar a visualização
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')

# Registra o usuário utilizando a configuração customizada que criamos acima
admin.site.register(Usuario, CustomUsuarioAdmin)

# Registra as entidades do sistema Sigma
admin.site.register(Monitoria)
admin.site.register(PlanoTrabalhoMensal)
admin.site.register(AtendimentoDiario)
admin.site.register(EntregaMensal)
admin.site.register(AvaliacaoSemestral)
admin.site.register(AvaliacaoPrograma)