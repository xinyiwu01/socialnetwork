from django.contrib.postgres import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout

from socialnetwork.forms import *

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm
from socialnetwork.models import Profile

import json


@login_required
def global_action(request):
    post = Post.objects.all().order_by("creation_time").reverse()
    context = {'posts': post}
    if request.method == 'GET':
        return render(request, 'socialnetwork/global.html', context)

    if 'text' not in request.POST or not request.POST['text']:
        return render(request,'socialnetwork/global.html', {'message': "You must enter some text to post."})

    new_post = Post(text=request.POST['text'], user=request.user, creation_time=timezone.now())
    new_post.save()
    post = Post.objects.all().order_by("creation_time").reverse()
    context = {'posts': post}
    return render(request, 'socialnetwork/global.html', context)

@login_required
def myprofile_action(request):
    if request.method == 'GET':
        context = {'profile': request.user.profile,
                   'form': ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/myprofile.html', context)

    form = ProfileForm(request.POST, request.FILES)
    if not form.is_valid():
        context = {'profile':request.user.profile, 'form':form}
        return render(request, 'socialnetwork/myprofile.html', context)

    profile = get_object_or_404(Profile, id=request.user.id)

    pic = form.cleaned_data['picture']
    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))

    profile.picture = form.cleaned_data['picture']
    profile.content_type = form.cleaned_data['picture'].content_type
    profile.bio = form.cleaned_data['bio']
    profile.save()


    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'socialnetwork/myprofile.html', context)

@login_required
def otherprofile_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'socialnetwork/otherprofile.html', {'profile': user.profile})

@login_required
def unfollow_action(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    # no context to return, so use redirect instead of render
    return redirect(reverse('other', kwargs={'user_id': user_id}))


@login_required
def follow_action(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return redirect(reverse('other', kwargs={'user_id': user_id}))


@login_required
def follower_action(request):
    post = Post.objects.all().order_by("creation_time").reverse()
    context = {'posts': post}
    return render(request, 'socialnetwork/follower.html', context)

@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, profile.picture, type(profile.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.picture:
        raise Http404

    return HttpResponse(profile.picture, content_type=profile.content_type)



def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    profile = Profile(bio="default bio", user=new_user)
    profile.save()
    new_user.profile = profile

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])


    login(request, new_user)
    return redirect(reverse('global'))



def get_global_json_dumps_serializer(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    posts = []
    for model_item in Post.objects.all():
        my_item = {
            'id': model_item.id,
            'text': model_item.text,
            'first_name': model_item.user.first_name,
            'last_name':model_item.user.last_name,
            'user_id':model_item.user_id,
            'creation_time': str(model_item.creation_time),
        }
        posts.append(my_item)

    comments= []
    for model_item in Comment.objects.all():
        my_item = {
            'id': model_item.id,
            'comment_text': model_item.comment_text,
            'first_name': model_item.user.first_name,
            'last_name':model_item.user.last_name,
            'user_id':model_item.user.id,
            'post_id':model_item.post.id,
            'creation_time': str(model_item.creation_time),
        }
        comments.append(my_item)

    response_data={}
    response_data['posts'] = posts
    response_data['comments'] = comments
    print(response_data)

    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    return response

def get_follower_json_dumps_serializer(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    posts = []
    for model_item in Post.objects.all():
        if model_item.user in request.user.profile.following.all():
            my_item = {
                'id': model_item.id,
                'text': model_item.text,
                'first_name': model_item.user.first_name,
                'last_name':model_item.user.last_name,
                'user_id':model_item.user_id,
                'creation_time': str(model_item.creation_time),
            }
            posts.append(my_item)

    comments= []
    for model_item in Comment.objects.all():
        if model_item.post.user in request.user.profile.following.all():
            my_item = {
                'id': model_item.id,
                'comment_text': model_item.comment_text,
                'first_name': model_item.user.first_name,
                'last_name':model_item.user.last_name,
                'user_id':model_item.user.id,
                'post_id':model_item.post.id,
                'creation_time': str(model_item.creation_time),
            }
            comments.append(my_item)

    response_data={}
    response_data['posts'] = posts
    response_data['comments'] = comments
    print(response_data)

    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    return response


def add_comment(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an comment to add.", status=400)

    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("post id missing.", status=400)

    if request.POST['post_id'].isnumeric()==False:
        return _my_json_error_response("post id is not numeric.", status=400)

    number = Post.objects.count()
    if int(request.POST['post_id']) > number:
        return _my_json_error_response("You must enter an comment to add.", status=400)


    new_comment = Comment(comment_text=request.POST['comment_text'], user=request.user,
                       creation_time=timezone.now(), post_id=request.POST['post_id'])
    new_comment.save()

    return get_global_json_dumps_serializer(request)


def add_comment_follower(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an comment to add.", status=400)

    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("post id missing.", status=400)

    if request.POST['post_id'].isnumeric()==False:
        return _my_json_error_response("post id is not numeric.", status=400)

    new_comment = Comment(comment_text=request.POST['comment_text'], user=request.user,
                          creation_time=timezone.now(), post_id=request.POST['post_id'])
    new_comment.save()

    return get_follower_json_dumps_serializer(request)

# def get_global_django_serializer(request):
#     all_objects = {'posts':Post.objects.all(),'comments':Comment.objects.all()}
#     response_json = serializers.serialize('json', all_objects)
#     return HttpResponse(response_json, content_type='application/json')


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

