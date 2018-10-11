# -*- coding: utf-8 -*-
# lets us dump decimals to JSON for debugging purposes
import simplejson as json
from decimal import Decimal

from scrapy.exceptions import DropItem

from utility_bill_scraper.items import BillingItem, UsageItem


class UtilityBillScraperPipeline(object):

    def __init__(self):
        self.meter_read_dict = {}

    def process_item(self, item, spider):

        # convert to decimal so bill amounts are easier to work with
        if isinstance(item, BillingItem):
            item['bill_amount'] = Decimal(item['bill_amount'].lstrip('$').replace(',',''))

        # Drop extraneous rows in the BillingItem table, eg just have date of payment 
        if [x for x in item.values() if not x]:
            raise DropItem('Missing info for item: {}'.format(item))

        else:
            # add the item to our {'meter_read_date: {properties}} dict
            self.add_to_dict(item)

        return item

    def close_spider(self, spider):
        # will ultimately print a table here
        print json.dumps(self.meter_read_dict)

    def add_to_dict(self, item):
        # store in our output dict

        # grab our key and then delete it from the item
        date_key = item.get('meter_read_date')
        del item['meter_read_date']

        # if our date key already exists, add the new properties from this item
        if date_key in self.meter_read_dict:
            for k, v in item.iteritems():
                self.meter_read_dict[date_key][k] = v

        # if it doesn't exist yet, copy our item dict and set it as the value for our date_key
        else:
            self.meter_read_dict[date_key] = dict(item.items())

