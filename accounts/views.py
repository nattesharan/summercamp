from django.views.generic import TemplateView
from django.shortcuts import render

class UserLoginView(TemplateView):
    template_name = 'accounts/login.html'
    def get(self, request):
        return render(request, self.template_name)