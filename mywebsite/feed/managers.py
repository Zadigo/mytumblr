from django.db.models import QuerySet
from django.db.models.expressions import Q, Case, When, F
from django.db.models import BooleanField


class VideosManager(QuerySet):
    def public_videos(self):
        return self.filter(public=True, visible=True)

    def search(self, q):
        logic = (
            Q(caption__icontains=q) |
            Q(user__username__icontains=q) |
            Q(tags__title__icontains=q)
        )
        return self.public_videos().filter(logic).distinct()

    def timeline(self, follows_ids):
        return self.filter(created_by__id__in=follows_ids)

    def annotated_videos(self, username, follows_ids=None, queryset=None):
        user_in_likes = When(like__user__username=username, then=True)
        cases = Case(user_in_likes, default=False, output_field=BooleanField())
        if queryset:
            return queryset.annotate(has_liked=cases)
        return self.timeline(follows_ids).annotate(has_liked=cases)
        
    def all_annotated_videos(self, username, follows_ids):
        user_in_likes = When(like__user__username=username, then=True)
        cases_for_likes = Case(user_in_likes, default=False, output_field=BooleanField())

        follows_user = When(user__id__in=follows_ids, then=True)
        cases_for_follows = Case(follows_user, default=False, output_field=BooleanField())

        return self.public_videos().annotate(has_liked=cases_for_likes, follows_user=cases_for_follows)
        