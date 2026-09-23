# Food Palace Family Restaurant — Django site

A six-page site for Food Palace Family Restaurant, Kengeri Satellite Town, Bengaluru.
Home, Menu, About us, Awards, Reviews and Contact us, with the full menu card and a
reusable review card you can feed your own Google Maps reviews into.

---

## Run it

You need Python 3.10 or newer.

```bash
cd foodpalace

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations core
python manage.py migrate
python manage.py seed_data         # loads the whole menu card
python manage.py createsuperuser   # so you can log in to /admin/

python manage.py runserver
```

Open http://127.0.0.1:8000 — and http://127.0.0.1:8000/admin/ to edit content.

There are shortcut scripts too: `./setup.sh` on macOS or Linux, `setup.bat` on Windows.

The page loads Tailwind and Google Fonts from a CDN, so keep an internet
connection the first time you open it.

---

## Adding your reviews

This is the part you asked to be able to do yourself. Three ways, pick whichever suits.

### 1. One at a time in the admin

Go to `/admin/core/review/add/`. Every field from the Google card is there —
name, Local Guide status, review and photo counts, star rating, "a year ago",
the text, and the optional Order type / Meal type / Food / Service / Atmosphere block.
Tick **is featured** to also show that review on the home page.

### 2. Paste a batch as JSON

Copy `core/data/reviews.sample.json` to `core/data/reviews.json`, fill it with
your reviews, then:

```bash
python manage.py import_reviews core/data/reviews.json
```

Only `user_name`, `rating` and `text` are required. Add `--replace` to wipe the
existing reviews first. Re-running the command updates rather than duplicates.

### 3. From a spreadsheet

Export to CSV using the headers in `core/data/reviews.sample.csv`, then:

```bash
python manage.py import_reviews core/data/reviews.csv
```

### The review card itself

`templates/partials/review_card.html` is the single card, matching the Google
layout in your screenshot: circular avatar, name, Local Guide credits, the
five-star row, time ago, the review text, Like and Share at the bottom, and the
three-dot menu top right. Use it anywhere:

```django
{% for review in reviews %}
  {% include "partials/review_card.html" %}
{% endfor %}
```

It reads `review.user_name`, `review.profile_pic_url`, `review.rating`,
`review.text`, `review.time_ago`, `review.is_local_guide`, `review.review_count`,
`review.photo_count`, `review.likes` and the optional detail fields. Leave
`profile_pic_url` blank and it draws a coloured initial instead, with a stable
colour per person.

Behaviour that comes free: reviews longer than six lines get a "Read more"
toggle, Like posts to the server and remembers itself per browser session,
Share uses the phone's native share sheet and falls back to the clipboard,
and the three-dot menu closes on Escape or an outside click.

---

## Editing the menu

`python manage.py seed_data` loads everything transcribed from your menu
photographs — around 300 dishes across three counters:

- **Food Palace** — soups, salads, veg and non-veg starters, the Food Palace
  specials, Indian bread, veg and non-veg gravies, mutton, egg, seasonal fish,
  biryani, fried rice and noodles, Arabian dishes, rolls, Kerala specials
- **Broasted King** — meals, family buckets, burgers, wraps, the grill counter,
  pizza, add-ons
- **Juice Palace** — juice, lime, mojitos, shakes, chocolate crunches, mango
  specials, dry fruit shakes, lassi, falooda, ice cream and desserts

After that, edit anything at `/admin/core/menuitem/` — the list view lets you
change prices inline. Prices are stored as text so `160/300` (half/full),
`440/230/120` (full/half/quarter) and `Season` all display correctly.

Tick **is signature** on a dish and it appears in the "What to order first"
block on the home page.

`python manage.py seed_data --fresh` clears the menu, awards and reviews first.

---

## Project layout

```
foodpalace/
├── manage.py
├── requirements.txt
├── setup.sh / setup.bat
├── config/
│   ├── settings.py          templates dir, static dirs, IST timezone
│   ├── urls.py              admin + core
│   ├── wsgi.py  asgi.py
├── core/
│   ├── models.py            MenuCategory, MenuItem, Review, Award, Booking
│   ├── views.py             home, menu, about, awards, reviews, contact, like_review
│   ├── urls.py              named routes under the "core" namespace
│   ├── forms.py             BookingForm
│   ├── admin.py             content editing for the whole site
│   ├── context_processors.py   address, phones, hours → {{ site.* }} everywhere
│   ├── templatetags/core_extras.py   stars, split_price, liked_by
│   ├── management/commands/
│   │   ├── seed_data.py     the full menu card, awards, sample reviews
│   │   └── import_reviews.py   bulk JSON/CSV review import
│   └── data/                sample review files
├── templates/
│   ├── base.html
│   ├── partials/  header.html  footer.html  review_card.html
│   └── pages/     home.html  menu.html  about.html  awards.html
│                  reviews.html  contact.html
└── static/
    ├── css/style.css        design tokens and all components
    ├── js/main.js           nav, reveals, live hours, menu filter, review actions
    └── img/                 drop your own photos here
```

### Routes

| URL | Name | Page |
|---|---|---|
| `/` | `core:home` | Home |
| `/menu/` | `core:menu` | Menu (`?kitchen=food_palace` filters a counter) |
| `/about/` | `core:about` | About us |
| `/awards/` | `core:awards` | Awards |
| `/reviews/` | `core:reviews` | Reviews (`?rating=5`, `?sort=highest`) |
| `/contact/` | `core:contact` | Contact us, booking form |
| `/reviews/<id>/like/` | `core:like_review` | POST endpoint behind the Like button |

---

## Design notes

The visual language comes from the restaurant's own printed menu card rather
than a generic template: a dark cocoa board, the yellow angled banner tags used
for each section heading, and gold pricing. The palette is set once in
`static/css/style.css`:

```css
--board:   #140F0C    /* the menu card itself      */
--ember:   #C2431F    /* tandoor coals             */
--saffron: #E9A83A    /* the yellow banner tags    */
--leaf:    #1F5B4E    /* Malabar green, veg marker */
--coconut: #F4EADC    /* text                      */
```

Type is Fraunces for display and Inter for everything else, with Noto Sans
Kannada for ಫುಡ್ ಪ್ಯಾಲೇಸ್. Change a colour in `:root` and the whole site follows.

Motion is deliberate rather than decorative: one reveal as sections enter, a
live open/closed pill that recalculates against 6 am–11:30 pm IST every minute,
hover states on things you can actually click, and everything switched off under
`prefers-reduced-motion`.

### Adding photos

Drop images into `static/img/` and reference them with
`{% load static %}` then `{% static 'img/biryani.jpg' %}`. The design works
without photography, so add it where it earns its place — the hero and the
signature dish cards first.

---

## Going live

Before this touches a real server:

1. Set a fresh `SECRET_KEY` in `config/settings.py`, ideally from an env var.
2. `DEBUG = False` and put your real domain in `ALLOWED_HOSTS`.
3. `python manage.py collectstatic` and serve `staticfiles/` from your web server.
4. Swap SQLite for Postgres if more than a handful of people will use the admin.
5. Wire the contact form to email or WhatsApp so the counter actually sees
   bookings — right now they land in `/admin/core/booking/`.
6. Replace the Tailwind CDN with a built stylesheet (`npx tailwindcss -o`), since
   the CDN build prints a console warning and is slower.

---

Content is from the restaurant's Google Maps listing and the menu photographs
dated March 2025 and August 2026. Check prices against the board before printing.
