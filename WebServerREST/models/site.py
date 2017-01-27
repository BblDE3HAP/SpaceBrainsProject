from db import db


class SiteModel(db.Model):
    __tablename__ = 'Sites'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80))

    # pages = db.relationship('PageModel', lazy='dynamic')

    def __init__(self, Name=None):
        self.Name = Name

    def json(self):
        return {'id': self.ID, 'name': self.Name}
        # return {'id': self.id, 'name': self.name, 'pages': [page.json() for
        # page in self.pages.all()]}

    @classmethod
    def find_by_name(cls, Name):
        return cls.query.filter_by(Name=Name).first()

    @classmethod
    def find_by_id(cls, ID):
        return cls.query.filter_by(ID=ID).first()  # TODO?

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
