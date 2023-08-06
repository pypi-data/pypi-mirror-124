from django.http import HttpResponse


def get_fedi_name(name, instance, local):
    """Turn username to fediverse style."""
    if local:
        return name
    else:
        return f'{name}@{instance}'


def get_minimal_post(post):
    """Get only essential information for a post preview."""
    return {
        'url': f'/posts/{post["id"]}',
        'title': post['title'],
        'created': post['created'],
        'author': get_fedi_name(
            post['author']['username'],
            post['author']['host'],
            post['author']['local']),
        'author_url': f'/users/{post["author"]["id"]}',
        'community': get_fedi_name(
            post['community']['name'],
            post['community']['host'],
            post['community']['local']),
        'community_url': f'/communities/{post["community"]["id"]}'
    }


def handle_error(response):
    """Return uniform HTTP response."""
    return HttpResponse(
        'Some error occured when trying to retrieve data',
        status_code=response.status_code,
        headers=response.headers
    )
