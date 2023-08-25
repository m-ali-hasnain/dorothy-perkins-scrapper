# Imports
import scrapy
from currency_converter import CurrencyConverter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from ..items import DorothyperkinsScrapperItem
import re
from webdriver_manager.chrome import ChromeDriverManager

# Constants

# Scroll pause time for scrapping pages having infinite scroll
PAUSE_TIME = 5
FIT_KEYWORDS = ["Maternity", "Petite", "Plus Size", "Curvy", "Tall"]
NECK_LINE_KEYWORDS = ["Scoop", "Round Neck," "U Neck", "U-Neck", "V Neck",
                      "V-neck", "V Shape", "V-Shape", "Deep", "Plunge", "Square",
                      "Straight", "Sweetheart", "Princess", "Dipped", "Surplice",
                      "Halter", "Asymetric", "One-Shoulder", "One Shoulder",
                      "Turtle", "Boat", "Off- Shoulder", "Collared", "Cowl", "Neckline"]

OCCASIONS_KEYWORDS = ["office", "work", "smart", "workwear", "wedding", "nuptials",
                      "night out", "evening", "spring", "summer", "day", "weekend",
                      "outdoor", "outdoors", "adventure", "black tie", "gown",
                      "formal", "cocktail", "date night", "vacation", "vacay", "fit",
                      "fitness", "athletics", "athleisure", "work out", "sweat",
                      "swim", "swimwear", "lounge", "loungewear"]

LENGTH_KEYWORDS = ["length", "mini", "short", "maxi", "crop", "cropped", "sleeves",
                   "tank", "top", "three quarter", "ankle", "long"]

STYLE_KEYWORDS = ["bohemian", "embellished", "sequin", "floral", "off shoulder",
                  "puff sleeve", "bodysuit", "shell", "crop", "corset", "tunic",
                  "bra", "camisole", "polo", "aviator", "shearling", "sherpa",
                  "biker", "bomber", "harrington", "denim", "jean", "leather",
                  "military", "quilted", "rain", "tuxedo", "windbreaker", "utility",
                  "duster", "faux fur", "overcoat", "parkas", "peacoat", "puffer",
                  "skater", "trench", "Fleece", "a line", "bodycon", "fitted",
                  "high waist", "high-low", "pencil", "pleat", "slip", "tulle",
                  "wrap", "cargo", "chino", "skort", "cigarette", "culottes",
                  "flare", "harem", "relaxed", "skinny", "slim", "straight leg",
                  "tapered", "wide leg", "palazzo", "stirrup", "bootcut", "boyfriend",
                  "loose", "mom", "jeggings", "backless", "bandage", "bandeau",
                  "bardot", "one-shoulder", "slinger", "shift", "t-shirt", "smock",
                  "sweater", "gown"]

AESTHETIC_KEYWORDS = ["E-girl", "VSCO girl", "Soft Girl", "Grunge", "CottageCore",
                      "Normcore", "Light Academia", "Dark Academia ", "Art Collective",
                      "Baddie", "WFH", "Black", "fishnet", "leather"]

DISALLOWED_LINKS = ["view-all", "seasonal-offers", "sale", "new-in", "new-in-dresses", "wedding-guest-dresses",
                    "inspire-me", "shoes", "holiday-shoes", "hot-pink", "shades-of-green", "denimfitguide", "Earrings",
                    "jewellery", "sunglasses", "socks", "scarves", "healty-beauty", "home-fragrance", "Fascinator",
                    "belts", "accessories", "tote-bag", "bags", "sandals", "boots", "shoes", "loafers", "wedges",
                    "shoes/wide-fit", "#", "occasion-wear", "summer-shop", "Sale", "Cyber Monday", "Shift dresses",
                    "clothing", "prefn1=classification&prefv1=Main%20Collection",
                    ]
DISALLOWED_KEYWORDS = ["jogger", "joggers", "sandals","sandal", "shoe",
                       "shoes", "heels", "accessories", "earrings", "PROMOTION", "INSPIRE ME",
                       "Cyber Monday", "Sale","Shift dresses"]
