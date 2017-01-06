import atexit, datetime, os, time, threading
from app.RTS.models import *
from app import app, db

def update_towns():
    towns = Town.query.all()
    for town in towns:
        town.update_resources()
        town.update_upgrade()
        db.session.add(town)
    db.session.commit()

def update_attacks():
    now = datetime.datetime.now()
    attack = Attack.query.order_by(Attack.arrival_time).first()
    while attack and now >= attack.arrival_time:
        attack.resolve()
        attack = Attack.query.order_by(Attack.arrival_time).first()

def activate_background_task():
    if not "TEST" in os.environ:
        def fizz():
            update_attacks()
            threading.Timer(1, fizz).start()
        def buzz():
            update_towns()
            threading.Timer(5, buzz).start()

        fizz()
        buzz()

