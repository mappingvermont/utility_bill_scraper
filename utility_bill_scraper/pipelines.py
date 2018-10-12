# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from prettytable import PrettyTable
from scrapy.exceptions import DropItem

from utility_bill_scraper.items import BillingItem, UsageItem


class UtilityBillScraperPipeline(object):

    def __init__(self):
        self.service_end_dict = {}

    def process_item(self, item, spider):

        # Drop extraneous rows, eg just have date of payment or totals
        if [x for x in item.values() if not x]:
            raise DropItem('Missing info for item: {}'.format(item))

        # calculate service start date
        if isinstance(item, UsageItem):
            bill_day_count = int(item['bill_day_count'])
            service_end_date = datetime.strptime(item['service_end_date'], '%m/%d/%Y')

            # add service_start_date to this item
            item['service_start_date'] = service_end_date - timedelta(days=bill_day_count)
            del item['bill_day_count']
            
        # add the item to our {'service_end_date: {properties}} dict
        self.add_to_dict(item)

        return item

    def close_spider(self, spider):
        # build list of rows and sort
        bill_list = []

        x = PrettyTable()
        x.field_names = ['Service Start Date', 'Service End Date', 'Bill Amount',
                         'Usage (kWh)', 'Bill Due Date']

        for service_end_date, d in self.service_end_dict.iteritems():
            x.add_row([d['service_start_date'], service_end_date,
                      d['bill_amount'], d['usage_kwh'], d['bill_due_date']])

        x.sortby = 'Service Start Date'
        print x

    def add_to_dict(self, item):
        # store in our output dict

        # grab our key and then delete it from the item
        date_key = item.get('service_end_date')
        del item['service_end_date']

        # if our date key already exists, add the new properties from this item
        if date_key in self.service_end_dict:
            for k, v in item.iteritems():
                self.service_end_dict[date_key][k] = v

        # if it doesn't exist yet, copy our item dict and set it as the value for our date_key
        else:
            self.service_end_dict[date_key] = dict(item.items())

