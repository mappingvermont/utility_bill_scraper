import os

from scrapy.spiders.init import InitSpider
from scrapy.http import FormRequest

class Bill(InitSpider):
    name = 'bill'
    start_urls = ['https://mya.dominionenergy.com/Usage/ViewPastUsage']

    def parse(self, response):

        username = os.environ.get('BILL_USERNAME')
        password = os.environ.get('BILL_PASSWORD')

        if not username or not password:
            raise ValueError('Credentials not found - check environment variables')

        return FormRequest.from_response(
            response,
            formdata={'USER': username, 'PASSWORD': password},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "incorrect user name" in response.body:
            self.logger.error("Login failed")
            return

        else:
            for row in response.xpath('//table[@id="billingAndPaymentsTable"]//tbody//tr')[1:]:
                yield {
                    'meter_read_date': self.get_table_text(row, 1),
                    'bill_amount': self.get_table_text(row, 2),
                    'bill_due_date': self.get_table_text(row, 3)
                      }

    def get_table_text(self, row, idx):
        return row.xpath('td[{}]//text()'.format(idx)).extract_first().strip()

