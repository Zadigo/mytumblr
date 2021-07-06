import json
import re
import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator
from django.db import models, transaction
from django.db.models import Count
from django.db.models.expressions import F
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, View
from nltk.tokenize import TweetTokenizer
from notifications import choices as notification_choices
from notifications import models as notification_models

from feed import models

MYUSER = get_user_model()

def parse_users(text):
    has_users = re.match(r'\@([a-z]+)\s?', text)
    if has_users:
        users = has_users.groups()
        return MYUSER.objects.filter(username__in=list(users))
    return None


class TimeLineView(LoginRequiredMixin, ListView):
    model = models.Video
    template_name = 'pages/feed.html'
    context_object_name = 'videos'
    paginate_by = 100
    follows_ids = []

    def get_queryset(self):
        user = self.request.user
        follows_ids = list(user.myuserprofile.follows.values_list('id', flat=True))
        self.follows_ids = follows_ids
        return self.model.video_manager.all_annotated_videos(user.username, follows_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_users = cache.get('suggested_users')
        if not existing_users:
            suggested_users = MYUSER.objects.exclude(id__in=self.follows_ids)
            cache.set('suggested_users', suggested_users, 7200)
        context['suggested_users'] = cache.get('suggested_users')[:10]
        return context


def test_timeline(request):
    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 100)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'pages/test_feed.html', {'items': numbers})


@require_POST
def test_timeline_more(request):
    numbers_list = range(1, 1000)
    page = json.loads(request.body).get('page', 1)
    paginator = Paginator(numbers_list, 100)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return JsonResponse(data={'items': str(numbers)})


class CustomDetailView(DetailView):
    """
    Custom detail view that returns the user's profile
    """
    model = MYUSER
    queryset = MYUSER.objects.all()
    context_object_name = 'user_feed'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        username = self.kwargs.get('username')
        if username is not None:
            queryset = queryset.filter(username__iexact=username)
            try:
                user_timeline_to_view = queryset.get()
            except:
                raise Http404(f"The following user '{username}' could not be found")
            return user_timeline_to_view
        else:
            raise AttributeError('CustomDetailView should be called with a username in the url parameters')


class UserTimeLine(LoginRequiredMixin, CustomDetailView):
    template_name = 'pages/user_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_videos = user.video_set.all()
        context['likes'] = user_videos.aggregate(Count('like'))
        return context


class SearchView(LoginRequiredMixin, ListView):
    model = models.Video
    template_name = 'pages/search.html'
    context_object_name = 'videos'

    def get(self, request, *args, **kwargs):
        obj = super().get(request, *args, **kwargs)
        q = self.request.GET.get('q')
        models.Search.objects.create(
            user=request.user,
            terms=self.clean_text(q)
        )
        return obj

    def get_queryset(self):
        q = self.request.GET.get('q')
        return self.model.video_manager.search(q)

    @staticmethod
    def clean_text(items):
        return items.strip().lower()


@login_required
@require_POST
def follow_user(request, **kwargs):
    username = kwargs['username']
    if username is None:
        return JsonResponse(data={'state': False})
        
    user_to_follow = MYUSER.objects.get(username__iexact=username)
    current_user = MYUSER.objects.get(username__iexact=request.user.username)

    follows = current_user.myuserprofile.follows.all()
    if user_to_follow in follows:
        return JsonResponse(data={'state': False, 'reason': 'Followed'})
    current_user.myuserprofile.follows.add(user_to_follow.myuserprofile)

    notification_models.Notification.objects.create(
        user=user_to_follow,
        notification_type=notification_choices.NotificationTypes.FOLLOW
    )
    return JsonResponse(data={'state': True})


@login_required
@require_POST
def unfollow_user(request, **kwargs):
    username = kwargs['username']
    if username is None:
        return JsonResponse(data={'state': False})
    user_to_unfollow = MYUSER.objects.get(username__iexact=username)
    current_user = MYUSER.objects.get(username__iexact=request.user.username)
    current_user.myuserprofile.follows.remove(user_to_unfollow.myuserprofile)
    return JsonResponse(data={'state': True})


@login_required
@require_POST
def add_like(request):
    data = json.loads(request.body)
    method = data.get('method')
    if method is None:
        pass

    if method == 'comment':
        pass

    if method == 'video':
        pass

    try:
        video = models.Video.objects.get(id=data['id'])
    except:
        return JsonResponse(data={'state': False})

    likes = video.like_set.filter(user=request.user)
    if likes.exists():
        video.like_set.filter(user=request.user).delete()
    else:
        video.like_set.create(user=request.user)
        video.notification_set.create(
            user=request.user, 
            notification_type=notification_choices.NotificationTypes.LIKE
        )
    return JsonResponse(data={'state': True, 'total_likes': video.like_set.all().count()})


@login_required
@require_POST
def share(request):
    pass


@require_POST
@login_required
@transaction.atomic
def create_comment(request):
    data = {'state': False}
    text = request.POST.get('text')
    reference = request.POST.get('reference')

    if reference is not None:
        video = get_object_or_404(models.Video, reference=reference)
        comment = video.comment_set.create(user=request.user, text=text)
        comments = video.comment_set.values('user__username', 'id', 'text', 'in_reply_to', 'created_on')
        details = {
            'user__username': request.user.username,
            'id': comment.id,
            'text': comment.text,
            'in_reply_to': comment.in_reply_to,
            'created_on': comment.created_on,
            'liked': False
        }
        data.update({'state': True, 'comment': details, 'comments': list(comments)})

        tokenizer = TweetTokenizer()
        tokens = tokenizer.tokenize(text)

        raw_usernames = filter(lambda x: '@' in x, tokens)
        if raw_usernames:
            usernames = []
            for username in raw_usernames:
                _, name = username.split('@')
                if name != request.user.username:
                    usernames.append(name)

            username_objects = MYUSER.objects.filter(username__in=usernames)
            notifications = []
            for username_object in username_objects:
                notifications.append(
                    notification_models.Notification(
                        user=username_object,
                        comment=comment,
                        notification_type=notification_choices.NotificationTypes.MESSAGE
                    )
                )
            if notifications:
                video.notification_set.bulk_create(notifications)
    return JsonResponse(data=data)


@login_required
@require_POST
def delete(request):
    pass


@login_required
@require_POST
def embed(request):
    pass


@login_required
@require_POST
def report(request):
    video_id = json.loads(request.body)
    try:
        video = models.Video.objects.get(id=video_id['id'])
    except:
        return JsonResponse(data={'state': False})
    else:
        with transaction.atomic():
            if not video.reported:
                video.reported = True
            video.reports = F('reports') + 1

            try:
                video.save()
            except:
                transaction.rollback()
                return JsonResponse(data={'state': False})
        return JsonResponse(data={'state': True})


@login_required
@require_POST
def single_card_comments(request, **kwargs):
    reference = request.POST.get('reference')
    comments = []
    if reference is not None:
        video = get_object_or_404(models.Video, reference=reference)
        comments = video.comment_set.values('id', 'user__username', 'text', 'in_reply_to', 'created_on')
    return JsonResponse(data=list(comments), safe=False)
