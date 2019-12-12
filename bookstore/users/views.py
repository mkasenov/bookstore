from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy

class Register(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('blog-Home')
    template_name = 'users/registration.html'
