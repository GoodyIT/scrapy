

def validate(value):
	value.replace('&#039;', '')
	value.replace(u'\u2013', '-')
	value.replace(u'\u2019', '-')