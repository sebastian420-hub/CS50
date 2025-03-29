import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
import json
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import ensure_csrf_cookie
from .models import POST_CATEGORIES, User, Post, Following, Comment

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

class PostForm(forms.Form):
    post = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'placeholder': "What's on your mind?",
            'class': 'form-control',
            'id': 'uploadTextArea',
            'rows': 3
        })
    )


#API 

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"success": False, "error": "User not authenticated"}, status=403)
    
    if request.method == "POST":
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)  # Unlike
        else:
            post.likes.add(user)  # Like
        return JsonResponse({"success": True, "likes": post.likes.count()})
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

def fetch_profile_posts(request, username):
    posts = Post.objects.filter(user=username)
    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def upload_post(request):
    if request.method == "POST":
        post_text = request.POST.get('post')
        print(post_text)
        image = request.FILES.get('image')
        category = request.POST.get('category')
        link = request.POST.get('link')

        
        if not post_text:
            return JsonResponse({"success": False, "error": "Post text cannot be empty"}, status=400)
        
        
        post = Post.objects.create(
            user=request.user,
            post=post_text,
            image=image if image else None,
            category=category if category else None,
            link=link if link else None 
        )
        return JsonResponse({
            "success": True,
            "post": post.serialize()
        })
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)


# def upload_artwork(request):
#     if request.method == "POST":
#         post_content = request.POST.get('post')
#         image = request.FILES.get('image')
#         category = request.POST.get('category') 
#         print(category)
#         link = request.POST.get('link') 
        
        
#         if not image:
#             return JsonResponse({"success": False, "error": "Image cannot be empty"}, status=400)
        
        
#         post = Post.objects.create(
#             user=request.user,
#             post=post_content,
#             image=image,
#             category=category,
#             link=link if link else ''
#         )
#         return JsonResponse({
#             "success": True,
#             "post": post.serialize()
#         })
#     return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)


@login_required
def load_posts(request,category):
    
    if category:
            posts = Post.objects.filter(category=category).order_by('-timestamp')
            return JsonResponse([post.serialize() for post in posts], safe=False)
    else:
        posts = Post.objects.filter(category=category).order_by('-timestamp')
        
    return JsonResponse([post.serialize() for post in posts], safe=False)

page_number = 0    
@ensure_csrf_cookie
def view_allposts(request,page):
    print(page)
    allposts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(allposts, 10)
    page_obj = paginator.get_page(page)
    print(page_obj)

    time.sleep(1)

    if page <= paginator.num_pages:
         return JsonResponse(
            {
                'posts': [post.serialize() for post in page_obj],
                'has_next': page_obj.has_next(),
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None
            })
    else:
        return JsonResponse({
            'error': 'Page not found'
        }, status=404)


    


def get_comment(request, id):
    try:
        post = Post.objects.get(pk=id)
        comments = post.comments.all()
        
        serialized_comments = [comment.serialize() for comment in comments]
        
        return JsonResponse(serialized_comments, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({
            'status': 'Post Not Found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'Error',
            'message': str(e)
        }, status=500)
    
@csrf_exempt
def upload_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        comment = Comment.objects.create(
            post=post,
            user=user,
            comment=comment_text
        )
        return JsonResponse({
            "success": True,
            "comment": {
                "id": comment.id,
                "text": comment.comment,
                "username": user.username,
                "created_at": comment.created.strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)

#####

# def index(request):
#     allposts = Post.objects.all()
#     allposts = allposts.order_by("-timestamp").all()
#     return render(request, "network/index.html", {
#         'form': PostForm(),
    
#     })

def index(request):
    return render(request, 'network/index.html')

def artworks(request):
    return render(request, "network/artworks.html")

def view_func(request):
    context = {
        'urls': {
            'upload_comment': reverse('upload_comment', args=['__id__']),
        }
    }
    return render(request, 'index.html', context)

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    followings = Following.objects.filter(following=user)
    followers = Following.objects.filter(followers=user)
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        'form': PostForm(),
        'followings': followings,
        'followers': followers
    })



def follow(request, username):
    user = request.user
    followed_user = User.objects.get(username=username)
    follow = Following.objects.create(
        user = user,
        followed_user = followed_user
    )
    follow.save()
    return HttpResponseRedirect(reverse("index"))



def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
