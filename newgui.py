# from decimal import *
from datetime import timedelta
from tkinter import *
from tkinter import ttk

import database as db


class PaymentsGUI:
	# status_window = None

	def __init__(self, parent):

		# setting up the locale
		# all the texts on buttons, etc. goes here
		self.button_labels_en = ["Calculate", "Quit", "Clear selection"]
		self.button_labels_pl = ["Przelicz", "Wyjdź", "Wyczyść zaznaczenie"]

		self.checkbox_labels_en = [
			"Show empty days",
			"Show status window",
			"Automatic\nselection clearing"
		]
		self.checkbox_labels_pl = [
			"Pokaż puste dni",
			"Pokaż okno statusu",
			"Automatyczne\nczyszczenie wyboru"
		]

		self.status_window_text_en = [
			"Total income: £",
			"Direct debit spending: £",
			"Standing order spending: £",
			"Card payment spending: £",
			"Total spending: £",
			"Income - spending: £"
		]
		self.status_window_text_pl = [
			"Całkowity dochód: £",
			"Wydatki przez direct debits: £",
			"Wydatki przez standing orders: £",
			"Płatności kartą: £",
			"Wydatki całkowite: £",
			"Przychód - wydatki: £"
		]

		self.label_text_en = ["Payments for the spending period\nfrom {} to {}".format(
			db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B"))]
		self.label_text_pl = ["Płatności za okres rozliczeniowy\nod {} do {}".format(
			db.get_start_date().strftime("%A, %d of %B"), db.get_end_date().strftime("%A, %d of %B"))]

		self.frame_labels_en = ["Language selection", "Selection Clearing", "Clearing delay"]
		self.frame_labels_pl = ["Wybór języka", "Czyszczenie wyboru", "Opóźnienie\nczyszczenia"]

		# ###############  default locale is polish
		self.current_button_labels = self.button_labels_pl
		self.current_checkbox_labels = self.checkbox_labels_pl
		self.current_label_text = self.label_text_pl
		self.current_status_window_text = self.status_window_text_pl
		self.current_frame_labels = self.frame_labels_pl

		# ###############  OTHER VARIABLES

		# selection memory is a dictionary
		# key is the listbox object
		# value is listbox selection
		self.selection_memory = {}

		# list to hold all the listbox objects
		# those object will also be the keys in the dictionary
		self.listbox_list = []

		# variable to mirror data displayed in listbox objects
		# output = [week0, week1, week2, week3, week4, week5]
		# weekX = [[date string or Payment object, line position in listbox for that week], [...], ...
		self.output = [[] for _ in range(6)]

		# ###############  determining the window size
		self.myParent = parent
		size_x = parent.winfo_screenwidth() - 400  # leaving some breathing space
		size_y = parent.winfo_screenheight() - 150
		if size_x < 1000:
			size_x = 1000
		if size_y < 600:
			size_y = 600

		window_size = str(size_x) + "x" + str(size_y) + "+50+20"

		self.myParent.geometry(window_size)  # window size
		# self.myParent.geometry("1000x600")  # window size
		self.myParent.title("House Budget")  # window title

		# setting the widgets variables
		self.check_box_dd = IntVar(value=1)  # checkbox direct debit
		self.check_box_so = IntVar(value=1)  # checkbox standing order
		self.check_box_cp = IntVar(value=1)  # checkbox card payment
		self.check_box_sed = IntVar(value=1)  # checkbox empty days
		# self.check_box_sw = IntVar(value=1)  # checkbox status window - not currently used
		self.dialog_button_loc = IntVar(value=2)  # radio button for locale
		self.check_box_selection_timeout = IntVar(value=1)  # checkbox for selection timeout
		self.selection_timeout_val = IntVar(value=6)  # selection timeout value

		# ###############  The topmost frame is called myContainer1  ###############
		self.myContainer1 = Frame(self.myParent)
		self.myContainer1.pack(expand=YES, fill=BOTH, padx=5, pady=5)
		self.myContainer1.columnconfigure(0, weight=2, minsize=20)
		self.myContainer1.columnconfigure(1, weight=2, minsize=20)
		# self.myContainer1.columnconfigure(2, weight=2, minsize=20)
		self.myContainer1.columnconfigure(3)
		self.myContainer1.rowconfigure(0)
		self.myContainer1.rowconfigure(1, weight=1)
		self.myContainer1.rowconfigure(2, weight=1)
		self.myContainer1.rowconfigure(3, weight=1)

		# ############### financial period label
		self.financial_period_label = ttk.Label(
			self.myContainer1,
			text=self.current_label_text[0],
			justify=CENTER,
			font=("Garamond", 12)
		)
		self.financial_period_label.grid(columnspan=2)

		# ############### The main title ###############
		self.title_frame = Frame(self.myContainer1)
		self.title_frame.grid(row=0, column=2, columnspan=2, pady=(5, 10))

		# ############### Home budget
		self.title_label = ttk.Label(
			self.title_frame,
			text="Budżet domowy",
			foreground="blue",
			font=("Arial", 30, "italic", "bold")
		)
		self.title_label.pack(side=LEFT)

		# ############### version
		self.version_label = ttk.Label(
			self.title_frame,
			text="v0.5",
			font=("Tahoma", 10)
		)
		self.version_label.pack(side=LEFT, anchor=S)

		# ###############  check-buttons frame at the bottom
		self.cbuttons_frame = Frame(self.myContainer1)
		self.cbuttons_frame.grid(row=4, columnspan=2, sticky=E+W)

		# ###############  preparing the list boxes grid  ###############
		lsbox_column = 0
		lsbox_row = 1

		for w in range(6):
			the_listbox = Listbox(
				self.myContainer1,
				bg="#CCC",
				fg="#444",
				selectmode=EXTENDED,
				width=45,
				height=10,
				activestyle=NONE,
				exportselection=0
			)
			self.listbox_list.append(the_listbox)

			the_listbox.bind("<ButtonRelease>", self.store_selection)
			the_listbox.grid(column=lsbox_column, row=lsbox_row, ipadx=5, ipady=5, sticky=N+E+W+S)
			lsbox_row += 1

			if w == 2:
				lsbox_row = 1
				lsbox_column += 1

		# self.list_update()  # filling the list for the first time
		self.list2_update()  # filling the list for the first time

		# ###############  the status window  ###############
		self.status_window = Frame(
				self.myContainer1,
				# bg="#CCC",
				width=250,
				borderwidth=3,
				relief=GROOVE
		)
		self.status_window.grid(column=2, row=1, rowspan=3, ipadx=5, ipady=5, sticky=N+S)
		self.status_window.grid_propagate(0)

		# ###############  the view control check buttons
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

		# ###############  Frame for the right-hand-side buttons  ###############
		self.control_frame = Frame(self.myContainer1, width=250)
		self.control_frame.grid(column=3, row=1, rowspan=5, sticky=N+S, padx=10)
		self.control_frame.grid_propagate(0)

		# ###############  Calculate button
		self.button_get_selection = ttk.Button(
							self.control_frame,
							text=self.current_button_labels[0],
							command=self.get_selection
		)
		# self.button_get_selection.grid(row=0, column=2, sticky=W+N, padx=7, pady=5)
		self.button_get_selection.pack(anchor=N+W)

		# ############### QUIT button
		s = ttk.Style()
		s.configure("my.TButton", font=("Tahoma", 11), foreground="#990000")
		self.button_quit = ttk.Button(
							self.control_frame,
							text=self.current_button_labels[1],
							command=parent.destroy,
							style="my.TButton"
		)
		# self.button_quit.grid(row=0, column=2, sticky=S, padx=20, pady=2)
		self.button_quit.pack(side=BOTTOM, pady=(10, 18), padx=30, ipady=8)

		# ###############  Language selection  ###############
		self.language_selection_frame = LabelFrame(
							self.control_frame,
							labelanchor=NW,
							text=self.current_frame_labels[0],
							relief=GROOVE,
							borderwidth=3
		)
		self.language_selection_frame.pack(side=BOTTOM, anchor=W, fill=X)

		# ###############  Language selection Radio Buttons  ###############
		self.button_locale_eng = ttk.Radiobutton(
							self.language_selection_frame,  # locale selection radio buttons
							variable=self.dialog_button_loc,
							value=1,
							text="English",
							command=self.locale_toggle
		)
		self.button_locale_pl = ttk.Radiobutton(
							self.language_selection_frame,  # locale selection radio buttons
							variable=self.dialog_button_loc,
							value=2,
							text="Polski",
							command=self.locale_toggle
		)
		self.button_locale_pl.pack(side=LEFT, padx=5, pady=5)
		self.button_locale_eng.pack(side=RIGHT, padx=5, pady=5)

		# ###############  Selection clearing timeout frame  ###############
		self.selection_timeout_frame = LabelFrame(
							self.control_frame,
							labelanchor=NW,
							text=self.current_frame_labels[1],
							relief=GROOVE,
							borderwidth=3,
		)
		self.selection_timeout_frame.pack(side=BOTTOM, anchor=W, fill=X, pady=10, ipady=5)
		self.selection_timeout_frame.columnconfigure(0, minsize=85)
		self.selection_timeout_frame.columnconfigure(1, minsize=40)
		self.selection_timeout_frame.columnconfigure(2, minsize=10)
		self.selection_timeout_frame.rowconfigure(0, minsize=40)
		self.selection_timeout_frame.rowconfigure(1, minsize=40)

		# ###############  check box for selection timeout
		self.button_selection_timeout = ttk.Checkbutton(
							self.selection_timeout_frame,
							variable=self.check_box_selection_timeout,
							text=self.current_checkbox_labels[2],
							command=self.selection_timeout_change
		)
		self.button_selection_timeout.grid(row=0, column=0, columnspan=3, sticky=W)

		# ###############  selection timeout label
		self.selection_timeout_label = Label(self.selection_timeout_frame, text=self.current_frame_labels[2])
		self.selection_timeout_label.grid(row=1, column=0, sticky=E)
		Label(self.selection_timeout_frame, text="s").grid(row=1, column=2, sticky=E)

		# ###############  entry field for selection timeout value
		self.input_selection_timeout = ttk.Entry(
							self.selection_timeout_frame,
							width=5,
							textvariable=self.selection_timeout_val
		)
		self.input_selection_timeout.grid(row=1, column=1, sticky=W)

		# ###############  clear selection button
		s.configure("selection.TButton")
		self.clear_selection_button = ttk.Button(
							self.selection_timeout_frame,
							text=self.current_button_labels[2],
							command=self.clear_selection,
							width=20,
							style="selection.TButton",
							state=DISABLED
		)
		self.clear_selection_button.grid(row=3, column=0, columnspan=3, sticky=W, padx=7)

		# ###############  summary of payments
		self.show_summary()

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
				lst_data = "{}, {} {}".format(fpd.strftime("%a"), str(fpd.day), str(fpd.strftime("%B")))

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
			self.current_status_window_text = self.status_window_text_en
			self.current_frame_labels = self.frame_labels_en

		else:
			self.current_button_labels = self.button_labels_pl
			self.current_checkbox_labels = self.checkbox_labels_pl
			self.current_label_text = self.label_text_pl
			self.current_status_window_text = self.status_window_text_pl
			self.current_frame_labels = self.frame_labels_pl

		self.button_get_selection.configure(text=self.current_button_labels[0])
		self.button_quit.configure(text=self.current_button_labels[1])
		self.button_sed.configure(text=self.current_checkbox_labels[0])
		self.button_selection_timeout.configure(text=self.current_checkbox_labels[2])
		self.financial_period_label.configure(text=self.current_label_text[0])
		self.language_selection_frame.configure(text=self.current_frame_labels[0])
		self.selection_timeout_frame.configure(text=self.current_frame_labels[1])
		self.selection_timeout_label.configure(text=self.current_frame_labels[2])
		self.clear_selection_button.configure(text=self.current_button_labels[2])

		self.show_summary()

	# def status_window_toggle(self):
	# 	if self.check_box_sw.get():
	# 		self.status_window.grid()
	# 	else:
	# 		self.status_window.grid_remove()

	def store_selection(self, event):
		# self.selection_memory = []  # clear the current state of variable if it's the same widget

		# first item in the list is the list itself
		self.selection_memory[event.widget] = event.widget.curselection()

		# ############### setting the timeout for selection, if the checkbox is ticked
		if self.check_box_selection_timeout.get() == 1:
			# event.widget.after(self.selection_timeout_val.get() * 1000, lambda: event.widget.selection_clear(0, END))
			event.widget.after(self.selection_timeout_val.get() * 1000, lambda: self.clear_selection(event.widget))

	def get_selection(self):
		""" Collects the data selected in the Listbox"""
		total = 0  # sum of all selected payments
		for lst in self.selection_memory.keys():
			# print(lst)
			# lst = l  # getting the list

			for item in self.selection_memory[lst]:
				payment = self.output[self.listbox_list.index(lst)][item][0]
				total += payment.amount

		Label(self.status_window, text=str(total)).grid(sticky=W)

	def clear_selection(self, widget=None):
		if widget:
			widget.selection_clear(0, END)
			self.selection_memory[widget] = list()
		else:
			for lst in self.listbox_list:
				lst.selection_clear(0, END)
				self.selection_memory[lst] = list()

	def selection_timeout_change(self):
		if self.check_box_selection_timeout.get() == 0:
			self.input_selection_timeout.configure(state=DISABLED)
			self.clear_selection_button.configure(state=ACTIVE)
		else:
			self.input_selection_timeout.configure(state=ACTIVE)
			self.clear_selection_button.configure(state=DISABLED)

	def show_summary(self):
		# self.status_window.insert(0, "Całkowity przychód: £" + str(db.calculate_total("income")))
		# self.status_window.insert(0, "Wydatki przez direct debits: £" + str(db.calculate_total("directDebit")))
		# self.status_window.insert(0, "Wydatki przez standing orders: £" + str(db.calculate_total("standingOrder")))
		# self.status_window.insert(0, "Płatności kartą: £" + str(db.calculate_total("cardPayment")))
		#
		# full_outcome = db.calculate_total("directDebit") + db.calculate_total("standingOrder")\
		# 	+ db.calculate_total("cardPayment")
		#
		# self.status_window.insert(0, "Wydatki całkowite: £" + str(full_outcome))
		# self.status_window.insert(0, "Przychód - wydatki: £" + str(db.calculate_total("income") - full_outcome))
		# self.status_window.configure(state=DISABLED)

		# clearing the status window
		for w in self.status_window.winfo_children():
			w.destroy()

		Label(self.status_window, text=self.current_status_window_text[0] + str(db.calculate_total("income")))\
			.grid(sticky=W)
		Label(self.status_window, text=self.current_status_window_text[1] + str(db.calculate_total("directDebit")))\
			.grid(sticky=W)
		Label(self.status_window, text=self.current_status_window_text[2] + str(db.calculate_total("standingOrder")))\
			.grid(sticky=W)
		Label(self.status_window, text=self.current_status_window_text[3] + str(db.calculate_total("cardPayment")))\
			.grid(sticky=W)

		full_outcome = db.calculate_total("directDebit") + db.calculate_total("standingOrder")\
			+ db.calculate_total("cardPayment")

		Label(self.status_window, text=self.current_status_window_text[4] + str(full_outcome)).grid(sticky=W)
		Label(self.status_window, text=self.current_status_window_text[5] + str(db.calculate_total("income") - full_outcome))\
			.grid(sticky=W)
