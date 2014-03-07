from Tables import *
import datetime
from datetime import date

allTables = [User, Quarter, Department, Chairmen, PaymentOrder, LineItem, Receipt, LineReceipt, Approvals]

# Drops all of the existing tables but doesn't stop if one doesn't exist
for table in reversed(allTables):
    table.drop_table(True)

# Recreates all of the tables
for table in allTables:
    table.create_table()



# Users
admin = User(firstName='first', lastName='last', email='admin@admin.com', passHash='password', passSalt='salt')
admin.save()
treasurer = User(firstName='Mike', lastName='Cirracco', email='mcirraco@pike.com', passHash='password', passSalt='salt')
treasurer.save()
vp1 = User(firstName='Jacob', lastName='Lueck', email='jlueck@pike.com', passHash='password', passSalt='salt')
vp1.save()
vp2 = User(firstName='Alex', lastName='Memering', email='amemering@pike.com', passHash='password', passSalt='salt')
vp2.save()
vp3 = User(firstName='Nick', lastName='Diskerude', email='ndiskerude@pike.com', passHash='password', passSalt='salt')
vp3.save()
scholar = User(firstName='Tucker', lastName='Nelson', email='tnelson@pike.com', passHash='password', passSalt='salt')
scholar.save()
groundsU = User(firstName='Seth', lastName='Keiffer', email='skeiffer@pike.com', passHash='password', passSalt='salt')
groundsU.save()
housingU = User(firstName='Nick', lastName='Burris', email='nburris@pike.com', passHash='password', passSalt='salt')
housingU.save()
spurr = User(firstName='Matt', lastName='Spurr', email='mspurr@pike.com', passHash='password', passSalt='salt')
spurr.save()
brent = User(firstName='Brent', lastName='Austgen', email='baustgen@pike.com', passHash='password', passSalt='salt')
brent.save()

# Quarter
winter = Quarter(start=date(2013, 11, 17), end=date(2014, 2, 25))
winter.save()
spring = Quarter(start=date(2014, 3, 9), end=date(2014, 6, 20))
spring.save()

# Departments
old = Department(name='Old', quarter=winter, budget=1000)
old.save()
executive = Department(name='Executive', quarter=spring, budget=500)
executive.save()
programs = Department(name='Programs', quarter=spring, budget=500, parent=executive)
programs.save()
enrichment = Department(name='Enrichment', quarter=spring, budget=1000, parent=executive)
enrichment.save()
social = Department(name='Social', quarter=spring, budget=2500, parent=executive)
social.save()
scholarship = Department(name='Scholarship', quarter=spring, budget=1000, parent=enrichment)
scholarship.save()
grounds = Department(name='Grounds', quarter=spring, budget=2000, parent=programs)
grounds.save()
housing = Department(name='Housing', quarter=spring, budget=1500, parent=programs)
housing.save()
housingCapEx = Department(name='Housing Cap Ex', quarter=spring, budget=1000, parent=housing)
housingCapEx.save()

# Chairmen
adminOld = Chairmen(user=admin, department=old)
adminOld.save()
adminCurrent = Chairmen(user=admin, department=executive)
adminCurrent.save()
executiveC = Chairmen(user=treasurer, department=executive)
executiveC.save()
programsC = Chairmen(user=vp1, department=programs)
programsC.save()
enrichmentC = Chairmen(user=vp2, department=enrichment)
enrichmentC.save()
socialC = Chairmen(user=vp3, department=social)
socialC.save()
scholarshipC = Chairmen(user=scholar, department=scholarship)
scholarshipC.save()
groundsC = Chairmen(user=groundsU, department=grounds)
groundsC.save()
housingC = Chairmen(user=housingU, department=housing)
housingC.save()
housingCapExC = Chairmen(user=spurr, department=housingCapEx)
housingCapExC.save()
housingCapExC = Chairmen(user=brent, department=housingCapEx)
housingCapExC.save()