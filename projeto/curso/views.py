from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin, SecretariaRequiredMixin

from .forms import CursoForm

from .models import Curso


class CursoListView(LoginRequiredMixin, SecretariaRequiredMixin, ListView):
    model = Curso


class CursoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    success_url = 'curso_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Curso cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class CursoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = 'curso_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Dados do curso atualizados com sucesso na plataforma!')
        return reverse(self.success_url) 


class CursoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Curso
    success_url = 'curso_list'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse curso, permissão negada!')
        return redirect(self.success_url)