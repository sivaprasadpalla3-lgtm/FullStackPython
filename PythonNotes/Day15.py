units=int(input("Enter units= "))
senior=input("Enter senior or not= ").lower()=="senior"
if 0 < units <=100:
    bill = units*1.5
elif 100 < units <=200:
    bill = units*2.5
elif 200 < units <=500:
    bill = units*4
elif 500 < units <=800:
    bill = units*6
else :
    bill = units*6*1.05
if senior:
    bill *=0.9
print(bill)