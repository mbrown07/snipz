import base64, io, os
from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from ..forms import RegistrationForm, LoginForm, SnippetUploadForm, ShareSnippetForm, SearchForm, SnippetReviewForm
from ..models import User, CodeSnippet, load_user, Review, Snippet
from ..utils import current_time

snippets = Blueprint("snippets", __name__)

def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

@snippets.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    language_data = CodeSnippet.objects.aggregate([
        {"$group": {"_id": "$language", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    languages_with_counts = {data['_id']: data['count'] for data in language_data if data['_id']}
    form.language.choices = [(lang, f"{lang} ({count})") for lang, count in languages_with_counts.items()]

    form.language.choices.insert(0, ("None", "None"))

    snippets = []
    if form.validate_on_submit():
        query = {}
        
        if form.title.data.strip():
            query['title'] = {'$regex': form.title.data.strip(), '$options': 'i'}
        if form.tag.data.strip():
            query['tags'] = {'$in': [tag.strip().lower() for tag in form.tag.data.split(',')]}
        if form.language.data.strip() and form.language.data.strip() != "None":
            query['language'] = form.language.data.strip()
        if form.difficulty.data.strip() and form.difficulty.data.strip() != "None":
            query['difficulty'] = form.difficulty.data.strip()
        snippets = CodeSnippet.objects(__raw__=query)
    else:
        snippets = CodeSnippet.objects.all()

    return render_template('index.html', form=form, snippets=snippets)

@snippets.route("/upload", methods=["GET", "POST"])
@login_required
def upload_snippet():
    form = SnippetUploadForm()
    if form.validate_on_submit():
        newList = form.tags.data.split(",")
        for i in range(len(newList)):
            newList[i] = newList[i].lower()
        snippet = CodeSnippet(
            author=current_user._get_current_object(),
            title=form.title.data,
            code=form.code.data,
            language=form.language.data,
            tags=newList,
            difficulty=form.difficulty.data
        )
        snippet.save()
        share_form = ShareSnippetForm()
        form2 = SnippetReviewForm()
        return render_template("snippet_display.html", share_form=share_form, form=form2, snippet=snippet)

    for f, err in form.errors.items():
        for e in err:
            flash(f"Error: {f} {e}")
    return render_template("upload_snippet.html", form=form)

@snippets.route("/snippet/<snippet_id>", methods=["GET", "POST"])
def snippet_detail(snippet_id):
    snippet = CodeSnippet.objects(id=snippet_id).first()
    if not snippet:
        return redirect(url_for('snippets.index')) 

    form = SnippetReviewForm()
    share_form = ShareSnippetForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            snippet_id=snippet_id,
            snippet_title=snippet.title,
        )
        review.save()
        return redirect(request.path)

    review_objects = Review.objects(snippet_id=snippet_id)
    reviews = [{'commenter': review.commenter.username,
                'content': review.content,
                'date': review.date,
                'image': get_b64_img(review.commenter.username)
            } for review in review_objects]

    return render_template( "snippet_display.html", form=form, share_form=share_form, snippet=snippet, reviews=reviews)

@snippets.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    if not user:
        return render_template('user_detail.html', error=f'User {username} does not exist')
    reviews = Review.objects(commenter=user)
    image = get_b64_img(username)
    return render_template('user_detail.html', username=username, reviews=reviews, image=image)

@snippets.route('/like-snippet/<string:snippet_id>', methods=['POST'])
@login_required
def like_snippet(snippet_id):
    snippet = CodeSnippet.objects(id=snippet_id).first()
    username = current_user.username
    if username in snippet.likes:
        snippet.likes.remove(username)
    else:
        if username in snippet.dislikes:
            snippet.dislikes.remove(username)
        snippet.likes.append(username)

    snippet.save()

    if not snippet.likes:
        snippet.update(set__likes=[])

    return jsonify({'likes': len(snippet.likes), 'dislikes': len(snippet.dislikes)})

@snippets.route('/dislike-snippet/<string:snippet_id>', methods=['POST'])
@login_required
def dislike_snippet(snippet_id):
    snippet = CodeSnippet.objects(id=snippet_id).first()
    username = current_user.username
    if username in snippet.dislikes:
        snippet.dislikes.remove(username)
    else:
        if username in snippet.likes:
            snippet.likes.remove(username)
        snippet.dislikes.append(username)

    snippet.save()

    if not snippet.dislikes:
        snippet.update(set__dislikes=[])
    return jsonify({'likes': len(snippet.likes), 'dislikes': len(snippet.dislikes)})

@snippets.route('/send-email/<string:snippet_id>', methods=['POST'])
@login_required
def send_email(snippet_id):
    mail = Mail(app)

    snippet = CodeSnippet.objects(id=snippet_id).first()
    share_form = ShareSnippetForm()
    if share_form.validate_on_submit():
        recipient_email = request.form['email']
        msg = Message('You received a new Code Snippet!',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[recipient_email])
        msg.body = f"Here's a code snippet titled {snippet.title}:\n\n{snippet.code}"
        mail.send(msg)
        flash(f'The snippet has been sent to {recipient_email}!')
        return redirect(url_for('snippets.snippet_detail', snippet_id=snippet_id))
    return render_template("snippet_display.html", snippet=snippet, form=share_form)

@snippets.route('/save-snippet/<string:snippet_id>', methods=['GET', 'POST'])
@login_required
def save_snippet(snippet_id):
    snippet = CodeSnippet.objects(id=snippet_id).first()
    if snippet:
        existing_snippet = Snippet.objects(user=current_user._get_current_object(), snippet=snippet).first()
        if not existing_snippet:
            saved_snippet = Snippet(user=current_user._get_current_object(), snippet=snippet)
            saved_snippet.save()
            flash('Snippet saved successfully!')
        else:
            flash('You have already saved this snippet.')
    return redirect(url_for('snippets.snippet_detail', snippet_id=snippet_id))

@snippets.route('/my-snippets', methods=['GET'])
@login_required
def my_snippets():
    saved_snippets = Snippet.objects(user=current_user._get_current_object())
    return render_template('my_snippets.html', snippets=saved_snippets)