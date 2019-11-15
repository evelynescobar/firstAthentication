# f19-authentication-evelynescobar
f19-authentication-evelynescobar created by GitHub Classroom
# My Project

## Authentication

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
