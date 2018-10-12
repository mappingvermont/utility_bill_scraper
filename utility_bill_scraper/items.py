# -*- coding: utf-8 -*-
import scrapy


class BillingItem(scrapy.Item):
    service_end_date = scrapy.Field()
    bill_amount = scrapy.Field()
    bill_due_date = scrapy.Field()


class UsageItem(scrapy.Item):
    service_end_date = scrapy.Field()
    bill_day_count = scrapy.Field()
    usage_kwh = scrapy.Field()
    service_start_date = scrapy.Field()

