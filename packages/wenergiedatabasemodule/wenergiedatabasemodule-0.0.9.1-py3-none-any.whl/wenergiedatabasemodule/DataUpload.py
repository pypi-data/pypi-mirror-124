import firebase_admin
from firebase_admin import db

class dataupload :
    def initialize_firebase(credentiallocation,databaseurl,basepath):
        cred = credentials.Certificate(credentiallocation)
        firebase_admin.initialize_app(cred, {databaseurl})
        ref= db.reference(basepath)
        return ref
    def helloworld():
        return "Hello world"
