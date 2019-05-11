from flask import Flask, render_template, url_for, request, session, redirect,make_response, jsonify,flash
from flask_pymongo import PyMongo
from db import newItemCreate,itemStockUpdate,itemOutStock,itemInsert5, notificationUnautItem, productInfo,itemStockUpdate2, userInfo, userInsert, itemInsert,itemInsert3, categories,envelope, catagoryCreate, itemInsert2,shopName
import re
import dateparser
from csv import reader
from pymongo import MongoClient
import pprint
from werkzeug import secure_filename
import os
import xlrd
from pprint import pprint
client = MongoClient('localhost', 27017)
db = client.mongoengine_test
tHistory = db.transaction_history 
mProductAdd =db.product_info
printingSes =db.transaction_history

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
mongo = PyMongo(app)

@app.route('/' ,methods=['POST', 'GET'])
def index():
		if 'username' in session:
				return redirect(url_for('home'))

		return render_template('login.html')
				

@app.route('/login',methods=['POST', 'GET'])
def login():
		#temp = Ticket.objects.get(ticketID=ticketNum)

		user = request.form['username']
		password = request.form['password']
		temp = userInfo.objects.get(username = user.lower())
		if password == temp.password:
				session['username'] = request.form['username']
				return redirect(url_for('home'))
		else: 
				return 'password is wrong'

		

@app.route('/home')
def home():
	if 'username' in session:


		return render_template('home.html',unregisteredItem = notificationUnautItem.objects(),itemOutStock = itemOutStock.objects())
	return render_template('login.html')


@app.route('/accounts')
def accounts():
		if 'username' in session:

				return render_template('accounts.html')
		return render_template('login.html')

@app.route('/add-product',methods=['POST', 'GET'])
def addProduct():
		if 'username' in session:
			temp=categories.objects() 
			
			return render_template('add-product.html',categories =categories.objects(),envelope = envelope.objects() )
		return render_template('login.html')

