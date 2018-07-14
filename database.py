# -*- coding: utf-8 -*-
# handling the data from "database.txt"
# payments details as per database file
from datetime import date, timedelta, datetime
from decimal import *  # decimal numbers
# from newgui import *

# payments is the dictionary that collects all the Payment objects in accordance to where they belong
# key: string describing the kind of the payment - 'directDebit', 'standingOrder', etc...
# value: list of Payment objects that belong to the category
payments = {
	"directDebit": list(),
	"standingOrder": list(),
	"cardPayment": list(),
	"income": list()
	}

# day of the first payday; used for calculating financial period
PAY_DAY = 24

# Today is that day. It's used for calculating current financial period
today = date.today()

# calculating beginning and the end of current financial period
if today.day >= PAY_DAY:
	start_date = date(today.year, today.month, PAY_DAY)
	end_date = date(today.year, today.month + 1, PAY_DAY - 1)
else:
	start_date = date(today.year, today.month - 1, PAY_DAY)
	end_date = date(today.year, today.month, PAY_DAY - 1)

# If start_date comes up on Saturday or Sunday, it is kicked back to the Friday before
if start_date.isoweekday() == 6 or start_date.isoweekday() == 7:
	start_date += timedelta(days=5 - start_date.isoweekday())

# calendar_dict is the dictionary that will hold all generated Payment objects
# key: date string in format 'mmm-dd'
# value: list of Payment objects that are to be paid on that date
calendar_dict = dict()

# print("Start date: " + str(start_date))  # testing
# print("End date: " + str(end_date))  # testing


def read_data():
	"""reads the data from file and creates the Payment objects"""

	data = open("database.txt", "r", encoding="UTF-8")  # opening the file
	for line in data:  # iterating through the database.txt file
		if line[0] == "#":  # this is comment, so skip it
			continue
		else:
			values = line.split(",")  # split line into values

			for i in range(len(values)):
				values[i].strip()  # removing spaces from values

			# values are separated by comma
			# line no.      description
			# 0: type of payment (directDebit, standingOrder, cardPayment, income)
			#    this will be used to create a respective Payment class object
			# 1: is the payment active
			# 2: description of the payment
			# 3: amount of the payment
			# 4: day of the payment
			# 5: how many payments is intended (0=indefinite, 1=one-off, x=number of payments)
			# 6: frequency: how often is the payment processed (1=weekly, 2=monthly, 4=four-weekly)
			# 7: count of how many payments has gone since the first payment
			# 8: lastPaid: the date of the last payment

			# setting the payment date
			payment_day = int(values[4])  # payment day taken from database file
			frequency = int(values[7])  # how often is it paid taken from database file

			if payment_day >= PAY_DAY:
				payment_month = start_date.month
			else:
				payment_month = end_date.month

			payment_date = date(start_date.year, payment_month, payment_day)

			insert_payment(payment_day, payment_date, values)

			# calendar_dict[calendar_key] = payment
			print(calendar_dict)

			# getting the next payment date
			next_payment = calculate_next_payment(frequency, payment_date, payment_month)
			# print("Calculated next payment - 1: " + str(next_payment))

			# checking the next payment date
			while start_date <= next_payment <= end_date:
				insert_payment(payment_day, next_payment, values)

				# calendar_dict[calendar_key] = payment
				print(calendar_dict)

				next_payment = calculate_next_payment(frequency, next_payment, payment_month)
				# print("Calculated next payment - 2: " + str(next_payment))

	data.close()


def insert_payment(pd, p_d, v):
	"""
	Creates Payment object and inserts it into payments and calendar_dict dictionaries
	:param pd: payment_day
	:param p_d: payment_date
	:param v: values
	"""

	# if the payment comes on Saturday or Sunday it needs to be moved to the following Monday
	# print(p_d.strftime("%a"), v[2])
	if p_d.strftime("%a") == "Sat":
		if v[0] != "income":
			p_d += timedelta(days=2)
		else:
			p_d += timedelta(days=-1)

	elif p_d.strftime("%a") == "Sun":
		if v[0] != "income":
			p_d += timedelta(days=1)
		else:
			p_d += timedelta(days=-2)

	payment = Payment(  # creating the Payment object
		check_active(v[1]),  # is the payment active
		v[2],  # description
		Decimal(v[3]),  # amount
		pd,
		int(v[5]),  # how many payments
		int(v[6]),  # frequency of payment
		p_d,
		datetime.strptime("09/05/1978" + "06:00", "%d/%m/%Y%H:%M")  # date of last payment
	)

	# adding the Payment object to the payments dictionary
	payments[v[0]].append(payment)

	# adding the payment object to the dictionary
	calendar_key = p_d.strftime("%b-%d")
	if calendar_key in calendar_dict:
		calendar_dict[calendar_key].append(payment)
	else:
		calendar_dict[calendar_key] = [payment]


