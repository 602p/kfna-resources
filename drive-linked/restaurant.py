from jinja2 import Environment, FileSystemLoader, select_autoescape
from sheetsloader import load_spreadsheet, get_sheet, get_text, get_html

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('listing_restaurants.html')

class Restaurant:
	def __init__(self, row):
		self.name = get_text(row[0])
		self.slug = ''.join([x for x in self.name.lower() if x in 'abcdefghijklmnopqrstuvwxyz'])
		self.link = row[0].get('hyperlink')
		self.hours = get_html(row[1])
		self.phone = get_text(row[2])
		self.email = get_text(row[3])
		self.address = get_text(row[4])
		self.pickup = get_text(row[5]).lower() == "yes"

		delivery_tags = get_text(row[6]).split('\n')
		if delivery_tags[0].lower() == "no":
			delivery_tags = []

		if delivery_tags:
			delivery_tags.append("any-delivery")

		self.tags = [x for x in (delivery_tags + \
					get_text(row[7]).split('\n') + \
					get_text(row[8]).split('\n')) if x.strip()]

		self.notes = get_html(row[9])
		if get_html(row[9]) and get_html(row[10]):
			self.notes += "<br/>"
		self.notes += get_html(row[10])
		if get_html(row[10]):
			self.tags.append("giftcards")
		self.notes = self.notes.replace("<br/>", "<br/>&rarr; ")

		self.updated = get_text(row[11])

	def slug_as_json(self):
		return repr(self.slug)

	def tags_as_json(self):
		return repr(self.tags)

	def __repr__(self):
		return "<Restaurant "+repr(self.__dict__)+">"

rows = get_sheet(load_spreadsheet('1WsuS_2tOo0iMiVDOquAd21RbzuyYQ0UaWqTwNcfD_jU'), 'Restaurants')
i=0
while "RESTAURANTS - STILL OPEN" not in get_text(rows[i][0]):
	i+=1
i+=1

restaurants = []
while get_text(rows[i][0]):
	restaurants.append(Restaurant(rows[i]))
	i+=1

tag_names = {
	"bitesquad": "Bitesquad delivery",
	"ubereats": "Uber Eats delivery",
	"doordash": "DoorDash delivery",
	"phone": "Order on the phone",
	"card": "Pay via card",
	"curbside": "Curbside pick-up",
	"takeout": "Takeout-style pick-up",
	"firstparty": "First-party delivery",
	"cash": "Pay via cash",
	"postmates": "Postmates delivery",
	"inperson": "Order in-person",
	"email": "Order via email",
	"any-delivery": "Delivery options",
	"giftcards": "Gift cards available"
}

nofilter_tags = ['bitesquad', 'ubereats', 'doordash', 'firstparty', 'postmates']
hidden_tags = ['any-delivery']

with open('public/restaurants/index.html', 'w') as fd:
	fd.write(template.render(items=restaurants, tag_names=tag_names, nofilter_tags=nofilter_tags, hidden_tags=hidden_tags))
