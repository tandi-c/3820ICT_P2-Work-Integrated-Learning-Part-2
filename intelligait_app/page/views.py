from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound, FileResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.storage import FileSystemStorage
from .models import Client, Video
from .forms import VideoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tf_pose_estimation import main


@login_required
def home(request): 
    if request.user.is_authenticated():
        empty = False
        clients = Client.objects.all()
        if clients.count == 0:
            empty = True

        context = {
            'clients': Client.objects.all(),
            'empty': empty
        }
        return render(request, 'page/home.html', context)
    else:
        return redirect('login')

def search(request):
    if request.method('POST'):
        term = request.POST.get('search')
        print(term)

        return HttpResponseRedirect('home', term)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'page/home.html'
    context_object_name = 'clients'
    ordering = ['first_name']

    def post(self, request):
        if request.method == 'POST':
            term = request.POST.get('search')
            print(term)
            context = {
                'term': term,
            }
            print(context)

            return HttpResponseRedirect('', context)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/client.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        # Add in a QuerySet of all the books
        context['videos'] = Video.objects.filter(client_id=client)
        return context


class ClientVideoView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/video_modal.html'
    def get_context_data(self, *args, **kwargs):

        video_pk = self.kwargs.get('video_pk', None)

        context = super().get_context_data(*args, **kwargs)

        client = self.get_object()
        context['video'] = Video.objects.get(client_id=client, id=video_pk)
        return context


class ClientPoseVideoView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/pose_video_modal.html'
    def get_context_data(self, *args, **kwargs):

        video_pk = self.kwargs.get('video_pk', None)

        context = super().get_context_data(*args, **kwargs)

        client = self.get_object()
        context['video'] = Video.objects.get(client_id=client, id=video_pk)
        return context


class VideoListView(LoginRequiredMixin, ListView):

    def get_queryset(self, *args, **kwargs):
        qs = Video.objects.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(VideoListView, self).get_context_data(*args, **kwargs)
        return context 


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/create_client.html'
    context_object_name = 'clients'

    def form_valid(self, form):
        #form.instance.client_id = self.request.user.id 
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/update_client.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context = {
            'client': self.get_object(),
        }
        return context

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


class ClientUploadView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/upload_video.html'

    context = {
        'clients': Client.objects.all()
    }

    # Video upload 
    # Saves video to client model instance
    def post(self, request, pk):
        form = VideoForm(request.POST, request.FILES)
        
        if request.method == 'POST' and form.is_valid(): 
            client_id = request.POST.get('client_id')
            client = Client.objects.get(pk=pk)
            title = request.POST.get('title')
            video = request.FILES.get('video')
            
            client.num_analyses += 1
            client.num_videos += 1
            client.save()
            form.save()
            video_path = str(Video.objects.filter(title=title).last())
            pose_video_path = video_path.split('.', 1)
            pose_video_path = pose_video_path[0]
            pose_video_path = pose_video_path.replace("\\", "/")

            # This is what runs the pose estimation and analysis module 
            pdf_path = main.main(video_path, title) 
            video = Video.objects.last()
            video.analysis = pdf_path
            video.analysis_title = title + ".pdf"
            skeleton_video_path = str(video).split('.', 1)
            skeleton_video_path = str(skeleton_video_path[0]).split('\\')
            skeleton_video_path1 = "videos/" + skeleton_video_path[-1] 
            video.skeleton_video = skeleton_video_path1 + "_pose_estimation.mp4"
            video.save(force_update=True)

            context = {
                'client': Client.objects.get(pk=pk), 
                'videos': {Video.objects.filter(client_id=client)},
            }

            return HttpResponseRedirect(reverse('client', kwargs={'pk': pk}), context)
        
        client = Client.objects.get(pk=pk)
        context = {
            'client': Client.objects.get(pk=pk), 
            'videos': Video.objects.get(client_id=client),
        }

        return HttpResponseRedirect(reverse('client', kwargs={'pk': pk}), context)



class VideoDeleteView(LoginRequiredMixin, DeleteView):
    context = {
        'clients': Client.objects.all()
    }
    model = Video
    success_url = reverse_lazy('client', context)
    template_name = 'delete_video.html'


def pdf_view(request, *args, **kwargs):
    pdf_name = str(kwargs['path'])
    fs = FileSystemStorage()
    filename = 'analyses/' + pdf_name
    if fs.exists(filename):
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition']='attachment; filename="{}"'.format(pdf_name)
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in the server.')