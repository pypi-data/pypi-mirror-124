from http import HTTPStatus
from requests import get

from django.http import HttpResponse
from django.shortcuts import render

from .utils import get_minimal_post, handle_error

# TODO: read API base URL from database
BASE_URL = 'https://narwhal.city/api/unstable'


def index(request):
    """Return default feed: all posts."""
    return render(request, 'index.html')


def timeline(request, timeline_type='all', page=None):
    """View timeline of posts.

    timeline_type: string
        either `all` or `local`

    page: string
        the page ID assigned by lotide
    """
    endpoint = f'{BASE_URL}/posts?limit=20'
    if timeline_type == 'local':
        endpoint += '&in_any_local_community=true'
    if page is not None:
        endpoint += f'&page={page}'
    response = get(endpoint)
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    json = response.json()
    posts = [get_minimal_post(post) for post in json['items']]
    next_page = json['next_page']
    return render(
        request, 'timeline.html',
        {'posts': posts,
         'timeline_type': timeline_type,
         'next_page': next_page})


def list_communities(request):
    """View list of communities."""
    response = get(f'{BASE_URL}/communities')
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    communities = response.json()['items']
    local = [community for community in communities
             if community['local']]
    remote = [community for community in communities
             if not community['local']]
    return render(
        request, 'communities.html',
        {'local': local, 'remote': remote})


def community(request, community_id, page=None):
    """View community and its posts."""
    community_response = get(f'{BASE_URL}/communities/{community_id}')
    if community_response.status_code != HTTPStatus.OK:
        return handle_error(community_response)
    timeline_url = f'{BASE_URL}/posts/?community={community_id}'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = get(timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)
    community = community_response.json()
    timeline_json = timeline_response.json()
    posts = [get_minimal_post(post) for post in timeline_json['items']]
    next_page = timeline_json['next_page']
    return render(
        request, 'community.html',
        {'community': community,
         'posts': posts,
         'timeline_type': 'community',
         'next_page': next_page})


def user(request, user_id, page=None):
    """View user and their posts."""
    user_response = get(f'{BASE_URL}/users/{user_id}')
    if user_response.status_code != HTTPStatus.OK:
        return handle_error(user_response)
    timeline_url = f'{BASE_URL}/users/{user_id}/things'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = get(timeline_url)
    if timeline_response.status_code != HTTPStatus.OK:
        return handle_error(timeline_response)
    user = user_response.json()
    timeline_json = timeline_response.json()
    items = timeline_json['items']
    next_page = timeline_json['next_page']
    return render(
        request, 'user.html',
        {'user': user,
         'items': items,
         'timeline_type': 'user',
         'next_page': next_page})


def post(request, post_id):
    """View post and its comment."""
    post_response = get(f'{BASE_URL}/posts/{post_id}')
    if post_response.status_code != HTTPStatus.OK:
        return handle_error(post_response)
    comment_response = get(f'{BASE_URL}/posts/{post_id}/replies')
    if comment_response.status_code != HTTPStatus.OK:
        return handle_error(comment_response)
    comment_json = comment_response.json()
    return render(
        request, 'post.html',
        {'post': post_response.json(),
         'comments': comment_json['items'],
         'next_page': comment_json['next_page']})
