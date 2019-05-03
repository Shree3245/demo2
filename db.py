from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)
from pprint import pprint
import datetime


def stringToFloat(val):
	if val != "":
		return float(val)
	else:
		val = float(0)
		return val

class productInfo(Document):
	productName = StringField(required=False, max_length=2000)
	chineseName = StringField(required=False, max_length=200)
	SKU = StringField(required=False, max_length=300)
	colour = StringField(required=False, max_length=200)
	size =StringField(required=False, max_length=200)
	weight = IntField(required=False, max_length=200)
	height =IntField(required=False, max_length=200)
	width =IntField(required=False, max_length=200)
	length =IntField(required=False, max_length=200)
	description = StringField(required=False, max_length=20000)
	material = StringField(required=False, max_length=200)
	quantity_inStock = IntField(required=False, max_length=200)
	cost_AUD = IntField(required=False, max_length=7)
	cost_RMB = IntField(required=False, max_length=7)
	cost_USD = IntField(required=False, max_length=7)
	picture =StringField(required=False, max_length=200)
	quantity_sold = IntField(required=False, max_length=200, default = 0)
	envelope = StringField(required=False, max_length=200)
	category =StringField(required=False, max_length=200)
	status = StringField(required=True, max_length=10)

class categories(Document):
	category =StringField(required=False, max_length=200)

class envelope(Document):
	envelope =StringField(required=False, max_length=200)


class userInfo(Document):
	username = StringField(required=True, max_length=200)
	firstName = StringField(required=True, max_length=200)
	lastName = StringField(required=True, max_length=200)
	password = StringField(required=True, max_length=200)
	email = StringField(required=True, max_length=200)
	position = StringField(required=True, max_length=200)


class itemOutStock(Document):
	SKU=StringField(required=False, max_length=200)
	itemName = StringField(required=False, max_length=200)
	Sales_Record_Number = IntField(required=False, max_length=2000)

class notificationUnautItem(Document):
	SKU=StringField(required=False, max_length=200)
	itemName = StringField(required=False, max_length=200)

def userInsert(username,firstName,lastName,email,position,password):
	username=username.lower()
	firstName = firstName.capitalize()
	lastName = lastName.capitalize()
	userEntry=userInfo(
				        username=(username),
				        firstName=(firstName),
				        lastName=(lastName),
				        email=(email),
				        position=(position),     
				        password = password    
    )
	userEntry.save()

def itemInsert(productName, chineseName ,SKU ,colour ,weight, height,width,length ,description ,material ,quantity_inStock ,cost_AUD ,cost_RMB ,cost_USD ,category,status ):
	itemEntry = productInfo(

		productName = productName.lower(),
		chineseName = chineseName ,
		SKU = SKU ,
		colour = colour.lower(),
		weight = weight ,
		height = height ,
		width =width,
		length=length,
		description = description ,
		material = material ,
		quantity_inStock = (quantity_inStock) ,
		cost_AUD = cost_AUD ,
		cost_RMB = cost_RMB ,
		cost_USD = cost_USD ,
		category =category,
		status = status
		)
	itemEntry.save()

def itemInsert2(productName, chineseName ,SKU ,colour ,weight, dimensions ,description ,material ,quantity_inStock ,cost_AUD ,cost_RMB ,cost_USD ,category,status,quantity_sold ):
	itemEntry = productInfo(

		productName = productName.lower(),
		chineseName = chineseName ,
		SKU = SKU ,
		colour = colour.lower(),
		weight = weight ,
		height = height ,
		width = width,
		length = length,
		description = description ,
		material = material ,
		quantity_inStock = (quantity_inStock) ,
		cost_AUD = cost_AUD ,
		cost_RMB = cost_RMB ,
		cost_USD = cost_USD ,
		category =category,
		status = status,
		quantity_sold = quantity_sold
		)
	itemEntry.save()



def catagoryCreate(category):
	categoryCreation = categories(
		category = category
		)
	categoryCreation.save()

def enveCreate(category):
	categoryCreation = envelope(
		envelope = category
		)
	categoryCreation.save()

def newItemCreate(SKU,itemName):
	note = notificationUnautItem(
	SKU = SKU,
	itemName =itemName)
	note.save()

def itemStockUpdate(SKU,itemName,recordNumber):

	note = itemOutStock(

		SKU = SKU,
		itemName =itemName,
		Sales_Record_Number = recordNumber
		)
	note.save()

def itemStockUpdate2(SKU,itemName):

	note = itemOutStock(

		SKU = SKU,
		itemName =itemName
		)
	note.save()

class shopName(Document):
	name=StringField(required=False, max_length=200)
	code = StringField(required=False, max_length=200)

def shopCreate(name,Code):

	note = shopName(
		name =name,
		code =Code
		)
	note.save()

def itemInsert3(li):

	if categories.objects(category=li[-5].capitalize()).count()>0:
		pass
	else:
		catagoryCreate(li[-5].capitalize())
	
	if envelope.objects(envelope=li[-4]).count()>0:
		print(envelope.objects(envelope=li[-4]).count())
	else:
		enveCreate(li[-4])
	
	
	if li[-3] == 'AUD':
		AUD = float(li[-2])
		USD = AUD/1.4
		RMB = AUD* 4.77
	elif li[-3] == 'USD':
		AUD = 1.4 * float(li[-2])
		USD = float(li[-2])
		RMB = 6.68 * float(li[-2])
	elif li[-3] == 'RMB':
		RMB = float(li[-2])
		USD = RMB/6.68
		AUD = .21 * RMB 
	else:
		AUD = 0.00
		USD = 0.00
		RMB = 0.00
	itemEntry = productInfo(

		chineseName = li[1] ,
		productName = li[0].lower(),
		SKU = li[2] ,
		colour = li[3].lower(),
		weight = li[4] ,
		height = li[5] ,
		width = li[6] ,
		length = li[7] ,
		description = li[8] ,
		material = li[9] ,
		quantity_inStock = (li[10]) ,
		category =li[11].capitalize(),
		cost_RMB = RMB,
		cost_USD = USD,
		cost_AUD = AUD, 
		status = li[-1],
		envelope=(li[-4])
		)
	itemEntry.save()
	
