from django import template

register = template.Library()

def filter_location(location_list, location_filter):
    return [location for location in location_list if location[0].startswith(location_filter[0])]


register.filter('filter_location', filter_location)