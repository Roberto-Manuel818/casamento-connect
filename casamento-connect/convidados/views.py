from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from noivos.models import Presentes
from.models import Convidados, Acompanhante

def get_convidado_por_token(request):
    token = request.GET.get('token')
    if not token:
        return None, 'Token não informado.'
    try:
        convidado = Convidados.objects.prefetch_related('acompanhantes').get(token=token)
        return convidado, None
    except Convidados.DoesNotExist:
        return None, 'Convidado não encontrado.'

def convidados(request):
    convidado, erro = get_convidado_por_token(request)
    if erro:
        messages.error(request, erro)
        return redirect('lista_convidados')

    if request.method == 'POST':
        nome_acompanhante = request.POST.get('acompanhantes', '').strip()

        if not nome_acompanhante:
            messages.error(request, "O nome do acompanhante não pode estar vazio.")
        else:
            Acompanhante.objects.create(nome=nome_acompanhante, convidado=convidado)
            messages.success(request, f"Acompanhante '{nome_acompanhante}' adicionado com sucesso!")

        return redirect(f"{reverse('convidados')}?token={convidado.token}")

    presentes = Presentes.objects.all().order_by('-importancia')

    return render(request, 'convidados/convidados.html', {
        'convidado': convidado,
        'presentes': presentes,
        'token': convidado.token,
        'acompanhantes': convidado.acompanhantes.all()
})

def lista_convidados(request):
    if request.method == 'GET':
        convidados = Convidados.objects.prefetch_related('acompanhantes').all()
        return render(request, 'convidados/lista_convidados.html', {'convidados': convidados})

    elif request.method == 'POST':
        nome_convidado = request.POST.get('nome_convidado', '').strip()
        whatsapp = request.POST.get('whatsapp', '').strip()
        maximo_acompanhantes_str = request.POST.get('maximo_acompanhantes', '').strip()

        if not nome_convidado or not whatsapp:
            messages.error(request, "Nome e WhatsApp são obrigatórios.")
            return redirect('lista_convidados')

        try:
            maximo_acompanhantes = int(maximo_acompanhantes_str)
        except ValueError:
            messages.error(request, "Máximo de acompanhantes precisa ser número.")
            return redirect('lista_convidados')

        convidado = Convidados(
            nome_convidado=nome_convidado,
            whatsapp=whatsapp,
            maximo_acompanhantes=maximo_acompanhantes
)
        convidado.save()

        messages.success(request, "Convidado adicionado com sucesso!")
        return redirect('lista_convidados')

def responder_presenca(request):
    resposta = request.GET.get('resposta')
    token = request.GET.get('token')

    convidado, erro = get_convidado_por_token(request)
    if erro:
        messages.error(request, erro)
        return redirect('lista_convidados')
    if resposta not in ['C', 'R']:
        messages.error(request, 'Confirmação inválida.')
        return redirect(f"{reverse('convidados')}?token={token}")

    if convidado.status in ['C', 'R']:
        messages.info(request, "Você já respondeu.")
        return redirect(f"{reverse('convidados')}?token={token}")

    convidado.status = resposta
    convidado.save()

    messages.success(request, "Sua resposta foi registrada.")
    return redirect(f"{reverse('convidados')}?token={token}")

def reservar_presente(request, id):
    token = request.GET.get('token')

    if not token:
        messages.error(request, "Token não informado.")
        return redirect('lista_convidados')

    try:
        convidado = Convidados.objects.get(token=token)
    except Convidados.DoesNotExist:
        messages.error(request, "Convidado não encontrado.")
        return redirect('lista_convidados')

    try:
        presente = Presentes.objects.get(id=id)
    except Presentes.DoesNotExist:
        messages.error(request, "Presente não encontrado.")
        return redirect(f"{reverse('convidados')}?token={token}")

    presente.reservado = True
    presente.reservado_por = convidado
    presente.save()

    messages.success(request, f"Presente reservado: {presente.nome_presente}")
    return redirect(f"{reverse('convidados')}?token={token}")
