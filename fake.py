from app import create_app
from app.models.base import db
from app.models.tcl import Notice, Healthy, Article

    
def fake_notice(msg):
    notice = Notice()
    notice.msg = msg
    notice.add()


def fake_healthy():
    healthy = Healthy()
    
    healthy.blood_pressure = '150/90'
    healthy.uid = 3
    healthy.heart_rate = 65
    healthy.blood_sugar = 7.5
    healthy.alarm_msg = r'''血压较往常而言有所提高，由于家族有高血压病史，需特别注意\n饮食建议:\n    可食用当季时蔬，如：秋葵'''
    healthy.add()


app = create_app(debug=False)

if __name__ == "__main__":
    with app.app_context():
        with db.auto_commit():
            fake_healthy()



