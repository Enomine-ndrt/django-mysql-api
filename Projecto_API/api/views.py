from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Company
import json

# Create your views here.


class CompanyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id > 0):
            companies = list(Company.objects.filter(id=id).values())
            if len(companies) > 0:
                company = companies[0]
                datos = {'message': "Sucess", 'companies': company}
            else:
                datos = {'message': "Company not found..."}
            return JsonResponse(datos)
        else:
            companies = list(Company.objects.values())
            if len(companies) > 0:
                datos = {'message': "Sucess", 'companies': companies}
            else:
                datos = {'message': "Companies not found..."}
            return JsonResponse(datos)

    def post(self, request):
        # print('normal ', request.body)#json
        jd = json.loads(request.body)  # conversion a diccionario
        # print(jd)
        Company.objects.create(
            name=jd['name'], website=jd['website'], foundation=jd['foundation']
        )
        datos = {'message': "Sucess"}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)  # conversion a diccionario
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            company = Company.objects.get(id=id)
            company.name = jd['name']
            company.website = jd['website']
            company.foundation = jd['foundation']
            company.save()
            datos = {'message': "Sucess"}

        else:
            datos = {'message': "Company not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            Company.objects.filter(id=id).delete()
            datos = {'message': "Sucess"}
        else:
            datos = {'message': "Company not found..."}
        return JsonResponse(datos)
