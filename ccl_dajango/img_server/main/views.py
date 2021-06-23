from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post, Image


def blog_view(request):
    posts = Post.objects.all()

    return render(request, 'blog.html', {'posts':posts})

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = Image.objects.filter(post=post)
    return render(request, 'detail.html',{
        'post': post,
        'photos': photos
    })