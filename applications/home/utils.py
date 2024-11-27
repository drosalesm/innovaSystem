from django.http import HttpResponse
import csv


def exportar_a_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registros.csv"'

    writer = csv.writer(response)
    campos = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(campos)

    for obj in queryset:
        row = [getattr(obj, field) for field in campos]
        writer.writerow(row)

    return response
exportar_a_csv.short_description = "Exportar a CSV"