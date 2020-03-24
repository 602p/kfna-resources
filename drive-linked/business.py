from jinja2 import Environment, FileSystemLoader, select_autoescape
from sheetsloader import load_spreadsheet, get_sheet, get_text, get_html

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('listing_businesses.html')

class Business:
	def __init__(self, row):
		self.name = get_text(row[0])
		self.slug = ''.join([x for x in self.name.lower() if x in 'abcdefghijklmnopqrstuvwxyz'])
		self.link = row[0].get('hyperlink')
		self.hours = get_html(row[1])
		self.phone = get_text(row[2])
		self.email = None
		self.address = get_text(row[3])
		self.pickup = get_text(row[4]).lower() == "yes"

		delivery_tags = get_text(row[5]).split('\n')
		if delivery_tags[0].lower() in ("no", "n/a"):
			delivery_tags = []

		if delivery_tags:
			delivery_tags.append("delivery")

		self.tags = [x for x in (delivery_tags + \
					get_text(row[6]).split('\n')) if x.strip()]

		self.notes = get_html(row[7])
		if get_html(row[7]) and get_html(row[8]):
			self.notes += "<br/>"
		self.notes += get_html(row[8])
		if get_html(row[8]):
			self.tags.append("giftcards")
		self.notes = self.notes.replace("<br/>", "<br/>&rarr; ")

		self.updated = get_text(row[9])

	def slug_as_json(self):
		return repr(self.slug)

	def tags_as_json(self):
		return repr(self.tags)

	def __repr__(self):
		return "<Business "+repr(self.__dict__)+">"

rows = get_sheet(load_spreadsheet('1WsuS_2tOo0iMiVDOquAd21RbzuyYQ0UaWqTwNcfD_jU'), 'Businesses')
i=0
while "SHOPS - OPEN" not in get_text(rows[i][0]):
	i+=1
i+=1

businesses = []
while get_text(rows[i][0]):
	businesses.append(Business(rows[i]))
	i+=1

tag_names = {
	"services-online": "Offering services online",
	"curbside-pickup": "Curbside pickup",
	"shipping": "Shipping available",
	"if-in-need": "Delivery available if in need",
	"delivery": "Delivery available",
	"giftcards": "Gift cards available"
}

nofilter_tags = ['if-in-need']
hidden_tags = []

with open('public/businesses/index.html', 'w') as fd:
	fd.write(template.render(items=businesses, tag_names=tag_names, nofilter_tags=nofilter_tags, hidden_tags=hidden_tags))
