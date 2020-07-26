# starnavi

***A simple REST API that represents how social network works.***

---
**Usage**

- Install docker and git on your machine

- Clone this repository via http `https://github.com/tuipik/starnavi.git`
or via ssh `git@github.com:tuipik/starnavi.git`

- In terminal open directory with source code of repo

- Build or pull docker image. In terminal: `make build` or `make pull`

- Start local server by `make run` command in Terminal

- To start tests use command `make test`
---
**Endpoints:**


sign up: `http://0.0.0.0:8000/api/v1/user/signup/`

sign in: `http://0.0.0.0:8000/api/v1/user/signin/`

user profile: `http://0.0.0.0:8000/api/v1/user/profile/`

post list or create post: `http://0.0.0.0:8000/api/v1/posts/`

to like post: `http://0.0.0.0:8000/api/v1/posts/1/like/`

user filtered analitics: `http://0.0.0.0:8000/api/v1/user/analitics/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
  
---
**Postman Collection:**

starnavi.postman_collection.json in the root directory of the repo