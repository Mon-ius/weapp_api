# WEAPP_API

## PreKnowledge

#### Host: **api.xxx.com**
#### DataBase: PostgreSQL
#### Python Version: 3.6+



## Features

#### 1. User Login

- add user
- login user
- token access 

#### 2. Admin Control

- View  users
- Add/End tasks
- Give comment


#### 3. Public Info Interaction

- user submmit self informations
- user submit task materils
- user view self tasks
- View teachers



## Deploy

#### 1. Create New virtual env (OPTIONAL)

- For Anaconda
  > conda create -n api python=3.6
  > source activate api

- For virtualenv
  > virtualenv -p /usr/bin/python3.6  api
  > . api/bin/activate

#### 2. Install requrements

> pip install -r requirements.txt

#### 3. Run

> python ./run.py

## Heroku

### git push heroku deploy:master

## Usage

==========  ===============================================  =============================
HTTP 方法   URL                                               动作
==========  ===============================================  ==============================
GET         http://[hostname]/todo/api/v1.0/tasks                 Get the tasks list
GET         http://[hostname]/todo/api/v1.0/tasks/[task_id]       检索某个任务
POST        http://[hostname]/todo/api/v1.0/tasks                 创建新任务
PUT         http://[hostname]/todo/api/v1.0/tasks/[task_id]       更新任务
DELETE      http://[hostname]/todo/api/v1.0/tasks/[task_id]       删除任务
==========  ================================================ =============================

==========  ===============================================  =============================
HTTP 方法   URL                                               动作
==========  ===============================================  ==============================
GET         http://[hostname]/todo/api/v1.0/answers                检索回答列表
GET         http://[hostname]/todo/api/v1.0/answers/[answer_id]    检索某个回答
POST        http://[hostname]/todo/api/v1.0/answers                创建回答
PUT         http://[hostname]/todo/api/v1.0/answers/[answer_id]    更新回答
DELETE      http://[hostname]/todo/api/v1.0/answers/[answer_id]    删除回答
==========  ================================================ =============================


==========  ===============================================  =============================
HTTP 方法   URL                                               动作
==========  ===============================================  ==============================
GET         http://[hostname]/auth/api/v1.0/answers                检索回答列表
GET         http://[hostname]/todo/api/v1.0/answers/[answer_id]    检索某个回答
POST        http://[hostname]/todo/api/v1.0/answers                创建回答
PUT         http://[hostname]/todo/api/v1.0/answers/[answer_id]    更新回答
DELETE      http://[hostname]/todo/api/v1.0/answers/[answer_id]    删除回答
==========  ================================================ =============================

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



curl -u monius:fuckadmin -i -X DELETE http://127.0.0.1:5000/stu
curl -u monius:fuckadmin -i -X GET http://127.0.0.1:5000/stu/1
curl  -i -H "Content-Type: application/json" -X POST -d '{"username":"monius","password":"fuckadmin"}' http://127.0.0.1:5000/stu
curl -u monius:fuckadmin -i -H "Content-Type: application/json" -X POST -d '{"username":"quryfine","realname":"quryfine","engname":"fuck"}' http://127.0.0.1:5000/stu/1

curl -u monius:fuckadmin -i -H "Content-Type: application/json" -X POST -d '{"username":"quryfine","realname":"quryfine","engname":"fuck","email":"fuckyou@asshole.com","exam_type":"1","score":"32.0"}' http://127.0.0.1:5000/stu/1

curl -u miguel:python -i -X GET http://127.0.0.1:5000/tasks
curl -u miguel:python -i -X GET http://127.0.0.1:5000/tasks/2
curl -u miguel:python -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book","body":"2333","done":"false"}' http://127.0.0.1:5000/tasks