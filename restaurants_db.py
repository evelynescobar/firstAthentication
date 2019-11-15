import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class RestaurantsDB:
    def __init__(self):
        self.connection = sqlite3.connect("restaurants_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def insertRestaurant(self, name, date, location, pTitle, pBody):
        data = [name, date, location, pTitle, pBody]
        self.cursor.execute(
            "INSERT INTO posts (name, date, location, pTitle, pBody) VALUES (?, ?, ?, ?, ?)", data)
        self.connection.commit()

    def insertUser(self, f_name, l_name, email, hashed):
        data = [f_name, l_name, email, hashed]
        self.cursor.execute(
            "INSERT INTO newUser (f_name, l_name, email, hashed) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def getUsers(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM newUser WHERE email = ?", data)
        result = self.cursor.fetchone()
        return result

    def getRestaurants(self):
        self.cursor.execute("SELECT * FROM posts")
        result = self.cursor.fetchall()
        return result
        # Return a dict
        # sqlite3pythOn

    def getOneRestaurant(self, restaurant_id):
        data = [restaurant_id]
        self.cursor.execute("SELECT * FROM posts WHERE id = ?", data)
        result = self.cursor.fetchone()
        return result

    def deletePost(self, id):
        if self.getOneRestaurant(id) != None:
            self.cursor.execute("DELETE FROM posts WHERE id = ?", [id])
            self.connection.commit()
            return True
        else:
            return False

    def editPost(self, id, name, date, location, pTitle, pBody):
        if self.getOneRestaurant(id) != None:
            self.cursor.execute("UPDATE posts SET name=?, date=?, location=?, pTitle=?, pBody=? WHERE id = ?", [
                                name, date, location, pTitle, pBody, id])
            self.connection.commit()
            return True
        else:
            return False
