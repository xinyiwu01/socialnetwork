from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_action, name='global'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('myprofile', views.myprofile_action,name='myprofile'),
    path('follower', views.follower_action, name='follower'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('otherprofile/<int:user_id>', views.otherprofile_action, name='other'),
    path('unfollow/<int:user_id>', views.unfollow_action, name='unfollow'),
    path('follow/<int:user_id>', views.follow_action, name='follow'),
    path('get-global', views.get_global_json_dumps_serializer),
    # path('get-global-django-serializer', views.get_global_django_serializer),
    path('add-comment', views.add_comment, name='add-comment'),
    path('add-comment-follower', views.add_comment_follower, name='add-comment-follower'),
    path('get-follower', views.get_follower_json_dumps_serializer),
    # !! make urls different (the first parameter in path() )
    # One url can't be associated with different action function, otherwise it doesn't know which function
    # to call when loading the url. But an action function can be associated with different urls.
]