@app.route('/temp',methods=['POST', 'GET'])
def temp():
	print((request.form.getlist('productName')))
	incompleteVal ='False'
	multi =False
	if len(request.form.getlist('productName'))>2:

		productName =request.form.get('productName','')
		if productName == "":
			incompleteVal = 'True'
		products =request.form.getlist('productName')
		chineseName = request.form.get('chinese_name','')
		chinese = request.form.getlist('chinese_name')
		if chineseName == "":
			incompleteVal = 'True'
		SKU =request.form.get('SKU','')
		SKUS =request.form.getlist('SKU')
		if SKU == "":
			incompleteVal = 'True'

		multi ='True'
	else:
		productName =request.form.get('productName')
		if productName == "":
			incompleteVal = 'True'
		chineseName = request.form.get('chinese_name')
		if chineseName == "":
			incompleteVal = 'True'
		SKU =request.form.get('SKU')
		if SKU == "":
			incompleteVal = 'True'
		multi = 'False'

	colour =request.form.get('Colour','')
	if colour == "":
			incompleteVal = 'True'
	weight =request.form.get('weight','')
	if weight == "":
			incompleteVal = 'True'
	height =request.form.get('Height','')
	if height == "":
			incompleteVal = 'True'
	width =request.form.get('Width','')
	if width == "":
			incompleteVal = 'True'
	lenght =request.form.get('Lenght','')
	if lenght == "":
			incompleteVal = 'True'
	description =request.form.get('item_description','')
	if description == "":
			incompleteVal = 'True'
	material =request.form.get('item_materials','')
	if material == "":
			incompleteVal = 'True'
	quantity_inStock =request.form.get('stock','')
	
	if quantity_inStock == '':
			quantity_inStock = 0
			incompleteVal = 'True'
	currency =request.form.get('currencyType')
	if currency == "":
			incompleteVal = 'True'
	cost_price =request.form.get('cost_price',0.00)
	if cost_price == 0.00:
			incompleteVal = 'True'
	category = request.form.get('category')
	print(category)
	if category == "none":
		print('cat true')
		incompleteVal = 'True'
	elif category == 'OtherCat':
		print('other cat')
		category = request.form['otherCat']
		if categories.objects(category=(request.form['otherCat']).capitalize()).count()>0:
			pass
		else:
			catagoryCreate((request.form['otherCat']).capitalize())
	envelope = request.form.get('envelope','none')  
	if envelope == "none":
		incompleteVal = 'True'
	elif envelope == "Other":
		envelope = request.form['envName']
		enveCreate(envelope)
	if 1==1:
		if productInfo.objects(productName=productName).count()>1:
			print('asdfasdfsdf')
			return(redirect(url_for('products')))
	
		else:
			if productInfo.objects(SKU=SKU) == True:
					pass
			else:
				if currency == 'AUD':
					AUD = float(cost_price)
					USD = AUD/1.4
					RMB = AUD* 4.77
				elif currency == 'USD':
					AUD = 1.4 * float(cost_price)
					USD = float(cost_price)
					RMB = 6.68 * float(cost_price)
				elif currency == 'RMB':
					RMB = float(cost_price)
					USD = RMB/6.68
					AUD = .21 * RMB 
				else:
					AUD = 0.00
					USD = 0.00
					RMB = 0.00

				
				fileExists = tHistory.find({ "Item Title": productName})
				if fileExists.count() >0:
					stockOut = 0
					for i in range(fileExists.count()):
						stockOut += int(fileExists[i]['Quantity'])

					if int(quantity_inStock) - int(stockOut)<1:
						itemStockUpdate2(SKU,productName)
						incompleteVal = 'True'
					if multi =='True':
						itemInsert5(productName,chineseName,SKU,products,chinese,SKUS,colour,weight,height,width,lenght,description,material,int(quantity_inStock),int(AUD),int(RMB),int(USD),category,incompleteVal,stockOut)
					else:
						itemInsert2(productName,chineseName,SKU,colour,weight,height,width,lenght,description,material,int(quantity_inStock),int(AUD),int(RMB),int(USD),category,incompleteVal,stockOut)
					
					noteExists = notificationUnautItem.objects(itemName=productName).delete()
					
				else:
					#if len(productName)>1:
					if multi =='True':
						itemInsert5(productName,chineseName,SKU,products,chinese,SKUS,colour,weight,height,width,lenght,description,material,int(quantity_inStock),int(AUD),int(RMB),int(USD),category,incompleteVal)
					else:	
						itemInsert(productName,chineseName,SKU,colour,weight,height,width,lenght,description,material,int(quantity_inStock),int(AUD),int(RMB),int(USD),category,incompleteVal)
		
		if notificationUnautItem.objects(SKU = request.form.get('SKU','')).count()>0:
			notificationUnautItem.objects(SKU = request.form.get('SKU','')).delete()		
			x = tHistory.find({'Custom Label': request.form.get('SKU','')})
			for i in x:
				if i['Status'] == 'Incomplete_SKU':
					i['Status'] = 'None'		
	return(redirect(url_for('products')))




@app.route('/itemDelete/<productName>')
def itemDelete(productName):
		
	productInfo.objects(productName=productName).delete()
	#packagingInfo.objects(productName=productName).delete()
	
	
	return redirect(url_for('products'))

@app.route("/categoryDelete/<category>")
def categoryDelete(category):
		categories.objects(category=category).delete()
		return redirect(url_for('products'))

@app.route('/edit-product/<ItemName>',methods=['POST', 'GET'])
def editProduct(ItemName):
	if 'username' in session:
		for product in productInfo.objects( productName= ItemName):
			aud = product.cost_AUD
			usd =product.cost_USD
			rmb = product.cost_RMB
			cat = product.category

			if (aud != 0):
				currencyType = 'AUD'
				cost = product.cost_AUD
			elif (usd != 0):
				currencyType = 'USD'
				cost = product.cost_USD
			elif rmb != 0:
				currencyType = 'RMB'
				cost = product.cost_RMB 
			else:
				currencyType ='Select Currency'
				cost = 0.00
			
			item = productInfo.objects( productName= ItemName).first()
			envelopeItem = item.envelope
			


			return render_template('edit-product.html',product = product, currencyType = currencyType, cost = cost, envelope= envelopeItem,selectCat =cat,categories =categories.objects(),envelopes = envelope.objects() )
	return render_template('login.html')


@app.route('/create-new-productTemp/<SKUold>',methods=['POST', 'GET'])
def createNewItemTemp(SKUold):
	if 'username' in session:
		temp = tHistory.find({ "Custom Label": SKUold })

		return render_template('add-product.html',SKU = temp[0]['Custom Label'])
	return render_template('login.html')


