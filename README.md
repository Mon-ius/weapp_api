# WEAPP_API

- Test Host: **xideas.herokuapp.com**
- DataBase: PostgreSQL
- Python Version: 3.7+

## UI

- Backend : Flat UI
- Weapp Client : WuxUI

## Features

### 1. User System

- basic auth
- session/token
- openid(wechat)

### 2. Role model

- database struct
  - name
  - password
  - email
  - phone
  - avatar
  - level
  - Cluster{}

- privilege
  - all : `*`
  - relevant: `r`
  - self: `s`

#### Primary Model(Level 0)

- privilege
  - View infomation(*)
  - Change infomation(*)
  - Delete infomation(*)

  - View event(*)
  - Change event(*)
  - Delete event(*)

#### Primary Model(Level 1)

- privilege
  - View infomation(s)
  - Change infomation(s)
  - Delete infomation(s)

  - View event(r)
  - Change event(r)
  - Delete event(r)

#### Primary Model(Level 2)

- privilege
  - View infomation(s)
  - Change infomation(s)
  - Delete infomation(s)

  - View event(s)
  - Change event(s)
  - Delete event(s)

### 3. Event model

- database struct
  - name
  - type
  - content
  - uuid
  - image
  - audio
  - Cluster{}

## API Test Mothed

### 1. File API test

#### Curl

`curl -F file1=@/home/monius/Pictures/Wallpapers/test.jpg -X POST http://127.0.0.1:5000/media`

#### Python

  ```python
  import requests
  r = requests.post('http://127.0.0.1:5000/media', files={'file1': open('/home/monius/Pictures/Wallpapers/test.jpg','rb')})
  ```

#### wx

```js
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

#### dart

> TO DO

## TestData Genetator

### Fake user info

```python
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

```

### Fake avator

```python
import io
from PIL import Image

avatar = Avatar.generate(size=128,string='example@sysnove.fr')
image = Image.open(io.BytesIO(avatar))
image.show()

```

### Fake audio

```python
import io
from gtts import gTTS

tts = gTTS(text='Good morning', lang='en')
mp3_fp = io.BytesIO()

tts.write_to_fp(mp3_fp)
t =Task.query.get(1)
t.title="adadsda"
db.session.commit()


a = Answer(title='1',body='2')
```