import os
import base64


class SessionStore:

    def __init__(self):
        # Need a dictTIONARY OF DICTIONARIES
        self.sessions = {}

    # ADD A NEW SISSION TO THE SESSION STORE
    def createSession(self):
        newSessionID = self.generateSessionId()
        self.sessions[newSessionID] = {}
        return newSessionID

    # RETRIEVE AND EXISTING SESSION fROM THE SESSION STORE
    def getSession(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None

    # WE NEED TO CREATE A NEW SESSION ID
    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr
