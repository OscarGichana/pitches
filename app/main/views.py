from flask import render_template,request,redirect,url_for,abort
from . import main
#from ..requests import get_movies,get_movie,search_movie
from .forms import PitchForm,UpdateProfile,CommentForm
from ..models import Pitch,User
from flask_login import login_required, current_user
from .. import db,photos
import markdown2  


@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    # Getting pitches
    pitches = Pitch.query.all()
    popular = Pitch.query.filter_by(category = 'popular').all()
    interview = Pitch.query.filter_by(category = 'interview').all()
    pichup = Pitch.query.filter_by(category = 'pickup').all()

    title = 'Pitch'

    return render_template('index.html', title = title, popular = popular, interview = interview, pickup = pick-up )


@main.route('/new_pitch', methods = ['GET','POST'])
@login_required
def new_pitch(id):
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        category = form.category.data
        user_id = current_user

        # Updated pitch instance        #
        new_pitch = Pitch(pitch=pitch,movie_title=title,category=category,user_id=current_user)

        # save pitch method
        new_pitch.save_pitch()
        return redirect(url_for('.new_pitch'))

    title = 'Pitch'
    return render_template('new_pitch.html',title = title, form=form, pitch=pitch, category=category)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/like/<int:id>',methods = ['POST','GET'])
@login_required
def up_vote(id):
    get_pitches = Upvote.get_upvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_vote = Upvote(user = current_user, pitch_id=id)
    new_vote.save()
    return redirect(url_for('main.index',id=id))

@main.route('/dislike/<int:id>',methods = ['POST','GET'])
@login_required
def down_vote(id):
    pitch = Downvote.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for p in pitch:
        to_str = f'{p}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.index',id=id))
        else:
            continue
    new_downvote = Downvote(user = current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index',id = id))


@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(pitch_id):
    form = CommentForm()
    pitch = Pitch.query.get(pitch_id)
    all_comments = Comment.query.filter_by(pitch_id = pitch_id).all()
    if form.validate_on_submit():
        comment = form.comment.data 
        pitch_id = pitch_id
        user_id = current_user._get_current_object().id


        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)


        new_comment.save_comment()
        return redirect(url_for('.comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form, pitch = pitch,all_comments=all_comments)
