
		R= tHistory.find({'Shop Name':'Raggaza'})
		T= tHistory.find({'Shop Name':'Tronic'})
		y= tHistory.find({'Shop Name':'YOU'})
		I= tHistory.find({'Shop Name':'IS'})
		
		total_R = 0
		for i in R:
			try:
				total_R +=float(i['Sale Price'][4::])
			except:
				pass 
		total_T = 0
		for i in T:
			try:
				total_T +=float(i['Sale Price'][4::])
			except:
				pass 

		total_Y = 0
		for i in y:
			try:
				total_Y +=float(i['Sale Price'][4::])
			except:
				pass 
		total_I = 0
		for i in I:
			try:
				total_I +=float(i['Sale Price'][4::])
			except:
				pass

		#print(total_R)
		#print(total_T)
		#print(total_I)
		#print(total_Y)
		try:
			d1 = tHistory.find({'Shop Name':'Raggaza'})[0]
			dateS = d1['Paid on Date'][:2]
			dateS2 = d1['Paid on Date'][2:9]
			dateS =  int(dateS) #startdate
			print(dateS)
			Rd = tHistory.find({'Shop Name':'Raggaza'})
			R_day = 0
			rdata = []

			for i in range(0,7):
				print(str(dateS) + dateS2)
				for j in Rd:
					aa = str(dateS) + dateS2
					if j['Paid on Date'] == aa:
						R_day = R_day + float(j['Total Price'])
				print(R_day)
				rdata.append(R_day)
				R_day = 0
				dateS += 1
				if dateS == 30:
					rdata.append(0)	
			print("rag")
			print(rdata)
		except:
			pass
		try:
			d2 = tHistory.find({'Shop Name':'YOU'})[0]
			dateS12 = d2['Paid on Date'][:2]
			dateS22 = d2['Paid on Date'][2:9]
			dateS12 =  int(dateS12) #startdate
			print(dateS12)
			Yd = tHistory.find({'Shop Name':'YOU'})
			Y_day = 0
			ydata = []

			for i in range(0,7):
				print(str(dateS12) + dateS22)
				for j in Yd:
					aa2 = str(dateS12) + dateS22
					if j['Paid on Date'] == aa2:
						Y_day = Y_day + float(j['Total Price'])
				print(Y_day)
				ydata.append(Y_day)
				Y_day = 0
				dateS12 += 1
				if dateS12 == 30:
					ydata.append(0)	
			print("you")
			print(ydata)		
		except:
			pass
		try:
			d3 = tHistory.find({'Shop Name':'Tronic'})[0]
			dateS13 = d3['Paid on Date'][:2]
			dateS23 = d3['Paid on Date'][2:9]
			dateS13 =  int(dateS13) #startdate
			print(dateS13)
			Td = tHistory.find({'Shop Name':'Tronic'})
			T_day = 0
			tdata = []

			for i in range(0,7):
				print(str(dateS13) + dateS23)
				for j in Td:
					aa3 = str(dateS13) + str(dateS23)
					if j['Paid on Date'] == aa3:
						T_day = T_day + float(j['Total Price'])
				print(T_day)
				tdata.append(T_day)
				T_day = 0
				dateS13 += 1
				if dateS13 > 30:
					tdata.append(0)
			print("tr")
			print(tdata)
		except:
			pass
		try:
			d4 = tHistory.find({'Shop Name':'IS'})[0]
			dateS14 = d4['Paid on Date'][:2]
			dateS24 = d4['Paid on Date'][2:9]
			dateS14 =  int(dateS14) #startdate
			print(dateS14)
			Id = tHistory.find({'Shop Name':'IS'})
			I_day = 0
			idata = []

			for i in range(0,7):
				print(str(dateS14) + dateS24)
				for j in Id:
					aa4 = str(dateS14) + dateS24
					if j['Paid on Date'] == aa4:
						I_day = I_day + float(j['Total Price'])
				print(I_day)
				idata.append(I_day)
				I_day = 0
				dateS14 += 1
				if dateS14 == 30:
					idata.append(0)	
			print("is")
			print(idata)
		except:
			pass

		try:
			if tdata[0] > 1:
				pass
			pass	
		except:
			tdata = [5,5,5,5,5,5,5]

		try:
			if ydata[0] > 1:
				pass
			pass	
		except:
			ydata = [7,7,7,7,7,7,7]

		try:
			if idata[0] > 1:
				pass
			pass	
		except:
			idata = [9,9,9,9,9,9,9]				

		try:
			if rdata[0] > 1:
				pass
			pass	
		except:
			rdata = [11,11,11,11,11,11,11]

		d15 = tHistory.find()[0]
		dateS5 = d15['Paid on Date'][:2]
		dateS25 = d15['Paid on Date'][2:9]	
		dlabels = []
		try:
			dateS5 = int(dateS5)
			for i in range(1,7):
				dlabels.append(str(dateS5) + dateS25) 
				dateS5 = dateS5 + 1

		except:
			pass

		
		print(dlabels)
		
		qt = tHistory.find()
		topq =[] 
		plabels = []
		

		for q in qt:
			topq.append(int(q['Quantity']))

			plabels.append(str(q['Item Title']))

		con = zip(topq,plabels)
		a23 = list(con)
		a23.sort(reverse=True)
		a23 = a23[0:10]
		print(a23[0][0])
		pname = []
		pquan = []

		for i in range(0,10):
		 	pname.append(a23[i][1])
		 	pquan.append(a23[i][0])

		
		return render_template('home.html',records = tHistory.find()
			,total_R = ("%.2f" % round(total_R,2))
			,total_T = ("%.2f" % round(total_T,2))
			,total_I = ("%.2f" % round(total_I,2))
			,total_Y = ("%.2f" % round(total_Y,2))
			,stotal = str(total_R)
			,Rdata = rdata ,Tdata = tdata,Idata =idata,Ydata=ydata
			,Dlabels= dlabels,Topq = pquan,Plabels=pname )