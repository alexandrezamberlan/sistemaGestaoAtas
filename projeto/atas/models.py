from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from utils.gerador_hash import gerar_hash
    
class Ata(models.Model):
    codigo = models.CharField(_('Código da ata *'), unique=True, max_length=20, help_text='* Campos obrigatórios')
    data = models.DateField(_('Data da reunião *'), max_length=11, help_text='dd/mm/aaaa')
    hora = models.CharField(_('Hora da reunião *'), max_length=5, help_text='hh:mm')
    local = models.CharField(_('Local da reunião *'), max_length=50)
    pauta = models.TextField(_('Pauta da reunião'), max_length=200)
    redator = models.ForeignKey('usuario.Usuario', null=True, blank=True, verbose_name= 'Redator *', on_delete=models.PROTECT,related_name='redator')
    texto = models.TextField(_('Texto da reunião'), null=True, blank=True, max_length=10000)
    validada = models.BooleanField(_('Ata validada? '), default=False, null=True, blank=True)
    integrantes = models.ManyToManyField('usuario.Usuario', verbose_name='Integrantes', null=True, blank=True, related_name='integrantes')
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['codigo','-data','-hora']
        verbose_name        =   ('ata')
        verbose_name_plural =   ('atas')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "%s: %s. Curso: %s" % (self.codigo, self.data, self.hora)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.codigo = self.codigo.upper()
        super(Ata, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('ata_update', args=[str(self.id)])

    @property
    def get_delete_url(self):
        return reverse('ata_delete', args=[str(self.id)])