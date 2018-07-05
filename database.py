# handling the data from "database.txt"
# payments details as per database file

# import payments as p
from datetime import date, timedelta, datetime
from decimal import *  # decimal numbers

getcontext().prec = 10  # setting the decimals to two numbers, as in payments

payments = {  # dictionary that will collect all the Payments objects
    "directDebit": list(),
    "standingOrder": list(),
    "cardPayment": list(),
    "income": list()
    }

PAY_DAY = 24  # day of the first payday; used for calculating financial period
today = date.today()

if today.day >= PAY_DAY:  # calculating beginning and the end of current financial period
    start_date = date(today.year, today.month, PAY_DAY)
    end_date = date(today.year, today.month + 1, PAY_DAY - 1)
else:
    start_date = date(today.year, today.month - 1, PAY_DAY)
    end_date = date(today.year, today.month, PAY_DAY - 1)

print("Start date: " + str(start_date))  # testing
print("End date: " + str(end_date))  # testing

# setting up the financial period's calendar
week = 1
period = timedelta(days=1)
week_date = start_date
day = week_date.strftime("%A")
print("Week " + str(week) + ":")

while True:  # loop to populate the calendar
    print(str(day) + ":" + str(week_date))
    week_date += period
    if day == "Sunday":
        week += 1
        break


def read_data():
    """reads the data from file and creates the Payment objects"""

    data = open("database.txt", "r")  # opening the file
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

            payments[values[0]].append(Payment(
                check_active(values[1]),  # is the payment active
                values[2],  # description
                Decimal(values[3]),  # amount
                payment_day,
                int(values[5]),
                int(values[6]),
                payment_date,
                datetime.strptime("09/05/1978" + "06:00", "%d/%m/%Y%H:%M")
            ))

            # getting the next payment date
            next_payment = calculate_next_payment(frequency, payment_date, payment_month)
            # print("Calculated next payment - 1: " + str(next_payment))

            # checking the next payment date
            while start_date <= next_payment <= end_date:
                payments[values[0]].append(Payment(
                    check_active(values[1]),  # is the payment active
                    values[2],  # description
                    Decimal(values[3]),  # amount
                    payment_day,
                    int(values[5]),
                    int(values[6]),
                    next_payment,
                    datetime.strptime("09/05/1978" + "06:00", "%d/%m/%Y%H:%M")
                ))

                next_payment = calculate_next_payment(frequency, next_payment, payment_month)
                # print("Calculated next payment - 2: " + str(next_payment))

    data.close()


def calculate_next_payment(frequency, payment_date, payment_month):
    # calculating the next payment date
    if frequency == 1 or frequency == 4:
        period = timedelta(weeks=frequency)
        next_payment = payment_date + period
    elif frequency == 2:
        next_payment = payment_date.replace(month=payment_month + 1)
    else:
        next_payment = date(1, 1, 1)

    print("Frequency : " + str(frequency))
    print("Payment date: " + str(payment_date))
    print("Next payment: " + str(next_payment))

    return next_payment


def check_active(value):  # checks for the value of "True" and returns appropriately
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


# Class definition
class Payment(object):
    """Payment - a payment class that declares all the payments"""

    def __init__(self, is_active, description, amount, payment_day, count, toll, frequency, last_paid):
        """

        :param is_active: is the payment active
        :param description: payment's description
        :param amount: payment's amount
        :param payment_day: day of the month the payment is being processed
        :param count: how many payments are being set (-1 for indefinite)
        :param toll: how many payments have already been processed
        :param frequency: how often is the payment processed (1=weekly, 2=monthly, 4=four-weekly)
        :param last_paid: the date of the last payment
        """

        # self.isOutcome = isOutcome
        self.is_active = is_active
        self.payment_day = payment_day
        self.amount = amount
        self.description = description
        self.count = count
        self.toll = toll
        self.frequency = frequency
        self.last_paid = last_paid

    def __repr__(self):
        return "\"{}\", paid on {}, for £{}".format(self.description, self.payment_day, self.amount)
