# from datetime import datetime
import database as db
import newgui as gui

# import payments as p
# from decimal import *  # decimal numbers
# getcontext().prec = 10  # setting the decimals to two numbers, as in payments

# paymentDay = 24  # do skasowania
# PAYDAY = 24
#
# today = datetime.now()
# payment = today.replace(day=paymentDay)

db.read_data()
# # print("gui tutaj", gui.PaymentsGUI.get_sw())
# # gui.Label(gui.get_status_window(), text="Całkowity przychód: £" + str(db.calculate_total("income")))
# print("Wydatki przez direct debits: £" + str(db.calculate_total("directDebit")))
# print("Wydatki przez standing orders: £" + str(db.calculate_total("standingOrder")))
# print("Płatności kartą: £" + str(db.calculate_total("cardPayment")))
#
# full_outcome = db.calculate_total("directDebit") + db.calculate_total("standingOrder") \
#                + db.calculate_total("cardPayment")
#
# print("Wydatki całkowite: £" + str(full_outcome))
# print("Przychód - wydatki: £" + str(db.calculate_total("income") - full_outcome))

# ------ Starting the GUI adn the main loop
root = gui.Tk()
myapp = gui.PaymentsGUI(root)
root.mainloop()
