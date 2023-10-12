from app import logger
from app.database.postgres.run_query import run_query
import requests

def find_nakies():
    logger.info('Starting to find naked domains...')
    query_name = "get_naked_domains"
    result = run_query(query_name)

    logger.debug('SQL result: %s', result)

    if result:
        try:
            domain_id, domain = result[0]
        except IndexError:
            logger.error('No rows were returned from the SQL query.')
            return False  # No data to process

        home_url = get_home_url(domain)
        record_home_url(domain_id, home_url)

        if home_url != "BADDIE":
            upsert_url(domain_id, home_url)

        if home_url == "BADDIE":
            logger.debug(f'We got a BADDIE for %s', domain)
        else:
            logger.debug(f'%s\'s home url is: %s', domain, home_url)

        return True  # There is data to process

    else:
        logger.info('No naked domains found.')
        return False  # No data to process


def get_home_url(domain):
    logger.debug(f'Getting home url for %s', domain)

    try:
        response = requests.get(f'http://{domain}', timeout=5, allow_redirects=True)

        if response.status_code == 200:
            return response.url
        else:
            return "BADDIE"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while getting home URL for {domain}: {str(e)}")
        return "BADDIE"

def record_home_url(domain_id, home_url):
    logger.debug('Fixing home_url for domain_id: %s', domain_id)
    query_name = "clothe_domains"
    variables = {"domain_id": domain_id, "home_url": home_url}
    result = run_query(query_name, variables)

def upsert_url(domain_id, home_url):
    logger.debug('Upserting url for domain_id: %s', domain_id)
    query_name = "upsert_url"
    variables = {"domain_id": domain_id, "home_url": home_url}
    result = run_query(query_name, variables)
