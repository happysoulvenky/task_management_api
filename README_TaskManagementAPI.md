\# 🗂 Task Management API



A production-ready \*\*Flask + Celery + MySQL + Redis\*\* based Task Management API with background job processing.  

This project supports task creation, scheduling, and status tracking using Celery workers.



---



\## 🚀 Features



\- Create, update, and delete tasks

\- Schedule tasks to run in the future

\- Background job processing with \*\*Celery + Redis\*\*

\- MySQL as the primary database

\- JWT authentication (optional)

\- Dockerized for easy deployment

\- Postman collection included



---



\## 📦 Tech Stack



\- \*\*Flask\*\* – API framework

\- \*\*Flask-SQLAlchemy\*\* – ORM

\- \*\*Celery\*\* – Background job processing

\- \*\*Redis\*\* – Celery broker

\- \*\*MySQL\*\* – Relational database

\- \*\*Docker \& Docker Compose\*\* – Deployment



---



\## 📂 Project Structure

task\_management\_api/

│   .dockerignore

│   .env

│   celerybeat-schedule

│   celerybeat-schedule-shm

│   celerybeat-schedule-wal

│   config.py

│   docker-compose.yml

│   Dockerfile

│   requirements.txt

│   run.py

│   

├───.vscode

│       launch.json

│

├───app

│   │   celery\_app.py

│   │   extensions.py

│   │   models.py

│   │   \_\_init\_\_.py

│   │

│   ├───routes

│   │   │   auth.py

│   │   │   main.py

│   │   │   projects.py

│   │   │   tasks.py

│   │   │   \_\_init\_\_.py

│   │        

│   │

│   ├───services

│   │   └───email\_service.cpython-311.pyc

│   │           

│   │

│   ├───tasks

│   │   │   email\_tasks.py

│   │   │

│   │   └───\_\_pycache\_\_

│   │           demo\_tasks.cpython-311.pyc

│   │

│   ├───utils

│   │   │   email\_utils.py

│

├───celery

│       celery\_config.py

│\_\_\_\_\_\_\_celery\_task.py



\## 🗄 Database Schema



ER Diagram:

User

----

id (PK)

email (unique, not null)

password (not null)



Relationships:

\- 1 User → Many Projects

\- 1 User → Many Tasks (as assignee)





Project

-------

id (PK)

name (not null)

description

created\_at (default: current UTC time)

user\_id (FK → User.id, not null)



Relationships:

\- 1 Project → Many Tasks





Task

----

id (PK)

title (not null)

description

status (default: "pending")

priority (default: 3)

due\_date

created\_at (default: current UTC time)

project\_id (FK → Project.id, not null)

assigned\_to\_id (FK → User.id, nullable)





Entity Relationships:

----------------------

User.id ────< Project.user\_id

User.id ────< Task.assigned\_to\_id

Project.id ────< Task.project\_id



```



---



\## ⚙️ Setup Instructions



\### \*\*1️⃣ Local Development\*\*



\#### Prerequisites

\- Python 3.10+

\- MySQL 8+

\- Redis

\- Docker (optional for local run)



\#### Clone Repo

```bash

git clone https://github.com/happysoulvenky/task-management-api.git

cd task-management-api

```



\#### Create Virtual Environment \& Install Dependencies

```bash

python -m venv venv

source venv/bin/activate  # On Mac/Linux

venv\\Scripts\\activate   # On Windows



pip install -r requirements.txt

```



\#### Set Environment Variables

Create a `.env` file in the root directory:

```env

FLASK\_ENV=development

SQLALCHEMY\_DATABASE\_URI=mysql://dbuser:dbpass@localhost/taskdb

REDIS\_URL=redis://localhost:6379/0

JWT\_SECRET\_KEY=supersecretkey


**Add email sender email id and APP password to .env file**

```



\#### Run Migrations

```bash

flask db upgrade

```



\#### Start Services Locally

```bash

flask run

celery -A app.celery worker --loglevel=info

celery -A app.celery beat --loglevel=info

```



---



\### \*\*2️⃣ Docker Deployment (Production)\*\*



```bash

docker compose -f docker-compose.prod.yml up -d --build

```



\*\*Production `.env` example:\*\*

```env

FLASK\_ENV=production

SQLALCHEMY\_DATABASE\_URI=mysql://dbuser:dbpass@mydb/taskdb

REDIS\_URL=redis://myredis:6379/0

JWT\_SECRET\_KEY=supersecretkey

```



---
Testing the API 

step 1 register with username and password 
step-2 login with username and password 
            if login successful you will get access_token 

All other task access_token is required 
in header section under authorization 


step-3 create a task 
step-4 get all tasks 
step-5 delete a task 


I have made the postman request public, you can acces them 
 

You can import the provided \*\*`TaskManagementAPI.postman\_collection.json`\*\* into Postman for quick testing.



https://www.postman.com/maintenance-astronomer-14710862/task-management-api/collection/j0a3aui/task-management-api

---



\## 🛠 Troubleshooting



\- \*\*MySQL connection error inside Docker\*\*  

&nbsp; Use the Docker service name (`mydb`) instead of `localhost` in `SQLALCHEMY\_DATABASE\_URI`.

\- \*\*Celery not processing tasks\*\*  

&nbsp; Ensure Redis is running and `REDIS\_URL` is correct.



---





