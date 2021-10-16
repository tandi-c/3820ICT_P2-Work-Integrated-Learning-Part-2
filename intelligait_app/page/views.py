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



# Checks if user is authenticated
# Sends all clients to home view
# Displays the home view
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



# Sends all clients created by user to client list view
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'page/home.html'
    context_object_name = 'clients'
    ordering = ['first_name']

    # Add in Queryset of all clients filtered by user id
    def get_context_data(self):
        context = {
            'clients': Client.objects.filter(user_id=self.request.user.id)
        }
        return context



# Sends client details and video details to client detail view
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/client.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get context
        context = super().get_context_data(**kwargs)
        
        # Get client object
        client = self.get_object()

        # Add in a QuerySet of all the videos filtered by client_id
        context['videos'] = Video.objects.filter(client_id=client)
        return context



# Sends client object and video object to video view
class ClientVideoView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/video_modal.html'

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get context
        context = super().get_context_data(*args, **kwargs)

        # Get client object
        client = self.get_object()

        # Add in a QuerySet of the video filtered by client_id and video pk
        video_pk = self.kwargs.get('video_pk', None)
        context['video'] = Video.objects.get(client_id=client, id=video_pk)
        return context



# Sends client object and pose video object to pose video view
class ClientPoseVideoView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/pose_video_modal.html'

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get context
        context = super().get_context_data(*args, **kwargs)

        # Get client object
        client = self.get_object()

        # Add in a QuerySet of the video filtered by client_id and video pk
        video_pk = self.kwargs.get('video_pk', None)
        context['video'] = Video.objects.get(client_id=client, id=video_pk)

        return context



# Sends all videos of that client to the video list view
class VideoListView(LoginRequiredMixin, ListView):

    # Add in a QuerySet of the video filtered by client_id and video pk
    def get_queryset(self, *args, **kwargs):
        qs = Video.objects.all()
        return qs

    # Call base implementation to obtain context data for client videos
    def get_context_data(self, *args, **kwargs):
        context = super(VideoListView, self).get_context_data(*args, **kwargs)
        return context 



# Displays create client form
# Validates create client form
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/create_client.html'
    context_object_name = 'clients'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)



# Displays update client form
# Validates update client form
class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    fields = ['first_name', 'last_name', 'notes']
    template_name = 'page/update_client.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the client
        context = {
            'client': self.get_object(),
        }
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.id:
            return True
        return True



# Displays delete client confirmation form
# Deletes client object
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = '/'
    template_name = 'page/delete_client.html'
    context_object_name = 'clients'

    def test_func(self):
        client = self.get_object()
        if self.request.user == client.id:
            return True
        return False



# Displays video upload form
# Creates instance of video associated with client
# Uploads and analyses video
class ClientUploadView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'page/upload_video.html'

    context = {
        'clients': Client.objects.all()
    }

    # Video upload 
    # Saves video to client model instance
    def post(self, request, pk):
        # Grab form fields
        form = VideoForm(request.POST, request.FILES)
        
        if request.method == 'POST' and form.is_valid(): 
            # Assign form fields to objects
            client = Client.objects.get(pk=pk)
            title = request.POST.get('title')
            video = request.FILES.get('video')
            
            # Update client information
            client.num_analyses += 1
            client.num_videos += 1
            client.save()

            # Save video into database
            form.save()

            # Grab last video saved to perform analysis and create pose video path
            video_path = str(Video.objects.filter(title=title).last())
            pose_video_path = video_path.split('.', 1)
            pose_video_path = pose_video_path[0]
            pose_video_path = pose_video_path.replace("\\", "/")

            # Run the pose estimation and analysis module 
            pdf_path = main.main(video_path, title) 

            # Save analysis pdf to video object
            video = Video.objects.last()
            video.analysis = pdf_path
            video.analysis_title = title + ".pdf"
            skeleton_video_path = str(video).split('.', 1)
            skeleton_video_path = str(skeleton_video_path[0]).split('/')
            video.skeleton_video = "videos/" + skeleton_video_path[-1] + "_pose_estimation.mp4"
            
            # Save video
            video.save(force_update=True)

            # Return client and videos objects to client view
            context = {
                'client': Client.objects.get(pk=pk), 
                'videos': {Video.objects.filter(client_id=client)},
            }

            return HttpResponseRedirect(reverse('client', kwargs={'pk': pk}), context)
        
        # If not post request then send client and videos objects to client view
        client = Client.objects.get(pk=pk)
        context = {
            'client': Client.objects.get(pk=pk), 
            'videos': Video.objects.get(client_id=client),
        }

        return HttpResponseRedirect(reverse('client', kwargs={'pk': pk}), context)



# Displays pdf in browser for viewing or saving
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