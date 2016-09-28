from datetime import date, timedelta

from jinja2.utils import generate_lorem_ipsum

from radar.fixtures.utils import random_date, add
from radar.models.posts import Post


def create_posts(n):
    for x in range(n):
        d = random_date(date(2008, 1, 1), date.today() - timedelta(days=1))

        post = Post()
        post.title = '%s Newsletter' % d.strftime('%b %Y')
        post.body = generate_lorem_ipsum(n=3, html=False)
        post.published_date = d
        add(post)

    post = Post()
    post.title = 'New RaDaR Conditions'
    post.body = 'RaDaR is now open to two new conditions - Calciphylaxis and IgA Nephropathy. '\
        'No new approvals are needed for these conditions and patients are registered in the normal fashion.'
    post.published_date = date.today()
    add(post)
