from django import template
from django.shortcuts import reverse

register = template.Library()


LINKS = [
    ['home', {'name': 'Home'}],
    ['accounts:login', {'name': 'Login'}],
    ['accounts:signup', {'name': 'Signup'}]
]


AUTHENTICATED_LINKS = [
    ['feed:timeline', {'name': 'Timeline'}],
    ['accounts:profile:home', {'name': 'Profile'}],
    ['accounts:logout', {'name': 'Logout'}]
]

EXTRA = [

]


@register.inclusion_tag('project_components/navs/links/icon.html')
def icon_links(*urls):
    pass


@register.inclusion_tag('project_components/navs/text.html')
def text_links(request):
    links_to_use = LINKS

    if request.user.is_authenticated:
        links_to_use = AUTHENTICATED_LINKS

    if EXTRA:
        links_to_use += EXTRA

    for link in links_to_use:
        link[1]['href'] = reverse(link[0])

    # if request.user.is_authenticated:
    #     if request.user.is_admin:
    #         links_to_use.append(['/admin/', {'name': 'Admin'}])
    return {'links': links_to_use}
