from django.shortcuts import render # noqa
from django.views import View # noqa    
from django.contrib.auth.mixins import LoginRequiredMixin # noqa


class IndexView(LoginRequiredMixin, View):
    template_name = 'feeds/index.html'

    def get(self, request):
        return render(request, self.template_name)
