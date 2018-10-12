import os

from scrapy.http import Request, TextResponse


def mock_response(file_name):
    """
    Create a Scrapy fake HTTP response from a HTML file
    Source: https://stackoverflow.com/a/12741030/
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    returns: A scrapy HTTP response which can be used for unittesting.
    """

    url_dict = {'billing.html': 'https://mya.dominionenergy.com/Usage/ViewPastUsage?statementType=2',
                'usage.html': 'https://mya.dominionenergy.com/Usage/ViewPastUsage?statementType=4'}
    url = url_dict[file_name]

    # return the proper scrapy Request type
    request = Request(url=url)

    # grab our saved HTML
    test_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(test_dir, 'fixtures', file_name )

    # open and return as a scrapy TextResponse
    file_content = open(file_path, 'r').read()

    return TextResponse(url=url,
                    request=request,
                    body=file_content)

