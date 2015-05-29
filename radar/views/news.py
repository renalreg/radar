from datetime import datetime

from flask import render_template, Blueprint, abort, redirect, url_for
from flask_login import current_user

from radar.lib.database import db
from radar.lib.forms.common import DeleteForm
from radar.lib.forms.news import StoryForm
from radar.models.news import Story
from radar.lib.pagination import paginate_query


bp = Blueprint('news', __name__)


@bp.route('/')
def view_story_list():
    query = Story.query.order_by(Story.published.desc())

    pagination = paginate_query(query, default_per_page=5)
    stories = pagination.items

    context = dict(
        stories=stories,
        pagination=pagination,
    )

    return render_template('news.html', **context)


@bp.route('/new/', methods=['GET', 'POST'])
def add_story():
    if not current_user.has_edit_news_permission:
        abort(403)

    form = StoryForm()

    if form.validate_on_submit():
        story = Story()
        story.published = datetime.now()
        form.populate_obj(story)
        db.session.add(story)
        db.session.commit()

        return redirect(url_for('news.view_story', story_id=story.id))

    context = dict(
        form=form,
    )

    return render_template('story_form.html', **context)


@bp.route('/<int:story_id>/edit/', methods=['GET', 'POST'])
def edit_story(story_id):
    if not current_user.has_edit_news_permission:
        abort(403)

    story = Story.query.get_or_404(story_id)

    if not story.can_edit(current_user):
        abort(403)

    form = StoryForm(obj=story)

    if form.validate_on_submit():
        form.populate_obj(story)
        db.session.commit()

        return redirect(url_for('news.view_story', story_id=story.id))

    delete_form = DeleteForm()

    context = dict(
        story=story,
        form=form,
        delete_form=delete_form,
    )

    return render_template('story_form.html', **context)


@bp.route('/<int:story_id>/')
def view_story(story_id):
    story = Story.query.get_or_404(story_id)

    context = dict(
        story=story,
    )

    return render_template('story.html', **context)


@bp.route('/<int:story_id>/delete/', methods=['POST'])
def delete_story(story_id):
    story = Story.query.get_or_404(story_id)

    if not story.can_edit(current_user):
        abort(403)

    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        db.session.delete(story)
        db.session.commit()
        return redirect(url_for('news.view_story_list'))
    else:
        abort(403)