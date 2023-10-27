# IPM Learning Platform
Sept 16 update

LINK TO GUIDE -> https://gist.github.com/mswaringen/cdc1bc46e25863fd14314a1a858e33a6

### Dev commands

NEWWWWw

running:
- python 3.9.9
- sqlite for local db, no need for postgres

pipenv commands
- `pipenv shell`
- `deactivate`
- `pipenv install <package>`

start server
- `python manage.py runserver`

OLDDDDDDDD
Always start the PSQL server locally
- `sudo service postgresql start`
- `export DJANGO_READ_DOT_ENV_FILE=True`
- `python manage.py runserver`

### Models
- Data Model in Kitt: https://kitt.lewagon.com/db/39345
- Proxy Models: https://dev.to/zachtylr21/model-inheritance-in-django-m0j
- https://learndjango.com/tutorials/django-best-practices-referencing-user-model

### Checkout
- Cart: https://codepen.io/abdelrhman/pen/BaNPVJO

### Payment
- https://bigflip.id/
- https://docs.flip.id/

### Create local Postgres DB
- `sudo -i -u postgres`
- `psql`
- `CREATE DATABASE "ipm_learning" WITH OWNER = "ipm_learning"  ENCODING = 'UTF8';`
- `\q`

#### Shell
- `python manage.py shell`
- `from ipm_learning.users.models import User`
- `User.objects.all()`

### Front End
- https://github.com/tailwindlabs/tailwindcss-typography
- https://markdown-it.github.io/
- https://codewithstein.com/django-markdown-tutorial-a-simple-blog-example/
- https://gist.github.com/clhefton/a3535e64a9b314339a2e1aabdfb4d1c7


Quizzes:
- https://medium.com/swlh/overview-building-a-full-stack-quiz-app-with-django-and-react-57fd07449e2f#f508




Course:
- Title
- Desc
- Price


Content
- Title
- Desc
- Order

Video (Content)
- youtube_id

Event (Content)
- event_url
- event_date

Text (Content)
- text_content

Quiz (Content)
- Question 1



Apps:
- User
- Content



## OLD

Models:

Course: 
- multiple Content Blocks
- price

Content Blocks
- content type: video / event / blog post
- data: 
    video: {youtube_video_id: 324239847293}
    blog post: { title, desc, image }

Video
- video_id(s)

Event:
- live_meeting_id(s)

BlogPost
- title
- desc

Content
- content: course / event
- data: {youtube_video_id: 324239847293}
- price

Course:
- video_id(s)

Event:
- video_id(s)
- live_meeting_id(s)

Video
- Title
- youtube_id

Live Meeting
- Title
- Desc
- Data/time
- Zoom_id
- Zoom_pwd


## Payment

Course (event)
- price
- currency
- id
- name

Purchase
 - User (FK)
 - stripe_purchase_id
 - Content (fk)
 - status


random shit
