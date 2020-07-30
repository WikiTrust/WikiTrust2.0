from mongoengine import *
connect('Test', host='localhost', port=27017)

class User(DynamicDocument):
    authorID: IntField(required=True, unique=True)
    rep: FloatField(default=0)

class Cache(DynamicDocument):
    rev_1: ReferenceField('Revision', required=True)
    rev_2: ReferenceField('Revision', required=True)
    distance: FloatField(required=True)

class Revision(DynamicDocument):
    author: ReferenceField('User', required=True)
    revisionID: IntField(required=True, unique=True)
    pageID: IntField(required=True)
    
class Block(DynamicDocument):
    pageID: IntField(required=True)
    revisions: ListField(ReferenceField('Revision'))
    nextBlock: ReferenceField('Block')
    prevBlock: ReferenceField('Block')