CATEGORY_KEYWORDS = ['Bottom', 'Shift', 'Swim Brief', 'Quilted', 'Boyfriend',
                     'Padded', 'Track', 'Other', 'Oversized', 'Denim Skirt',
                     'Stick On Bra', 'Cardigan', 'Thong', 'Romper', 'Pea Coat',
                     'Skater', 'Swing', 'Lingerie & Sleepwear', 'Wrap', 'Cargo Pant',
                     'Cape', 'Trucker', 'Nursing', 'Bikini', 'Parka', 'Regular', 'Denim',
                     'Duster', 'Faux Fur', 'Hoodie', 'Bralet', 'Overcoat', 'Corset Top',
                     'T-Shirt', 'Mini', 'Maxi', 'Blazer', 'Super Skinny', 'Summer Dresses',
                     'Chino', 'Short', 'Set', 'Military', 'Overall', 'Vest', 'Bomber Jacket',
                     'Tea', 'Ski Suit', 'Work Dresses', 'High Waisted', 'Culotte', 'Overall Dress',
                     'Jean', 'Loungewear', 'Leather Jacket', 'Unpadded', 'Coats & Jackets', 'Underwired',
                     'Corset', 'Night gown', 'Poncho', 'Pant', 'Cigarette', 'Sweatpant', 'Rain Jacket',
                     'Loose', 'Swimwear & Beachwear', 'Shirt', 'Denim Jacket', 'Co-ord', 'Tight', 'Vacation Dress',
                     'Harrington', 'Bandage', 'Bootcut', 'Biker', 'Crop Top', 'Trench', 'Tracksuit', 'Suit Pant',
                     'Relaxed', 'Day Dresses', 'Tuxedo', 'Tapered', 'Wide Leg', 'Bohemian', 'Pleated', 'Wiggle',
                     'One Shoulder', 'Smock Dress', 'Flare', 'Peg Leg', 'Cover Up', 'Unitard', 'Sweater',
                     'Lounge', 'Top', 'Bodycon', 'Push Up', 'Slip', 'Knitwear', 'Leather', 'Pencil Dress',
                     'Off Shoulder', 'Jersey Short', 'Multiway', 'Balconette', 'Wax Jacket', 'Coat', 'Brief',
                     'Coach', 'Jumpsuits & Rompers', 'Bra', 'Long Sleeve', 'Fleece', 'Activewear', 'Jegging',
                     'Outerwear', 'Bandeau', 'Slim', 'Going Out Dresses', 'Bardot', 'Pajama', 'Sweatsuit',
                     'Blouse', 'Sweaters & Cardigans', 'Straight Leg', 'Windbreaker', 'Tank Top', 'Cold Shoulder',
                     'Halter', 'Dresses', 'T-Shirt', 'Trouser', 'Cami', 'Camis', 'Wedding Guest', 'Bodysuit', 'Triangle',
                     'Casual Dresses', 'Chino Short', 'Boiler Suit', 'Raincoat', 'Formal Dresses', 'Skinny',
                     'Jumper', 'Strapless', 'Cropped', 'Jacket', 'Bridesmaids Dress', 'Tunic', 'A Line',
                     'Denim Dress', 'Cocktail', 'Skirt', 'Jumpsuit', 'Shapewear', 'Occasion Dresses',
                     'Hoodies & Sweatshirts', 'Sweatshirt', 'Aviator', 'Sweater Dress', 'Sports Short',
                     'Shirt', 'Puffer', 'Cargo Short', 'Tulle', 'Swimsuit', 'Mom Jean', 'Legging',
                     'Plunge', 'Teddie', 'Denim Short', 'Intimate', 'Pencil Skirt', 'Backless', 'Tank']

