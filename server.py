from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from restaurants_db import RestaurantsDB
from http import cookies
from session_store import SessionStore
import json
from passlib.hash import bcrypt

SESSION_STORE = SessionStore()


class MyRequestHandler (BaseHTTPRequestHandler):

    def loggedIn(self):
        if "userId" in self.session:
            print("LOGGED IN")
            return True
        else:
            print("NOT LOGGED IN")
            return False

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            print("cOOkie lOaded")
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session(self):
        self.load_cookie()
        # if session ID is in the cookie
        if "sessionId" in self.cookie:
            print("SessiOn id fOund")
            sessionId = self.cookie["sessionId"].value
            # if session ID matches in the session store
            # save the session for use later (data memeber)
            self.session = SESSION_STORE.getSession(sessionId)
            # otherwise, if session ID is NOT in the session ste
            if self.session == None:
                sessionId = SESSION_STORE.createSession()
                self.session = SESSION_STORE.getSession(sessionId)
                self.cookie["sessionId"] = sessionId
                print("set cookie with sessionId")

        else:
            sessionId = SESSION_STORE.createSession()
            self.session = SESSION_STORE.getSession(sessionId)
            self.cookie["sessionId"] = sessionId
            print("set cookie with sessionId but nt frm ckkie")

            # Create a new session
            # set the new session ID into the new cookie
        # otherwise if session ID is NoT in the cookie
            # Create a new session
            # set the new session ID into the new cookie

    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)

        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

    def do_GET(self):
        self.load_session()
        if self.loggedIn():
            if self.path == "/posts":
                print("SENT ALL THE RESTAURANT DATA")
                self.handleRestaurantsRetrieveCollection()
            elif self.path.startswith("/posts/"):
                self.handleRestaurantRetrieveMember()
            elif self.path == "/newUsers":
                pass
            else:
                self.handleNotFound()
        else:
            if self.path == "/posts":
                self.send_response(401)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
            else:
                self.send_response(422)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()

    def do_POST(self):
        self.load_session()
        if self.loggedIn():
            if self.path == "/posts":
                self.handleRestaurantCreate()
            else:
                self.handleNotFound()
        else:
            if self.path == "/newUsers":
                self.createNewUser()
            elif self.path == "/sessions":
                self.checkUser()
            else:
                self.handleNotFound()

    def do_PUT(self):
        self.load_session()
        parts = self.path.split("/")[1:]
        collection = parts[0]
        if len(parts) > 1:
            id = parts[1]
        else:
            id = None
        db = RestaurantsDB()
        if collection == "posts":
            if id == None or db.getRestaurants == None:
                self.handleNotFound()
            else:
                self.handleUpdate(id)
        else:
            self.handleNotFound()
        return

    def handleUpdate(self, id):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("BODY:", body)
        parsed_body = parse_qs(body)
        print("PARSED BODY:", parsed_body)
        name = parsed_body["name"][0]
        date = parsed_body["date"][0]
        location = parsed_body["location"][0]
        pTitle = parsed_body["pTitle"][0]
        pBody = parsed_body["pBody"][0]

        db = RestaurantsDB()
        db.editPost(id, name, date, location, pTitle, pBody)
        self.send_response(201)
        #self.send_header("Content-Type", "application/json")
        # self.send_header("Access-Control-Allow-Origin")
        self.end_headers()
        return

    def handleDelete(self, id):
        db = RestaurantsDB()
        if db.deletePost(id):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Updated", "utf-8"))
        else:
            self.handleNotFound()

    def do_DELETE(self):
        # if "userId" nOT in self.sessiOn:
            # self.handle(401)
            # return
        self.load_session()
        parts = self.path.split("/")[1:]
        collection = parts[0]
        if len(parts) > 1:
            id = parts[1]
        else:
            id = None
        db = RestaurantsDB()
        if collection == "posts":
            if id == None or db.getRestaurants == None:
                self.handleNotFound()
            else:
                self.handleDelete(id)
        else:
            self.handleNotFound()
        return

    def handleNotFound(self):
        self.send_error(404)
        self.end_headers()
        pass

    def handleRestaurantsRetrieveCollection(self):
        # respOnds accOrdingly
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        # sends bOdy
        db = RestaurantsDB()
        restaurants = db.getRestaurants()
        self.wfile.write(bytes(json.dumps(restaurants), "utf-8"))

    def handleRestaurantRetrieveMember(self):
        parts = self.path.split("/")
        restaurant_id = parts[2]

        db = RestaurantsDB()
        restaurant = db.getOneRestaurant(restaurant_id)
        if restaurant != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(restaurant), "utf-8"))
        else:
            self.handleNotFound()

    def handleRestaurantCreate(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("BODY:", body)
        parsed_body = parse_qs(body)
        print("PARSED BODY:", parsed_body)

        # saves the restaurant int the database
        name = parsed_body["name"][0]
        date = parsed_body["date"][0]
        location = parsed_body["location"][0]
        pTitle = parsed_body["pTitle"][0]
        pBody = parsed_body["pBody"][0]

        db = RestaurantsDB()
        db.insertRestaurant(name, date, location, pTitle, pBody)

        # RESTAURANTS.append(name)

        self.send_response(201)
        #self.send_header("Content-Type", "application/json")
        # self.send_header("Access-Control-Allow-Origin")
        self.end_headers()
        pass

    def createNewUser(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)
        print("PARSED BODY:", parsed_body)

        f_name = parsed_body["f_name"][0]
        l_name = parsed_body["l_name"][0]
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]

        db = RestaurantsDB()
        user = db.getUsers(email)
        if user == None:
            hashed = bcrypt.hash(password)
            print(hashed)
            db = RestaurantsDB()
            db.insertUser(f_name, l_name, email, hashed)
            user = db.getUsers(email)
            self.session['userId'] = user['id']

            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(422)
            self.end_headers()

    def checkUser(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        parsed_body = parse_qs(body)

        email = parsed_body["email"][0]
        password = parsed_body["hashed"][0]

        db = RestaurantsDB()
        user = db.getUsers(email)
        if user != None:
            if bcrypt.verify(password, user["hashed"]):
                print("It matches!")
                self.session["userId"] = user["id"]
                print("userId placed in sessiOn")
                self.send_response(201)
                self.end_headers()
            else:
                print("It does not match")
                self.send_error(401)
                self.end_headers()
        else:
            self.handleNotFound()


def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening...")
    server.serve_forever()


run()
