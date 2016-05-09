from datetime import date, timedelta

from jinja2.utils import generate_lorem_ipsum

from radar_fixtures.utils import random_date
from radar.models.posts import Post
from radar_fixtures.validation import validate_and_add


def create_posts(n):
    for x in range(n):
        d = random_date(date(2008, 1, 1), date.today() - timedelta(days=1))

        post = Post()
        post.title = '%s Newsletter' % d.strftime('%b %Y')
        post.body = generate_lorem_ipsum(n=3, html=False)
        post.published_date = d
        validate_and_add(post)

    post = Post()
    post.title = 'New RaDaR Conditions'
    post.body = 'RaDaR is now open to two new conditions - Calciphylaxis and IgA Nephropathy. '\
        'No new approvals are needed for these conditions and patients are registered in the normal fashion.'
    post.published_date = date.today()
    validate_and_add(post)
