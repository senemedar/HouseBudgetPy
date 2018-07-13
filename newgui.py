from tkinter import *
from tkinter import ttk
from decimal import *
from datetime import date, timedelta, datetime
import database as db


class PaymentsGUI:
	def __init__(self, parent):

		# setting up the locale
		self.button_labels_en = ["Calculate", "Quit"]
		self.button_labels_pl = ["Przelicz", "Wyjdź"]
		self.checkbox_labels_en = ["Show Empty Days"]
		self.checkbox_labels_pl = ["Pokaż puste dni"]
		self.label_text_en = ["Payments for the spending period\nfrom {} to {}".format(
			db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B"))]
		self.label_text_pl = ["Płatności za okres rozliczeniowy\nod {} do {}".format(
			db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B"))]

		# default locale is english (but not for long)
		self.current_button_labels = self.button_labels_en
		self.current_checkbox_labels = self.checkbox_labels_en
		self.current_label_text = self.label_text_en

		self.myParent = parent

		# determining the window size
		size_x = parent.winfo_screenwidth() - 400  # leaving some breathing space
		size_y = parent.winfo_screenheight() - 150
		if size_x < 800:
			size_x = 800
		if size_y < 600:
			size_y = 600

		window_size = str(size_x) + "x" + str(size_y) + "+50+20"

		self.myParent.geometry(window_size)  # window size
		self.myParent.title("House Budget")  # window title

		# setting the variables to control from view buttons
		self.check_box_dd = IntVar(value=1)
		self.check_box_so = IntVar(value=1)
		self.check_box_cp = IntVar(value=1)
		self.check_box_sed = IntVar(value=1)
		self.dialog_button_loc = IntVar(value=1)

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

		# message = "Payments for the spending period\nfrom {} to {}".format(
		# 	db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B")
		# )
		self.financial_period_label = ttk.Label(
			self.myContainer1,
			text=self.current_label_text[0],
			justify=CENTER,
			font=("Verdana", 10)
		)
		self.financial_period_label.grid(columnspan=2)

		# Frame for the right-hand-side buttons
		self.control_frame = Frame(self.myContainer1)
		self.control_frame.grid(column=2, rowspan=5, sticky=N+S, padx=10)
		# self.control_frame.rowconfigure(0, minsize=400)

		# check-buttons frame
		self.cbuttons_frame = Frame(self.myContainer1)
		self.cbuttons_frame.grid(row=4, columnspan=2, sticky=W)

		# list to hold all the listbox objects
		# those object will also be the keys in the dictionary
		self.listbox_list = []

		# variable to mirror data displayed in listbox objects
		# output = [week0, week1, week2, week3, week4, week5]
		# weekX = [[date string or Payment object, line position in listbox for that week], [...], ...
		self.output = [[] for _ in range(6)]

		# setting the list to store the latest selected items from the listbox objects
		self.selection_memory = []

		lsbox_column = 0
		lsbox_row = 1

		# propagating the list boxes grid
		for w in range(6):
			the_listbox = Listbox(
				self.myContainer1,
				bg="#CCC",
				selectmode=EXTENDED,
				width=45,
				height=10,
				activestyle=NONE
			)
			self.listbox_list.append(the_listbox)

			the_listbox.bind("<ButtonRelease>", self.store_selection)
			the_listbox.grid(column=lsbox_column, row=lsbox_row, sticky=N+E+W+S)
			lsbox_row += 1

			if w == 2:
				lsbox_row = 1
				lsbox_column += 1

		self.list_update()  # filling the list for the first time
		self.list2_update()

		# the view control checkbutton
		self.button_dd = ttk.Checkbutton(
							self.cbuttons_frame,  # show Direct Debits checkbox
							variable=self.check_box_dd,
							text="Direct Debit",
							width=16,
							command=self.list2_update
		)
		self.button_so = ttk.Checkbutton(
							self.cbuttons_frame,  # show Standing Orders checkbox
							variable=self.check_box_so,
							text="Standing Order",
							width=16,
							command=self.list2_update
		)
		self.button_cp = ttk.Checkbutton(
							self.cbuttons_frame,  # show Card Payments checkbox
							variable=self.check_box_cp,
							text="Card Payment",
							width=16,
							command=self.list2_update
		)
		self.button_sed = ttk.Checkbutton(
							self.cbuttons_frame,  # show empty days checkbox
							variable=self.check_box_sed,
							text=self.current_checkbox_labels[0],
							width=16,
							command=self.list2_update
		)
		self.button_dd.grid(row=0, column=0, sticky=E+N)
		self.button_so.grid(row=0, column=1, sticky=W+N)
		self.button_cp.grid(row=0, column=2, sticky=W+N)
		self.button_sed.grid(row=1, column=0, sticky=W+N)

		# Calculate button
		self.button_get_selection = ttk.Button(
							self.control_frame,
							text=self.current_button_labels[0],
							command=self.get_selection
		)
		# self.button_get_selection.grid(row=0, column=2, sticky=W+N, padx=7, pady=5)
		self.button_get_selection.pack(anchor=N+W)

		# QUIT button
		s = ttk.Style()
		s.configure("my.TButton", font=("Tahoma", 11), foreground="#990000")
		self.button_quit = ttk.Button(
							self.control_frame,
							text=self.current_button_labels[1],
							command=parent.destroy,
							style="my.TButton"
		)
		# self.button_quit.grid(row=0, column=2, sticky=S, padx=20, pady=2)
		self.button_quit.pack(side=BOTTOM, pady=(10, 18), padx=20)

		# Language selection Radio Buttons
		self.button_locale_eng = ttk.Radiobutton(
							self.control_frame,  # locale selection radio buttons
							variable=self.dialog_button_loc,
							value=1,
							text="English",
							command=self.locale_toggle
		)
		self.button_locale_pl = ttk.Radiobutton(
							self.control_frame,  # locale selection radio buttons
							variable=self.dialog_button_loc,
							value=2,
							text="Polski",
							command=self.locale_toggle
		)
		self.button_locale_eng.pack(side=BOTTOM, anchor=W)
		self.button_locale_pl.pack(side=BOTTOM, anchor=W)

	# updating the view on the list ???
	def list_update(self):
		""" Updates the information displayed inside the Listbox"""

		lst = self.listbox_list[5]  # get the lst object
		lst.delete(0, END)  # clearing lst before repopulating

		lst.insert(0, "Direct Debit: " + str(self.check_box_dd.get()))
		lst.insert(1, "Standing Order: " + str(self.check_box_so.get()))
		lst.insert(2, "Card Payment: " + str(self.check_box_cp.get()))
		lst.insert(3, db.payments["directDebit"][0])
		# lst.grid()

	def list2_update(self):
		""" Updates the information displayed inside the Listbox"""

		# variables to populate
		week = 0
		# lst_line = 0
		period = timedelta(days=1)
		fpd = db.start_date  # financial period day
		self.output = [[] for _ in range(6)]

		# populating the payments
		while fpd <= db.end_date:  # outer loop to go through each week
			week += 1
			lst = self.listbox_list[week - 1]
			lst.delete(0, END)
			lst_line = 0
			while True:  # inner loop to go through each day
				# putting the string together
				lst_data = "Week {} - {}, {} {}".format(
					str(week), fpd.strftime("%a"), str(fpd.day), str(fpd.strftime("%B")))

				# self.output[week - 1].append([lst_data, 0])  # filling the output data
				# lst.insert(lst_line, lst_data)  # displaying output data in the listbox
				#
				# lst_line += 1

				key_date = fpd.strftime("%b-%d")  # setting the key value to check against dictionary
				if key_date in db.calendar_dict:  # are there any payments that day?
					self.output[week - 1].append([lst_data, 0])  # filling the output data
					lst.insert(lst_line, lst_data)  # displaying output data in the listbox
					lst_line += 1

					for item in db.calendar_dict[key_date]:
						if item in db.payments["directDebit"] and self.check_box_dd.get():
							fg = "#660000"
						elif item in db.payments["cardPayment"] and self.check_box_cp.get():
							fg = "#666600"
						elif item in db.payments["income"]:
							fg = "#006600"
						else:
							continue

						self.output[week - 1].append([item, lst_line])
						lst.insert(lst_line, "  - " + str(item))
						lst.itemconfigure(lst_line, foreground=fg)

						lst_line += 1

				else:
					if self.check_box_sed.get():
						self.output[week - 1].append([lst_data, 0])  # filling the output data
						lst.insert(lst_line, lst_data)  # displaying output data in the listbox

						lst_line += 1

				if fpd.strftime("%a") == "Sun" or fpd == db.end_date:  # condition to end the inner loop
					break
				else:
					fpd += period
			# end of inner loop

			fpd += period
			# end of outer loop

	def locale_toggle(self):
		# self.listbox_list[5].insert(20, self.dialog_button_loc.get())
		if self.dialog_button_loc.get() == 1:
			self.current_button_labels = self.button_labels_en
			self.current_checkbox_labels = self.checkbox_labels_en
			self.current_label_text = self.label_text_en
		else:
			self.current_button_labels = self.button_labels_pl
			self.current_checkbox_labels = self.checkbox_labels_pl
			self.current_label_text = self.label_text_pl

		self.button_get_selection.configure(text=self.current_button_labels[0])
		self.button_quit.configure(text=self.current_button_labels[1])
		self.button_sed.configure(text=self.current_checkbox_labels[0])
		self.financial_period_label.configure(text=self.current_label_text[0])

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

		lst = self.selection_memory[0]  # getting the list
		total = 0  # sum of all selected payments

		for item in self.selection_memory[1:]:
			payment = self.output[self.listbox_list.index(lst)][item][0]
			total += payment.amount
			# print(payment.description)

		print(total)
		# lst.selection_clear(0, END)
