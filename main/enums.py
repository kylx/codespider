			

class LocationCode():
	"""
	see https://psa.gov.ph/classification/psgc/
	Browse PSGC database on right-side of web page
	
	PSGC codes have the format: rrppccxxx
		region = rr
		province = pp
		city = cc
		xxx is not used
	"""
	def __init__(self, region, province=0, city=0):
		self.region = region
		self.province = province
		self.city = city
		
	"""
	Convert to string
	- concatenate region + province + city using python fstrings
	- :02d formats the numbers to always use 2 digits. i.e, 3 -> '03', 0 -> '00'
	"""
	def __str__(self):
		return f'{self.region:02d}{self.province:02d}{self.city:02d}'
		
class Location():
	def __init__(self, code, long_name, short_name=''):
		self.code = code
		self.long_name = long_name
		if short_name: 
			self.short_name = short_name
		else:
			self.short_name = long_name
		
	def __str__(self):
		return f'{self.code}: {self.short_name} - {self.long_name}'
	
# Helper functions for easier encoding of locations
def region(region_number, long_name, short_name=''):
	code = LocationCode(region_number)
	location = Location(code, long_name, short_name)
	return location
	
def province(region_number, province_code, long_name, short_name=''):
	code = LocationCode(region_number, province_code)
	location = Location(code, long_name, short_name)
	return location
	
def city(region_number, province_code, city_code, long_name, short_name=''):
	code = LocationCode(region_number, province_code, city_code)
	location = Location(code, long_name, short_name)
	return location

	"""
	TODO
		- get regions, provinces, cities as arrays/list of a certain format which can be used in models
		- get provinces in a region
		- get cities in a province
		- get cities in a region ?? (maybe not needed)
		- refactor (daghan redundant codes, after encode dako ra kaayo ang file, need to split, etc..)
	"""
	
# ----- Encode information here -----
class Enums():

	SEX = [
		['m', 'male'],
		['f', 'female'],
	]

	# region number, long name, short name(optional)
	REGIONS = [
		region(1, 'Sacrificer XY', 'SAC'),
		region(2, 'Zewtalia', 'ZEWT'),
		# ...
		# ... other regions
		# ...
	]
	
	# region number, province code, long name, short name(optional)
	PROVINCES = [
		province(1, 1, 'asdweees', 'aasx'),
		province(2, 23, 'as  asd2', 'sdse'),
		# ...
		# ... other provinces
		# ...
	]
	
	# region number, province code, long name, short name(optional)
	CITIES = [
		city(1, 1, 23, 'davao city', 'dvo'),
		city(1, 5, 13, 'aaswe city', 'aa'),
		city(4, 12, 3, '2sdf city', 'zss'),
		# ...
		# ... other cities
		# ...
	]
	
	# For simple visual checking
	# call this method somewhere to check
	@staticmethod
	def print_all():
		print('Regions')
		print(Enums.REGIONS)
		for region in Enums.REGIONS:
			print('  ', region)
		print('Provinces')
		for province in Enums.PROVINCES:
			print('  ', province)
		print('Cities')
		for city in Enums.CITIES:
			print('  ', city)

		