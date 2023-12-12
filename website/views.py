#homepage, user profile, etc
from _ast import Lambda
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Event, User, Like
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/create-events", methods=['GET', 'POST'])
@login_required
def create_Events():
    if request.method == "POST":
        eventName = request.form.get('eventName')
        location = request.form.get('location')
        category = request.form.get('category')
        eventDate_str = request.form.get('eventDate')
        eventPrice = request.form.get('eventPrice')
        ticketsNo = request.form.get('ticketsNo')

        if (not eventName
                or not location
                or not category
                or not eventDate_str
                or not eventPrice
                or not ticketsNo):
            flash('Please fill in all required fields.', 'error')
        else:
            try:
                # Convert the string to a datetime object
                eventDate = datetime.strptime(eventDate_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DDTHH:MM.', 'error')
                return redirect(url_for('views.create_Events'))

            event = Event(
                eventName=eventName,
                location=location,
                category=category,
                eventDate=eventDate,
                eventPrice=eventPrice,
                ticketsNo=ticketsNo,
                author=current_user.id
            )

            db.session.add(event)
            db.session.commit()
            flash('Event created!', category='success')

            return redirect(url_for('views.browse_Events'))

    return render_template("createevents.html", user=current_user)

@views.route("/browse-events")
@login_required
def browse_Events():
    event = Event.query.all()
    return render_template("browseevents.html", user=current_user, event=event)

@views.route("/delete-event/<id>")
@login_required
def delete_post(id):
    event = Event.query.filter_by(id=id).first()

    if not event:
        flash("Event does not exist.", category='error')
    elif current_user.id != event.author:
        flash("You do not have permission to delete this post", category='error')
    else:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted', category='success')

    return redirect(url_for('views.home'))

@views.route("/my-event", methods=['GET', 'POST'])
@login_required
def my_Event():
    userEvents = current_user.events

    if request.method == 'POST':
        event_id = request.form.get('event_id')
        new_tickets_no = request.form.get('tickets_no')

        event = Event.query.get(event_id)
        if event and event.author == current_user.id:
            event.ticketsNo = new_tickets_no
            db.session.commit()
            flash('Number of tickets updated successfully!', 'success')
            return redirect(url_for('views.my_Event'))

    return render_template("my_event.html", user=current_user, userEvents=userEvents, author=current_user.username)

@views.route("/like-event/<event_id>", methods=["POST"])
@login_required
def like(event_id):
    event = Event.query.filter_by(id=event_id).first()
    like = Like.query.filter_by(author=current_user.id, event_id=event_id).first()

    if not event:
        jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, event_id=event_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(event.likes), "liked": current_user.id in map(lambda x: x.author, event.likes)})

@views.route("/purchase-event/", methods=["POST"])
@login_required
def purchase_Event():
    print("Purchase event view triggered")

    if request.method == 'POST':
        print(request.form.get('quantity'))

        event_id = request.form.get('event_id')
        quantity_purchased = int(request.form.get('quantity', 0))

        event = Event.query.get(event_id)

        if not event:
            return jsonify({"error": "Event not found"}, 404)

        if quantity_purchased <= 0 or quantity_purchased > event.ticketsNo:
            jsonify({"error": "Not enough tickets available"}, 400)

        else:
            event.ticketsNo = event.ticketsNo - quantity_purchased
            db.session.commit()
            flash("Purchase successful", "success")
            return redirect(url_for('views.browse_Events'))









