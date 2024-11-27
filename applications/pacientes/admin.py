from django.contrib import admin

from applications.pacientes.models import Pacientes
import csv
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from applications.home.forms import *
from django.http import HttpResponse
from applications.home.utils import exportar_a_csv



class OpacientesAdmin(admin.ModelAdmin):
    actions = [exportar_a_csv]
    list_display = [field.name for field in Pacientes._meta.fields]  
    list_display_links = ['id']  



admin.site.register(Pacientes,OpacientesAdmin)















