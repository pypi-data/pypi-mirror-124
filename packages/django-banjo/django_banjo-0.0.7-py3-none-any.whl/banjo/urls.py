from django.urls import path
from django.http import JsonResponse, HttpResponseNotAllowed
from banjo import http
import json

urlpatterns = []

def get_request_params(request):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return json.loads(request.body.decode("utf-8"))
    elif content_type == 'application/x-www-form-urlencoded':
        if request.method == "GET":
            return request.GET
        elif request.method == "POST":
            return request.POST

def create_view(fn, method):
    def view(request):
        if request.method == method:
            params = get_request_params(request)
            try:
                result = fn(params)
                return JsonResponse(result)
            except http.BadRequest as e:
                return JsonResponse({'error': str(e)}, status=e.status_code)
        else:
            return HttpResponseNotAllowed([method])  
    return view

def route_get(url):
    def bind_url_to_view(fn):
        view = create_view(fn, "GET")
        urlpatterns.append(path(url, view))
        return view
    return bind_url_to_view

def route_post(url):
    def bind_url_to_view(fn):
        view = create_view(fn, "POST")
        urlpatterns.append(path(url, view))
        return view
    return bind_url_to_view
