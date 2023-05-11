from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Photo, Like
from django.contrib.auth.decorators import login_required


'''Like and Follow'''
@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    user = request.user
    try:
        Like.objects.get(user=user, photo=photo).delete()
    except Like.DoesNotExist:
        Like.objects.create(user=user, photo=photo)
    return redirect('photo_detail', pk=photo.pk)

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(get_user_model(), id=user_id)
    request.user.following.add(user_to_follow)
    return redirect('user_profile', pk=user_id)


class PhotoListView(ListView):
    model = Photo     
    template_name = 'photoapp/list.html'
    context_object_name = 'photos'

class PhotoTagListView(PhotoListView):
    template_name = 'photoapp/taglist.html'

    # Custom method
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context
    

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['title', 'description', 'image', 'tags']
    template_name = 'photoapp/create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        return super().form_valid(form)
    
class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')
        
class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    fields = ['title', 'description', 'tags']
    success_url = reverse_lazy('photo:list')

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')

