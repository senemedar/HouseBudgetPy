from tkinter import *
from datetime import *


class PaymentsCalendar:
	"""Calendar class to deal with all financial period calculations"""
	today = date.today()  # what day is today?
	day_now = today.day  # retrieving the day ...
	month_now = today.month  # ... the month ...
	year_now = today.year  # ... and the year

	PAY_DAY = 24  # day of the first income

	if day_now >= PAY_DAY:
		start_date = date(year_now, month_now, PAY_DAY)
		end_date = date(year_now, month_now + 1, PAY_DAY - 1)
	else:
		start_date = date(year_now, month_now - 1, 24)
		end_date = date(year_now, month_now, PAY_DAY - 1)

	# If start_date comes up on Saturday or Sunday, it is kicked back to the Friday before
	if start_date.isoweekday() == 6 or start_date.isoweekday() == 7:
		start_date += timedelta(days=5 - start_date.isoweekday())

	week = 1
	period = timedelta(days=1)  # we're adding a day at a time
	fpd = start_date  # financial period day

	# calendar_days = []
	# for i in range(32):
	# calendar_days.append(list())
	calendar_days = [[] for _ in range(32)]  # same as above but 'Python way' in just one line

	calendar_days[3].append(100)  # add a few random amounts
	calendar_days[5].append(250)
	calendar_days[5].append(350)

	# populating the payments
	output = []
	while fpd <= end_date:  # outer loop to go through each week
		while True:  # inner loop to go through each day
			data_string = "Week " + str(week) + " - " + fpd.strftime("%a") + ", " + str(fpd.day) + " " + str(
				fpd.strftime("%B"))

			if calendar_days[fpd.day]:  # are there any payments that day?
				data_string += " : "
				for amount in calendar_days[fpd.day]:
					data_string += "£" + str(amount) + ", "

			if fpd.strftime("%a") == "Sun" or fpd == end_date:
				break
			else:
				fpd += period

			output.append(data_string)
		# end of inner loop

		fpd += period
		week += 1
		output.append("--------")

	# end of outer loop

	def get_month(self):
		return self.output

	def get_start_date(self):  # getter for start_date
		return self.start_date

	def get_end_date(self):  # getter method for end_date
		return self.end_date


class PaymentsGUI:
	def __init__(self, parent):

		self.myParent = parent
		self.myParent.geometry("640x800")

		# setting the variables to control from view buttons
		self.check_button_dd = IntVar(value=1)
		self.check_button_so = IntVar(value=1)
		self.check_button_cp = IntVar(value=1)

		# Our topmost frame is called myContainer1
		self.myContainer1 = Frame(parent)
		self.myContainer1.pack(expand=YES, fill=BOTH)

		# We will use HORIZONTAL (left/right) orientation inside myContainer1.
		# Inside myContainer1, we create list_view_frame, view_control_frame and buttons_frame.

		# control frame - basically everything except the main buttons frame
		self.list_view_frame = Frame(self.myContainer1)
		self.list_view_frame.pack(side=LEFT, expand=YES, fill=BOTH, padx=10, pady=5, ipadx=5, ipady=5)

		# control frame - basically everything except the main buttons frame
		self.program_frame = Frame(self.myContainer1)
		self.program_frame.pack(side=LEFT, expand=NO, fill=Y, padx=10, pady=5, ipadx=5, ipady=5)

		# inside list_view_frame we create a header label
		# and a list_frame at the top,
		# and buttons_frame at the bottom

		message = "Payments for the spending period\nfrom {} to {}".format(
			cal.get_start_date().strftime("%A, %d of %B"), cal.get_end_date().strftime("%A, %d of %B")
		)
		Label(self.list_view_frame, text=message, justify=CENTER).pack(side=TOP, anchor=N)

		# buttons frame
		self.buttons_frame = Frame(self.list_view_frame)
		self.buttons_frame.pack(side=BOTTOM, expand=NO, fill=X)

		# list element to display all the payments
		self.lb = Listbox(self.list_view_frame, bg="#CCC", selectmode=EXTENDED)  # week 1 listbox
		# self.lb.insert(0, "Direct Debit: " + str(self.check_button_dd.get()))
		# self.lb.insert(1, "Standing Order: " + str(self.check_button_so.get()))
		# self.lb.insert(2, "Card Payment: " + str(self.check_button_cp.get()))
		self.list_update()  # filling the list for the first time
		self.lb.pack(side=TOP, fill=BOTH, expand=YES)

		self.lb2 = Listbox(self.list_view_frame, bg="#CCC", selectmode=EXTENDED)  # week 2 listbox
		self.lb2.insert(0, "Week 2")
		self.lb2.pack(side=TOP, fill=BOTH, expand=YES)
		self.list2_update()

		# the view control checkbutton
		self.button_dd = Checkbutton(
							self.buttons_frame,  # Direct Debits button
							variable=self.check_button_dd,
							text="Direct Debits",
							width=12,
							command=self.list_update
		)
		self.button_so = Checkbutton(
							self.buttons_frame,  # Standing Orders button
							variable=self.check_button_so,
							text="Standing Order",
							width=12,
							command=self.list_update
		)
		self.button_cp = Checkbutton(
							self.buttons_frame,  # Card Payments button
							variable=self.check_button_cp,
							text="Card Payment",
							width=12,
							command=self.list_update
		)
		self.button_dd.pack(side=LEFT)
		self.button_so.pack(side=LEFT, padx=10)
		self.button_cp.pack(side=LEFT)

		# the main program buttons
		self.placeholder = Label(self.program_frame, height=3)  # empty space to drop the Calcuate button down
		self.placeholder.pack(side=TOP)

		self.button_get_selection = Button(
							self.program_frame,  # Calculate button
							text="Calculate",
							command=self.get_selection
		)
		self.button_get_selection.pack(side=TOP, pady=5)

		self.button_quit = Button(
							self.program_frame,  # QUIT button
							text="QUIT",
							command=root.destroy,
							bg="#F70",
							activebackground="#F50",
							width=10,
							height=3
		)
		self.button_quit.pack(side=BOTTOM)

	# updating the view on the list ???

	def list_update(self):
		""" Updates the information diplayed inside the Listbox"""

		lst = self.lb  # get the lst object
		lst.delete(0, END)  # clearing lst before repopulating

		lst.insert(0, "Direct Debit: " + str(self.check_button_dd.get()))
		lst.insert(1, "Standing Order: " + str(self.check_button_so.get()))
		lst.insert(2, "Card Payment: " + str(self.check_button_cp.get()))
		lst.pack()
		print(self.list_view_frame.focus_get())

	def list2_update(self):
		""" Updates the information diplayed inside the Listbox"""

		data = cal.get_month()
		line = 0

		lst = self.lb2  # get the lst object
		lst.delete(0, END)  # clearing lst before repopulating

		for item in data:
			lst.insert(line, item)
			line += 1

		lst.pack()

	def get_selection(self):
		""" Collects the data selected in the Listbox"""

		# lst = self.lb2  # get the list of objects
		lst = self.list_view_frame.focus_get()
		amount_list = []

		print(lst.curselection)
		for i in lst.curselection():  # getting the currently selected items
			numbers = (str(lst.get(i)).split("£"))
			for j in range(0, len(numbers)):
				am = ""
				for digit in numbers[j]:
					if digit.isdigit():
						am += digit

				am = int(am)
				amount_list.append(am)

		total = 0
		for item in amount_list:
			total += item

		print(total)

		lst.selection_clear(0, END)


# ------ Starting the GUI
cal = PaymentsCalendar()
root = Tk()
myapp = PaymentsGUI(root)
root.mainloop()
