from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('sair/', views.logout_view, name='logout'),



path('monitor/', views.dashboard_monitor, name='dashboard_monitor'),




path('professor/', views.dashboard_professor, name='dashboard_professor'),
    path('professor/avaliar/<int:entrega_id>/<str:acao>/', views.avaliar_entrega, name='avaliar_entrega'),
    path('pedagogico/', views.dashboard_pedagogico, name='dashboard_pedagogico'),
    path('professor/historico/<int:monitoria_id>/', views.historico_monitor, name='historico_monitor'),




path('pedagogico/', views.dashboard_pedagogico, name='dashboard_pedagogico'),
    path('pedagogico/usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('pedagogico/usuarios/novo/', views.criar_usuario, name='criar_usuario'),






]