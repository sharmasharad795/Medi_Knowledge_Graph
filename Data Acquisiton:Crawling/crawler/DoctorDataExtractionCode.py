import scrapy


class AllSpider(scrapy.Spider):
    name = 'doctors'
    download_delay = 0.3
    #start_urls=['https://www.healthgrades.com/specialty-directory']
    start_urls=['https://www.healthgrades.com/specialty-directory']
    
    
    def parse(self, response):
        
        for href in response.xpath('//*[@id="root"]//li[has-class("listArray__name")]/a/@href').getall():
            yield response.follow(href, callback=self.get_state)
   
    def get_state(self,response):
        state=response.xpath('//*[@id="root"]//div[has-class("city-w-providercount")]/a[contains(@href,"california")]/@href').get()
        if state=='' or state is None:
            state=response.xpath('//*[@id="root"]//div[has-class("seo-city-content__body")]/a[contains(@href,"california")]/@href').get()
        
        yield response.follow(state, callback=self.get_city)
        
    def get_city(self,response):
        city=response.xpath('//*[@id="root"]//div[has-class("city-w-providercount")]/a[contains(@href,"angeles")]/@href').get()
        if city=='' or city is None:
            city=response.xpath('//*[@id="root"]//div[has-class("seo-city-content__body")]/a[contains(@href,"angeles")]/@href').get()
        
        yield response.follow(city, callback=self.get_doc_page)
        
   
    def get_doc_page(self,response):
        for href in response.xpath('//*[@id="usearch-container"]//div/h3[has-class("provider-details__provider-name")]/a/@href').getall():
            yield response.follow(href, callback=self.get_doc_info)
    
    def get_doc_info(self, response):
        
        url=response.url
        name=response.xpath('//*[@id="summary-section"]//div[has-class("summary-column")]/h1/text()').get()
        gender=''.join(response.xpath('//*[@id="summary-section"]//div/span[@data-qa-target="ProviderDisplayGender"]/text()').getall()).strip()
        age=response.xpath('//*[@id="summary-section"]//div/span[@data-qa-target="ProviderDisplayAge"]/text()').getall()
        age=[x for x in age if x.isdigit()]
        age=''.join(age)
        address1=response.xpath('//*[@id="summary-section"]//div/p[has-class("location-practice")]/text()').get()
        address2=''.join(response.xpath('//*[@id="summary-section"]//div/address[has-class("location-row-address")]/text()').getall()).strip()
        if address1 is not None and address2 is not None:
            main_address=address1+': '+address2
        elif address1 is None and address2 is not None:
            main_address=address2
        elif address1 is not None and address2 is None:
            main_address=address1
        elif address1 is None and address2 is None:
            main_address=''
            
        phone_number=response.xpath('//*[@id="summary-section"]//div/a[has-class("hg-track toggle-phone-number-button")]/text()').get()
        score=response.xpath('//*[@id="premium-review-section"]//div/p[has-class("score")]/strong/text()').get()
        speciality=''.join(response.xpath('//*[@id="summary-section"]//div/span[@data-qa-target="ProviderDisplaySpeciality"]/text()').getall()).strip()
        
        if score is None:
            score='Not rated yet'

      
        scraped_info = {
                'DoctorURI':url,
                'Doctor_Name':name,
                'Doctor_Speciality':speciality,
                'Doctor_Age':age,
                'Doctor_Gender':gender,
               'Doctor_PhoneNo' : phone_number,
               'Doctor_Address' : main_address,
               'Doctor_Score' : score
           }
        
        yield scraped_info
    
   
            
    
            
            
            
            
            
            
            
            
            
            