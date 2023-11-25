import pandas as pd
from io import StringIO
import textdistance
import random

# Sample CSV data
csv_data = """foodname,country,รสชาติ,type,ราคา
ผัดไทย,ไทย,เค็ม,ของคาว,ถูก
ขาหมู,ไทย,เค็ม,ของคาว,ถูก
ไข่เจียว,ไทย,ธรรมดา,ของคาว,ถูก
หมูกรอบ,ไทย,เค็ม,ของคาว,ถูก
ข้าวผัด,ไทย,ปกติ,ของคาว,ถูก
บะหมี่หมูแดง,ไทย,เค็ม,ของคาว,ถูก
ส้มตำ,ไทย,เผ็ด/เปรี้ยว,ของคาว,ถูก
ข้าวซอย,ไทย,เผ็ด,ของคาว,ถูก
มาม่า,ไทย,เค็ม,ของคาว,ถูก
กล้วยบวชชี,ไทย,หวาน,ของหวาน,ถูก
ขนมกล้วย,ไทย,หวาน,ของหวาน,ถูก
ขนมใส่ไส้,ไทย,หวาน,ของหวาน,ถูก
ข้าวต้มมัด,ไทย,หวาน,ของหวาน,ถูก
ทองหยอด,ไทย,หวาน,ของหวาน,ถูก
ลูกชุบ,ไทย,หวาน,ของหวาน,ถูก
ทองหยอด,ไทย,หวาน,ของหวาน,ถูก
ขนมเบื้อง,ไทย,หวาน,ของหวาน,ถูก
บัวลอย,ไทย,หวาน,ของหวาน,ถูก
สลิ่ม,ไทย,หวาน,ของหวาน,ถูก
pizza,italy,various,one-dish,happy
Sushi,japan,various,snack,happy
"""

# Function to correct user input using Jaccard similarity
def correct_word(input_word, dictionary):
    similarities = [(word, textdistance.jaccard(input_word, word)) for word in dictionary]
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_similarities[0][0]

# Creating pandas dataframe from CSV data
df = pd.read_csv(StringIO(csv_data), encoding='utf-8')

# Getting user input
user_country = input("Enter country: ")
user_taste = input("Enter taste: ")
user_type = input("Enter type: ")
user_price = input("Enter price: ")

# Correcting user input
corrected_country = correct_word(user_country, ['ไทย', 'italy', 'japan'])
corrected_taste = correct_word(user_taste, ['เค็ม', 'ธรรมดา', 'ปกติ', 'เผ็ด/เปรี้ยว', 'เผ็ด', 'หวาน'])
corrected_type = correct_word(user_type, ['ของคาว', 'ของหวาน', 'เครื่องดื่ม', 'ของกินเล่น', 'อาหารทะเล', 'พาสต้า', 'ซุป'])
corrected_price = correct_word(user_price, ['ถูก', 'แพง'])

# Finding the intersection based on corrected user input
count = 0 

intersection = df[
    (df['country'] == corrected_country) &
    (df['รสชาติ'] == corrected_taste) &
    (df['type'] == corrected_type) &
    (df['ราคา'] == corrected_price)
]

# Displaying 5 food names from the intersecting DataFrame
if not intersection.empty:
    print("Food names that intersect with the given criteria:")
    food_names = intersection['foodname'].tolist()
    
    # Ensure there are at least 5 food names
    if len(food_names) >= 5:
        random_food_names = random.sample(food_names, 5)
        for food_name in random_food_names:
            print(food_name)
    else:
        print("There are fewer than 5 food names in the intersection.")
else:
    print("No matches found based on the given criteria.")
