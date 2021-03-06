import logging
from persiantools.jdatetime import JalaliDateTime
from persiantools import characters, digits
from decimal import Decimal
from django.template import Library
import datetime
from django.utils.text import slugify

register = Library()
logger = logging.getLogger(__name__)


def valid_numeric(arg):
	if isinstance(arg, (int, float, Decimal)):
		return arg
	try:
		arg= str(arg).replace(',','').replace('/','.').replace('\\','.')
		return int(arg)
	except ValueError:
		return float(arg)


def handle_float_decimal_combinations(value, arg, operation):
	if isinstance(value, float) and isinstance(arg, Decimal):
		logger.warning(
			'Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg)
		)
		value = Decimal(str(value))
	if isinstance(value, Decimal) and isinstance(arg, float):
		logger.warning(
			'Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg)
		)
		arg = Decimal(str(arg))
	return value, arg


@register.filter
def sub(value, arg):
	"""Subtract the arg from the value."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '-'
		)
		return nvalue - narg
	except (ValueError, TypeError):
		try:
			return value - arg
		except Exception:
			return ''


@register.filter
def mul(value, arg):
	"""Multiply the arg with the value."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '*'
		)
		return nvalue * narg
	except (ValueError, TypeError):
		try:
			return value * arg
		except Exception:
			return ''


@register.filter
def div(value, arg):
	"""Divide the arg by the value."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '/'
		)
		return nvalue / narg
	except (ValueError, TypeError):
		try:
			return value / arg
		except Exception:
			return ''


@register.filter
def intdiv(value, arg):
	"""Divide the arg by the value. Use integer (floor) division."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '//'
		)
		return nvalue // narg
	except (ValueError, TypeError):
		try:
			return value // arg
		except Exception:
			return ''


@register.filter(name='abs')
def absolute(value):
	"""Return the absolute value."""
	try:
		return abs(valid_numeric(value))
	except (ValueError, TypeError):
		try:
			return abs(value)
		except Exception:
			return ''


@register.filter
def mod(value, arg):
	"""Return the modulo value."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '%'
		)
		return nvalue % narg
	except (ValueError, TypeError):
		try:
			return value % arg
		except Exception:
			return ''


@register.filter(name='addition')
def addition(value, arg):
	"""Float-friendly replacement for Django's built-in `add` filter."""
	try:
		nvalue, narg = handle_float_decimal_combinations(
			valid_numeric(value), valid_numeric(arg), '+'
		)
		return nvalue + narg
	except (ValueError, TypeError):
		try:
			return value + arg
		except Exception:
			return ''

@register.filter(name='format')
def format(value, arg):
	return arg.format(value)


@register.filter(name='intcomma')
def intcomma(value):
	"""Return the absolute value."""
	try:
		value = valid_numeric(value)
		if str(value).endswith('.0'): value =int(float(value))
		return "%s"%'{0:,}'.format(value)
	except (ValueError, TypeError):
		try:
			value =int(float(value))
			return "%s"%'{0:,}'.format(value)
		except Exception:
			return value


@register.filter(name='to_int')
def to_int(value):
	"""Return the absolute value."""
	try:
		return int(float(value))
	except (ValueError, TypeError):
		try:
			return int(float(value.replace(',','').replace('/','.').replace('\\','.')))
		except Exception:
			return 0

@register.filter(name='jdatetime')
def jdatetime(value,arg=""):
	try:
		if str(value) == "now":
			if arg=="": arg="%Y-%m-%d %H:%M:%S"
			resultdate= JalaliDateTime.now()
		elif str(value) == "time":
			if arg=="": arg ="%H:%M:%S"
			resultdate= JalaliDateTime.now()
		elif str(value) == "date":
			if arg=="": arg ="%Y-%m-%d"
			resultdate= JalaliDateTime.now()
		else:
			if isinstance(value, datetime.date):
				resultdate= JalaliDateTime.to_jalali(value)
			else:
				year, month, day = map(int, value[:10].split('-'))
				hour = minute = second =millisecond=0
				if value.find(' ') == 10:
					date,time = value.split(' ')
					time=time.split(':')
					if len(time)==1:
						hour= int(time[0])
					elif len(time)==2:
						hour= int(time[0])
						minute= int(time[1])
					elif len(time)==3:
						hour= int(time[0])
						minute= int(time[1])
						time=time[2].split('.')
						second= int(time[0])
						if len(time)>1:
							millisecond= int(time[1])						
				resultdate= JalaliDateTime.to_jalali(datetime.datetime(year, month, day,hour, minute, second, millisecond))
		if arg :
			return resultdate.strftime(arg)
		else:
			return resultdate
	except Exception as err:
		return "jdatetime error:%s"%err


@register.filter(name='digit')
def digit(values,arg):
	values = str(values)
	if arg=="" or arg =="en_to_fa":
		return digits.en_to_fa(values)
	elif arg =="ar_to_fa":
		return digits.ar_to_fa(values)
	elif arg =="fa_to_en":
		return digits.fa_to_en(values)	
	elif arg =="fa_to_ar":
		return digits.fa_to_ar(values)	
	else:
		return values
	
@register.filter(name='character')
def character(values):
	return characters.ar_to_fa(values)	

@register.filter(name='slugify_unicode')
def slugify_unicode(value):
	"""Return the slugify unicode value."""
	try:
		return "%s"%(slugify(value, allow_unicode=True))
	except (ValueError, TypeError):
		try:			
			return str(value).replace("  "," ").replace(" ","_").replace("__","_")
		except Exception:
			return value