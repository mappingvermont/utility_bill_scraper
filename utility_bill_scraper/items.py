# -*- coding: utf-8 -*-
import scrapy


class BillingItem(scrapy.Item):
    bill_due_date = scrapy.Field()
    bill_amount = scrapy.Field()
    meter_read_date = scrapy.Field()


class UsageItem(scrapy.Item):
    meter_read_date = scrapy.Field()
    usage_kwh = scrapy.Field()

