# utility_bill_scraper

An example project to sign in to your utility account and scrape a few different data tables. Uses `scrapy` to parse the pages, then pushes both tables through a pipeline to join valid rows. Current output is a CLI table.

### Installation and credentials
- [Install docker](https://docs.docker.com/install/)
- [Install docker-compose](https://docs.docker.com/compose/install/)
- Copy the .env.sample to .env and populate the credentials
 
### Run the tests
- Build the service locally: `docker-compose build`
- Test: `docker-compose run test`

### Print the table
To scrape the utility company pages and print the table, execute `docker-compose run scrape`

### Develop
- To start and `ssh` in to the docker container, run `docker-compose run base`
- To mimic the `scrape` service run `scrapy crawl bill`
- This will print the table and all associated logging info. To develop, edit the code and re-run the crawl command

### Future work
- Additional tests - pipeline, login/authentication
- Identify commonalites with other utilty bill workflows - make a generic spider to inherit from
- Pass args to filter start/end date
- Actually parse the dollar and date text to allow for summary values


