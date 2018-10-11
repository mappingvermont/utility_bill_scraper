import os

from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

from utility_bill_scraper.items import BillingItem, UsageItem


class Bill(InitSpider):
    name = 'bill'

    def __init__(self):
        self.base_url = 'https://mya.dominionenergy.com/Usage/ViewPastUsage'

        # start out by scraping this URL, which will kick us to the login page first
        self.start_urls = [self.base_url + '?statementType=2']

    def parse(self, response):
        # this is the default callback for any start_urls

        # we'll get back the login page and respond with the proper creds
        # which will go to the original statementType=2 page we requested
        return FormRequest.from_response(
            response,
            formdata=self.load_creds(),
            callback=self.after_login
        )

    def after_login(self, response):

        # check login succeeded before going on
        if "incorrect user name" in response.body:
            self.logger.error("Login failed")
            return

        # if we get valid data back, parse table
        else:
            for row in response.xpath('//table[@id="billingAndPaymentsTable"]//tbody//tr')[1:]:
                yield self.parse_billing_statement(row)

        # once logged in, make a request for statementType=4
        yield Request(self.base_url + '?statementType=4', self.parse_usage_statement)

    def parse_billing_statement(self, row):
        return BillingItem({
            'meter_read_date': self.get_table_text(row, 1),
            'bill_amount': self.get_table_text(row, 2),
            'bill_due_date': self.get_table_text(row, 3)
              })

    def parse_usage_statement(self, response):
        for row in response.xpath('//table[@id="paymentsTable"]//tbody//tr')[1:]:
            yield UsageItem({
                'meter_read_date': self.get_table_text(row, 1),
                'usage_kwh': self.get_table_text(row, 5),
                  })

    def get_table_text(self, row, idx):
        return row.xpath('td[{}]//text()'.format(idx)).extract_first().strip()

    def load_creds(self):

        username = os.environ.get('BILL_USERNAME')
        password = os.environ.get('BILL_PASSWORD')

        if not username or not password:
            raise ValueError('Credentials not found - check environment variables')

        return {'USER': username, 'PASSWORD': password}

