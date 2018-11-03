import os
import pandas as pd
import numpy as np
import xlrd

from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import load_workbook

from elucidata import models

# Create your views here.

def ques1(request):
	context_dict = {}
	if request.method == 'POST':
		try:
			my_file = models.File()
			if "file" in request.FILES:
				my_file.media = request.FILES["file"]
				name = request.FILES["file"].name
			excel_file = my_file.media
			df = pd.read_excel(excel_file)
			df["Accepted Compound ID"] = df["Accepted Compound ID"].astype(str)
			end_with_lpc = df[df["Accepted Compound ID"].map(lambda x: x.endswith('LPC'))] 
			df1 = df[df["Accepted Compound ID"].map(lambda x: x.endswith('PC'))]
			end_with_pc = df1[~df1["Accepted Compound ID"].map(lambda x: x.endswith('LPC'))]
			end_with_plasmalogen = df[df["Accepted Compound ID"].map(lambda x: x.endswith('plasmalogen'))] 
			print("Accepted Compound ID : Ends with PC")
			print(end_with_pc)
			print("Accepted Compound ID : Ends with LPC")
			print(end_with_lpc)
			print("Accepted Compound ID : Ends with PLASMALOGEN")
			print(end_with_plasmalogen)
			writer = pd.ExcelWriter(excel_file, engine = 'xlsxwriter')
			df.to_excel(writer, sheet_name='Raw Data')
			end_with_pc.to_excel(writer, sheet_name = 'PC')
			end_with_lpc.to_excel(writer, sheet_name= 'LPC')
			end_with_plasmalogen.to_excel(writer, sheet_name= 'Plasmalogen')
			writer.save()
			writer.close()
			my_file.save()
			fname = my_file.media.name
			path = 'media/'+fname
			print(path)
			if os.path.exists(path):
				with open(path, "r") as excel:
					data = excel.read()
				response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
				response['Content-Disposition'] = 'attachment; filename=ques1.xlsx'
				if os.path.isfile(path):
					os.remove(path)
				return response
		except Exception as e:
			print(e)
	return render(
		request, "ques1.html", context_dict
	)

def ques2(request):
	context_dict = {}
	if request.method == 'POST':
		try:
			my_file = models.File()
			if "file" in request.FILES:
				my_file.media = request.FILES["file"]
			excel_file = my_file.media
			df = pd.read_excel(excel_file)
			df["Retention Time Roundoff (in mins)"] = df['Retention time (min)'].apply(np.round)
			df.to_excel("./media/files/ques2.xlsx", index=False);
			path = 'media/files/ques2.xlsx'
			if os.path.exists(path):
				with open(path, "r") as excel:
					data = excel.read()
				response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
				response['Content-Disposition'] = 'attachment; filename=ques2.xlsx'
				if os.path.isfile(path):
					os.remove(path)
				return response
		except Exception as e:
			print(e)
	return render(
		request, "ques2.html", context_dict
	)

def ques3(request):
	context_dict = {}
	if request.method == 'POST':
		try:
			my_file = models.File()
			if "file" in request.FILES:
				my_file.media = request.FILES["file"]
			excel_file = my_file.media
			df = pd.read_excel(excel_file)
			df1 = df.groupby('Retention Time Roundoff (in mins)').mean().count()
			print(df1)
		except Exception as e:
			print (e)
	return render(
		request, "ques3.html", context_dict
	)

def ques4(request):
	context_dict = {}
	if request.method == 'POST':
		try:
			my_file = models.File()
			if "file" in request.FILES:
				my_file.media = request.FILES["file"]
			csv_file = my_file.media
			df = pd.read_csv(csv_file)
			print(pd.concat([df.ix[:,i:i+3].mean(axis=1) for i in range(2,len(df.columns),3)], axis=1))
		except Exception as e:
			print(e)
	return render(
		request, "ques4.html", context_dict
	)
