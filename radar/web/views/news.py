from datetime import datetime

from flask import render_template, Blueprint, abort, redirect, url_for
from flask_login import current_user

from radar.lib.database import db
from radar.web.forms.core import DeleteForm
from radar.web.forms.news import PostForm
from radar.models.news import Post
from radar.lib.pagination import paginate_query


bp = Blueprint('news', __name__)


@bp.route('/')
def view_posts():
    query = Post.query.order_by(Post.published.desc())

    pagination = paginate_query(query, default_per_page=5)
    posts = pagination.items

    context = dict(
        posts=posts,
        pagination=pagination,
    )

    return render_template('news.html', **context)


@bp.route('/new/', methods=['GET', 'POST'])
def add_post():
    if not current_user.has_edit_news_permission:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post = Post()
        post.published = datetime.now()
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('news.view_post', post_id=post.id))

    context = dict(
        form=form,
    )

    return render_template('edit_post.html', **context)


@bp.route('/<int:post_id>/edit/', methods=['GET', 'POST'])
def edit_post(post_id):
    if not current_user.has_edit_news_permission:
        abort(403)

    post = Post.query.get_or_404(post_id)

    if not post.can_edit(current_user):
        abort(403)

    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('news.view_post', post_id=post.id))

    delete_form = DeleteForm()

    context = dict(
        post=post,
        form=form,
        delete_form=delete_form,
    )

    return render_template('edit_post.html', **context)


@bp.route('/<int:post_id>/')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)

    context = dict(
        post=post,
    )

    return render_template('post.html', **context)


@bp.route('/<int:post_id>/delete/', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if not post.can_edit(current_user):
        abort(403)

    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('news.view_posts'))
    else:
        abort(403)