@app.route('/editTemp/<ItemName>' ,methods=['POST', 'GET'])
def editTemp(ItemName):

	if not 'username' in session:
		return redirect(url_for('index'))

	
	incompleteVal = 'False'
	productName =request.form.get('productName','')
	if productName == "":
		incompleteVal = 'True'
	chineseName = request.form.get('chinese_name', '')
	if chineseName == "":
		incompleteVal = 'True'
	SKU =request.form.get('SKU','')
	if SKU == "":
		incompleteVal = 'True'
	colour =request.form.get('Colour','')
	if colour == "":
		incompleteVal = 'True'
	weight =request.form.get('weight','')
	if weight == "":
		incompleteVal = 'True'
	height =request.form.get('Height','')
	if height == "":
		incompleteVal = 'True'
	width =request.form.get('Width','')
	if width == "":
		incompleteVal = 'True'
	lenght =request.form.get('Lenght','')
	if lenght == "":
		incompleteVal = 'True'
	description =request.form.get('item_description','')
	if description == "":
		incompleteVal = 'True'
	material =request.form.get('item_materials','')
	if material == "":
		incompleteVal = 'True'
	quantity_inStock =request.form.get('stock','')
	if quantity_inStock == '':
		quantity_inStock = 0
		incompleteVal = 'True'
	currency =request.form.get('currencyType','none')
	if currency == "none":
		incompleteVal = 'True'
	cost_price =request.form.get('cost_price',0.00)
	if cost_price == 0.00:
		cost_price = 0.00
		incompleteVal = 'True'
	category = request.form.get('category','none')
	if category == "none":
		incompleteVal = 'True'
	elif category == 'OtherCat':
		category = request.form.get('otherCat')
		if categories.objects(category=(request.form['otherCat']).capitalize()).count()>0:
			pass
		else:
			catagoryCreate((request.form['otherCat']).capitalize())
	envelope = request.form.get('envelope','none')  
	if envelope == "none":
		incompleteVal = 'True'
	elif envelope == "Other":
		envelope = request.form['OtherEnvelope']
	temp = productInfo.objects(productName = ItemName).delete()
	if currency == 'AUD':
		AUD = int(cost_price)
		USD = AUD/1.4
		RMB = AUD* 4.77
	elif currency == 'USD':
		AUD = 1.4 * int(cost_price)
		USD = int(cost_price)
		RMB = 6.68 * int(cost_price)
	elif currency == 'RMB':
		RMB = int(cost_price)
		USD = RMB/6.68
		AUD = .21 * RMB
	else:
		RMB = 0.00
		USD = 0.00
		AUD =0.00
		currencyType = 'none'
	if productInfo.objects(productName=ItemName) == True:
		return(redirect(url_for('products')))
	else:
		try:
			skucheck = productInfo.objects(SKU = SKU).get()
			for i in skucheck:
				skucheck = i.sku
		except:
			skucheck = 'notExitst'
		if (skucheck)=="notExitst":
					
			itemInsert(productName,chineseName,SKU,colour,weight,height,width,lenght,description,material,int(quantity_inStock),float(AUD),float(RMB),float(USD),category,incompleteVal)
			
				
					
			return redirect(url_for('products'))
		elif skucheck!="notExitst":
			if skucheck !="":
				return render_template('edit-product.html', product = temp,currencyType= currencyType, cost = cost_price,envelope = envelope, hiddenText = 'This SKU is already in use. Please change it')
			else:
							
				itemInsert(productName,chineseName,SKU,colour,weight,height,width,lenght,description,material,int(quantity_inStock),float(AUD),float(RMB),float(USD),category,incompleteVal)
				
					
				return redirect(url_for('products'))
		return redirect(url_for('products'))

@app.route('/products',methods=['POST', 'GET'])
def products():
		if 'username' in session:
				return render_template('products.html',products= productInfo.objects,unregisteredItem =  notificationUnautItem.objects())
		return render_template('login.html')

@app.route('/products/searchItemBy',methods=['POST', 'GET'])
def productSearch():
		if 'username' in session:
				
				
				searchType = request.form.get('searchType')
				
				itemName = request.form.get('search_bar')
				
				if searchType == 'itemName':
						temp = productInfo.objects( productName__contains=itemName)
				elif searchType == 'SKU':
						temp = productInfo.objects( SKU__contains=itemName)
				elif searchType == 'cat':
						temp = productInfo.objects( category__contains=itemName)
				elif searchType == 'moSo':
						temp = productInfo.objects().sort('quantity_sold',1)
				elif searchType == 'leSo':
						temp = productInfo.objects().sort('quantity_sold',-1)
				return render_template('productsearch.html',products= temp, title = "psearch")
		return render_template('login.html')


