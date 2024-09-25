from database import app


with app.app_context():
    from user import *
    db.create_all()

    from password_reset import *
    db.create_all()

    from profiles import *
    db.create_all()

    from activation import *
    db.create_all()

    from account_type import *
    db.create_all()

    from trade_config import *
    db.create_all()

    from banks import *
    db.create_all()

    from gl import *
    db.create_all()

    from banks import *
    db.create_all()

    from equities import *
    db.create_all()

    from equities_charges import *
    db.create_all()

    from equities_stocks import *
    db.create_all()

    from equities_transactions import *
    db.create_all()

    from etfs import *
    db.create_all()

    from etfs_charges import *
    db.create_all()

    from etfs_stocks import *
    db.create_all()

    from etfs_transactions import *
    db.create_all()

    from treasury import *
    db.create_all()

    from transactions import *
    db.create_all()
