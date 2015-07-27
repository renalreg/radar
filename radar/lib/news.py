from radar.models.posts import Post


def get_latest_news(n=3):
    posts = Post.query.order_by(Post.published.desc()).limit(n).all()
    return posts