@app.route('/dailyReports')
def dailyReports():
		if 'username' in session:
				x= tHistory.find({ "Item Title":"Item Title"})
				if x.count()>1:
						tHistory.delete_many({ "Item Title":"Item Title"})
				x= tHistory.delete_many({ "Sales Record Number":re.compile("Seller ID:", re.IGNORECASE)})  
				x= tHistory.delete_many({ "Buyer State":"",'Item Title':'','PayPal Transaction ID':''})  
				total = 0
				quantity = 0
				for i in tHistory.find():
					try:
						total +=float(i['Sale Price'][4::] )*int(i['Quantity'])
						quantity +=int(i['Quantity'])
					except:
						pass         
				for i in tHistory.find({'Item Title':''}):
					quantity -= int(i['Quantity'])          
				transCount = tHistory.distinct('keys')                                                                                                                                                                         
																																																
				return render_template('daily-report.html',records = tHistory.find(),totalc = ("%.2f" % round(total,2)),quantity = quantity,transCount =transCount )
		return render_template('login.html')

@app.route('/printSession/',methods=['POST', 'GET'])
def printSession():
		if 'username' in session:
				
																																								
				return render_template("printSession.html",records = printingSes.find())
		return render_template('login.html')

@app.route('/printSession/multi',methods=['POST', 'GET'])
def printSessionMulti():
		if 'username' in session:
				x=tHistory.aggregate([
					{"$match": {"Sales Record Number" :{ "$ne" : None } } }, 
					{"$group" : {"_id": "$Sales Record Number", "count": { "$sum": 1 } } },
					{"$match": {"count" : {"$gt": 1} } }, 
					{"$project": {"Sales Record Number" : "$_id", "_id" : 0} }]
				)
				records = []
				for i in x:
						for y in i:
								records.append(i[y])
				data = []
				for i in records:
						data.append(printingSes.find({"Sales Record Number":i}))
				
				return render_template("printSesMulti.html", records = data)
		return render_template('login.html')

