from datetime import datetime
from models.db.otp_model import Otp
from conf.database import Session


def opt_create(phone, otp):
    session = Session()
    opt = Otp(phone=phone, otp=otp)
    session.add(opt)
    session.commit()
    session.close()


def otp_storage_time(phone, otp):
    session = Session()
    date = session.query(Otp).filter(Otp.phone == phone, Otp.otp == otp).first()
    current_time = datetime.now()
    if date.expires_at > current_time:
        return True
    return False


def validate_otp(phone, otp):
    session = Session()
    date = session.query(Otp).filter(Otp.phone == phone, Otp.otp == otp).first()
    if date:
        return True
    return False
