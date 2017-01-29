from db import db


class PageModel(db.Model):
    __tablename__ = 'Pages'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Url = db.Column(db.String(2048))
    FoundDateTime = db.Column(db.DateTime)
    LastScanDate = db.Column(db.DateTime)

    SiteID = db.Column(db.Integer, db.ForeignKey('Sites.ID'))
    Site = db.relationship('SiteModel')

    def json(self):
        return {'site':  self.SiteID,                  # SiteModel.query.filter_by(ID=self.SiteID).first(),
                'total_count':              PageModel.query.filter_by(SiteID=self.SiteID).count(),
                'total_count_not_round':    PageModel.query.filter_by(LastScanDate=None).count(),
                'total_count_round':        PageModel.query.filter(PageModel.LastScanDate!=None).count()}

    @classmethod
    def find_by_id(cls, ID):
        return cls.query.filter_by(SiteID=ID).first()

 #   @classmethod
 #   def find_by_name(cls, Name):
        # siteID = SiteModel.query.filter_by(Name=Name).first()
 #       return cls.query.filter_by(SiteID=siteID).first()