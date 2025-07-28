import secrets
from django.db import models
from django.urls import reverse

class Convidados(models.Model):
    status_choices = (
        ('AC', 'Aguardando confirmação'),
        ('C', 'Confirmado'),
        ('R', 'Recusado'),
)

    nome_convidado = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=25, null=True, blank=True)
    maximo_acompanhantes = models.PositiveIntegerField(default=0)
    token = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=2, choices=status_choices, default='AC')

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(16)
        super(Convidados, self).save(*args, **kwargs)

    @property
    def link_convite(self):
        return f'http://127.0.0.1:8000{reverse("convidados")}?token={self.token}'

    def __str__(self):
        return self.nome_convidado

class Acompanhante(models.Model):
    nome = models.CharField(max_length=100)
    convidado = models.ForeignKey(Convidados, on_delete=models.CASCADE, related_name='acompanhantes')

    def __str__(self):
        return self.nome
