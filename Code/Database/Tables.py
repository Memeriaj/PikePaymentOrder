import peewee
import json
from playhouse.proxy import Proxy

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
    def jsonEncode(self):
        payments = []
        for pay in PaymentOrder.select().where(PaymentOrder.user == self.id):
            payments.append(pay.id)
        return {"id": self.id, "firstName": self.firstName, \
                "lastName": self.lastName, "email": self.email, \
                "paymentOrders": payments}
    
class Quarter(BaseModel):
    start = peewee.DateField()
    end = peewee.DateField()
    def jsonEncode(self):
        return {"id": self.id, "start": str(self.start), "end": str(self.end)}

class Department(BaseModel):
    name = peewee.CharField()
    quarter = peewee.ForeignKeyField(Quarter)
    budget = peewee.DoubleField()
    parent = peewee.ForeignKeyField('self', related_name='children', null=True)
    def jsonEncode(self):
        parentObj = None
        if self.parent:
            parentObj = self.parent.id
        chairmen = []
        for person in Chairmen.select().where(Chairmen.department == self.id):
            chairmen.append(person.user.id)
        payments = []
        for pay in PaymentOrder.select().where(PaymentOrder.department == self.id):
            payments.append(pay.id)
        approved = []
        for depart in Approvals.select().where(Approvals.department == self.id):
            approved.append(depart.id)
        return {"id": self.id, "name": self.name, "quarter": self.quarter.id, \
                "budget": self.budget, "parent": parentObj, \
                "chairmen": chairmen, "paymentOrders": payments, \
                "approved": approved}

class Chairmen(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
    def jsonEncode(self):
        return {"id": self.id, "user": self.user.id, \
                "department": self.department.id}
    
class PaymentOrder(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
    description = peewee.TextField()
    paid = peewee.BooleanField()
    flagged = peewee.BooleanField()
    def jsonEncode(self):
        lines = []
        for line in LineItem.select().where(LineItem.paymentOrder == self.id):
            lines.append(line.id)
        approved = []
        for depart in Approvals.select().where(Approvals.paymentOrder == self.id):
            approved.append(depart.id)
        return {"id": self.id, "user": self.user.id, \
                "department": self.department.id, \
                "description": self.description, "paid": self.paid, \
                "flagged": self.flagged, "lineItems": lines, \
                "approvedBy": approved}
    
class LineItem(BaseModel):
    paymentOrder = peewee.ForeignKeyField(PaymentOrder)
    description = peewee.TextField()
    amount = peewee.DoubleField()
    def jsonEncode(self):
        receipts = []
        for receipt in LineReceipt.select().where(LineReceipt.lineItem == self.id):
            receipts.append(receipt.id)
        return {"id": self.id, "paymentOrder": self.paymentOrder, \
                "description": self.description, "amount": self.amount,\
                "receipts": receipts}
    
class Receipt(BaseModel):
    image = peewee.CharField()
    location = peewee.CharField()
    def jsonEncode(self):
        return {"id": self.id, "image": self.image, "location": self.location}
    
class LineReceipt(BaseModel):
    lineItem = peewee.ForeignKeyField(LineItem)
    receipt = peewee.ForeignKeyField(Receipt)
    def jsonEncode(self):
        return {"id": self.id, "lineItem": self.lineItem.id, \
                "receipt": self.receipt.id}
    
class Approvals(BaseModel):
    department = peewee.ForeignKeyField(Department)
    paymentOrder = peewee.ForeignKeyField(PaymentOrder)
    status = peewee.CharField()
    def jsonEncode(self):
        return {"id": self.id, "department": self.department.id, \
                "paaymentOrder": self.paymentOrder.id, "status": self.status}
        
    

class TablesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (User, Quarter, Department, Chairmen, PaymentOrder,\
                            LineItem, Receipt, LineReceipt, Approvals)):
            return obj.jsonEncode()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
