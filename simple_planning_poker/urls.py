"""
URL configuration for simple_planning_poker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from simple_planning_poker.views.empty import EmptyView
from simple_planning_poker.views.health import health_check
from simple_planning_poker.views.login import CustomAuthToken
from simple_planning_poker.views.logout import LogoutView
from simple_planning_poker.views.register import RegisterView
from simple_planning_poker.views.guestlogin import GuestLoginView
from simple_planning_poker.views.roomget import RoomGetByCodeView
from simple_planning_poker.views.userprofileupdate import UserProfileUpdateView
from simple_planning_poker.views.votecreate import VoteCreateView
from simple_planning_poker.views.voteget import VoteGetByStoryView
from simple_planning_poker.views.roomjoin import RoomJoinByCodeView
from simple_planning_poker.views.storydelete import StoryDeleteView
from simple_planning_poker.views.storycreate import StoryCreateView
from simple_planning_poker.views.votedelete import VoteDeleteByStoryView
from simple_planning_poker.views.roomlistcreate import RoomListCreateView
from simple_planning_poker.views.userget import UserGetByTokenView, UserGetByIdView
from simple_planning_poker.views.storyget import StoryGetByIdView, StoryGetByRoomView

urlpatterns = [
    # path('', include('simple_planning_poker.urls')),
    path('admin/', admin.site.urls),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('auth/guestlogin/', GuestLoginView.as_view(), name='guest-login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api/rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('api/rooms/<str:code>/', RoomGetByCodeView.as_view(), name='get-room'),
    path('api/rooms/<str:code>/join/', RoomJoinByCodeView.as_view(), name='join-room'),
    path('api/stories/', StoryCreateView.as_view(), name='story-create'),
    path('api/stories/<int:room_id>/', StoryGetByRoomView.as_view(), name='story-get-by-room'),
    path('api/stories/<int:pk>/getstory/', StoryGetByIdView.as_view(), name='story-get-by-id'),
    path('api/stories/<int:pk>/delete/', StoryDeleteView.as_view(), name='story-delete'),
    path('api/votes/', VoteCreateView.as_view(), name='vote-create'),
    path('api/votes/<int:story_id>/', VoteGetByStoryView.as_view(), name='vote-get'),
    path('api/votes/<int:story_id>/delete/', VoteDeleteByStoryView.as_view(), name='vote-delete'),
    path('api/userinfo/', UserGetByTokenView.as_view(), name='user-info-by-token'),
    path('api/userinfo/<int:user_id>/', UserGetByIdView.as_view(), name='user-info-by-id'),
    path('api/empty/', EmptyView.as_view(), name='empty-view'),
    path('api/profile/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('health/', health_check),
]
