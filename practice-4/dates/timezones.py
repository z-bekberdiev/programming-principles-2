import datetime

x = datetime.datetime.now(datetime.timezone.utc)
print(x.strftime("%z"))
print(x.strftime("%Z"))

"""
                        My output
 ----------------------------------------------------------
| +0000                      | for print(x.strftime("%z")) |
| UTC                        | for print(x.strftime("%Z")) |
 ----------------------------------------------------------

"""