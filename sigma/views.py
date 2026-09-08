from django.shortcuts import render

from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Monitoria, EntregaMensal
from .forms import UsuarioCreationForm

def login_view(request):
    # Se o usuário já estiver logado, manda direto para o dashboard
    if request.user.is_authenticated:
        return redirecionar_dashboard(request.user)

    if request.method == 'POST':
        # Como seu modelo base é o AbstractUser, o login padrão é o campo 'username'
        # O Setor Pedagógico pode usar o CPF, Matrícula ou Email como 'username' no momento de cadastrar.
        usuario_digitado = request.POST.get('username') 
        senha_digitada = request.POST.get('password')

        user = authenticate(request, username=usuario_digitado, password=senha_digitada)

        if user is not None:
            login(request, user)
            return redirecionar_dashboard(user)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'sigma/login.html')

def redirecionar_dashboard(user):
    """Função auxiliar para checar o tipo de usuário e redirecionar"""
    if user.tipo_usuario == 'A':
        return redirect('dashboard_pedagogico')
    elif user.tipo_usuario == 'P':
        return redirect('dashboard_professor')
    elif user.tipo_usuario == 'M':
        return redirect('dashboard_monitor')
    else:
        # Se for o superuser que você criou no terminal, manda pro admin nativo
        return redirect('/admin/')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- VIEWS DOS DASHBOARDS (Provisórias para não dar erro de página não encontrada) ---
@login_required
def dashboard_monitor(request):
    return render(request, 'sigma/dashboard_monitor.html')

@login_required
def dashboard_professor(request):
    monitorias = Monitoria.objects.filter(professor=request.user)
    
    # 2. Busca apenas as entregas com status 'P' (Pendente) vinculadas a essas monitorias
    entregas_pendentes = EntregaMensal.objects.filter(monitoria__in=monitorias, status='P')
    
    contexto = {
        'monitorias': monitorias,
        'entregas_pendentes': entregas_pendentes,
        'qtd_pendentes': entregas_pendentes.count(),
    }
    return render(request, 'sigma/dashboard_professor.html', contexto)

@login_required
def avaliar_entrega(request, entrega_id, acao):
    # Garante que o professor só pode avaliar documentos dos próprios alunos
    entrega = get_object_or_404(EntregaMensal, id=entrega_id, monitoria__professor=request.user)
    
    if acao == 'aprovar':
        entrega.status = 'A'
        entrega.feedback_professor = ''
        entrega.save()
        messages.success(request, f'Documento de {entrega.monitoria.monitor.get_full_name()} aprovado!')
        
    elif acao == 'recusar' and request.method == 'POST':
        motivo = request.POST.get('motivo_recusa')
        entrega.status = 'R'
        entrega.feedback_professor = motivo
        entrega.save()
        messages.error(request, f'Documento devolvido para {entrega.monitoria.monitor.get_full_name()} para ajustes.')
        
    return redirect('dashboard_professor')

@login_required
def historico_monitor(request, monitoria_id):
    # Busca a monitoria, garantindo por segurança que o aluno pertence ao professor logado
    monitoria = get_object_or_404(Monitoria, id=monitoria_id, professor=request.user)
    
    # Busca o histórico completo de entregas, ordenado da mais recente para a mais antiga
    entregas = EntregaMensal.objects.filter(monitoria=monitoria).order_by('-mes_referencia')
    
    contexto = {
        'monitoria': monitoria,
        'entregas': entregas
    }
    return render(request, 'sigma/historico_monitor.html', contexto)


@login_required
def dashboard_pedagogico(request):
   # Conta quantos usuários existem de cada tipo no banco de dados
    total_monitores = Usuario.objects.filter(tipo_usuario='M').count()
    total_professores = Usuario.objects.filter(tipo_usuario='P').count()
    
    contexto = {
        'total_monitores': total_monitores,
        'total_professores': total_professores,
    }
    return render(request, 'sigma/dashboard_pedagogico.html', contexto)

@login_required
def listar_usuarios(request):
    # Trava de segurança: apenas Setor Pedagógico (A) acessa
    if request.user.tipo_usuario != 'A' and not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao Setor Pedagógico.')
        return redirect('login')
    
    # Busca todos os usuários do banco, ordenados por nome
    usuarios = Usuario.objects.all().order_by('first_name')
    return render(request, 'sigma/listar_usuarios.html', {'usuarios': usuarios})
@login_required
def criar_usuario(request):
    # Trava de segurança
    if request.user.tipo_usuario != 'A' and not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo usuário cadastrado com sucesso!')
            return redirect('listar_usuarios')
    else:
        form = UsuarioCreationForm()
        
    return render(request, 'sigma/criar_usuario.html', {'form': form})