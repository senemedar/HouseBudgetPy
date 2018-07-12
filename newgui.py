from tkinter import *
from tkinter import ttk
from decimal import *
import database as db


class PaymentsGUI:
	def __init__(self, parent):

		self.myParent = parent
		self.myParent.geometry("800x600+50+20")  # window size
		self.myParent.title("Budżet domowy")  # window title

		# setting the variables to control from view buttons
		self.check_button_dd = IntVar(value=1)
		self.check_button_so = IntVar(value=1)
		self.check_button_cp = IntVar(value=1)

		# setting the list to store the latest selected items
		self.selection_memory = []

		# The topmost frame is called myContainer1
		self.myContainer1 = Frame(self.myParent)
		self.myContainer1.pack(expand=YES, fill=BOTH, padx=5, pady=5)
		self.myContainer1.columnconfigure(0, weight=1, minsize=20)
		self.myContainer1.columnconfigure(1, weight=1, minsize=20)
		# self.myContainer1.columnconfigure(2, minsize=20)
		self.myContainer1.rowconfigure(0)
		self.myContainer1.rowconfigure(1, weight=1)
		self.myContainer1.rowconfigure(2, weight=1)
		self.myContainer1.rowconfigure(3, weight=1)

		message = "Payments for the spending period\nfrom {} to {}".format(
			db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B")
		)
		ttk.Label(self.myContainer1, text=message, justify=CENTER, font=("Verdana", 10)).grid(columnspan=2)

		# Frame for the right-hand-side buttons
		self.control_frame = Frame(self.myContainer1)
		self.control_frame.grid(column=2, rowspan=5, sticky=N+S, padx=10)
		# self.control_frame.rowconfigure(0, minsize=400)

		# check-buttons frame
		self.cbuttons_frame = Frame(self.myContainer1)
		self.cbuttons_frame.grid(row=4, columnspan=2, sticky=W)

		# list element to display all the payments
		self.listbox_list = []  # list to hold all the list boxes
		lsbox_column = 0
		lsbox_row = 1

		# propagating teh list boxes grid
		for w in range(6):
			self.listbox_list.append(Listbox(
				self.myContainer1,
				bg="#CCC",
				selectmode=EXTENDED,
				width=45,
				height=10)
			)
			self.listbox_list[w].bind("<ButtonRelease>", self.store_selection)
			self.listbox_list[w].grid(column=lsbox_column, row=lsbox_row, sticky=N+E+W+S)
			lsbox_row += 1

			if w == 2:
				lsbox_row = 1
				lsbox_column += 1

		self.list_update()  # filling the list for the first time
		self.list2_update()

		# the view control checkbutton
		self.button_dd = ttk.Checkbutton(
							self.cbuttons_frame,  # Direct Debits checkbox
							variable=self.check_button_dd,
							text="Direct Debits",
							width=16,
							command=self.list_update
		)
		self.button_so = ttk.Checkbutton(
							self.cbuttons_frame,  # Standing Orders checkbox
							variable=self.check_button_so,
							text="Standing Order",
							width=16,
							command=self.list_update
		)
		self.button_cp = ttk.Checkbutton(
							self.cbuttons_frame,  # Card Payments checkbox
							variable=self.check_button_cp,
							text="Card Payment",
							width=16,
							command=self.list_update
		)
		self.button_dd.grid(row=0, column=0, sticky=E+N)
		self.button_so.grid(row=0, column=1, sticky=W+N)
		self.button_cp.grid(row=0, column=2, sticky=W+N)

		# Calculate button
		self.button_get_selection = ttk.Button(
							self.control_frame,
							text="Calculate",
							command=self.get_selection
		)
		# self.button_get_selection.grid(row=0, column=2, sticky=W+N, padx=7, pady=5)
		self.button_get_selection.pack(anchor=N+W)

		# QUIT button
		s = ttk.Style()
		s.configure("my.TButton", font=("Tahoma", 11), foreground="#990000")
		self.button_quit = ttk.Button(
							self.control_frame,
							text="QUIT",
							command=parent.destroy,
							# bg="#FFF7EA",
							# activebackground="#F70",
							# width=10,
							# height=3
							style="my.TButton"
		)
		# self.button_quit.grid(row=0, column=2, sticky=S, padx=20, pady=2)
		self.button_quit.pack(side=BOTTOM, pady=(5, 20), padx=20)

	# updating the view on the list ???
	def list_update(self):
		""" Updates the information diplayed inside the Listbox"""

		lst = self.listbox_list[5]  # get the lst object
		lst.delete(0, END)  # clearing lst before repopulating

		lst.insert(0, "Direct Debit: " + str(self.check_button_dd.get()))
		lst.insert(1, "Standing Order: " + str(self.check_button_so.get()))
		lst.insert(2, "Card Payment: " + str(self.check_button_cp.get()))
		lst.insert(3, db.payments["directDebit"][0])
		lst.grid()
		print(lst.get(3))

	def list2_update(self):
		""" Updates the information displayed inside the Listbox"""

		data = db.get_month(  # get the necessary data
			self.check_button_dd.get(),
			self.check_button_so.get(),
			self.check_button_cp.get()
		)

		# variables used for iterating through data
		line = 0
		current_week = 0

		# clearing the listboxes
		lst = self.listbox_list[current_week]  # selecting the listbox from the list
		lst.delete(0, END)  # clearing the list box

		for item in data:
			if item[5].isdigit():
				data_week = int(item[5]) - 1
			else:
				continue

			if data_week != current_week and data_week != "-":
				current_week += 1
				lst = self.listbox_list[current_week]
				lst.delete(0, END)

			lst.insert(END, item[8:])  # populating the listbox
			line += 1

	def store_selection(self, event):
		self.selection_memory = []  # clear the current state of variable

		# first item in the list is the list itself
		self.selection_memory.append(event.widget)

		# rest of the list will be the actual selection, but we need to
		# iterate through selection, otherwise I'll get the whole list added, and I don't need that
		for item in event.widget.curselection():
			self.selection_memory.append(item)

	def get_selection(self):
		""" Collects the data selected in the Listbox"""

		# lst = self.listbox_list[1]  # get the list of objects
		# lst = self.myContainer1.focus_get()
		amount_list = []

		# iterating through the listbox objects
		# i = 0  # iterator for listbox list
		# lst = self.listbox_list[0]  # default value
		# for item in self.listbox_list:
		# 	if item.curselection():
		# 		lst = item
		# 	else:
		# 		i += 1
		lst = self.selection_memory[0]  # getting the list
		for i in self.selection_memory[1:]:  # getting the selected items
			numbers = (str(lst.get(i)).split("£"))
			print(numbers)
			for j in range(1, len(numbers)):
				am = ""
				for digit in numbers[j]:
					if digit.isdigit():
						am += digit

				am = Decimal(am[:-2] + "." + am[-2:])
				amount_list.append(am)

		total = 0
		for item in amount_list:
			total += item

		print(total)

		# lst.selection_clear(0, END)
