import databases
import sqlalchemy

DATABASE_URL = "sqlite:///homework6.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

table_users = sqlalchemy.Table(
    "users", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(64)),
    sqlalchemy.Column("surname", sqlalchemy.String(64)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128))    
    )

table_shop_items = sqlalchemy.Table(
    "shop_items", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128)), 
    sqlalchemy.Column("description", sqlalchemy.Text()),
    sqlalchemy.Column("price", sqlalchemy.Numeric())
    )

table_orders = sqlalchemy.Table(
    "orders", 
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),    
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("shop_item_id", sqlalchemy.ForeignKey('shop_items.id')),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("is_completed", sqlalchemy.Boolean)
    )

engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    )

metadata.create_all(engine)