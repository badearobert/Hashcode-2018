from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()


class DatabaseEntry(db.Model):
    __bind_key__ = 'sql_scores'
    db_alias = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    db_score = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)
    db_score_a = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)
    db_score_b = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)
    db_score_c = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)
    db_score_d = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)
    db_score_e = db.Column(db.Integer, unique=False, nullable=True, primary_key=False, default=0)

    def __repr__(self):
        return '<Alias {0}>'.format(self.db_alias)


class DatabaseHandler:
    highest_score = 0

    @staticmethod
    def get_entries():
        return DatabaseEntry.query.order_by(desc(DatabaseEntry.db_score)).all()

    @staticmethod
    def set(alias, filename, score):  # sets or updates the score based on existing value
        # check if alias exists
        entry = DatabaseEntry.query.filter_by(db_alias=alias).first()
        print(entry)

        # if we don't have the alias in db, we add it
        if entry is None:
            db_entry = DatabaseEntry(db_alias=alias)
            db.session.add(db_entry)
            db.session.commit()

        # update the entries in db for the entry
        entry = DatabaseEntry.query.filter_by(db_alias=alias).first()

        if filename == 'a_example.out':
            entry.db_score_a = score if entry.db_score_a < score else entry.db_score_a
        if filename == 'b_should_be_easy.out':
            entry.db_score_b = score if entry.db_score_b < score else entry.db_score_b
        if filename == 'c_no_hurry.out':
            entry.db_score_c = score if entry.db_score_c < score else entry.db_score_c
        if filename == 'd_metropolis.out':
            entry.db_score_d = score if entry.db_score_d < score else entry.db_score_d
        if filename == 'e_high_bonus.out':
            entry.db_score_e = score if entry.db_score_e < score else entry.db_score_e

        entry.db_score = (entry.db_score_a + entry.db_score_b + entry.db_score_c + entry.db_score_d + entry.db_score_e)
        DatabaseHandler.highest_score = entry.db_score if DatabaseHandler.highest_score < entry.db_score else DatabaseHandler.highest_score
        db.session.commit()


class SessionEntry(db.Model):
    __bind_key__ = 'sql_sessions'
    db_alias = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    db_ip = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)

    def __repr__(self):
        return '<Alias {0}>'.format(self.db_alias)


class SessionHandler:

    @staticmethod
    def get_entries():
        return SessionEntry.query.all()

    @staticmethod
    def add(alias, ip):
        # check if alias exists
        entry = SessionEntry.query.filter_by(db_alias=alias).first()
        print(entry)
        if entry is None:
            db_entry = SessionEntry(db_alias=alias, db_ip=ip)
            db.session.add(db_entry)
            db.session.commit()

    @staticmethod
    def get(ip):
        # check if alias exists
        entry = SessionEntry.query.filter_by(db_ip=ip).first()
        if entry is not None:
            return entry.db_alias
        return None

    @staticmethod
    def print():
        entries = SessionHandler.get_entries()
        for entry in entries:
            print("Session: {0} -> {1}".format(entry.db_alias, entry.db_ip))
