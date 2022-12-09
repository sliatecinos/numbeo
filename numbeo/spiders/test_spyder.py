import scrapy


class TestSpider(scrapy.Spider):
    """
    """

    name = 'test'

    def start_requests(self):
        urls = [
            'https://www.numbeo.com/costofliving/',
            'https://www.numbeo.com/property-investment/',
            'https://www.numbeo.com/crime/',
            'https://www.numbeo.com/health-care/',
            'https://www.numbeo.com/pollution/',
            'https://www.numbeo.com/traffic/',
            'https://www.numbeo.com/quality-of-life/',
            'https://www.numbeo.com/taxi-fare/',
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'numbeo-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
