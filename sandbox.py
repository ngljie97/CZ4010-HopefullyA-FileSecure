from datetime import date, datetime

now = datetime.now()
print(now)

str_now = str(now)
print(str_now)

obj_now = datetime.fromisoformat(str_now)
print(obj_now.strftime("%d/%m/%Y, %H:%M:%S"))
