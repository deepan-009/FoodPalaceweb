"""
Loads the real Food Palace menu card, awards and a few sample reviews.

    python manage.py seed_data          # add anything missing
    python manage.py seed_data --fresh  # wipe menu/awards/reviews first

Prices transcribed from the menu photographs (Mar 2025 / Aug 2026 boards).
"Season" means market price on the day. Edit anything in /admin/.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Award, Kitchen, MenuCategory, MenuItem, Review

V, N = True, False

# (kitchen, category, blurb, [(name, price, is_veg, is_signature), ...])
MENU = [
    (Kitchen.FOOD_PALACE, "Veg Soup", "Poured hot, straight off the range", [
        ("Tomato Soup", "100", V, N),
        ("Cream of Mushroom Soup", "100", V, N),
        ("Hot and Sour Veg Soup", "110", V, N),
        ("Mushroom Soup", "110", V, N),
        ("Sweet Corn Veg Soup", "110", V, N),
        ("Veg Manchow Soup", "110", V, N),
        ("Veg Clear Soup", "110", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Non-Veg Soup", "", [
        ("Chicken Clear Soup", "130", N, N),
        ("Mutton Clear Soup", "150", N, N),
        ("Chicken Manchow Soup", "130", N, N),
        ("Hot & Sour Chicken Soup", "130", N, N),
        ("Sweet Corn Chicken Soup", "130", N, N),
        ("Cream of Chicken Soup", "120", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Salad & Raitha", "", [
        ("Russian Salad", "130", V, N),
        ("Green Salad", "100", V, N),
        ("Mix Veg Raitha", "100", V, N),
        ("Pineapple Raitha", "100", V, N),
        ("Masala Papad", "60", V, N),
        ("French Fry", "110", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Veg Starters", "", [
        ("Gobi Manchurian / Chilly", "130", V, N),
        ("Baby Corn Manchurian / Chilly", "150", V, N),
        ("Mushroom Manchurian / Chilly", "150", V, N),
        ("Paneer Manchurian / Chilly", "160", V, N),
        ("Paneer Schezwan / 65", "160", V, N),
        ("Crispy Chilly Potato", "160", V, N),
        ("Veg Manchurian Dry", "160", V, N),
        ("Aloo Zeera Dry", "130", V, N),
        ("Crispy Veg", "140", V, N),
        ("Paneer Tikka", "190", V, True),
    ]),
    (Kitchen.FOOD_PALACE, "Non-Veg Starters", "Off the charcoal tandoor", [
        ("Tandoori Chicken Full", "440", N, N),
        ("Tandoori Chicken Half", "230", N, N),
        ("Tandoori Quarter", "130", N, N),
        ("Hariyali Tandoori Full", "460", N, True),
        ("Hariyali Tandoori Half", "240", N, N),
        ("Afghani / Malai Tandoori Full", "480", N, N),
        ("Afghani / Malai Tandoori Half", "250", N, N),
        ("Chicken Tikka", "180/360", N, N),
        ("Malai Kabab", "410", N, N),
        ("Hariyali Kabab", "410", N, N),
        ("Kalmi Kabab", "160/300", N, True),
        ("Chicken Kabab", "120/220", N, N),
        ("Chicken Lollipop", "150/290", N, N),
        ("Chicken Pepper Dry / Masala", "190", N, N),
        ("Chicken Sukka", "200", N, N),
        ("Chicken 65", "200", N, N),
        ("Chicken Chilly Gravy / Dry", "200", N, N),
        ("Lemon Chicken Dry", "210", N, N),
        ("Dragon Chicken Dry", "210", N, N),
        ("Garlic Chicken Gravy / Dry", "210", N, N),
        ("Schezwan Chicken Dry", "210", N, N),
        ("Chicken Manchurian Dry", "200", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Food Palace Special", "Malabar plates you will not find down the road", [
        ("Drums of Heaven", "250", N, True),
        ("Chicken Malabar", "220", N, True),
        ("Chicken Kuttanad", "220", N, N),
        ("Chicken Kondattam", "220", N, N),
        ("Chicken Kanthari", "220", N, N),
        ("Chicken Angar", "220", N, N),
        ("Chicken Mulakittath", "220", N, N),
        ("Chicken Chopes", "220", N, N),
        ("Garden Chicken Dry", "230", N, N),
        ("Chicken Banaras", "240", N, N),
        ("Chicken Kashmiri", "240", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Indian Bread", "Kerala parotta layered to order", [
        ("Kerala Parotta", "20", V, True),
        ("Wheat Parotta", "25", V, N),
        ("Rumali Roti", "25", V, N),
        ("Tandoor Roti", "20", V, N),
        ("Butter Roti", "25", V, N),
        ("Kuboos", "10", V, N),
        ("Chapathi", "20", V, N),
        ("Tandoor Naan", "30", V, N),
        ("Butter Naan", "35", V, N),
        ("Kulcha", "30", V, N),
        ("Butter Kulcha", "35", V, N),
        ("Garlic Naan", "40", V, N),
        ("Pudina Naan", "35", V, N),
        ("Butter Cheese Garlic Naan", "70", V, N),
        ("Cheese Naan", "50", V, N),
        ("Pudina Kulcha", "35", V, N),
        ("Stuffed Kulcha", "70", V, N),
        ("Aloo Parotta", "45", V, N),
        ("Egg Parotta", "65", N, N),
        ("Lacha Parotta", "35", V, N),
        ("Pudina Parotta", "45", V, N),
        ("Gobi Parotta", "55", V, N),
        ("Paneer Parotta", "60", V, N),
        ("Kothu Parotta Veg / Non Veg", "140/170", N, True),
    ]),
    (Kitchen.FOOD_PALACE, "Veg Gravy & Dry", "", [
        ("Daal Makhani", "130", V, N),
        ("Dal Fry", "80", V, N),
        ("Dal Palak", "100", V, N),
        ("Dal Tadka", "90", V, N),
        ("Paneer Makhani", "160", V, N),
        ("Paneer 65 (Dry)", "160", V, N),
        ("Tomato Fry", "100", V, N),
        ("Green Peas Masala", "110", V, N),
        ("Channa Masala", "100", V, N),
        ("Mix Veg Curry", "140", V, N),
        ("Aloo Gobi", "140", V, N),
        ("Gobi Masala", "130", V, N),
        ("Aloo Channa", "130", V, N),
        ("Paneer Butter Masala", "160", V, True),
        ("Paneer Tikka Masala", "180", V, N),
        ("Palak Paneer", "160", V, N),
        ("Mushroom Masala", "140", V, N),
        ("Veg Kadai", "140", V, N),
        ("Aloo Tomato", "130", V, N),
        ("Malai Kofta", "160", V, N),
        ("Shahi Paneer", "170", V, N),
        ("Paneer Kadai", "160", V, N),
        ("Veg Makhanwala", "170", V, N),
        ("Paneer Kolhapuri", "160", V, N),
        ("Aloo Mutter", "120", V, N),
        ("Veg Hyderabadi", "140", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Non-Veg Gravy", "", [
        ("Butter Chicken (Bone)", "180", N, N),
        ("Butter Chicken (Boneless)", "200", N, True),
        ("Chicken Curry Masala", "180", N, N),
        ("Kadai Chicken", "200", N, N),
        ("Chicken Rogan Josh", "210", N, N),
        ("Chicken Punjabi", "200", N, N),
        ("Chicken Mughlai", "210", N, N),
        ("Methi Chicken", "200", N, N),
        ("Chicken Do Pyaza", "210", N, N),
        ("Chicken Tikka Masala", "220", N, N),
        ("Chicken Chettinad", "200", N, N),
        ("Chicken Hyderabadi", "200", N, N),
        ("Chicken Kolhapuri", "200", N, N),
        ("Chicken Lahori (B/L)", "210", N, N),
        ("Chicken Jaipuri", "210", N, N),
        ("Chicken Patiyala", "210", N, N),
        ("Chicken Kunthapuri", "220", N, N),
        ("Tandoori Chicken Masala", "230", N, N),
        ("Kalmi Masala", "230", N, N),
        ("Chicken Sholay Dry (B/L)", "220", N, N),
        ("Hot Garlic Chicken", "210", N, N),
        ("Handi Chicken", "220", N, N),
        ("Food Palace Special Gravy", "230", N, True),
    ]),
    (Kitchen.FOOD_PALACE, "Mutton", "Slow-cooked, bone-in", [
        ("Special Nawabi Mutton Masala", "250", N, True),
        ("Special Mutton Pepper Dry / Masala", "250", N, N),
        ("Special Mutton Chilly Dry / Gravy", "250", N, N),
        ("Special Mutton Kolhapur", "250", N, N),
        ("Special Mutton Rogan Josh", "260", N, N),
        ("Special Mutton Schezwan", "250", N, N),
        ("Mutton Kanthari Dry", "250", N, N),
        ("Mutton Fry", "250", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Egg", "Served from 6 am with the breakfast counter", [
        ("Egg Masala", "90", N, N),
        ("Egg Masala Fry", "100", N, N),
        ("Egg Bhurji", "60", N, N),
        ("Egg Omelette", "40", N, N),
        ("Egg Chilly Dry / Gravy", "130", N, N),
        ("Egg Kadai", "130", N, N),
        ("Egg Boiled", "30", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Special Fish", "Priced by the day's catch", [
        ("Anjal", "Season", N, True),
        ("Bangada Tawa & Masala Fry", "Season", N, N),
        ("Fish Angar Dry / Gravy", "230", N, N),
        ("Fish Mulakittath", "230", N, True),
        ("Fish Kabab", "190", N, N),
        ("Fish Manchurian Dry", "220", N, N),
        ("Fish Chilly Dry / Masala", "220", N, N),
        ("Fish Pepper Dry", "220", N, N),
    ]),
    (Kitchen.FOOD_PALACE, "Biryani & Rice", "Thalassery dum biryani, sealed and slow-finished", [
        ("Special Chicken Thalassery Dum Biryani", "180", N, True),
        ("Special Mutton Thalassery Dum Biryani", "240", N, True),
        ("Chicken Hyderabadi Biryani", "190", N, N),
        ("Mutton Hyderabadi Biryani", "260", N, N),
        ("Fish Biryani", "Season", N, N),
        ("Paneer Biryani", "160", V, N),
        ("Mushroom Biryani", "150", V, N),
        ("Egg Biryani", "130", N, N),
        ("Veg Biryani", "120", V, N),
        ("Biryani Rice", "90", V, N),
        ("Ghee Rice", "80", V, N),
        ("Jeera Rice", "90", V, N),
        ("Curd Rice", "90", V, N),
        ("Masala Rice", "110", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Fried Rice & Noodles", "", [
        ("Chicken Fried Rice", "170", N, N),
        ("Egg Fried Rice", "130", N, N),
        ("Schezwan Chicken Fried Rice", "180", N, N),
        ("Veg Fried Rice", "110", V, N),
        ("Schezwan Veg Fried Rice", "120", V, N),
        ("Paneer Fried Rice", "150", V, N),
        ("Schezwan Paneer Fried Rice", "160", V, N),
        ("Mushroom Fried Rice", "130", V, N),
        ("Mix Fried Rice (Cocktail)", "220", N, N),
        ("Triple Fried Rice", "220", N, N),
        ("Prawns Fried Rice", "220", N, N),
        ("Chicken Noodles", "180", N, N),
        ("Schezwan Chicken Noodles", "180", N, N),
        ("Egg Noodles", "140", N, N),
        ("Paneer Noodles", "160", V, N),
        ("Veg Noodles", "120", V, N),
        ("Schezwan Veg Noodles", "140", V, N),
        ("Mix Noodles", "230", N, N),
        ("Veg Pulav", "140", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Special Arabian Dishes", "Al Faham and shawarma off the vertical grill", [
        ("Chicken Shawarma Roll", "80", N, True),
        ("Rumali Shawarma Roll", "140", N, N),
        ("Special Chicken Shawarma Roll", "130", N, N),
        ("Shawarma Plate", "170", N, N),
        ("Special Shawarma Plate", "200", N, N),
        ("Grill Chicken Full", "440", N, N),
        ("Grill Chicken Half", "230", N, N),
        ("Special Al Faham Full", "500", N, True),
        ("Special Al Faham Half", "260", N, N),
        ("Al Faham Chicken Full", "480", N, N),
        ("Al Faham Chicken Half", "250", N, N),
        ("Fish Al Faham", "Season", N, N),
        ("Mayonnaise", "10", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Rolls", "", [
        ("Chicken Roll", "100", N, N),
        ("Egg Roll", "70", N, N),
        ("Paneer Roll", "80", V, N),
        ("Mushroom Roll", "80", V, N),
        ("Veg Roll", "60", V, N),
    ]),
    (Kitchen.FOOD_PALACE, "Kerala Specials", "Morning counter, from 6 am", [
        ("Puttu", "", V, True),
        ("Appam", "", V, N),
        ("Idiappam", "", V, N),
        ("Pathal Kappa", "", V, N),
        ("Wheat Dosa", "", V, N),
        ("Thalassery Special Snacks", "", V, N),
    ]),

    # ---------------- Broasted King ----------------
    (Kitchen.BROASTED_KING, "Broasted Meals", "Pressure-fried chicken, buns, fries and a Pepsi", [
        ("Special Meal", "299", N, N),
        ("Favour Meal", "399", N, N),
        ("Couple Meal", "199", N, N),
        ("Kids Meal", "139", N, N),
        ("Dinner Meal (4 pc chicken)", "320", N, N),
        ("Dinner Special Meal (6 pc chicken)", "480", N, N),
        ("Fab Chicken Fillet", "299", N, N),
        ("Chicken Strip Meal", "137", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Family Buckets", "Built for the whole table", [
        ("Jumbo Family Meal (14 pc chicken)", "1050", N, True),
        ("Mini Jumbo Family (12 pc chicken)", "900", N, N),
        ("Family Special Meal (10 pc chicken)", "850", N, N),
        ("Small Family Meal (8 pc chicken)", "680", N, N),
        ("Party Box", "89", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Burgers", "Individual / with combo", [
        ("Kids Pop Burger", "99/110", N, N),
        ("Kids Burger", "99/139", N, N),
        ("Veg Burger", "119/139", V, N),
        ("Veg Double Burger", "169/189", V, N),
        ("Crispy Burger", "130/159", N, True),
        ("Crispy Double Burger", "179/199", N, N),
        ("Spicy Crispy Burger", "169/189", N, N),
        ("Chilli Chicken Burger", "169/189", N, N),
        ("Chicken Cheese Burger", "120/159", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Wraps, Strips & Sides", "", [
        ("Veg Wrap Meal", "119/149", V, N),
        ("Rumali Roll", "79", N, N),
        ("Rumali Roll Special Spicy", "139", N, N),
        ("Chicken Nuggets", "139/199", N, N),
        ("Chicken Momos", "169", N, N),
        ("Poppy Chick", "69/120", N, True),
        ("French Fries", "69/120", V, N),
        ("Broasted King Prawns", "230", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Grill Counter", "Full / half / quarter", [
        ("Al Faham", "440/230/120", N, True),
        ("Peri Peri Chicken", "440/230/120", N, N),
        ("Shawai Chicken", "390/200", N, N),
        ("Pepper Al Faham", "440/230/120", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Pizza", "Hand-built, baked to order", [
        ("Margherita", "289", V, N),
        ("Farm Fresh", "389", V, N),
        ("Neapolitan", "389", V, N),
        ("Tandoori Veg", "390", V, N),
        ("Crispy Chicken", "360", N, N),
        ("Tandoori Chicken", "380", N, N),
        ("BBQ Chicken", "390", N, True),
        ("Extra Cheese Topping", "69", V, N),
        ("Veg Topping", "60", V, N),
        ("Non-Veg Topping", "80", N, N),
    ]),
    (Kitchen.BROASTED_KING, "Add Ons", "", [
        ("Bun", "9", V, N),
        ("Mayonnaise", "20", V, N),
        ("Ketchup", "20", V, N),
        ("Garlic Paste", "20", V, N),
        ("Coleslaw", "30", V, N),
        ("Extra Cheese", "20", V, N),
        ("Kuboos", "7", V, N),
        ("One Piece Chicken", "90", N, N),
        ("Chicken Piece of Your Choice", "110", N, N),
        ("Pepsi 750 ml", "65", V, N),
        ("Pepsi 1.25 L", "90", V, N),
    ]),

    # ---------------- Juice Palace ----------------
    (Kitchen.JUICE_PALACE, "Fresh Juice", "Fruit pressed at the counter", [
        ("Orange", "40", V, N),
        ("Musambi", "40", V, N),
        ("Grape", "40", V, N),
        ("Mango", "50", V, N),
        ("Pomegranate", "80", V, N),
        ("Muskmelon", "40", V, N),
        ("Strawberry", "60", V, N),
        ("Green Apple", "60", V, N),
        ("Kiwi", "60", V, N),
        ("Blackcurrant", "60", V, N),
        ("Guava", "60", V, N),
        ("Rose Milk", "60", V, N),
        ("Litchi", "60", V, N),
        ("Butterscotch", "60", V, N),
        ("Chocolate", "60", V, N),
        ("Pista", "60", V, N),
        ("Cold Coffee", "60", V, True),
        ("Cold Boost", "60", V, N),
        ("Cold Horlicks", "60", V, N),
        ("Cold Badam", "60", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Lime & Soda", "", [
        ("Lemon", "30", V, N),
        ("Lime Soda", "30", V, N),
        ("Mint Lime", "40", V, N),
        ("Grape Lime", "40", V, N),
        ("Mango Lime", "40", V, N),
        ("Masala Soda", "40", V, N),
        ("Pineapple Lime", "40", V, N),
        ("Chilly Lime Soda", "40", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Mojitos", "All ₹70", [
        ("Virgin", "70", V, N),
        ("Mint", "70", V, True),
        ("Blue Ocean", "70", V, N),
        ("Kiwi", "70", V, N),
        ("Litchi", "70", V, N),
        ("Jeera Special", "70", V, N),
        ("Passion Fruit", "70", V, N),
        ("Green Apple", "70", V, N),
        ("Kokum", "70", V, N),
        ("Ice Coffee", "70", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Shakes", "", [
        ("Mango Shake", "80", V, N),
        ("Apple Shake", "60", V, N),
        ("Pomegranate Shake", "70", V, N),
        ("Chikku Shake", "60", V, N),
        ("Sharjah", "70", V, True),
        ("Sharjah with Ice Cream", "90", V, N),
        ("Banana Shake", "60", V, N),
        ("Butter Fruit Shake", "80", V, N),
        ("Musk Melon Shake", "60", V, N),
        ("Papaya Shake", "60", V, N),
        ("Tender Coconut Shake", "60", V, N),
        ("Tender Coconut with Ice Cream", "90", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Chocolate Crunches", "Blended with real bars", [
        ("Dairy Milk Crunch", "90", V, N),
        ("Galaxy Crunch", "90", V, N),
        ("KitKat Crunch", "90", V, True),
        ("Five Star Crunch", "90", V, N),
        ("Oreo Crunch", "90", V, N),
        ("Snickers Crunch", "100", V, N),
        ("Brownie with Crunch", "100", V, N),
        ("Tender Coconut Crunch", "100", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Mango Specials", "In season, all day", [
        ("Mango Chocos", "80", V, N),
        ("Mango Masthani", "80", V, N),
        ("Mango Oreo", "80", V, N),
        ("Mango Smoothie", "100", V, N),
        ("Mango Split", "130", V, N),
        ("Mango Falooda", "160", V, N),
        ("Juice Palace Special", "180", V, True),
    ]),
    (Kitchen.JUICE_PALACE, "Dry Fruit Shakes", "", [
        ("Dates", "90", V, N),
        ("Anjeer", "90", V, N),
        ("Cherry", "90", V, N),
        ("Badam", "90", V, N),
        ("Cashew", "100", V, N),
        ("Mixed Dry Fruit", "120", V, True),
    ]),
    (Kitchen.JUICE_PALACE, "Lassi", "", [
        ("Sweet Lassi", "50", V, N),
        ("Mango Lassi", "60", V, N),
        ("Banana Lassi", "60", V, N),
        ("Strawberry Lassi", "60", V, N),
        ("Badam Lassi", "60", V, N),
        ("Chocolate Lassi", "60", V, N),
        ("Fruit Lassi", "70", V, N),
        ("Dry Fruit Lassi", "90", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Falooda", "Layered tall, eat with a spoon", [
        ("Choco Chip", "120", V, N),
        ("Dry Fruits Queen", "150", V, N),
        ("Gadbad", "120", V, True),
        ("Royal Falooda", "160", V, N),
        ("Arabian Falooda", "180", V, N),
        ("Rose Falooda", "140", V, N),
        ("Strawberry Falooda", "140", V, N),
        ("Butterscotch Falooda", "150", V, N),
        ("Pista Falooda", "150", V, N),
        ("Classic Falooda", "150", V, N),
        ("Chocolate Falooda", "150", V, N),
        ("Dilkush", "160", V, N),
        ("Jackpot", "150", V, N),
        ("Italian Delight", "220", V, True),
        ("Oilwala Tender", "180", V, N),
        ("Puttu Ice Cream", "180", V, N),
    ]),
    (Kitchen.JUICE_PALACE, "Ice Cream & Dessert", "", [
        ("Vanilla", "80", V, N),
        ("Mango", "80", V, N),
        ("Strawberry", "80", V, N),
        ("Pista", "60", V, N),
        ("Chocolate", "80", V, N),
        ("Butterscotch", "80", V, N),
        ("Tutty Frutty", "80", V, N),
        ("Black Currant", "90", V, N),
        ("Pineapple Pudding", "50", V, N),
        ("Tender Coconut Pudding", "50", V, N),
        ("Jackfruit Pudding", "60", V, N),
    ]),
]

AWARDS = [
    {
        "title": "1,059 reviews and counting on Google Maps",
        "issuer": "Google Maps, Kengeri Satellite Town",
        "year": "2026",
        "metric": "1,059",
        "metric_label": "reviews",
        "description": "Nine years of walk-ins, late dinners and Sunday families, "
                       "all rated in public. We read every one of them.",
        "is_highlight": True,
        "order": 1,
    },
    {
        "title": "3.8 stars held across nine years of service",
        "issuer": "Verified diner rating",
        "year": "2017\u20132026",
        "metric": "3.8",
        "metric_label": "average rating",
        "description": "Not a perfect score, and we do not pretend otherwise. "
                       "It is an honest one, earned a plate at a time.",
        "is_highlight": True,
        "order": 2,
    },
    {
        "title": "Open 17 and a half hours, every single day",
        "issuer": "6 am to 11:30 pm, seven days",
        "year": "Since day one",
        "metric": "6 am",
        "metric_label": "first puttu of the day",
        "description": "Breakfast puttu for the early shift, biryani at noon, "
                       "shawarma past eleven. No weekly off.",
        "is_highlight": True,
        "order": 3,
    },
    {
        "title": "Three kitchens working under one roof",
        "issuer": "Food Palace \u00b7 Broasted King \u00b7 Juice Palace",
        "year": "",
        "metric": "3",
        "metric_label": "counters",
        "description": "A Malabar kitchen, a broasted chicken counter and a juice bar, "
                       "so one table can order in three directions at once.",
        "is_highlight": True,
        "order": 4,
    },
    {
        "title": "Certified halal kitchen",
        "issuer": "Sourcing and preparation",
        "year": "",
        "description": "All meat is halal, handled on separate boards from the "
                       "vegetarian line.",
        "order": 5,
    },
    {
        "title": "Catering trusted for small and large parties",
        "issuer": "Home and hall orders across west Bengaluru",
        "year": "",
        "description": "Biryani vessels, al faham trays and falooda counters, "
                       "delivered and set up. Call the store manager to plan numbers.",
        "order": 6,
    },
    {
        "title": "Free home delivery within 3 km",
        "issuer": "Minimum order \u20b9300",
        "year": "",
        "description": "Kengeri Satellite Town, Hoysala Circle and the streets around "
                       "the Ring Road, delivered by our own riders.",
        "order": 7,
    },
]

REVIEWS = [
    {
        "user_name": "usman khan",
        "is_local_guide": True,
        "review_count": 87,
        "photo_count": 117,
        "rating": 5,
        "time_ago": "2 years ago",
        "is_edited": True,
        "text": "Food quality, quantity and service is good, especially should try "
                "Kerala style Thalassery briyani, chicken Al-fham, kalmi kabab, Tandoori "
                "kabab and Haryali toondori. They also have good vegetarian food options. "
                "Newly added fruit Juice, milk shakes, lassi, ice cream as well. Also one "
                "can get tea/coffee here. Newly added broasted chicken as well, you can try "
                "chicken popcorn, fried chicken KFC style, burgers, prawns broasted popcorn "
                "and many other fried snacks options available. Take away option is also "
                "available. Have a parking place for around 15-20 bikes. For cars you have "
                "to park nearby places.",
        "order_type": "Dine in",
        "meal_type": "Dinner",
        "price_range": "\u20b9200\u2013400",
        "food_rating": 5,
        "service_rating": 5,
        "atmosphere_rating": 4,
        "likes": 12,
        "is_featured": True,
        "order": 1,
    },
    {
        "user_name": "Vivekanand Exambi",
        "is_local_guide": True,
        "review_count": 37,
        "photo_count": 51,
        "rating": 4,
        "time_ago": "5 years ago",
        "is_edited": True,
        "text": "Shawarama of really good here. All other chicken items like kabab, kalmi, "
                "tandoori are all really good here. Biryani and other rice items aren't that "
                "good. So, if you're going here just order chicken and get the rice someplace "
                "else.",
        "likes": 6,
        "is_featured": True,
        "order": 2,
    },
    {
        "user_name": "Manju Manjunath",
        "is_local_guide": True,
        "review_count": 6,
        "photo_count": 2,
        "rating": 1,
        "time_ago": "a year ago",
        "text": "Very worst food I never had in my life so please choose a good restaurant "
                "which is a good test",
        "likes": 1,
        "order": 3,
    },
]


class Command(BaseCommand):
    help = "Load the Food Palace menu, awards and sample reviews."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete existing menu, awards and reviews before loading.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["fresh"]:
            MenuItem.objects.all().delete()
            MenuCategory.objects.all().delete()
            Award.objects.all().delete()
            Review.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared menu, awards and reviews."))

        items = 0
        for index, (kitchen, name, blurb, rows) in enumerate(MENU, start=1):
            category, _ = MenuCategory.objects.get_or_create(
                kitchen=kitchen,
                name=name,
                defaults={"blurb": blurb, "order": index},
            )
            category.blurb = blurb
            category.order = index
            category.save()

            for position, (item_name, price, is_veg, is_signature) in enumerate(rows, start=1):
                MenuItem.objects.update_or_create(
                    category=category,
                    name=item_name,
                    defaults={
                        "price": price,
                        "is_veg": is_veg,
                        "is_signature": is_signature,
                        "order": position,
                    },
                )
                items += 1

        for award in AWARDS:
            Award.objects.update_or_create(title=award["title"], defaults=award)

        for review in REVIEWS:
            Review.objects.update_or_create(
                user_name=review["user_name"],
                time_ago=review["time_ago"],
                defaults=review,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {MenuCategory.objects.count()} categories, {items} dishes, "
                f"{Award.objects.count()} awards and {Review.objects.count()} reviews."
            )
        )
