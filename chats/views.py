from django.shortcuts import render
from .models import Mychats
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
# Create your views here.

@login_required
def chats(request):
    frnd_name = request.GET.get('user', None)
    mychats_data = None
    if frnd_name:
        if User.objects.filter(username=frnd_name).exists() and Mychats.objects.filter(me=request.user, frnd=User.objects.get(username=frnd_name)).exists():
            frnd_ = User.objects.get(username=frnd_name)
            mychats_data = Mychats.objects.get(me=request.user, frnd=frnd_).chats
        return render(request, 'chat/chats.html', {'my': mychats_data, 'chats': mychats_data, 'frnd_name': frnd_name})
    frnds = User.objects.exclude(pk=request.user.id)
    my_convo = Mychats.objects.filter(me=request.user)
    for i in my_convo:
        print(i.frnd)
    return render(request, 'chat/inbox.html', {'my': mychats_data, 'chats': mychats_data, 'frnds': frnds, 'frnd_name': frnd_name, 'my_convo': my_convo})