@app.route('/dailyReports/searchItemBy',methods=['POST', 'GET'])
def dailyReportSearch():
		if 'username' in session:

				searchBy = request.form.get('searchType')
				itemName = request.form.get('search_bar')       
				start = dateparser.parse(request.form.get('begin_date'), settings={'DATE_ORDER': 'DMY'})
				end = dateparser.parse(request.form.get('expire_date')  , settings={'DATE_ORDER': 'DMY'})       


				if start == None and end == None:
				
						if searchBy == 'itemName':
								x= tHistory.find({ "Item Title": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'SKU':
								x =tHistory.find({ "Custom Label": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'recordID':
								x =tHistory.find({ "Sales Record Number": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'buyerName':
								x =tHistory.find({ "Buyer Fullname": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'buyerNum':
								x =tHistory.find({ "Buyer Phone Number": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'buyerEmail':
								x =tHistory.find({ "Buyer Email": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'state':
								x =tHistory.find({ "Buyer State": re.compile(itemName, re.IGNORECASE)})
						elif searchBy == 'state':
								if len(itemName)>2:
										x =tHistory.find({ "'Shop Name'": re.compile(itemName, re.IGNORECASE)})
								elif len(itemName)<=2:
										shopTemp = shopName.objects(code=itemName.upper()).first()
										x =tHistory.find({ "'Shop Name'": re.compile(shopTemp.name, re.IGNORECASE)})
				
				elif start == None or end == None:
						if start == None:
								start = dateparser.parse('1 jan 10', settings={'DATE_ORDER': 'DMY'})
						elif end == None:
								end = dateparser.parse('today', settings={'DATE_ORDER': 'DMY'})
						if searchBy == 'itemName':
								x= tHistory.find({ "Item Title": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'SKU':
								x =tHistory.find({ "Custom Label": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'recordID':
								x =tHistory.find({ "Sales Record Number": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'buyerName':
								x =tHistory.find({ "Buyer Fullname": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'buyerNum':
								x =tHistory.find({ "Buyer Phone Number": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'buyerEmail':
								x =tHistory.find({ "Buyer Email": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'state':
								x =tHistory.find({ "Buyer State": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
						elif searchBy == 'state':
								if len(itemName)>2:
										x =tHistory.find({ "'Shop Name'": re.compile(itemName, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
								elif len(itemName)<=2:
										shopTemp = shopName.objects(code=itemName.upper()).first()
										x =tHistory.find({ "'Shop Name'": re.compile(shopTemp.name, re.IGNORECASE),'Sale Date':{'$lt': end, '$gte': start}})
				history = []
				for i in x:

						history.append(i)

				total = 0
				
				for i in history:
						try:
								total +=float(i['Sale Price'][4::])
						except:
								pass
				return render_template('daily-report.html',records = history,total = ("%.2f" % round(total,2)))
		return render_template('login.html')

@app.route('/viewReport/<recordID>/<status>')
def viewReport(recordID,status):
	if 'username' in session:
		
		records =tHistory.find({"PayPal Transaction ID":(recordID),'Status':status})
		if records.count()>1:
			headers = []
			init = []
			x=tHistory.find_one({"PayPal Transaction ID":recordID,'Status':status})
			for k in x:
				headers.append(k)
				init.append(x[k])
			from collections import defaultdict
			dd  = defaultdict(list)
			for d in (record for record in records): # you can list as many input dicts as you want here
				for key, value in d.items():

					if value =='':
						pass
					elif value in(dd[key]):
						pass
					else:
						dd[key].append(value)

			
			return render_template('tempMulti.html',result = dd,title ="report",status = status.capitalize(),recordID=recordID)
		else:	
			
			return render_template('temp.html',result = records,title ="report",status = status.capitalize(),recordID=recordID)
	return render_template('login.html')

@app.route('/ogTrans/<recordID>',methods=['POST','GET'])
def ogTrans(recordID):

	if 'username' not in session:
		return redirect(url_for('index'))
	
	records =tHistory.find({"PayPal Transaction ID":recordID,'Status':{'$ne':'Repeat'}})
	if records.count()>1:
		headers = []
		init = []
		x=tHistory.find_one({"PayPal Transaction ID":recordID,'Status':{'$ne':'Repeat'}})
		for k in x:
			headers.append(k)
			init.append(x[k])
		from collections import defaultdict
		dd  = defaultdict(list)
		for d in (record for record in records): # you can list as many input dicts as you want here
			for key, value in d.items():

				if value =='':
					pass
				elif value in(dd[key]):
					pass
				else:
					dd[key].append(value)

			
			
		return render_template('tempMulti.html',result = dd,title ="report",status = '',recordID=recordID)
	else:	
		
		return render_template('temp.html',result = records,title ="report",status = "",recordID=recordID)



def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)

    modified = {o : (d1[o], d2[o]) for o in intersect_keys if (d1[o] != d2[o]) }
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return  modified


@app.route('/upload_file',methods=['POST'])
def upload_file():
	if 'username' not in session:
		return redirect(url_for('index'))
	if not 'fileInput' in request.files:
		return redirect(url_for('dailyReports'))

	
	for f in request.files.getlist('fileInput'):
		fName = secure_filename(f.filename)
		f.save(fName)
		f= open(fName,'r')
		try:
			file =newFile.read().splitlines()
		except:
			os.system("dos2unix " + fName)
			newFile= open(fName, 'r',encoding = "ISO-8859-1")
			file =newFile.read().splitlines()
		in_db = False
		if not in_db:
			x = []
			for i in reader((file)):
							
				if len(i)>0:
					if i[0]=='':
						pass
					else:
						if len(str(i).strip()) == 0 or len(str(i).strip())==1 :
							pass
						else:
							x.append(i)


			for i in x:
				if i == ['\t']:
					x.remove(i)
				elif i == []:
					x.remove(i)
							
			
			li = []
			headers = x[0]
			
			x=x[1::]
			inc=[]		
			for iterA in range(len(x)):

							
				dictI = {}
				
				if len(x[iterA])>10:
					for i in range(len(headers)):
						try:
							dictI[headers[i].strip()]=x[iterA][i]
						except:
							pass
					try:
						dictI['Sales Record Number'] = int(dictI['Sales Record Number'])
					except:
						dictI['Sales Record Number'] = ''
					dictI['filename'] = fName
					dictIF = True
					try:
						dictI['Total Price'] = dictI['Total Price'][4::]
					except:
						dictIF = False
					try:
						dictI['Sale Date']=dateparser.parse(dictI['Sale Date'], settings={'DATE_ORDER': 'DMY'})
					except:
						dictIF = False
					try:
						temp = dictI['Custom Label'].split('-')
						
						if len(temp) != 0:
							itemCode = temp[2]
							sku = dictI['Custom Label']
							shopTemp = shopName.objects(code=temp[0]).first()
							dictI['Shop Name']=shopTemp.name
							dictI['Quantity'] = int(dictI['Quantity']) * int(temp[4])


					except:

						dictIF = False
					dictI['Status']='None'
					
					if dictIF != False:
						try:
							skuLookup = productInfo.objects(SKU__contains=itemCode).get()
						except:
							skuLookup  = ''
						if len(skuLookup)>0:
							if skuLookup.quantity_inStock - int(dictI['Quantity']) <0:
								itemStockUpdate(sku,skuLookup.productName,dictI['Sales Record Number'])
							else:
								skuLookup.quantity_sold=skuLookup.quantity_sold+int(dictI['Quantity'])
								skuLookup.quantity_inStock = skuLookup.quantity_inStock - int(dictI['Quantity']) 
								skuLookup.save()
							
						else:
							dictI['Status'] = 'Incomplete_SKU'
							temp = notificationUnautItem.objects(SKU = dictI['Custom Label'])
							if len(temp)==0:
								newItemCreate(str(dictI['Custom Label']),dictI['Item Title'])
								
						try:
							if dictI['Sales Record Number']==li[-1]['Sales Record Number']:
								dictI['Buyer State'] = li[-1]['Buyer State']
								dictI['PayPal Transaction ID'] = li[-1]['PayPal Transaction ID']

						except:
							pass
						
					li.append(dictI)	
			trans =[]
			rep=[]
			done = []
			for i in li:
				trans.append([i['PayPal Transaction ID'],i['Sales Record Number'],i['Buyer Postcode'],i['Buyer Address 1'],i['User Id']])
			for i in trans:

				if tHistory.find({'PayPal Transaction ID':i[0]}).count()>0:
					rep.append(i)

				for x in trans:
					if i[0]==x[0]:
						if i[1]==x[1]:
							pass
						else:
							done.append(x)
			for i in li:
				for x in rep:
					if (i['PayPal Transaction ID'])==x:
						i['Status'] ='Repeat'

				for x in done:
					
					if ([i['PayPal Transaction ID']])==[x[0]]:
							if i['User Id'] == x[4]:
								if (i['Buyer Postcode'],i['Buyer Address 1']) !=(x[2],x[3]):

									i['Status'] ='DropShip'

							elif (i['User Id'],i['Buyer Address 1'] )== (x[4],x[3]):
								if (i['PayPal Transaction ID'],i['Sales Record Number']) !=(x[0],x[1]):
									i['Status'] = 'Multi'
									
							elif [i['PayPal Transaction ID'],i['Sales Record Number'],i['Buyer Postcode']]==[x[0],x[1],x[2]]:	
								i['Status'] ='Repeat'					
														
			tHistory.insert_many(li)
					 
		
			#print(rep)
			return redirect(url_for('dailyReports'))
		else:
				
			flash('Database is Already Stored')
			return redirect(url_for('dailyReports'))
 

@app.route('/product_upload_file',methods=['POST'])
def product_upload_file():
	if 'username' not in session:
		return redirect(url_for('index'))
	if not 'fileInput' in request.files:
		return redirect(url_for('products'))

	f = request.files['fileInput']
	fName = secure_filename(f.filename)
	
	f.save(fName)
	f= open(fName,'r',encoding="GBK")
	try:
		file =f.read().splitlines()
		print(type(file))

	except:
		if  'xlsx' in fName:
			loc = (fName) 
  
# To open Workbook 
			wb = xlrd.open_workbook(loc) 
			sheet = wb.sheet_by_index(0) 
			file = []
			for i in range(sheet.nrows):
				if (len(set(sheet.row_values(i)))) ==1:
					pass
				else:
					file.append(sheet.row_values(i))
			file =file[1::]
			for i in file:
				if len(set(i)) ==1:
					pass
				else:
					for x in range(len(i)):
				
						if i[x] =='':
							i.append('True')
							break

					if 'True' not in i:
						i.append('False')
				
					itemInsert3(i)
			return redirect(url_for('products'))

		else:
			os.system("dos2unix " + fName)
			f= open(fName, 'r',encoding = "ISO-8859-1")
			file =f.read().splitlines()

	x = []

	for i in reader((file)):
					
		if len(i)>0:
			if len(str(i).strip()) == 0 or len(str(i).strip())==1 :
				pass
			else:
				x.append(i)
	for i in x:
		if i == ['\t']:
			x.remove(i)
		elif i == []:
			x.remove(i)
	li = []
	headers = x[0]
	
	x=x[1::]
	for iterA in x:
		if (len(set(iterA))) ==1:
			pass
		else:

			for i in range(len(iterA)):
				
				if iterA[i] =='':
					iterA.append('True')
					break

			if 'False' not in iterA[i]:
				iterA.append('False')
		
			itemInsert3(iterA)
		
	return redirect(url_for('products'))


@app.route('/editSKU/<oldSKU>',methods=['POST', 'GET'])
def editSKU(oldSKU):
	if 'username' in session:
		temp = tHistory.find({'SKU':oldSKU})
		

		skuTemp = productInfo.objects()
		
		try:
			return render_template("editSKU.html" ,SKU =skuTemp ,productName = temp.productName,oldSKU = oldSKU,title = "edit_sku")
		except:
			return render_template("editSKU.html" ,SKU = skuTemp,productName ='',oldSKU =oldSKU,title = "edit_sku")
	return render_template('login.html')

		
@app.route('/editSKUChange/<oldSKU>',methods=['POST', 'GET'])
def editSKUChange(oldSKU):
	if 'username' in session:
		x= request.form.get('body')
		
		hist = tHistory.find({ "Custom Label": oldSKU})
		temp = productInfo.objects(SKU=x)
		temp.to_json()
		

		
		tHistory.update_many({"Custom Label": oldSKU},
								{'$set': {'Custom Label':x,'Item Title':temp[0]['productName'],'Status':''}})
									
		stockOut = 0
									
		for i in (hist):	
			stockOut += int(i['Quantity'])

			if int(temp[0]['quantity_inStock']) - int(stockOut)<1:
				temp[0]['quantity_inStock'] =int(temp[0]['quantity_inStock']) - int(stockOut)
				itemStockUpdate2(x,temp[0]['productName'])
			else:
				temp[0]['quantity_inStock'] =int(temp[0]['quantity_inStock']) - int(stockOut)
				temp[0]['quantity_sold'] = temp[0]['quantity_sold']+stockOut
			
		noteExists = notificationUnautItem.objects(SKU=oldSKU).delete()
			

		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/reorder/<SKU>')
def reorder(SKU):
		return 'reorder'

@app.route('/dataRemAll')
def dataRemAll():
	if 'username' in session:
		tHistory.delete_many({})
		productInfo.objects.delete()
		notificationUnautItem.objects().delete()
		itemOutStock.objects().delete()
	return redirect(url_for('index'))

@app.route('/dataRemTrans')
def dataRemTrans():
	if 'username' in session:
		tHistory.delete_many({})
		notificationUnautItem.objects().delete()
	return redirect(url_for('index'))

@app.route('/dataRemProducts')
def dataRemProducts():
	if 'username' in session:
		productInfo.objects.delete()
		itemOutStock.objects().delete()
	return redirect(url_for('index'))

@app.route('/delTran/<recordID>')
def delTran(recordID):
	if 'username' in session:
		x = tHistory.find({'PayPal Transaction ID':(recordID),'Status':'Repeat'}).count()
		if x>1:
			tHistory.delete_many({'PayPal Transaction ID':(recordID),'Status':'Repeat'})
		else:
			tHistory.delete_one({'PayPal Transaction ID':(recordID),'Status':'Repeat'})
		return redirect(url_for('dailyReports'))
	return redirect(url_for('index'))


@app.route('/logout')
def logout():
		session.clear()
		return redirect(url_for('index'))

#host="0.0.0.0", port=80
app.secret_key = 'mysecret'
if __name__ == "__main__":
	app.run(debug = True)



#ssh -L 27000:localhost:27017 -i c:/Users/karuna/Desktop/jobs/demo/awsInst2.pem ubuntu@ec2-18-223-122-195.us-east-2.compute.amazonaws.com
