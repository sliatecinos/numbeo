from lxml import html, etree
import scrapy


class NumbeoSpider(scrapy.Spider):
    name = "numbeo"
    rows_countries=0
    start_urls = []

    url1 = 'https://www.numbeo.com/cost-of-living/country_result.jsp?country='
    countries = ['Brazil'
        # 'Afghanistan', 'Aland+Islands', 'Albania', 'Algeria', 'Andorra', 'Angola', 
        # 'Antigua+And+Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 
        # 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 
        # 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire', 'Bosnia+And+Herzegovina', 
        # 'Botswana', 'Brazil', 'British+Virgin+Islands', 'Brunei', 'Bulgaria', 'Burkina+Faso', 
        # 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape+Verde', 'Cayman+Islands', 'Chile', 
        # 'China', 'Colombia', 'Congo', 'Costa+Rica', 'Croatia', 'Cuba', 'Curacao', 'Cyprus', 
        # 'Czech+Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican+Republic', 'Ecuador', 
        # 'Egypt', 'El+Salvador', 'Equatorial+Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faroe+Islands', 
        # 'Fiji', 'Finland', 'France', 'French+Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 
        # 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guam', 'Guatemala', 'Guernsey', 
        # 'Guyana', 'Haiti', 'Honduras', 'Hong+Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 
        # 'Iran', 'Iraq', 'Ireland', 'Isle+Of+Man', 'Israel', 'Italy', 'Ivory+Coast', 'Jamaica', 
        # 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kosovo+%28Disputed+Territory%29', 
        # 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 
        # 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 
        # 'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 
        # 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 
        # 'New+Caledonia', 'New+Zealand', 'Nicaragua', 'Nigeria', 'Northern+Mariana+Islands', 'Norway', 
        # 'Oman', 'Pakistan', 'Palestinian+Territory', 'Panama', 'Papua+New+Guinea', 'Paraguay', 'Peru', 
        # 'Philippines', 'Poland', 'Portugal', 'Puerto+Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 
        # 'Rwanda', 'Saint+Kitts+And+Nevis', 'Saint+Lucia', 'Saint+Vincent+And+The+Grenadines', 'Samoa', 
        # 'Saudi+Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Singapore', 'Sint+Maarten', 'Slovakia', 
        # 'Slovenia', 'Solomon+Islands', 'Somalia', 'South+Africa', 'South+Korea', 'Spain', 'Sri+Lanka', 
        # 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 
        # 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad+And+Tobago', 'Tunisia', 
        # 'Turkey', 'Turkmenistan', 'Turks+And+Caicos+Islands', 'Uganda', 'Ukraine', 'United+Arab+Emirates', 
        # 'United+Kingdom', 'United+States', 'Uruguay', 'Us+Virgin+Islands', 'Uzbekistan', 'Vanuatu', 
        # 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
    ]
    url2 = '&displayCurrency=USD'

    for country in countries:
        url = url1 + country + url2
        start_urls.append(url)


    # Get the extracted content (indices, measures and prices)
    def parse(self, response):
        countries = (response.url.split("=")[-2]).split("&")[0]
        self.log("***Country \"scraped\": %s***" % countries)

        table = response.css('table.data_wide_table.new_bar_table')   # tabela de dados
        linha = table.css('tr')
        broken_html = linha.extract()
        trs = [html.fromstring(i) for i in broken_html]
        categories = table.css('div.category_title::text').getall()

        h2 = response.css('h2')
        h2_text = h2[0].css('h2::text').getall()

        country = []
        country.append(countries)

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        #   Scrapy contributions data
        #   =========================[0]
        for tx_country in country:
            data = dict()
            bag=[]
            result=[]

            item = -1
            for tr in trs:
                for child in tr:
                    if child.tag=='td':
                        result.append(child.text_content())
                    else:
                        bag.append(child.tag)
                        bag_th = len(bag)
                        if bag_th > 2:
                            if item > -1:
                                result=list(chunks(result, bag_th))   # sized: 'th-list'
                                data[categories[item]].append(result)
                                result=[]
                            
                            bag=[]
                            item +=1   # seta 'id' da categoria
                            data[categories[item]]=[]    # inicializa categoria

            #   Contribution $1
            for k, v in data.items():
                for i, j in enumerate(v):
                    for g, h in enumerate(j):
                        for n in range(len(h)):
                            if n == 1:
                                data[k][i][g][1] = data[k][i][g][1].replace('$', "").replace('\u00a0', "").lstrip()
            
            rows = 0
            for k, v in enumerate(data):
                rows += 1
                self.rows_countries = self.rows_countries + 1
                scraped_info = {
                    '_rowcountry': self.rows_countries,
                    'country': tx_country,
                    '_rowdata': rows,
                    'measure': v,
                    'data': data[v],
                }
                yield scraped_info
