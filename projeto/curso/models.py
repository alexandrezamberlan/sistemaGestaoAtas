from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash


class Curso(models.Model):
    #1 campo da tupla fica no banco de dados
    #2 campo da tupla eh mostrado para o usuario
    AREAS_CONHECIMENTO = (
        ('CIÊNCIAS DA SAÚDE', 'Ciências da Saúde'),
        ('CIÊNCIAS HUMANAS', 'Ciências Humanas' ),
        ('CIÊNCIAS SOCIAIS', 'Ciências Sociais'),
        ('CIÊNCIAS TECNOLÓGICAS', 'Ciências Tecnológicas' ),
    )

    nome = models.CharField(_('Nome do curso *'), unique=True, max_length=100, help_text='* Campos obrigatórios')
    area = models.CharField(_('Área de conhecimento do curso *'), max_length=25, choices=AREAS_CONHECIMENTO)
    email = models.EmailField(_('Email do curso'), max_length=100, db_index=True)
    coordenador = models.ForeignKey('usuario.Usuario', verbose_name= 'Coordenador *', on_delete=models.PROTECT, related_name='coordenador')
    is_active = models.BooleanField(_('Ativo'), default=True, help_text='Se ativo, o curso pode ser usado no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    
    class Meta:
        ordering            =   [u'nome']
        verbose_name        =   _(u'curso')
        verbose_name_plural =   _(u'cursos')

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()
        super(Curso, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('curso_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('curso_delete', args=[str(self.id)])
