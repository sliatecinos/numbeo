# Coleção de dados do site NUMBEO.COM
> Webscrapping básico usando `Scrapy` dos dados da site de comparação de custo de vida [Numbeo](https://numbeo.com/), com uso de Python.

___Projeto pessoal___ 
**@author**: sliatecinos

## Instalação das dependências usadas no scraping
Fazer a instalação via pip:

```bash
pip install -r requirements.txt
```

## Bloco de captura dos dados
```python
import scrapy 

# Get the extracted content (indices, measures and prices)
def parse(self, response):
    countries = (response.url.split("=")[-2]).split("&")[0]
    self.log("***Country \"scraped\": %s***" % countries)   # retorno da url sendo capturada

    table = response.css('table.data_wide_table.new_bar_table')   # tabela de dados
    linha = table.css('tr')
    broken_html = linha.extract()
    trs = [html.fromstring(i) for i in broken_html]
    categories = table.css('div.category_title::text').getall()

    h2 = response.css('h2')
    h2_text = h2[0].css('h2::text').getall()

    country = []
    country.append(countries)

    # """Yield successive n-sized chunks from lst."""
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

```

## Estrutura do projeto
    .
    ├── ...             
    ├── .pytest_cache             # Compiled files (alternatively `dist`)
    ├── .vscode                   # Compiled files (alternatively `dist`)
    ├── README.md                  
    └── numbeo                       # Source files (alternatively `py`)
        ├── __pycache__              # Compiled files (alternatively `dist`)
        └── spiders                  # Runner "spider" location
            └── __pycache__          # Compiled files (alternatively `dist`)

## Links externos
Site de Scrapy: [Numbeo - Cost of Living](https://www.numbeo.com/cost-of-living/)

Scrapy - official documentation: [DOCS](https://docs.scrapy.org/en/latest/index.html)