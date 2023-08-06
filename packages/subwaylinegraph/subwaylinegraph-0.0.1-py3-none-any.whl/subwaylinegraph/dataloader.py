import csv
import io
import collections
import os
import pandas


filename = '서울특별시 노선별 지하철역 정보(신규).csv'
opendata = os.path.join(os.path.abspath("subwaylinegraph"), 'data', filename)

def read_seoul_metro():
	samdasu = {}
	df = pandas.read_csv(opendata, sep=',', encoding='CP949')
	for rows in df.values:
		li = []
		li.append(str(rows[1]))
		li.append(str(rows[3]))
		samdasu[rows[4]] = li
	od = collections.OrderedDict(sorted(samdasu.items(), key=str))
	return od


def readSeoulMetro():
	samdasu = {}
	with io.open(opendata, mode='r', encoding='utf-8') as csvfile:
		datareader = csv.reader(csvfile, delimiter=' ', quotechar=',')
		next(datareader)
		for row in datareader:
			str = "\" ".join(row)
			str = str.replace('\"','')
			obj = str.rstrip().split(',')

			li = []
			li.append(obj[1])
			li.append(obj[2])
			samdasu[obj[3]] = li

	od = collections.OrderedDict(sorted(samdasu.items()))
	return od

def name_fr_mapping(od):
	mapping = {}
	for fr, name_line in od.items():
		mapping[name_line[0]] = fr
	return mapping

def fr_station_mapping(od):
	mapping = {}
	for fr, name_line in od.items():
		mapping[fr] = name_line[0]
	return mapping