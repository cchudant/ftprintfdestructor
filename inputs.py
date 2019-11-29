import random
import string

def random_string(length):
	letters = string.ascii_letters + string.digits + " "
	return ''.join(random.choice(letters) for i in range(length))

def random_unicode(length):
	# sample ranges
	include_ranges = [
		(0x0021, 0x0021),
		(0x0023, 0x0026),
		(0x0028, 0x005B),
		(0x005D, 0x007E),
		(0x00A1, 0x00AC),
		(0x00AE, 0x00FF),
	]

	def format_unicode(code_point):
		return chr(code_point)

	alphabet = [
		format_unicode(code_point) for current_range in include_ranges
			for code_point in range(current_range[0], current_range[1] + 1)
	]
	return ''.join(random.choice(alphabet) for i in range(length))

def input_string(size_modifier):
	choice = random.choice([0, 1, 2])

	if (size_modifier != "l"):
		if (choice == 0):
			return '"{}"'.format(random_string(random.randint(1, 100)))
		if (choice == 1):
			return "NULL"
		if (choice == 2):
			return '""'
	else:
		if (choice == 0):
			return 'L"{}"'.format(random_unicode(random.randint(1, 10)))
		if (choice == 1):
			return "(wchar_t *)NULL"
		if (choice == 2):
			return 'L""'

def input_int_with_limits(minimum, maximum, litteral, suffix=""):
	choice = random.choice([0, 1, 2, 3] if minimum != 0 else [0, 1, 3])
	if (choice == 0):
		return str(random.randint(minimum + 1, maximum)) + suffix
	if (choice == 1):
		return "{}_MAX".format(litteral)
	if (choice == 2):
		return "{}_MIN".format(litteral)
	if (choice == 3):
		return str(0) + suffix

def input_uint(size_modifier):
	if (size_modifier == "hh"): # unsigned char
		return "(unsigned char)" + input_int_with_limits(0, 255, "UCHAR")
	elif (size_modifier == "h"): # unsigned short
		return "(unsigned short)" + input_int_with_limits(0, 65535, "USHRT")
	elif (size_modifier == ""): # unsigned int
		return input_int_with_limits(0, 4294967295, "UINT", "u")
	elif (size_modifier == "l"): # unsigned long int
		return input_int_with_limits(0, 18446744073709551615, "ULONG", "lu")
	elif (size_modifier == "ll"): # unsigned long long int
		return input_int_with_limits(0, 18446744073709551615, "ULLONG", "llu")

def input_int(size_modifier):
	if (size_modifier == "hh"): # signed char
		return "(signed char)" + input_int_with_limits(-128, 127, "SCHAR")
	elif (size_modifier == "h"): # short
		return "(short)" + input_int_with_limits(-32768, 32767, "SHRT")
	elif (size_modifier == ""): # int
		return input_int_with_limits(-2147483648, 2147483647, "INT")
	elif (size_modifier == "l"): # long int
		return input_int_with_limits(-9223372036854775808, 9223372036854775807, "LONG", "l")
	elif (size_modifier == "ll"): # long long int
		return input_int_with_limits(-9223372036854775808, 9223372036854775807, "LLONG", "ll")

def input_ptr():
	return "(void *)({})".format(input_int("ll")) # unsigned long long int

def input_char(size_modifier):
	choice = random.choice([0, 1])
	if (size_modifier != "l"):
		if (choice == 0):
			return "'" + random.choice(string.ascii_letters + string.digits) + "'"
		if (choice == 1):
			return "'\\0'"
	else:
		if (choice == 0):
			return "L'" + random_unicode(1) + "'"
		if (choice == 1):
			return "L'\\0'"

def input_float():
	choice = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
	if (choice == 0):
		return ".0 / .0"
	elif (choice == 1):
		return ".1 / .0"
	elif (choice == 2):
		return "-.1 / .0"
	elif (choice == 3):
		return "0." + str(random.randint(0, 1000000))
	elif (choice == 4):
		return "-0." + str(random.randint(0, 1000000))
	elif (choice == 5):
		return str(random.randint(-1000000, 1000000)) + ".0"
	elif (choice == 6):
		return str(random.randint(-1000000, 1000000)) + "." + str(random.randint(0, 1000000))
	elif (choice == 7):
		return str(random.randint(-100, 100)) + "e" + str(random.randint(-10, 10))
	elif (choice == 8):
		return "0."

def random_arg(tests):
	format = "%"
	data = []
	choices = ["s", "c", "i", "d", "x", "X", "%", "u", "p"]
	if (tests["bonus_float_conversion_f"]):
		choices += ["f"]
	if (tests["bonus_float_conversion_e"]):
		choices += ["e"]
	if (tests["bonus_float_conversion_g"]):
		choices += ["g"]

	type = random.choice(choices)

	size_modifier = ""
	if (random.random() > .5):
		if (type in "cs"):
			size_modifier = "l"
		elif (random.random() > .5):
			size_modifier = "h" * random.choice([1, 2])
		else:
			size_modifier = "l" * random.choice([1, 2])

	width = ""
	if (random.random() > .5 and type not in "%"):
		if (random.random() > .8):
			width = "*"
			data.append(str(random.randint(-10, 10)))
		else:
			width = str(random.randint(1, 20))

	size = ""
	if (random.random() > .5 and type not in  "%cp"):
		if (random.random() > .8):
			size = ".*"
			data.append(str(random.randint(-10, 10)))
		else:
			size = "." + str(random.randint(0, 5))

	flags = ""

	if (type in "xXfge" and tests["bonus_hashtag"] and random.random() > .5):
		flags += "#"

	choice = random.choice([0, 1, 2])
	if (choice == 1 or type in "psc"):
		flags += "-"
	elif (choice == 2):
		flags += "0"

	choice = random.choice([0, 1, 2])
	if (type in "di" and tests["bonus_space"] and choice == 1):
		flags += " "
	elif (type in "di" and tests["bonus_plus"] and choice == 2):
		flags += "+"

	if (type == "s"):
		format += flags
		format += width
		format += size
		if (tests["bonus_size_modifier_wide_char"]):
			format += size_modifier
			data.append(input_string(size_modifier))
		else:
			data.append(input_string(""))
	if (type == "c"):
		format += flags
		format += width
		if (tests["bonus_size_modifier_wide_char"]):
			format += size_modifier
			data.append(input_char(size_modifier))
		else:
			data.append(input_char(""))
	if (type in "id"):
		format += flags
		format += width
		format += size
		if (tests["bonus_size_modifier"]):
			format += size_modifier
			data.append(input_int(size_modifier))
		else:
			data.append(input_int(""))
	if (type == "x"):
		format += flags
		format += width
		format += size
		if (tests["bonus_size_modifier"]):
			format += size_modifier
			data.append(input_uint(size_modifier))
		else:
			data.append(input_uint(""))
	if (type == "X"):
		format += flags
		format += width
		format += size
		if (tests["bonus_size_modifier"]):
			format += size_modifier
			data.append(input_uint(size_modifier))
		else:
			data.append(input_uint(""))
	if (type == "u"):
		format += flags
		format += width
		format += size
		if (tests["bonus_size_modifier"]):
			format += size_modifier
			data.append(input_uint(size_modifier))
		else:
			data.append(input_uint(""))
	if (type == "p"):
		format += flags
		format += width
		data.append(input_ptr())
	if (type == "f"):
		format += flags
		format += width
		format += size
		data.append(input_float())
	if (type == "e"):
		format += flags
		format += width
		format += size
		data.append(input_float())

	format += type
	return (format, data)
