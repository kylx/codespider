

from enum import Enum

class Enums():

	SEX = [
		['m', 'male'],
		['f', 'female'],
	]

	# GSCS code, Short name, long name
	REGIONS = [
		['130000000', 'NCR', 'National Capital Region'],
		['140000000', 'CAR', 'Cordillera Administrative Region'],
		# ... other regions
		
		
		
		
	]
	
	# GSCS code, name
	CITIES = [
		# sadakwdjosado
	]
	
	@staticmethod
	def print_all():
		print("Sex")
		for sex in Enums.SEX:
			print( f'  {sex[0]} - {sex[1]}' )
			
		for rgn in Enums.REGIONS:
			print( f'  {rgn[0]} : {rgn[1]} - {rgn[2]}' )
		