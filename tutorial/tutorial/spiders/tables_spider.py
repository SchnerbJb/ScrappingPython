import scrapy

class TableScraper(scrapy.Spider):
    name = "tables"

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }

    start_urls = [
        'https://www.autocentrum.pl/dane-techniczne/',
    ]

    def parse_table(self, response):
        
        name = response.xpath('//div[@class="name"]/text()').get()
        url_split = response.request.url.split('/')
        right_values = response.xpath('//span[@class="dt-param-value"]/text()').getall()
        right_values = [r_v.replace(u'\xa0', u' ') for r_v in right_values]
        print(right_values)
        car = {
            'name': name.strip(),
            'brand': url_split[-4],
            'model': url_split[-3],
            'version': url_split[-2],
            'nbDoor': right_values[0],
            'nbSeats': right_values[1],
            'turningCircle': right_values[2],
            'turningRadius': right_values[3],
            'length': right_values[4],
            'width': right_values[5],
            'widthWSideMirror': right_values[6],
            'height': right_values[7],
            'wheelbase': right_values[8],
            'wheelTrackFront': right_values[9],
            'trackWidthRear': right_values[10],
            'Clearance': right_values[11],
            'luggageCapacity': right_values[12],
            'luggageMin': right_values[13],
        }
        yield car

    def parse_version(self, response):
        names = response.xpath('//a/h2[@class="name-of-the-car"]/text()').getall()
        links = []
        for name in names:
            link = response.request.url + name.split('(')[0].lower().strip().replace(" ", "-")
            links.append(response.urljoin(link))
        namesNLinks = list(zip(names, links))
        for (name, link) in namesNLinks:
            print("_____________________________________________")
            print("Name : \t\t", name, "\t\t", "link : ", response.urljoin(link), "\n")
            yield scrapy.Request(url=link, callback=self.parse_table)
            # break

    def parse_model(self, response):
        names = response.xpath('//a/h2[@class="name-of-the-car"]/text()').getall()
        links = []
        for name in names:
            link = response.request.url + name.lower().strip().replace(" ", "-")
            links.append(response.urljoin(link))
        namesNLinks = list(zip(names, links))
        for (name, link) in namesNLinks:
            print("_____________________________________________")
            print("Name : \t\t", name, "\t\t", "link : ", response.urljoin(link), "\n")
            yield scrapy.Request(url=link, callback=self.parse_version)
            # break


    def parse(self, response):
        
        # models = response.xpath('//div[@class="flex-row"]')
        # for model in models:
        names = response.xpath('//a/span[@class="name"]/text()').getall()
        links = response.xpath('//a[@class="make"]/@href').getall()
        namesNLinks = list(zip(names, links))
        for (name, link) in namesNLinks:
            print("Name : \t\t", name, "\t\t", "link : ", response.urljoin(link), "\n")
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_model)
            # break