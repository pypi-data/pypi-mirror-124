import firebase_admin
from firebase_admin import *
from firebase_admin import db
class dataupload :
    def initialize_firebase(credentiallocation,databaseurl,basepath,auth):
        cred = credentials.Certificate(credentiallocation)
        firebase_admin.initialize_app(cred, {
        'databaseURL': databaseurl,
        'databaseAuthVariableOverride': {'uid': auth}
        })
        ref = db.reference(basepath)
        return ref
    def helloworld():
        return "Hello world"
    def uploaddata(ref,path,dictonartname):
        return ref.child(path).update(dictonartname)
