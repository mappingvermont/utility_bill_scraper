import unittest
from utility_bill_scraper.spiders import bill_spider

from fake_response_from_file import mock_response


class BillSpiderTest(unittest.TestCase):

    def setUp(self):
         self.spider = bill_spider.Bill()

    def unpack_results(self, results):
        return [x for x in results]

    def test_billing_parse(self):

        # parse billing page
        raw_results = self.spider.after_login(mock_response('billing.html'))
        results = self.unpack_results(raw_results)

        # check that table has the correct number of rows
        self.assertEqual(len(results), 32)

        # check second row
        second_row =  {'bill_amount': '$122.17',
                      'bill_due_date': '10/16/2018',
                      'service_end_date': '09/21/2018'}
        self.assertEqual(results[1], second_row)

        
    def test_usage_parse(self):

        # parse usage page
        raw_results = self.spider.parse_usage_statement(mock_response('usage.html'))
        results = self.unpack_results(raw_results)

        # check that table has the correct number of rows
        self.assertEqual(len(results), 13)

        # check first row
        first_row = {'bill_day_count': u'30',
                     'service_end_date': u'09/21/2018',
                     'usage_kwh': u'990'}

        self.assertEqual(results[0], first_row)

