from http import HTTPStatus

import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .utils import get_minimal_post, handle_error

# TODO: read API base URL from database
BASE_URL = 'https://%s/api/unstable'


def index(request):
    """Return default feed: all posts."""
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    if instance is None:
        return render(request, 'index.html', {'luna_theme': theme})
    return redirect('timeline', 'home')


def timeline(request, timeline_type='all', page=None):
    """View timeline of posts.

    timeline_type: string
        `all`: all posts from local and connected instances
        `local`: only posts from local instance
        `home`: posts from communities the user follow

    page: string
        the page ID assigned by lotide
    """
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    token = request.COOKIES.get('token')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    endpoint = f'{BASE_URL % instance}/posts?limit=20'
    if timeline_type == 'local':
        endpoint += '&in_any_local_community=true'
    elif timeline_type == 'home':
        endpoint += '&include_your_follow=true'
    if page is not None:
        endpoint += f'&page={page}'
    response = requests.get(
        endpoint, headers={'Authorization': f'Bearer {token}'})
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    json = response.json()
    posts = [get_minimal_post(post) for post in json['items']]
    next_page = json['next_page']
    return render(
        request, 'timeline.html',
        {'posts': posts,
         'timeline_type': timeline_type,
         'logged_in': {'name': username, 'id': user_id},
         'luna_theme': theme,
         'next_page': next_page})


def list_communities(request):
    """View list of communities."""
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    response = requests.get(
        f'{BASE_URL % instance}/communities')
    if response.status_code != HTTPStatus.OK:
        return handle_error(response)
    communities = response.json()['items']
    local = [community for community in communities
             if community['local']]
    remote = [community for community in communities
              if not community['local']]
    return render(
        request, 'communities.html',
        {'local': local,
         'logged_in': {'name': username, 'id': user_id},
         'luna_theme': theme,
         'remote': remote})


def community(request, community_id, page=None):
    """View community and its posts."""
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    community_response = requests.get(
        f'{BASE_URL % instance}/communities/{community_id}')
    if community_response.status_code != HTTPStatus.OK:
        return handle_error(community_response)
    timeline_url = f'{BASE_URL % instance}/posts/?community={community_id}'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = requests.get(timeline_url)
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
         'logged_in': {'name': username, 'id': user_id},
         'luna_theme': theme,
         'next_page': next_page})


def user(request, user_id, page=None):
    """View user and their posts."""
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    username = request.COOKIES.get('username')
    current_user_id = request.COOKIES.get('user_id')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    user_response = requests.get(f'{BASE_URL % instance}/users/{user_id}')
    if user_response.status_code != HTTPStatus.OK:
        return handle_error(user_response)
    timeline_url = f'{BASE_URL % instance}/users/{user_id}/things'
    if page is not None:
        timeline_url += f'&page={page}'
    timeline_response = requests.get(timeline_url)
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
         'logged_in': {'name': username, 'id': current_user_id},
         'luna_theme': theme,
         'next_page': next_page})


def post(request, post_id):
    """View post and its comment."""
    instance = request.COOKIES.get('instance')
    theme = request.COOKIES.get('luna-theme', 'auto')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    post_response = requests.get(f'{BASE_URL % instance}/posts/{post_id}')
    if post_response.status_code != HTTPStatus.OK:
        return handle_error(post_response)
    comment_response = requests.get(
        f'{BASE_URL % instance}/posts/{post_id}/replies')
    if comment_response.status_code != HTTPStatus.OK:
        return handle_error(comment_response)
    comment_json = comment_response.json()
    return render(
        request, 'post.html',
        {'post': post_response.json(),
         'comments': comment_json['items'],
         'logged_in': {'name': username, 'id': user_id},
         'luna_theme': theme,
         'next_page': comment_json['next_page']})


def settings(request):
    """Setting client preferences."""
    instance = request.COOKIES.get('instance')
    username = request.COOKIES.get('username')
    user_id = request.COOKIES.get('user_id')
    theme = request.COOKIES.get('luna-theme', 'auto')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    if request.method == 'GET':
        return render(
            request, 'settings.html',
            {'luna_theme': theme,
             'logged_in': {'name': username, 'id': user_id}})
    theme = request.POST['theme']
    response = redirect('settings')
    response.set_cookie('luna-theme', theme)
    return response


def login(request):
    """View for login form."""
    if request.method == 'GET':
        request.session.set_test_cookie()
        return render(request, 'login.html', {'luna_theme': theme})
    username = request.POST['username']
    instance = request.POST['instance']
    theme = request.COOKIES.get('luna-theme', 'auto')
    password = request.POST['password']
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(f'{BASE_URL % instance}/logins', json=payload)
    json = response.json()
    print(json)
    cookies = {
        'username': username,
        'instance': instance,
        'token': json['token'],
        'user_id': json['user']['id'],
        'is_site_admin': json['user']['is_site_admin'],
        'has_unread_notifications': json['user']['has_unread_notifications']
    }
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = redirect('index')
        for k, v in cookies.items():
            response.set_cookie(k, v)
        return response
    else:
        return render('error/no_cookie.html')


def logout(request):
    """Log out endpoint."""
    instance = request.COOKIES.get('instance')
    token = request.COOKIES.get('token')
    if instance is None:
        return HttpResponse(
            'Not Authenticated', status_code=HTTPStatus.NOT_AUTHENTICATED)
    response = requests.delete(
        f'{BASE_URL % instance}/logins/~current',
        headers={'Authorization': f'Bearer {token}'})
    print(response)
    response = redirect('index')
    cookies = [
        'username',
        'instance',
        'token',
        'user_id',
        'is_site_admin',
        'has_unread_notifications'
    ]
    for cookie in cookies:
        response.delete_cookie(cookie)
    return response
