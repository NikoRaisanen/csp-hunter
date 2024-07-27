import requests
import os
from pprint import pprint


def call_api(url: str):
    r = requests.get(url)
    print('Status:', r.status_code)
    
    # Check if the Content-Security-Policy header exists
    csp_header = r.headers.get('Content-Security-Policy')
    return csp_header

def parse_csp(csp: str):
    directives = csp.split(';')
    csp_dict = {}
    
    for directive in directives:
        if directive.strip():
            parts = directive.strip().split(' ')
            directive_name = parts[0]
            sources = parts[1:] if len(parts) > 1 else []
            csp_dict[directive_name] = sources

    return csp_dict


# TODO: some kind of in memory db could be cool to cache domain availability results for 24 hrs - 1 week
def domain_is_available(domain: str) -> bool:
    api_key = os.getenv('WHOIS_API_KEY')
    if not api_key:
        raise ValueError('Missing Whois api key')
    res = requests.get('https://api.whoapi.com', dict(
        domain=domain,
        r='taken',
        apikey=api_key))

    if res.status_code == 200:
        data = res.json()
        if int(data['status']) != 0:
            # api status codes https://whoapi.com/api-documentation/
            raise ValueError(f"Domain availability lookup failed with status {data['status']}")
        return True if data['taken'] == '0' else False
    else:
        raise Exception('Unexpected status code %d' % res.status_code)


if __name__ == '__main__':
    # csp = call_api('https://nikoraisanen.com')
    # if not csp:
    #     raise ValueError('No CSP to evaluate')
    # parsed_csp = parse_csp(csp)
    # print("Parsed Content-Security-Policy:")
    # pprint(parsed_csp)

    data = domain_is_available('nikoraisanen.com')
    print('Domain available ', data)