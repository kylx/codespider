from .enums import Enums
# from .forms import PatientForms

def filter_location(location_list, location_filter):
    return [location for location in location_list if location[0].startswith(location_filter[0])]

def run():
	
    pass
    
	# print(PatientForms())
    # print('Running startup...')
    # print(Enums.REGIONS)
    # print(Enums.PROVINCES)
    
    # r = Enums.REGIONS[0]
    # fp = filter(Enums.PROVINCES
    
    # for region in Enums.REGIONS:
        # print(region)
        # for province in filter_location(Enums.PROVINCES, region):
            # print('   ' + ' '.join(province))
            # for city in filter_location(Enums.CITIES, province):
                # print('       ' + ' '.join(city))