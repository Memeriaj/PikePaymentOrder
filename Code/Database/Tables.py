import peewee
import json

db = peewee.MySQLDatabase('PikePaymentOrder', user='root', passwd='')

class BaseModel(peewee.Model):
    class Meta:
        database = db
    
    neededNewAttribute = []
    foreigns = {}
    
    '''Checks for attributes that are needed for the creation of an entry to 
    the table.  If an attribute is missing then the name of that attribute is 
    returned, otherwise False is returned.'''
    def checkNotInNewDictionary(self, args):
        for attribute in self.neededNewAttribute:
            if attribute not in args:
                return attribute
        return False 
                
    '''Returns the id of the newly created entry to the table.'''   
    def createNew(self, args):
#         print "CREATING"
        for attribute in self.neededNewAttribute:
#             print attribute + ":  " + str(args[attribute][0])
            if attribute in self.foreigns:
                type = self.foreigns[attribute]
                setattr(self, attribute, type.select().where(type.id == args[attribute][0]))
            else:
                setattr(self, attribute, args[attribute][0])
        self.save()
        return self.id

class User(BaseModel):
    firstName = peewee.CharField()
    lastName = peewee.CharField()
    email = peewee.CharField()
    passHash = peewee.CharField()
    passSalt = peewee.CharField()
    
    neededNewAttribute = ['firstName', 'lastname', 'email', 'password']   
    
    def jsonEncode(self):
        payments = []
        for pay in PaymentOrder.select().where(PaymentOrder.user == self.id):
            payments.append(pay.id)
        return {"id": self.id, "firstName": self.firstName, \
                "lastName": self.lastName, "email": self.email, \
                "paymentOrders": payments}             
        
    def createNew(self, args):
        for attribute in self.neededNewAttribute:
            if attribute == 'password':
                pass
#                 generate salt, hash password, save both
            else:
                setattr(self, attribute, args[attribute])
        self.save()
        return self.id
    
class Quarter(BaseModel):
    start = peewee.DateField()
    end = peewee.DateField()
    
    neededNewAttribute = ['start', 'end']   
    
    def jsonEncode(self):
        return {"id": self.id, "start": str(self.start), "end": str(self.end)}

class Department(BaseModel):
    name = peewee.CharField()
    quarter = peewee.ForeignKeyField(Quarter)
    budget = peewee.DoubleField()
    parent = peewee.ForeignKeyField('self', related_name='children', null=True)
        
    neededNewAttribute = ['name', 'quarter', 'budget', 'parent']
    
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
        
Department.foreigns = {'quarter': Quarter, 'parent': Department}

class Chairmen(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
        
    neededNewAttribute = ['user', 'department']
    foreigns = {'user': User, 'department': Department} 
    
    def jsonEncode(self):
        return {"id": self.id, "user": self.user.id, \
                "department": self.department.id}
    
class PaymentOrder(BaseModel):
    user = peewee.ForeignKeyField(User)
    department = peewee.ForeignKeyField(Department)
    description = peewee.TextField()
    paid = peewee.BooleanField()
    flagged = peewee.BooleanField()
        
    neededNewAttribute = ['user', 'department', 'description', 'paid', 'flagged']
    foreigns = {'user': User, 'department': Department}   
    
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
        
    neededNewAttribute = ['paymentOrder', 'description', 'amount']   
    foreigns = {'paymentOrder': PaymentOrder} 
    
    def jsonEncode(self):
        receipts = []
        for receipt in LineReceipt.select().where(LineReceipt.lineItem == self.id):
            receipts.append(receipt.id)
        return {"id": self.id, "paymentOrder": self.paymentOrder, \
                "description": self.description, "amount": self.amount, \
                "receipts": receipts}
    
class Receipt(BaseModel):
    image = peewee.CharField()
    location = peewee.CharField()
        
    neededNewAttribute = ['image', 'location']   
    
    def jsonEncode(self):
        return {"id": self.id, "image": self.image, "location": self.location}
    
class LineReceipt(BaseModel):
    lineItem = peewee.ForeignKeyField(LineItem)
    receipt = peewee.ForeignKeyField(Receipt)
        
    neededNewAttribute = ['lineItem', 'receipt']  
    foreigns = {'lineItem': LineItem, 'receipt': Receipt}  
    
    def jsonEncode(self):
        return {"id": self.id, "lineItem": self.lineItem.id, \
                "receipt": self.receipt.id}
    
class Approvals(BaseModel):
    department = peewee.ForeignKeyField(Department)
    paymentOrder = peewee.ForeignKeyField(PaymentOrder)
    status = peewee.CharField()
        
    neededNewAttribute = ['department', 'paymentOrder', 'status']  
    foreigns = {'department': Department, 'paymentOrder': PaymentOrder}   
    
    def jsonEncode(self):
        return {"id": self.id, "department": self.department.id, \
                "paaymentOrder": self.paymentOrder.id, "status": self.status}
        
    

class TablesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (User, Quarter, Department, Chairmen, PaymentOrder, \
                            LineItem, Receipt, LineReceipt, Approvals)):
            return obj.jsonEncode()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