CATEGORY_TO_TYPE = {
    'Co-ords': ['Co-ord', 'Sweatsuit', 'Tracksuit', 'Set'],
    'Coats & Jackets': ['Coats & Jacket', 'Cape', 'Cardigan', 'Coat', 'Jacket', 'Poncho', 'Ski Suit', 'Vest', 'Blazer'],
    'Dresses': ['Dresses', 'Bridesmaids Dress', 'Casual Dress', 'Going Out Dress', 'Occasion Dress',
                'Summer Dress', 'Work Dress', 'Formal Dress', 'Day Dress', 'Wedding Guest', 'Vacation Dress'],
    'Hoodies & Sweatshirts': ['Hoodies & Sweatshirts', 'Fleece', 'Hoodie', 'Sweatshirt'],
    'Denim': ['Denim Jacket', 'Denim Dress', 'Denim Skirt', 'Denim Short', 'Jean', 'Jegging'],
    'Jumpsuits & Rompers': ['Jumpsuits & Rompers', 'Boiler Suit', 'Jumpsuit', 'Overall', 'Romper', 'Unitard'],
    'Lingerie & Sleepwear': ['Lingerie & Sleepwear', 'Intimate', 'Bra', 'Brief', 'Corset', 'Bralet', 'Night gown',
                             'Pajama', 'Shapewear', 'Slip', 'Teddie', 'Thong', 'Tight', 'Bodysuit', 'Camis', 'Cami'],
    'Loungewear': ['Loungewear', 'Lounge', 'Activewear', 'Outerwear', 'Hoodie', 'Legging', 'Overall', 'Pajama',
                   'Sweatpant', 'Sweatshirt', 'Tracksuit', 'T-Shirt'],
    'Bottoms': ['Bottom', 'Chino', 'Legging', 'Pant', 'Suit Pant', 'Sweatpant', 'Tracksuit', 'Short', 'Skirt',
                'Trouser'],
    'Sweaters & Cardigans': ['Sweaters & Cardigans', 'Sweatpant', 'Cardigan', 'Sweater', 'Knitwear'],
    'Swimwear & Beachwear': ['Swimwear & Beachwear', 'Bikini', 'Cover Up', 'Short', 'Skirt', 'Swim Brief', 'Swimsuit'],
    'Tops': ['Top', 'Blouse', 'Bodysuit', 'Bralet', 'Camis', 'Corset Top', 'Crop Top', 'Shirt', 'Sweater',
             'Tank Top', 'T-Shirt', 'Tunic'],
}
CATEGORY_TO_STYLE = {
  'Co-ords' : ['Co-ords'],
  'Coats & Jackets' : ['Coats & Jackets', 'Aviator', 'Biker', 'Bomber Jacket', 'Coach', 'Denim Jacket', 'Duster', 'Faux Fur', 'Harrington', 'Leather', 'Leather Jacket', 'Military', 'Other', 'Overcoat', 'Parkas', 'Pea Coat', 'Puffer', 'Quilted', 'Raincoats', 'Rain Jackets', 'Regular', 'Skater', 'Track', 'Trench', 'Trucker', 'Tuxedo', 'Wax Jacket', 'Windbreaker'],
  'Dresses' : ['Dresses', 'A Line', 'Backless', 'Bandage', 'Bandeau', 'Bardot', 'Bodycon', 'Bohemian', 'Cold Shoulder', 'Denim', 'Jumper', 'Leather', 'Long Sleeve', 'Off Shoulder', 'One Shoulder', 'Other', 'Overall Dress', 'Pencil Dress', 'Shift', 'Shirt', 'Skater', 'Slip', 'Smock Dresses', 'Sweater Dress', 'Swing', 'Tea', 'T-Shirt', 'Wiggle', 'Wrap', 'Cocktail', 'Maxi', 'Mini'],
  'Hoodies & Sweatshirts' : ['Hoodies & Sweatshirts'],
  'Denim' : ['Jeans', 'Bootcut', 'Boyfriend', 'Cropped', 'Flare', 'High Waisted', 'Loose', 'Mom Jeans', 'Other', 'Regular', 'Skinny', 'Slim', 'Straight Leg', 'Super Skinny', 'Tapered', 'Wide Leg'],
  'Jumpsuits & Rompers' : ['Jumpsuits & Rompers'],
  'Lingerie & Sleepwear' : ['Lingerie & Sleepwear', 'Balconette', 'Halter', 'Multiway', 'Nursing', 'Padded', 'Plunge', 'Push Up', 'Stick On Bra', 'Strapless', 'Triangle', 'T-Shirt', 'Underwired', 'Unpadded'],
  'Loungewear' : ['Loungewear'],
  'Bottoms' : ['Bottoms', 'Cargo Pants', 'Cigarette', 'Cropped', 'Culottes', 'Flare', 'High Waisted', 'Other', 'Oversized', 'Peg Leg', 'Regular', 'Relaxed', 'Skinny', 'Slim', 'Straight Leg', 'Super Skinny', 'Tapered', 'Wide Leg', 'Cargo Shorts', 'Chino Shorts', 'Denim', 'High Waisted', 'Jersey Shorts', 'Other', 'Oversized', 'Regular', 'Relaxed', 'Skinny', 'Slim', 'Sports Shorts', 'A Line', 'Bodycon', 'Denim', 'High Waisted', 'Other', 'Pencil Skirt', 'Pleated', 'Skater', 'Slip', 'Tulle', 'Wrap'],
  'Sweaters & Cardigans' : ['Sweaters & Cardigans'],
  'Swimwear & Beachwear' : ['Swimwear & Beachwear', 'Halter', 'High Waisted', 'Multiway', 'Padded', 'Plunge', 'Strapless', 'Triangle', 'Underwired'],
  'Tops' : ['Tops'],
}

