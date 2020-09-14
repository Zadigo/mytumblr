import re
from string import Template

from django import template
from django.shortcuts import reverse
from django.utils.html import mark_safe
from nltk.tokenize import NLTKWordTokenizer, TweetTokenizer

register = template.Library()


def hashtags(tokens):
    new_tokens = []
    tag = Template("""<a href="$href" class="font-weight-bold" id="hashtag">$name</a>""")
    
    for token in tokens:
        if token.startswith('#'):
            value = re.match(r'\#(\w+)', token)
            if value:
                href = reverse('tags:tag', args=[value.group(1)])
                token = tag.substitute(href=href, name=token)
        new_tokens.append(token)
    return new_tokens


def shoutouts(tokens):
    new_tokens = []
    tag = Template("""<a href="$href" class="font-weight-bold" id="shoutout">$name</a>""")

    for token in tokens:
        if token.startswith('@'):
            value = re.match(r'\@(\w+)', token)
            if value:
                href = reverse('feed:user_timeline', args=[value.group(1)])
                token = tag.substitute(href=href, name=token)
        new_tokens.append(token)
    return new_tokens


@register.filter
def highlight(text):
    instance = TweetTokenizer()
    tokens = instance.tokenize(text)

    highlighted_caption = hashtags(shoutouts(tokens))
    return mark_safe(' '.join(highlighted_caption))
