from track import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Warehouse.query.get(int(user_id))

edges = db.Table('edges',
    db.Column('node_1', db.Integer, db.ForeignKey('warehouse.id')),
    db.Column('node_2', db.Integer, db.ForeignKey('warehouse.id'))
)

checkins = db.Table()


class Warehouse(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	location = db.Column(db.String(60), nullable=False)
	x = db.Column(db.Float)
	y = db.Column(db.Float)
	connected = db.relationship(
        'Warehouse', secondary=edges,
        primaryjoin=(edges.c.node_1 == id),
        secondaryjoin=(edges.c.node_2 == id),
        backref=db.backref('edges', lazy='dynamic'), lazy='dynamic')

	all_orders = db.relationship(
		'OrderDetails', backref = 'current_warehouse'
		)

	def connect(self, warehouse):
		if not self.is_following(warehouse):
			self.connected.append(warehouse)
	
	def unconnect(self, warehouse):
		if self.is_following(warehouse):
			self.connected.remove(warehouse)

	def is_following(self, warehouse):
		return self.connected.filter(
			edges.c.node_2 == warehouse.id).count() > 0


class OrderDetails(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	buyer_id = db.Column(db.Integer, nullable=False)
	seller_id = db.Column(db.Integer, nullable=False)
	current_warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))