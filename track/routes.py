from flask import render_template, session, request, redirect, flash, url_for
from track import app, db, bcrypt, csrf
from track.forms import WarehouseRegistrationForm, warehouseLoginForm, EmptyForm
from track.models import Warehouse
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/orders')
@login_required
def orders():
	orders = [
		{
			'o_id': 1,
			'w_id': 2
		},
		{
			'o_id': 2,
			'w_id': 4
		},
		{
			'o_id': 3,
			'w_id': 1
		},
		{
			'o_id': 4,
			'w_id': 3
		},
		{
			'o_id': 5,
			'w_id': 1
		},
		{
			'o_id': 6,
			'w_id': 3
		},
		{
			'o_id': 7,
			'w_id': 4
		},
		{
			'o_id': 8,
			'w_id': 2
		},
		{
			'o_id': 9,
			'w_id': 4
		},
		{
			'o_id': 10,
			'w_id': 1
		}
	]
	return render_template('orders.html', title = 'Orders', orders=orders)

@app.route('/order/<int:o_id>/<int:w_id>')
@login_required
def order(o_id, w_id):
	form = EmptyForm()
	print(type(current_user.id), type(w_id))
	return render_template('order.html', o_id=o_id, w_id=w_id, form=form)

@app.route('/checkin/<int:o_id>/<int:w_id>', methods=['POST'])
@login_required
def checkin(o_id, w_id):
	form = EmptyForm()
	if form.validate_on_submit():
		return "working!"
	else:
		return "not working"


@app.route('/addwarehouse', methods=['GET', 'POST'])
def addwarehouse():
	if current_user.is_authenticated:
		return redirect(url_for('orders'))
	form = WarehouseRegistrationForm()
	if request.method == 'POST' and form.validate_on_submit():
		hash_password = bcrypt.generate_password_hash(form.password.data)
		warehouse = Warehouse(name = form.name.data, email = form.email.data,password = hash_password, x = float(form.x.data), y = float(form.y.data))
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

