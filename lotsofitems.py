from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String

from database_setup import User, Category, CatalogItem, Base

engine = create_engine('sqlite:///categoryitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Categories are Tech, Style, Outdoors, Household, Dude I Want That!,

#Items for Tech
category1 = Category(name = "Tech")

session.add(category1)
session.commit()


catalogItem1 = CatalogItem(name = "goTenna", description = "Whether you're skiing or camping you know how annoying it can be to get ahold of your friends. The goTenna solves messaging this by sending messages without cell service.",
price = "$149.00", category = category1)


session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(name = "Hoverdock for iPhone", description = "Never deal with tangled cords again. This gadget lets you charge your phone upright so you can still see and play around with the screen as the battery fills up. A gift for the entire family.",
 price = "$28", category = category1)

session.add(catalogItem2)
session.commit()


catalogItem3 = CatalogItem(name = "Samsung 49-Inch Gaming Monitor", description = "The ultra-wide 49-inch screen with its innovative 32:9 aspect ratio means you always get to see game scenes in their entirety, exactly as their developers intended.",
 price = "$949.99", category = category1)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(name = "TinyCircuits Arcade Kit Toy", description = "The tiny arcade lets you relive the golden age of video games with an arcade cabinet that fits in the palm of your hand. The tiny arcade comes as a kit that is simple to put together.",
 price = "$59.99", category = category1)

session.add(catalogItem4)
session.commit()


catalogItem5 = CatalogItem(name = "Fitbit Ionic Smartwatch", description = "Personalized guidance and insights. Your favorite songs and apps. All the features you love from Fitbit. This is the watch you've been waiting for. Get this motivating timepiece today.",
 price = "$299.95", category = category1)

session.add(catalogItem5)
session.commit()



#Items for Style
category2 = Category(name = "Style")

session.add(category2)
session.commit()


catalogItem1 = CatalogItem(name = "Men's Performance Outdoor Sport Sandal", description = "From long backcountry hikes to stand-up paddling on the Caribbean Sea, the Decimal is the ideal sandal for active people who want performance, freedom and comfort in an open heel sandal.",
 price = "$79.99", category = category2)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(name = "Sitting-Pocket Sweatpants", description = "Pockets. Designed to hold stuff while your hands are busy. Pockets. Designed to drop stuff or make it really, really hard to get to when you sit down. Sitting pockets. Designed to conquer.",
 price = "$79.20", category = category2)

session.add(catalogItem2)
session.commit()


catalogItem3 = CatalogItem(name = "Protection Cut Resistant Sleeves", description = "DuPont Kevlar brand fiber, flexible, cool and comfortable to wear; with designed protection against bites, cuts, and scratches. Never worry again.",
 price = "19.99", category = category2)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(name = "Men's Soft Shell Heated Jacket Kit", description = "KEEPS YOU WARM AND COMFORTABLE: Soft shell fabric on the outside make the jacket water and wind resistance but still soft and flexible. The interior has some light insulation with fleece lining.",
 price = "154.99", category = category2)

session.add(catalogItem4)
session.commit()


catalogItem5 = CatalogItem(name = "NiteSPecs Lighted LED Reading Glasses", description = "NiteSpecs LED reading glasses are a clever combination of reading glasses and lighting, giving you the magnification and illumination all in one! Designed for both men and women.",
price = "$19.95", category = category2)

session.add(catalogItem5)
session.commit()



#Items for Outdoors
category3 = Category(name = "Outdoors")

session.add(category3)
session.commit()


catalogItem1 = CatalogItem(name = "Yaktrax Walk Traction Cleats", description = "Lightweight and affordable slip-on traction cleats to reduce the risk of falls when walking on snow or ice to work, school, or even to the mailbox. Always be safe with Yaktrax Cleats.",
 price = "$15.70", category = category3)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name = "Insect Shield Outdoor Blanket", description = "Insect Shield is a patent pending technology for treating gear that repels mosquitoes, ticks, flies and fleas. Whether in the backwoods or the backyard, Insect Shield helps keep you protected.",
 price = "$28.95", category = category3)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name = "Broil Chef Star Wars TIE Fighter Gas Grill", description = "Feeding a squadron of Imperial pilots can be tricky. Thankfully, there's a the TIE fighter edition Broilchef portable BBQ. In place of twin ion engines, this grill has a stainless steel burner.",
 price = "$249.99", category = category3)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name = "LOTR Fire Pit Eye Tower", description = "ONE OF A KIND very detailed hand made fire-pit from Canada. Approximately 5 foot high and 2 foot wide base made from heavy gauge steel. Have a taste of Mordor in your backyard today!",
 price = "$696.34", category = category3)

session.add(catalogItem4)
session.commit()



#Items for Household
category4 = Category(name = "Household")

session.add(category4)
session.commit()


catalogItem1 = CatalogItem(name = "Elm Tree Bookshelf", description = "Full bodied from the ground up just as you would find with a large old Elm tree. A practical tree with shelf surfaces at all heights makes it ideal for just about any room of the house.",
 price = "$1,128.99", category = category4)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name = "Spartan Shield XXL Fireproof Money Bag", description = "Measuring 16x12x3.5, Spartan Shield XXL is easily the largest fire resistant bag on Amazon. Our extra large fireproof bag provides ample space to store a laptop, tablet, passwords, and expensive jewelry.",
price = "$32.68", category = category4)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name = "Spinx", description = "The first ever toilet cleaning robot. With amazing design, through cleanliness, you'll never have to clean a toilet again. Buy one today without ever worrying about stains...ever.",
 price = "[To Be Announced]", category = category4)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name = "Logical Fallacies Poster", description = "This handy reference poster details 24 of the most common logical fallacies used by politicians, the media, advertisers and internetians. Printed on high quality #80 satin card stock.",
 price = "$20", category = category4)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name = "Effie", description = "Effie is a new domestic appliance that irons your clothes for you. Hang your clothes up straight from the washing machine, click go, and look smart. It's as simple as that!",
 price = "$985.66", category = category4)

session.add(catalogItem5)
session.commit()



#Items for Uncommon Goods
category5 = Category(name = "Uncommon Goods")

session.add(category5)
session.commit()


catalogItem1 = CatalogItem(name = "The Infrared Supine Sauna", description = "The Infrared Supine Sauna is a personal sauna that uses an array of tiny infrared lights to penetrate deeply into aching tissue. It's also full of jade stones used in traditional Chinese medicine.",
 price = "$14,000", category = category5)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name = "Scorkl", description = "Scorkl is lightweight, portable, refillable via hand pump and gives you up to 10min underwater. With Scorkl, you'll never have to deal with bulky, burdensome scuba gear for those short dives.",
 price = "$398", category = category5)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name = "GameSir G5", description = "GameSir G5 is the revolutionary gamepad designed for MOBA and first/third person shooting mobile games. iOS and Android compatible. Bring your home console wherever you go.",
 price = "$49", category = category5)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name = "Ephemeral's Tattoo Ink", description = "Want a tattoo without the lifetime committment? Ephemeral Tattoos makes inks that are applied like regular tattoos but disappear on their own. Reserve a spot at your city's exclusive pop-up shop today!",
 price = "Varies", category = category5)

session.add(catalogItem4)
session.commit()

print "added catalog items!"
