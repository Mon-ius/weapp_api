# WEAPP_API

- Test Host: **xideas.herokuapp.com**
- DataBase: PostgreSQL
- Python Version: 3.7+

## UI

- Backend : Flat UI
- Weapp Client : WuxUI

## Features

### 1. Models

#### Student

- OpenID based registeration
- Session based login

#### Teacher

coming soon
- Sign up
- Certification
- Generate avatar
- Bind wechat

### 2. Admin Pannel

- Start with admin account
- Data explores: students/teachers/tasks

### 3. System

- Image process
- Audio process
- Files process

### 4. Files

#### Curl 
```
curl -F file1=@/home/monius/Pictures/Wallpapers/test.jpg -X POST http://127.0.0.1:5000/media
```

#### Python Requests 
```
import requests
r = requests.post('http://127.0.0.1:5000/media', files={'file1': open('/home/monius/Pictures/Wallpapers/test.jpg','rb')})
```

#### Weapp

```
    wx.uploadFile({
      url: 'http://127.0.0.1:5000/media',
      filePath: "/home/monius/Pictures/Wallpapers/test.jpg",
      name: 'file1',
      success (res){
        const data = res.data
        //do something
      }
    })

```

## Deploy

### (Option 1.) Bare Linux

#### 1. Create New virtual env (OPTIONAL)

- For Anaconda
  > conda create -n api python=3.7
  > source activate api

- For virtualenv
  > virtualenv -p /usr/bin/python3.7  api
  > . api/bin/activate

#### 2. Install requrements

> pip install -r requirements.txt

#### 3. Run

> python ./run.py

### (Option 2.) Heroku

#### 1. Heroku
#### 2. Create app
#### 3. Necessary files
#### 3. Upload via Heroku CLI



```
==========  ===============================================  =============================
HTTP Method   URL                                               Actions
==========  ===============================================  ==============================
GET         http://[hostname]/stu/                           Get the students list
GET         http://[hostname]/stu/[stu_id]                   Get a student info
POST        http://[hostname]/stu/                           Create a new student 
PUT         http://[hostname]/stu/[stu_id]                   Update a student info
DELETE      http://[hostname]/stu/[stu_id]                   Delete a student
==========  ================================================ =============================

==========  ===============================================  =============================
HTTP Method   URL                                               Actions
==========  ===============================================  ==============================
GET         http://[hostname]/answers/                        Get the answers list
GET         http://[hostname]/answers/[answer_id]             Get an answers info
POST        http://[hostname]/answers/                        Create a new student
PUT         http://[hostname]/[answer_id]                     Update a student info
DELETE      http://[hostname]/answers/[answer_id]             Delete a student
==========  ================================================ =============================


==========  ===============================================  =============================
HTTP Method   URL                                               Actions
==========  ===============================================  ==============================

POST        http://[hostname]/weapi/                          create a new user or token

==========  ================================================ =============================



```
## TestData
from avatar_generator import Avatar
from faker import Faker
f = Faker()

for _ in range(100):
  fakes=[
  f.name(),
  f.first_name(),
  f.name_male(),
  f.email(),
  f.future_date(),
  f.random_int()%2,
  f.random_int()%1000/10
  ]
  u = Student(
    username=fakes[0],
    realname=fakes[1],
    engname=fakes[2],
    email=fakes[3],
    exam_date=fakes[4],
    exam_type=fakes[5],
    score=fakes[6],
    avatar=Avatar.generate(size=64,string=fakes[3])
    )
  db.session.add(u)
  db.session.commit()

for _ in range(10):
  fakes=[
  f.name(),
  f.first_name(),
  f.email(),
  f.future_date(),
  f.random_int()%2,
  f.random_int()%4
  ]
  t = Teacher(
    username=fakes[0],
    engname=fakes[1],
    email=fakes[2],
    teach_date=fakes[3],
    teach_type=fakes[4],
    teach_type_part=fakes[5],
    avatar=Avatar.generate(size=64,string=fakes[2])
    )
  db.session.add(t)
  db.session.commit()

for _ in range(10):
  fakes=[
  f.domain_word(),
  f.text(),
  ]
  tk = Task(
    title=fakes[0],
    body=fakes[1],
    picture=Avatar.generate(size=64,string=fakes[0])
    )
  db.session.add(tk)
  db.session.commit()


for _ in range(10):
  fakes=[
  f.domain_word(),
  f.text(),
  ]
  a = Answer(
    title=fakes[0],
    body=fakes[1],
    picture=Avatar.generate(size=64,string=fakes[0])
    sound=Avatar.generate(size=64,string=fakes[1])
    )
  db.session.add(a)
  db.session.commit()



import io
from PIL import Image

avatar = Avatar.generate(size=128,string='example@sysnove.fr')
image = Image.open(io.BytesIO(avatar))
image.show()

import io
from gtts import gTTS

tts = gTTS(text='Good morning', lang='en')
mp3_fp = io.BytesIO()

tts.write_to_fp(mp3_fp)


t =Task.query.get(1)
t.title="adadsda"
db.session.commit()


a = Answer(title='1',body='2')

curl -u miguel:python -i -X DELETE http://127.0.0.1:5000/tasks/16
curl -u miguel:python -i -H "Content-Type: application/json" -X PUT -d '{"title":"shutdown","body":"2333","done":"false"}' http://127.0.0.1:5000/tasks/15



curl -u monius:fuckadmin -i  -X DELETE http://127.0.0.1:5000/stu
curl -u monius:fuckadmin -i -X GET http://127.0.0.1:5000/stu/1
curl -u eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzODM4MTA2MiwiZXhwIjoxNTM4MzgxNjYyfQ.eyJpZCI6MX0.uK3u55YGBz8QIQ63E6Sa6TiYdVWsrlU0Iw_9vWmG_Ro -i -X GET http://127.0.0.1:5000/stu/1


curl  -i -H "Content-Type: application/json" -X POST -d '{"username":"monius","password":"fuckadmin"}' http://127.0.0.1:5000/stu
curl  -i -H "Content-Type: application/json" -X POST -d '{"js_code":"monius"}' http://127.0.0.1:5000/weapi
curl  -i -H "Content-Type: application/json" -X POST -d '{"appid":"monius","secret":"secret","js_code":"fuckadmin"}' http://127.0.0.1:5000/weapi
curl -u monius:fuckadmin -i -H "Content-Type: application/json" -X POST -d '{"nickname":"quryfine","realname":"quryfine","engname":"fuck"}' http://127.0.0.1:5000/stu/1


curl -u monius:fuckadmin -i -H "Content-Type: application/json" -X POST -d '{"username":"quryfine","realname":"quryfine","engname":"fuck","email":"fuckyou@asshole.com","exam_type":"1","score":"32.0"}' http://127.0.0.1:5000/stu/1

curl -u miguel:python -i -X GET http://127.0.0.1:5000/tasks
curl -u miguel:python -i -X GET http://127.0.0.1:5000/tasks/2
curl -u miguel:python -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book","body":"2333","done":"false"}' http://127.0.0.1:5000/tasks


https://segmentfault.com/a/1190000015310626

### Test parameters

curl -i -X GET http://127.0.0.1:5000/res
curl -i -H "Content-Type: application/json" -X POST -d '{"id":"1233"}' http://127.0.0.1:5000/res
curl -i -X PUT http://127.0.0.1:5000/res
curl -i -X DELETE http://127.0.0.1:5000/res