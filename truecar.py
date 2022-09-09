import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from mysql.connector import Error

# ------------------------------------
try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="ABEDsh1316!@#$%",
        port=3306,
        database="abed")
    if connection.is_connected():
        print("database connected", "\n")
except Error as e:
    print("Error while connecting to MySQL", e)
# ------------------------------------------------------
input_car = input(str("enter your favorite car: \n"))

url = 'https://www.truecar.com/used-cars-for-sale/listings/{car}'
url = url.format(car=input_car)
print("\n")
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
data = []
count = 0

output_results = soup.findAll('div', attrs={'data-test': "cardContent",
                                            'class': "card-content vehicle-card-body order-3 vehicle-card-carousel-body"},
                              limit=20)
for item in output_results:
    count += 1
    # print(z, item.text)
    names = item.findAll("span", attrs={'class': "truncate"})
    prices = item.findAll("div", attrs={'class': "heading-3 my-1 font-bold", 'data-qa': "Heading",
                                        'data-test': "vehicleCardPricingBlockPrice"})
    kilometers_traveled = item.findAll('div', attrs={'class': "truncate text-xs", 'data-test': "vehicleMileage"})

    data.append({
        'id': count,
        'model': names[0].text,
        'price': prices[0].text,
        'miles': kilometers_traveled[0].text
    })

cursor = connection.cursor()

query_1 = """CREATE TABLE IF NOT EXISTS cars
(Id varchar(45) ,
 model varchar(45),
 price varchar(45),
 miles varchar(45))"""
cursor.execute(query_1)

for item in data:
    km = re.sub(r'(\d) miles', '\g<1>', item['miles'])
    query_2 = "INSERT INTO cars VALUES (\'%s\' ,\'%s\' ,\'%s\' ,\'%s\')" % (
        item['id'], item['model'], item['price'], km,)
    cursor.execute(query_2)
    connection.commit()

print("data stored in database", "\n")

query_3 = 'select * from cars'
cursor.execute(query_3)
print("Id", "|", "model", "|", "price", "|", "miles")
for (Id, model, price, miles) in cursor:
    print("%s | %s | %s | %s" % (Id, model, price, miles))

print("\n")

connection.close()
# print dictionary of data
# for item in data:
#     print(item)
