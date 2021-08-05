from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.storage import FileSystemStorage
from .models import Client, Video
from .forms import VideoForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request): 
    if request.user.is_authenticated():
        context = {
            'clients': Client.objects.all()
        }
        return render(request, 'page/home.html', context)
    else:
        return redirect('login')

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'page/home.html'
    context_object_name = 'clients'
    ordering = ['first_name']

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/client.html'

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/create_client.html'
    context_object_name = 'clients'

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/update_client.html'
    context_object_name = 'clients'

    def form_valid(self, form):
        form.instance.client_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.id:
            return True
        return True

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = '/'
    template_name = 'page/delete_client.html'
    context_object_name = 'clients'
    # ordering = ['creation_date']

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.id:
            return True
        return False

class ClientAnalysisView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/client_analysis.html'

class ClientVideosView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/client_videos.html'

class ClientUploadView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/upload_video.html'


    def post(self, request, pk):
        form = VideoForm(request.POST, request.FILES)
        context = {
            'clients': Client.objects.all()
        }
        if form.is_valid():
            title = form.cleaned_data['title']
            video = form.cleaned_data['video']
            form.save()
            context = {
                'all_videos': Video.objects.all(),
                'clients': Client.objects.all(),
            }
            render(request, 'page/client.html', context)
            return redirect('page/client.html', pk=pk)
        all_videos = Video.objects.all()
        return render(request, 'page/home.html', context)


def display(request):

    videos = Video.objects.all()
    context = {
        'videos': videos,
    }
                
    return render(request, 'client_videos.html', context)


def pdf_view(request):
    fs = FileSystemStorage()
    filename = 'analysis.pdf'
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition']='attachment; filename="anaysis.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in the server.')