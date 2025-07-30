from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from convidados.models import Convidados
from.models import Presentes  # Corrigido: sem ponto antes do models para evitar ambiguidade

def home(request):
    token = request.GET.get('token') or request.POST.get('token') or request.session.get('token') or ''
    token = token.strip()

    convidado = Convidados.objects.filter(token=token).first()
    if not convidado or not convidado.nome_convidado or not convidado.whatsapp:
        messages.warning(request, "Antes de acessar os presentes, complete seu cadastro como convidado.")
        return redirect(reverse('lista_convidados'))

    request.session['token'] = token

    if request.method == 'GET':
        presentes_validos = [
            p for p in Presentes.objects.all()
            if isinstance(p.preco, (int, float, Decimal))
        ]
        data = {
            "reservado": Presentes.objects.filter(reservado=True).count(),
            "nao_reservado": Presentes.objects.filter(reservado=False).count()
}
        return render(request, 'noivos/home.html', {
            'presentes': presentes_validos,
            'data': data,
            'token': token
})

    nome_presente = request.POST.get('nome_presente', '').strip()
    foto = request.FILES.get('foto')
    preco_str = request.POST.get('preco', '').strip()
    importancia_str = request.POST.get('importancia', '').strip()

    if not nome_presente or not preco_str or not importancia_str:
        messages.error(request, "Todos os campos são obrigatórios.")
        return redirect(f'{request.path}?token={token}')

    try:
        preco = Decimal(preco_str)
        importancia = int(importancia_str)
        if not (1 <= importancia <= 5):
            raise ValueError()
    except (InvalidOperation, ValueError):
        messages.error(request, "Preço ou importância inválidos.")
        return redirect(f'{request.path}?token={token}')

    presente = Presentes(
        nome_presente=nome_presente,
        foto=foto,
        preco=preco,
        importancia=importancia,
        reservado=True,
        reservado_por=convidado
)
    presente.save()

    messages.success(request, "Presente adicionado com sucesso!")
    return redirect(f"{reverse('convidados')}?token={token}")
