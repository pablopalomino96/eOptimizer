#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from pdb import set_trace as breakpoint
from flask import jsonify

from flask import Flask, make_response, abort, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from models import Base, Users, Homes
from config import project_constants as const, prod_config
from simulation import Simulation
import home_consumption

import datetime as dt
import json
import os

app = Flask(__name__)
app.config.from_object(prod_config)
db = SQLAlchemy(app)
Base.metadata.create_all(bind=db.engine)

currentUser = None
currentHome = None
login_attempts = 0

@app.route('/')
def index():
   global currentUser
   global currentHome

   if currentUser is None or not session.get('logged_in'):
      return render_template('login.html', flag='login')
   elif currentHome is None:
      return render_template('new_home.html')
   else:
      return render_template('dashboard.html', user=currentUser, home=currentHome)

@app.route('/signup', methods=['POST'])
def sign_up():
   global currentUser
   # ---- creating user ----
   user = Users()
   user.name = request.form['form-first-name']
   user.lastname = request.form['form-last-name']
   user.email = request.form['form-email']
   user.set_password(request.form['form-newpassword'])
   db.session.add(user)

   try:
      db.session.commit()
   except IntegrityError:
      # User Error
      return render_template('login.html', flag='signup', error='An error has occurred')

   currentUser = user
   session['logged_in'] = True

   return render_template('new_home.html', user=user.email)

@app.route('/add-home', methods=['POST'])
def add_home():
   global currentUser
   global currentHome

   if currentUser is not None:
      # ---- creating user home ----
      home = Homes()
      home.pv_modules = request.form['form-pvmodules']
      home.city_code = str(request.form['form-city_code'])
      home.amortization_years_pv = request.form['form-amortization_years_pv']
      home.amortization_years_bat = request.form['form-amortization_years_bt']
      home.user = currentUser

      db.session.add(home)
      try:
         db.session.commit()
      except IntegrityError:
      # Error de insercion de home
         return render_template('new_home.html', error='Ha ocurrido un error')
      currentUser = home.user
      currentHome = home
   return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def do_login():
   global currentUser
   global currentHome
   global login_attempts

   if login_attempts >= 3:
      return render_template('login.html', flag='login', error='Has superado el número de intentos de acceso.')

   input_email = request.form['form-username']
   input_pass = request.form['form-password']
   user = db.session.query(Users).filter_by(email=input_email).first()

   if user is not None:
      if user.check_password(input_pass):
         currentUser = user
         currentHome = user.home
         session['logged_in'] = True
         return redirect(url_for('index'))
      else:
         # Password fails
         login_attempts += 1
         return render_template('login.html', flag='login', error='Contraseña incorrecta. Inténtalo de nuevo')
   else:
      # User fails
      return render_template('login.html', flag='login', error="El usuario {} no existe".format(input_email))

@app.route('/simulation', methods=['POST'])
def simulation():
   global currentUser
   global currentHome

   if currentUser is not None and currentHome is not None:
      simulation_date = request.form['form-start-date']
      consumption_file = request.form['consumption-file']
      #breakpoint()
      start_date = dt.datetime.strptime(simulation_date, '%Y-%m-%d')
      consumption = home_consumption.read_from_file(consumption_file)

      current_sim = Simulation(currentHome, consumption, start_date)
      data = current_sim.optimize()

      result = json.loads(data)

      return make_response(jsonify(result), 200)
   else:
      return redirect(url_for('do_login'))

@app.route('/logout')
def do_logout():
   global currentUser
   global currentHome
   global login_attempts

   currentUser = None
   currentHome = None
   login_attempts = 0
   session['logged_in'] = False

   return render_template('login.html', flag='login')

@app.route('/new_user')
def change_form():
   return render_template('login.html', flag='signup')

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html')


if __name__=="__main__":
   app.secret_key = os.urandom(10)
   app.run(debug=True, host='0.0.0.0', port=7000)