import base64

import requests as r
from avatar_generator import Avatar
from faker import Faker
from requests.auth import HTTPBasicAuth

# data = {"js_code": "fuckadmin"}

# url = "https://monius.top"
# url = "http://127.0.0.1:5000/stu/1"

labels = ["username","nickname", "realname", "engname",
          "email", "phone", "exam_type", "score", "avatar"]

def gen_stu():
    stu = []
    f = Faker()
    for _ in range(2):
        s = f.uuid4()
        print(s)
        passwd = s[:-2]
        fakes=[
                s,
                f.name(),
                f.first_name(),
                f.name_male(),
                f.email(),
                f.phone_number(),
                # f.future_date(),
                f.random_int()%2,
                f.random_int()%1000/10,
        ]
        avatar = Avatar.generate(size=64, string=fakes[2])
        fakes.append(base64.b64encode(avatar).decode('utf8'))

        info = dict(zip(labels,fakes))
        auth ={"usr":s,"passwd":passwd}
        stu.append({"info": info, "auth": auth})
    return stu

def auth(usr,passwd,target):
    
    print("auth "+usr)
    data = {"username": usr, "password": passwd}
    header = {"Content-Type": "application/json"}

    q = r.post(target, json=data, headers=header)

    if q.status_code==200:
        print(q.json())
        return True
    return False

def inject(usr,passwd,data,target):

    header = {"Content-Type": "application/json"}

    #https://[domain]/stu/<usr>
    print("inject "+target+usr)
    # print("Inject "+usr)
    q = r.put(target+usr, json=data, headers=header,auth=(usr,passwd))

    if q.status_code==200:
        print(q.json())
        return True
    return False


if __name__ == '__main__':
    url_01 = "http://127.0.0.1:5000/stu"
    url_02 = "http://127.0.0.1:5000/stu/"
    students = gen_stu()

    for i, stu in enumerate(students):
        # auth(**stu['auth'], target=url_01)
        usr, passwd = stu['auth']['usr'], stu['auth']['passwd']
        data = stu['info']

        print("begin "+usr)
        print(data)
        auth(usr, passwd, target=url_01)
        inject(usr, passwd, data,target=url_02)
        print("end ")
