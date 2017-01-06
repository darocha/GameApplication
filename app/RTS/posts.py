from app.RTS import rts
from app.RTS.helpers import current_player, generate_player_for_user, current_user
from app.auth.attributes import secure
from app.RTS.models import *
from app.auth.models.user import User
from flask import Blueprint, render_template, redirect, session, request
from app import db, bcrypt

@rts.route('/create-player', methods=['POST'])
@secure(cookie_authorization=True)
def create_player():
    if current_player():
        return "", 500
    user = User.query.filter_by(id=session['user_id']).first()
    if user:
        generate_player_for_user(user)
        return redirect('rts')
    return redirect('auth')

#TODO: Check if the user has enough resources.
@rts.route('/purchase-unit', methods=['POST'])
def create_unit():
    player = current_player()
    if not player:
        return redirect("rts/")
    cavalry_amount = int(request.form['amount_of_cavalry'])
    knight_amount = int(request.form['amount_of_knights'])
    pikemen_amount = int(request.form['amount_of_pikemen'])
    doges_amount = int(request.form["amount_of_doges"])
    id = int(request.form['townid'])
    town = Town.query.filter_by(id = id).first()
    if town.player.id != player.id:
        return redirect("rts/")


    town.add_units(knight_amount, cavalry_amount, pikemen_amount, doges_amount)
    db.session.add(town)
    db.session.commit()
    return redirect('rts/town/' + str(id))

#TODO: Check if the user has enough resources.
@rts.route('/purchase-building', methods=['POST'])
def upgrade_building():
    player = current_player()
    if not player:
        return redirect("rts/")

    building = request.form['building-name']
    id = int(request.form['townid'])
    town = Town.query.filter_by(id = id).first()
    if town.player.id != player.id:
        return redirect("rts/")

    town.add_upgrade(building)
    db.session.add(town)
    db.session.commit()
    password = bcrypt.generate_password_hash("password")


    return redirect('rts/town/' + str(id))

@rts.route('/send-attack', methods=['POST'])
def send_attack():
    id = int(request.form['townid'])
    if not 'destination' in request.form:
        return redirect('rts/town/' + str(id))
    player = current_player()
    if not player:
        return redirect("rts/")

    destination = int(request.form['destination'])
    cavalry_amount = int(request.form['amount_of_cavalry'])
    knight_amount = int(request.form['amount_of_knights'])
    pikemen_amount = int(request.form['amount_of_pikemen'])
    doges_amount = int(request.form['amount_of_doges'])
    town = Town.query.filter_by(id = id).first()
    destination = Town.query.filter_by(id = destination).first()
    if town.player.id != player.id:
        return redirect("rts/")

    if town.remove_units(knight_amount, cavalry_amount, pikemen_amount, doges_amount):
        attack = Attack(town.player, destination, town, knight_amount, cavalry_amount, pikemen_amount, doges_amount)
        db.session.add(attack)
        db.session.commit()
    return redirect('rts/town/' + str(id))