def calculate_next_payment(frequency, payment_date, payment_month):
	"""
	Calculates the date of next payment
	:param frequency: frequency of payments
	:param payment_date: date of payment
	:param payment_month:
	:return: next_payment: date of next payment
	"""
	if frequency == 1 or frequency == 4:  # weekly or four-weekly
		next_payment = payment_date + timedelta(weeks=frequency)
	elif frequency == 2:  # monthly
		next_payment = payment_date.replace(month=payment_month + 1)
	else:
		next_payment = date(1, 1, 1)

	print("Frequency : " + str(frequency))  # testing
	print("Payment date: " + str(payment_date))  # testing
	print("Next payment: " + str(next_payment))  # testing

	return next_payment


def check_active(value):
	"""
	converts from the string and returns appropriate Boolean value
	:param value: string to check
	:return: Boolean: True or False
	"""
	if value == "False":
		return False
	else:
		return True


def calculate_total(kind):
	""" Calculate total from the given list """
	total = 0
	for item in payments[kind]:
		if item.is_active:
			total += item.amount
	return total


# def get_month():
# 	"""
# 	iterate through the payments_dict dictionary
# 	and generates output list with all payments for the current financial period
# 	:return: output: list with all payments for financial period
# 	"""
# 	# output is the output list used for generating the month's
# 	output = []
# 	output1 = [[] for _ in range(6)]
# 	print(output1)
#
# 	# setting up the financial period's calendar
# 	week = 1
# 	period = timedelta(days=1)
# 	fpd = start_date  # financial period day
#
# 	# populating the payments
# 	while fpd <= end_date:  # outer loop to go through each week
# 		while True:  # inner loop to go through each day
# 			output.append("Week {} - {}, {} {}".format(
# 				str(week), fpd.strftime("%a"), str(fpd.day), str(fpd.strftime("%B"))
# 			))
#
# 			key_date = fpd.strftime("%b-%d")  # setting the key value to check against dictionary
# 			if key_date in calendar_dict:  # are there any payments that day?
# 				for item in calendar_dict[key_date]:
# 					output.append("Week {} -      {}: £{}".format(
# 						str(week),
# 						item.description.rstrip(),
# 						str(item.amount))
# 					)
# 					output1[week - 1].append([item, 0])
#
# 			if fpd.strftime("%a") == "Sun" or fpd == end_date:
# 				break
# 			else:
# 				fpd += period
#
# 		# end of inner loop
#
# 		fpd += period
# 		week += 1
# 		output.append("--------")
# 	# end of outer loop
# 	print(output1)
#
# 	return calendar_dict
#
#
def get_start_date():  # getter for start_date
	return start_date


def get_end_date():  # getter method for end_date
	return end_date


# Class definition
class Payment(object):
	"""Payment - a payment class that declares all the payments"""

	def __init__(self, is_active, description, amount, payment_day, count, toll, frequency, last_paid):
		"""

		:param is_active: is the payment active
		:param description: payment's description
		:param amount: payment's amnt
		:param payment_day: day of the month the payment is being processed
		:param count: how many payments are being set (-1 for indefinite)
		:param toll: how many payments have already been processed
		:param frequency: how often is the payment processed (1=weekly, 2=monthly, 4=four-weekly)
		:param last_paid: the date of the last payment
		"""

		# self.isOutcome = isOutcome
		self.is_active = is_active
		self.payment_day = payment_day
		self.amount = Decimal(amount)
		self.description = description.rstrip()
		self.count = count
		self.toll = toll
		self.frequency = frequency
		self.last_paid = last_paid

	def __repr__(self):
		return "{} na kwotę: £{}".format(self.description, self.amount)