WEBSITE_NAME = "dorothyperkins"


class DorothyperkinsSpider(scrapy.Spider):
    name = 'dorothyperkins'
    allowed_domains = ['www.dorothyperkins.com']

    # this method configures initial settings for selenium chrome webdriver
    def __init__(self, *a, **kw):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.currency_converter = CurrencyConverter()
        super().__init__(*a, **kw)

    def start_requests(self):
        base_url = "https://www.dorothyperkins.com/"
        yield scrapy.Request(url=base_url, callback=self.parse_categories)


    def parse_categories(self, response):
        categories = response.xpath(
            "(//div[@class='b-menu_item-submenu b-menu_subpanel-content m-level_3_content']) /div /a/@href").getall()
        for link in categories:
            if not self.in_disallowed_links(link) and not re.search(".*womens\/dresses$", link) \
                    and not re.search(".*womens\/tailoring$", link):
                yield scrapy.Request(url=link, callback=self.parse_pages)

    # This function will first find total products, and then yield
    # request for each page with 80 products on each.
    def parse_pages(self, response):
        total_products = int(response.css("span.b-load_progress-value:nth-of-type(2)::text").get().replace(",", ""))
        for page in range(0, total_products, 80):
            page_query = f"?start={page}&sz={self.get_pages_upperlimit(page, total_products)}"
            current_page = response.urljoin(page_query)
            yield scrapy.Request(url=current_page, callback=self.get_all_products)

    # This function, parse href of all products on current page
    def get_all_products(self, response):
        products = response.css(".l-plp_grid section div.b-product_tile-container div div a::attr('href')").getall()
        for product_url in products:
            if not (re.findall("delivery", product_url, re.IGNORECASE)):
                yield scrapy.Request(url=product_url, callback=self.parse_product)

    # This function parses data for a single product.
    def parse_product(self, response):
        meta = {}
        url = response.request.url
        external_id = response.css('.b-product_details-skn span::text').get()
        # brand = custom_page.css(".b-product_details-content  li::text").get()
        name = response.css('h1.b-product_details-name::text').get().strip()
        categories = []
        scrapped_categories = response.css("ol.b-breadcrumbs-list li a span::text").getall()
        extracted_categories = extract_categories_from(url)
        if extracted_categories:
            categories = find_actual_parent(scrapped_categories, extracted_categories)
        else:
            extracted_categories = extract_categories_from(name)
            if extracted_categories:
                categories = find_actual_parent(scrapped_categories, extracted_categories)
            else:
                extracted_categories = extract_categories_from(scrapped_categories)
                if extracted_categories:
                    categories = find_actual_parent(scrapped_categories, extracted_categories)

        price = self.convert_price(response.css("span.b-price-item::text").get().strip())
        sale_price = response.css("span.b-price-item.m-new::text").get()
        if sale_price:
            sale_price = sale_price.strip()
            meta["sale_price"] = self.convert_price(sale_price)

        colors = response.css("button.b-variation_swatch.m-swatch::attr('title')").getall()
        # Colors are with titles separated by colon, we will split on colon and get last value
        if colors:
            colors = [color.split(":")[-1].strip() for color in colors]

        # Meta Data about colors
        color_images = self.extract_image_url_from_style_tag(response.xpath("""//section[@class='b-variations_item m-swatch m-color']
                                                                            /div /div[@class='b-variations_item-content m-list' and
                                                                            @aria-label = 'Colour'] /button /span /span /@style""").getall())

        meta["color_images"] = color_images

        sizes = response.xpath("""//section[@class='b-variations_item m-swatch m-size']
                                    /div /div[@class='b-variations_item-content m-list' and @aria-label = 'Size']
                                    /button /span /span /text()""").getall()

        details = response.xpath('//meta[@property="og:description"] /@content').getall()
        details = [det for det in details if det is not ""]
        details_meta = self.clean_details(response.css("div.b-product_details-content *::text").getall())
        fabric = self.find_fabric_from_details(details_meta)
        fit = self.find_from_target_string_single(details_meta, FIT_KEYWORDS)
        neck_line = self.find_from_target_string_single(details_meta, NECK_LINE_KEYWORDS)
        length = self.find_from_target_string_multiple(details_meta, name, categories, LENGTH_KEYWORDS)
        gender = "women"
        number_of_reviews = ""
        review_description = []
        top_best_seller = ""
        occasions = self.find_from_target_multiple_list(details_meta, name, categories, OCCASIONS_KEYWORDS)
        style = self.find_from_target_multiple_list(details_meta, name, categories, STYLE_KEYWORDS)
        #aesthetics = self.find_from_target_string_multiple(details_meta, name, categories, AESTHETIC_KEYWORDS)
        self.driver.get(response.request.url)
        time.sleep(2)
        images = self.driver.find_elements(By.CSS_SELECTOR, "div.b-product_gallery-track div picture img")
        images = [image.get_attribute("src") for image in images]  # prepending all images with https:

        # Now Creating Item
        item = DorothyperkinsScrapperItem()
        item["url"] = url
        item["external_id"] = external_id
        item["categories"] = categories
        item["name"] = name
        item["price"] = price
        item["colors"] = colors
        item["sizes"] = sizes
        item["details"] = details
        item["fabric"] = fabric
        item["images"] = images
        item["fit"] = fit
        item["neck_line"] = neck_line
        item["length"] = length
        item["gender"] = gender
        item["number_of_reviews"] = number_of_reviews
        item["review_description"] = review_description
        item["top_best_seller"] = top_best_seller
        item["meta"] = meta
        item["occasions"] = occasions
        item["style"] = style
        item["website_name"] = WEBSITE_NAME
        # item["aesthetics"] = aesthetics
        if categories:
            yield item

    # Helpers

    def find_from_target_string_single(self, source_data, target_keywords):
        for each_element in source_data:
            if any(keyword.lower() in each_element.lower() for keyword in target_keywords):
                return each_element

        return ""

    def find_from_target_multiple_list(self, details, name, categories, target_keywords):
        target_list = details[:]
        target_list.extend(name)
        target_list.extend(categories)
        final_list = []

        for each_element in target_list:
            if any(keyword.lower() in each_element.lower() for keyword in target_keywords):
                final_list.append(each_element)

        return final_list

    def find_from_target_string_multiple(self, details, name, categories, target_keywords):
        target_list = details[:]
        target_list.extend(name)
        target_list.extend(categories)

        for element in target_list:
            if any(keyword.lower() in element.lower() for keyword in target_keywords):
                return element

        return ""

    # This helper finds fabric from details and returns it
        # This helper finds fabric from details and returns it
    def find_fabric_from_details(self, details):
        product_details = ' '.join(details)
        fabrics_founded = re.findall(r"""(\d+ ?%\s?)?(
            velvet\b|silk\b|satin\b|cotton\b|lace\b|
            sheer\b|organza\b|chiffon\b|spandex\b|polyester\b|
            poly\b|linen\b|nylon\b|viscose\b|Georgette\b|Ponte\b|
            smock\b|smocked\b|shirred\b|Rayon\b|Bamboo\b|Knit\b|Crepe\b|
            Leather\b|polyamide\b|Acrylic\b|Elastane\bTencel\bCashmere\b)\)?""", product_details,
                                     flags=re.IGNORECASE | re.MULTILINE)

        fabrics_founded = re.sub("\(|\)", "", ' '.join([''.join(tups) for tups in fabrics_founded]))
        already_founded = []
        if fabrics_founded:
            fabrics_founded = fabrics_founded.split(" ")
            for fabric in fabrics_founded:
                if not re.search(fabric, ' '.join(already_founded), re.IGNORECASE):
                    already_founded.append(fabric)

        return ' '.join(already_founded).strip() if already_founded else ""

    """
    this function returns upper limit of page, for example if we have total of 90 products with 20 products on each
    and page query is like 0 to 20, then 20 to 40 and so on, a time will come when we have 80 to 100 as a page query
    but products are only 90, so this function makes sure we have correct upper limit for pages query, in our case 80-90
    """

    def get_pages_upperlimit(self, current_page, total_pages):
        if (current_page + 80) > total_pages:
            return current_page + (total_pages - current_page)
        else:
            return current_page + 80

    """
    This is wrapper around strip function, it will remove trailing spaces
    iff str is not None
    """

    def remove_trailing_spaces(self, str):
        return str.strip() if str is not None else ""

    """
    As our product color is a image, so we need to parse style attribute from
    tag, style attribute include background image, so we need to extract only
    url of image in that case. this function helps us to do so
    """

    def extract_image_url_from_style_tag(self, colors):
        for i in range(len(colors)):
            colors[i] = "https:" + re.findall("'//.*'", colors[i])[0].replace("'", "")
        return colors

    # This function clean details

    def clean_details(self, details):
        details = [detail for detail in details if (detail is not "" and detail is not "\n")]
        return details

    def in_disallowed_links(self, link):
        for keyword in DISALLOWED_LINKS:
            if re.search(keyword, link, re.IGNORECASE):
                return True
        return False

    def convert_price(self, price):
        return "$" + str(
            round(self.currency_converter.convert(int(price.replace("£", "").split(".")[0]), 'GBP', 'USD')))

    def in_disallowed_keywords(self, url, name, categories):
        categories = ','.join(categories)
        for keyword in DISALLOWED_KEYWORDS:
            if re.search(keyword, url, re.IGNORECASE) or re.search(keyword, name, re.IGNORECASE) or \
                    re.search(keyword, categories, re.IGNORECASE):
                return True
        return False

    def remove_duplicates_using_regex(self, keywords_list):
        finals = []
        for keyword in keywords_list:
            if not re.search(keyword, ' '.join(finals), re.IGNORECASE):
                finals.append(keyword)

        return finals


