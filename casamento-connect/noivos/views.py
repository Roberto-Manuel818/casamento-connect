from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from convidados.models import Convidados
from.models import Presentes

def home(request):
    token = request.GET.get('token', '').strip() if request.method == 'GET' else request.POST.get('token', '').strip()

    if request.method == 'GET':
        # Filtra apenas presentes com preço válido
        presentes_validos = []
        for presente in Presentes.objects.all():
            try:
                preco_validado = Decimal(presente.preco)
                presentes_validos.append(presente)
            except (InvalidOperation, TypeError):
                continue

        data = {
            "reservado": Presentes.objects.filter(reservado=True).count(),
            "nao_reservado": Presentes.objects.filter(reservado=False).count()
}

        return render(request, 'noivos/home.html', {
            'presentes': presentes_validos,
            'data': data,
            'token': token
})

    elif request.method == 'POST':
        nome_presente = request.POST.get('nome_presente', '').strip()
        foto = request.FILES.get('foto')
        preco_str = request.POST.get('preco', '').strip()
        importancia_str = request.POST.get('importancia', '').strip()

        # Validação de campos obrigatórios
        if not nome_presente or not preco_str or not importancia_str:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect(f'{request.path}?token={token}')

        # Validação do preço
        try:
            preco = Decimal(preco_str)
        except InvalidOperation:
            messages.error(request, "O campo 'Preço' deve conter um número válido.")
            return redirect(f'{request.path}?token={token}')

        # Validação da importância
        try:
            importancia = int(importancia_str)
            if not (1 <= importancia <= 5):
                raise ValueError("Importância fora do intervalo permitido.")
        except ValueError:
            messages.error(request, "A importância deve ser um número entre 1 e 5.")
            return redirect(f'{request.path}?token={token}')

        # Criação do presente
        presente = Presentes(
            nome_presente=nome_presente,
            foto=foto,
            preco=preco,
            importancia=importancia,
            reservado=True
)

        convidado = Convidados.objects.filter(token=token).first()
        if convidado:
            presente.reservado_por = convidado
            redirecionamento = convidado.link_convite
        else:
            messages.warning(request, "Convidado não encontrado. O presente será salvo sem vínculo.")
            redirecionamento = f'{request.path}?token={token}'

        presente.save()
        messages.success(request, "Presente adicionado com sucesso!")

        return redirect(redirecionamento)
