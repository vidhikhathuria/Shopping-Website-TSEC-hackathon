from flask import render_template, session, request, redirect, flash, url_for, send_from_directory
from track import app, db, bcrypt, csrf, socket, trackData, client, mail, cli
from track.forms import WarehouseRegistrationForm, warehouseLoginForm, EmptyForm
from track.models import Warehouse, OrderDetails
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
import numpy as np
import pyzbar.pyzbar as pyzbar
import os, pyqrcode, png, cv2, nexmo
from flask_mail import Message



@socket.on('paymentDetails')
def payment(data):
	paymentData = data['data']
	qrcode = pyqrcode.create(paymentData['paymentID'])
	qrcode.png('qrcode'+ paymentData['paymentID'] + '.png', scale=15)
	o = OrderDetails(paymentID = paymentData['paymentID'], address = paymentData['address']['line1'])
	db.session.add(o)
	db.session.commit()
	pid = paymentData['paymentID']
	o = OrderDetails.query.filter_by(paymentID = pid).first()
	st = 'Your order with us has been placed. Order id is ' + pid + '. Thanks for shopping with us!'
	response = cli.send_message(
					{
					'from' : 'Vonage APIs',
					'to' : o.number,
					'text' : st
					})
	ncco = [
			  {
			    'action': 'talk',
			    'voiceName': 'Raveena',
			    'text': 'Hello user. Hope you are having a good day.' + st
			  }
			]


	response = client.create_call({
			  'to': [{
			    'type': 'phone',
			    'number': '917977753034'
			  }],
			  'from': {
			    'type': 'phone',
			    'number': '918850481046'
			  },
			  'ncco': ncco
			})

	msg = Message('Order Placed',
                  sender='anishkhathuria@gmail.com',
                  recipients=[o.email_id])
	msg.body = st
	mail.send(msg)
	# {'paid': True, 'cancelled': False, 'payerID': '68BAKYT797AX2', 'paymentID': 'PAYID-L4ADKJA9BN96914J6190123S', 'paymentToken': 'EC-73G95573H64136328', 'returnUrl': 'https://www.paypal.com/checkoutnow/error?paymentId=PAYID-L4ADKJA9BN96914J6190123S&token=EC-73G95573H64136328&PayerID=68BAKYT797AX2', 'address': {'recipient_name': 'John Doe', 'line1': 'Flat no. 507 Wing A Raheja Residency', 'line2': 'Film City Road', 'city': 'Mumbai', 'state': 'Maharashtra', 'postal_code': '400097', 'country_code': 'IN'}, 'email': 'sb-n043or2466727@personal.example.com'}

@app.route('/track', methods = ['GET', 'POST'])
def trackOrder():
	paymentID = request.args.get('id')
    # print(paymentID, type(paymentID), paymentID[1:])
    # return '<h1>The payment id is {}</h1>'.format(paymentID)
	# print(paymentID)
	o = OrderDetails.query.filter_by(paymentID = paymentID[1:]).first()
	w = o.current_warehouse
	return render_template('track.html', order = o, warehouse = w)



@app.route('/orders')
@login_required
def orders():
	return render_template('orders.html', title = 'Orders', orders=OrderDetails.query.all())

@app.route('/scan/<string:paymentID>/<int:current_warehouse_id>', methods=['GET','POST'])
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
					flash('Current warehouse of this order is already yours!', 'warning')
					return redirect(url_for('order_details', paymentID = o.paymentID))
				else:
					o.current_warehouse = current_user
					if o.status == 0:
						o.status = 1
					else:
						o.status += 1
					st = 'Your order is currently in our warehouse at ' + o.current_warehouse.location + '. Happy Shopping!!\n\n'
					msg = Message('Current status of your order',
				                  sender='anishkhathuria@gmail.com',
				                  recipients=[o.email_id])
					msg.body = st
					mail.send(msg)
					response = cli.send_message(
					{
					'from' : 'Vonage APIs',
					'to' : o.number,
					'text' : st
					})
					ncco = [
					  {
					    'action': 'talk',
					    'voiceName': 'Raveena',
					    'text': 'Hello user. Hope you are having a good day. We have updates for your order.' + st 
					  }
					]


					response = client.create_call({
					  'to': [{
					    'type': 'phone',
					    'number': '917977753034'
					  }],
					  'from': {
					    'type': 'phone',
					    'number': '918850481046'
					  },
					  'ncco': ncco
					})

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
				if current_warehouse_id == current_user.id:
					flash('Current warehouse of this order is already yours!', 'warning')
					return redirect(url_for('order_details', paymentID = paymentID))
				if paymentID == var[2:-1]:
					o.current_warehouse = current_user
					if o.status == 0:
						o.status = 1
					else:
						o.status += 1
					st = 'Your order is currently in our warehouse at ' + o.current_warehouse.location + '. Happy Shopping!!\n\n'
					msg = Message('Current status of your order',
				                  sender='anishkhathuria@gmail.com',
				                  recipients=[o.email_id])
					msg.body = st
					mail.send(msg)
					response = cli.send_message(
					{
					'from' : 'Vonage APIs',
					'to' : o.number,
					'text' : st
					})
					ncco = [
						  {
						    'action': 'talk',
						    'voiceName': 'Raveena',
						    'text': 'Hello user. Hope you are having a good day. We have updates for your order.' + st 
						  }
						]


					response = client.create_call({
						  'to': [{
						    'type': 'phone',
						    'number': '917977753034'
						  }],
						  'from': {
						    'type': 'phone',
						    'number': '918850481046'
						  },
						  'ncco': ncco
						})

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
def order_details(paymentID, current_warehouse_id = None):
	o = OrderDetails.query.filter_by(paymentID = paymentID).first()
	if o.current_warehouse_id == 0:
		w = None
	else:
		w = o.current_warehouse
	return render_template('order_details.html', order = o, warehouse = w)

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

