#Authentication is important because it enables organizations to keep their networks secure by permitting only authenticated users (or processes) to access its protected resources, which may include computer systems, networks, databases, websites and other network-based applications or services. I created a login and sign up form for my "social media" project. I used: Node.js Vue.js CSS and HTML. I used MySqlite for my Database.

**Posts**

Attributes:

* name (string)
* date (string)
* location (string)
* pTitle (string)
* pBody (string)

**newUser**

Attributes:

* f_name (string)
* l_name (string)
* email (string)
* hashed (string)

## Schema

```sql
CREATE TABLE posts (
id INTEGER PRIMARY KEY,
name TEXT,
date TEXT,
location TEXT,
pTitle, TEXT,
pBody, TEXT);
CREATE TABLE newUser (
id INTEGER PRIMARY KEY,
f_name TEXT,
l_name TEXT,
email TEXT,
hashed TEXT);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve posts collection | GET    | /posts
Retrieve one user          | GET    | /newUsers
Retrieve posts member     | GET    | /posts/*\<id\>*
Create posts member       | POST   | /posts
Create user               | POST   | /newUsers
Start Session             | POST   | /sessions
Update posts member       | PUT    | /posts/*\<id\>*
Delete posts member       | DELETE | /posts/*\<id\>*
