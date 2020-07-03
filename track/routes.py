from flask import render_template, session, request, redirect, flash, url_for
from track import app, db, bcrypt, csrf
from track.forms import WarehouseRegistrationForm, warehouseLoginForm, EmptyForm
from track.models import Warehouse, OrderDetails
from flask_login import login_user, current_user, logout_user, login_required
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar



@app.route('/orders')
@login_required
def orders():
	return render_template('orders.html', title = 'Orders', orders=OrderDetails.query.all())

# @login_required
# @app.route('/scan/<string:o_id>')
# def scan(o_id):

# 	

@app.route('/scan/<string:paymentID>', methods=['GET','POST'])
@app.route('/scan')
@login_required
def scan(paymentID = None, current_warehouse_id = None):
	if paymentID == None:
		var = '-1'
		cap = cv2.VideoCapture(0)
		font = cv2.FONT_HERSHEY_PLAIN

		while True:
		    _, frame = cap.read()
		    decodedObjects = pyzbar.decode(frame)
		    if(decodedObjects != []):
		        var = str(decodedObjects[0].data)
		        break
		    for obj in decodedObjects:
		        #print("Data", obj.data)
		        cv2.putText(frame, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)

		    cv2.imshow("Frame", frame)

		    key = cv2.waitKey(1)
		    if key == 27:
		        break
		if var != '-1':
			o = OrderDetails.query.filter_by(paymentID = var[2:-1]).first()
			if o != None:
				if o.current_warehouse_id == current_user.id:
					flash('Current warehouse of this order is already yours!', 'warn')
					return redirect(url_for('order_details', paymentID = o.paymentID))
				else:
					o.current_warehouse = current_user
					o.status += 1
					db.session.commit()
					flash('Warehouse has been updated!', 'success')
					return redirect(url_for('order_details', paymentID = o.paymentID))
			else:
				flash('You scanned the wrong QR', 'danger')
				return redirect(url_for('orders'))
	else:
		var = '-1'
		cap = cv2.VideoCapture(0)
		font = cv2.FONT_HERSHEY_PLAIN

		while True:
		    _, frame = cap.read()
		    decodedObjects = pyzbar.decode(frame)
		    if(decodedObjects != []):
		        var = str(decodedObjects[0].data)
		        break
		    for obj in decodedObjects:
		        #print("Data", obj.data)
		        cv2.putText(frame, str(obj.data), (50, 50), font, 2, (255, 0, 0), 3)

		    cv2.imshow("Frame", frame)

		    key = cv2.waitKey(1)
		    if key == 27:
		        break
		if var != '-1':
			o = OrderDetails.query.filter_by(paymentID = var[2:-1]).first()
			if o != None:
				# print(o.current_warehouse_id, current_user.id)
				# if o.current_warehouse_id == current_user.id:
				# 	flash('Current warehouse of this order is already yours!', 'warning')
				# 	return redirect(url_for('order_details', paymentID = paymentID))
				if paymentID == var[2:-1]:
					o.current_warehouse = current_user
					o.status += 1
					db.session.commit()
					flash('Warehouse has been updated!', 'success')
					return redirect(url_for('order_details', paymentID = paymentID))
				else:
					flash('You have got the wrong order', 'danger')
					return redirect(url_for('order_details', paymentID = var[2:-1]))
			else:
				flash('You scanned the wrong QR', 'danger')
				return redirect(url_for('orders'))
	return render_template('scan.html')

@app.route('/order_details/<string:paymentID>')
@login_required
def order_details(paymentID):
	o = OrderDetails.query.filter_by(paymentID = paymentID).first()
	w = o.current_warehouse
	return render_template('order_details.html', order = o, warehouse = w)

# @app.route('/order/<int:o_id>/<int:w_id>')
# @login_required
# def order(o_id, w_id):
# 	form = EmptyForm()
# 	print(type(current_user.id), type(w_id))
# 	return render_template('order.html', o_id=o_id, w_id=w_id, form=form)

# @app.route('/checkin/<int:o_id>/<int:w_id>', methods=['POST'])
# @login_required
# def checkin(o_id, w_id):
# 	form = EmptyForm()
# 	if form.validate_on_submit():
# 		return "working!"
# 	else:
# 		return "not working"


@app.route('/addwarehouse', methods=['GET', 'POST'])
def addwarehouse():
	if current_user.is_authenticated:
		return redirect(url_for('orders'))
	form = WarehouseRegistrationForm()
	if request.method == 'POST' and form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data)
		warehouse = Warehouse(name = form.name.data, email = form.email.data,password = hash_password, location = form.location.data, x = float(form.x.data), y = float(form.y.data))
		db.session.add(warehouse)
		db.session.commit()
		flash('Warehouse has been created! You are now able to log in', 'success')
		return redirect(url_for('warehouselogin'))
	return render_template('addwarehouse.html', form=form, title="Add Warehouse Page")

@app.route('/', methods=['GET', 'POST'])
@app.route('/warehouselogin', methods=['GET', 'POST'])
def warehouselogin():
	if current_user.is_authenticated:
		return redirect(url_for('orders'))
	form = warehouseLoginForm(request.form)
	if form.validate_on_submit():
		warehouse = Warehouse.query.filter_by(email=form.email.data).first()
		if warehouse and bcrypt.check_password_hash(warehouse.password, form.password.data):
			login_user(warehouse, remember=form.remember.data)
			flash('Login Success!', 'success')
			return redirect(url_for('orders'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('warehouselogin.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('warehouselogin'))

