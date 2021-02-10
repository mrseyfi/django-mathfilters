def valid_numeric(arg):
	arg= arg.replace(',','').replace('/','.')
	if isinstance(arg, (int, float)):
		return arg
	try:
		return int(arg)
	except ValueError:
		return float(arg)


def intcomma(value):
	"""Return the absolute value."""
	try:
		value = valid_numeric(value.replace(',',''))
		if str(value).endswith('.0'): value =int(float(value))
		return "%s"%'{0:,}'.format(value)
	except (ValueError, TypeError):
		try:
			value =int(float(value))
			return "%s"%'{0:,}'.format(value)
		except Exception:
			return ''

va = '222222222222222222222222222222222222'
print(intcomma(va))
# print((va))
# print(int(float(va)))