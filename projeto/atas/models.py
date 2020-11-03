from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
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
    curso = models.ForeignKey('curso.Curso', verbose_name= 'Curso *', on_delete=models.PROTECT, related_name='curso')
    arquivo_anexo1 = models.FileField(_('Anexo à reunião'), null=True, blank=True, upload_to='midias', help_text='Se houver mais de um arquivo, sugere-se enviar o compactado')
    
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering            =   ['codigo','-data','-hora']
        verbose_name        =   ('ata')
        verbose_name_plural =   ('atas')
        unique_together     =   ['codigo', 'data', 'hora'] #criando chave primária composta no BD

    def __str__(self):
        return "Ata: %s. Data: %s." % (self.codigo, self.data)

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
    
    @property
    def get_visualiza_url(self):
        return reverse('ata_detail', args=[str(self.id)])
    

#triggers para limpeza dos arquivos apagados ou alterados. No Django é chamado de signals
#deleta o arquivo fisico ao excluir o item da pasta midias
@receiver(models.signals.post_delete, sender=Ata)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.arquivo_anexo1:
        if os.path.isfile(instance.arquivo_anexo1.path):
            os.remove(instance.arquivo_anexo1.path)

#deleta o arquivo fisico ao alterar o arquivo da pasta midia
@receiver(models.signals.pre_save, sender=Ata)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        obj = Ata.objects.get(pk=instance.pk)

        if not obj.arquivo_anexo1:
            return False

        old_file = obj.arquivo_anexo1
    except Ata.DoesNotExist:
        return False

    new_file = instance.arquivo_anexo1
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
