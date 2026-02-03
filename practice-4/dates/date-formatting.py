import datetime

x = datetime.datetime.now()
print(x.strftime("%A"))

x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))

"""
                        My output
 ----------------------------------------------------------
| Tuesday                    | for print(x.strftime("%A")) |
| June                       | for print(x.strftime("%B")) |
 ----------------------------------------------------------

"""