# This function maps category we have extracted from name or url to taxonomy,
# and then it returns the list of extracted keywords.
def map_to_parents(cats):
    # where cats -> categories
    # cat -> category
    finals = []
    for cat in cats:
        for key in CATEGORY_TO_TYPE:
            if re.search(cat, ' '.join(CATEGORY_TO_TYPE[key]), re.IGNORECASE):
                finals.append(key)

    if not finals:
        for cat in cats:
            for key in CATEGORY_TO_STYLE:
                if re.search(cat, ' '.join(CATEGORY_TO_STYLE[key]), re.IGNORECASE):
                    finals.append(key)
    return list(set(finals))


# This function find real parent category from the list of extracted categories we provided
# Arguments: -> here first arg is scrapped categories and second is one which is list of extracted keywords
# we basically loop over scrapped categories and check if any category from scrapped one lies in extracted ones
def find_actual_parent(scrapped_cats, categories):
    finals = []
    final_categories = map_to_parents(categories)
    if len(final_categories) > 1:
        for fc in final_categories:
            if re.search(fc, ' '.join(scrapped_cats), re.IGNORECASE):
                finals.append(fc)

        if finals:
            return finals
        else:
            return []
    else:
        if final_categories:
            return final_categories
        else:
            return []


# This function extracts category keywords from product attribute passed as an argument to it
def extract_categories_from(keyword):
    cats = []  # categories
    if type(keyword) == list:
        keyword = ' '.join(keyword)

    for cat in CATEGORY_KEYWORDS:
        if re.search(cat, keyword, re.IGNORECASE):
            cats.append(cat)

    return cats
