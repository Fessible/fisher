from app.models.base import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Gift(db.Model):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=True)

    # 是否已经赠送出去了
    launched = Column(Boolean, default=False)