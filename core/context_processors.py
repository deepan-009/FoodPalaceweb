"""Restaurant facts available in every template as {{ site.* }}."""

RESTAURANT = {
    "name": "Food Palace Family Restaurant",
    "name_kn": "\u0cab\u0cc1\u0ca1\u0ccd \u0caa\u0ccd\u0caf\u0cbe\u0cb2\u0cc7\u0cb8\u0ccd \u0cab\u0ccd\u0caf\u0cbe\u0cae\u0cbf\u0cb2\u0cbf \u0cb0\u0cc6\u0cb8\u0ccd\u0c9f\u0ccb\u0cb0\u0cc6\u0c82\u0c9f\u0ccd",
    "tagline": "The real taste of Malabar",
    "cuisine": "North Indian \u00b7 Malabar \u00b7 Arabian",
    "rating": "3.8",
    "rating_count": "1,059",
    "price_range": "\u20b9200\u2013400",
    "address": "173, Kengeri Ring Rd, Stage I, Kengeri Satellite Town, Bengaluru, Karnataka 560056",
    "address_short": "Kengeri Satellite Town, Bengaluru",
    "landmark": "1st Main Road, opposite Union Bank, near Hoysala Circle",
    "plus_code": "WFFM+4V Bengaluru, Karnataka",
    "phone_primary": "09606602293",
    "phone_secondary": "09606602290",
    "phone_third": "09606602291",
    "email": "foodpalace77@gmail.com",
    "maps_url": "https://maps.app.goo.gl/DjnRuwYJ2eknyzaX7",
    "opens": "6:00 am",
    "closes": "11:30 pm",
    "open_hour": 6,          # used by the live open/closed indicator
    "close_hour": 23.5,
    "delivery_radius": "3 km",
    "delivery_minimum": "\u20b9300",
    "hours": [
        ("Monday", "6 am \u2013 11:30 pm"),
        ("Tuesday", "6 am \u2013 11:30 pm"),
        ("Wednesday", "6 am \u2013 11:30 pm"),
        ("Thursday", "6 am \u2013 11:30 pm"),
        ("Friday", "6 am \u2013 11:30 pm"),
        ("Saturday", "6 am \u2013 11:30 pm"),
        ("Sunday", "6 am \u2013 11:30 pm"),
    ],
}


def restaurant(request):
    return {"site": RESTAURANT}
