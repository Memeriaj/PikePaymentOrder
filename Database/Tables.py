import peewee
from peewee import *

db = peewee.MySQLDatabase('PikePaymentOrder', user='root', passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    firstName = peewee.CharField()
    lastName = peewee.CharField()
    email = peewee.CharField()
    passHash = peewee.CharField()
    passSalt = peewee.CharField()
    
class Quarter(BaseModel):
    start = peewee.DateField()
    end = peewee.DateField()

class Department(BaseModel):
    name = peewee.CharField()
    quarter = peewee.ForeignKeyField(Quarter)
    budget = peewee.DoubleField()
    parent = peewee.ForeignKeyField('self', related_name='children', null=True)

class Chairmen(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
    
# class DepartmentOrganization(BaseModel):
#     parent = peewee.ForeignKeyField(Department, related_name='parentDepartment')
#     child = peewee.ForeignKeyField(Department, related_name='childDepartment')
    
class PaymentOrder(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
    description = peewee.TextField()
    paid = peewee.BooleanField()
    flagged = peewee.BooleanField()
    
class LineItem(BaseModel):
    paymentOrder = peewee.ForeignKeyField(PaymentOrder)
    description = peewee.TextField()
    amount = peewee.DoubleField()
    
class Receipt(BaseModel):
    image = peewee.CharField()
    location = peewee.CharField()
    
class LineReceipt(BaseModel):
    lineItem = peewee.ForeignKeyField(LineItem)
    receipt = peewee.ForeignKeyField(Receipt)
    
class Approvals(BaseModel):
    user = peewee.ForeignKeyField(User)
    paymentOrder = peewee.ForeignKeyField(PaymentOrder)
    status = peewee.CharField()
    



# class Book(peewee.Model):
#     author = peewee.CharField()
#     title = peewee.TextField()
# 
#     class Meta:
#         database = db
