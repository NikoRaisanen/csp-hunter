import requests
import re
import regexes
from pprint import pprint


def call_api(url: str):
    r = requests.get(url)
    print("Status:", r.status_code)

    # Check if the Content-Security-Policy header exists
    csp_header = r.headers.get("Content-Security-Policy")
    return csp_header


def parse_csp(csp: str):
    directives = csp.split(";")
    csp_dict = {}

    for directive in directives:
        if directive.strip():
            parts = directive.strip().split(" ")
            directive_name = parts[0]
            sources = parts[1:] if len(parts) > 1 else []
            csp_dict[directive_name] = sources

    return csp_dict


if __name__ == "__main__":
    # res = regexes.is_virtual_hosted_s3_url('https://mybucket.s3.amazonaws.com/myfolder/myfile.txt')
    # print(res.groupdict())

    res = regexes.get_s3_match(
        "http://nikoraisanen.com.s3-website-us-west-1.amazonaws.com/"
    )
    print(res.groupdict())
    # text = [
    #     "https://mybucket.s3.amazonaws.com/myfolder/myfile.txt",
    #     "https://s3.us-west-2.amazonaws.com/mybucket/myfolder/myfile.txt",
    #     "https://my-access-point-123456789012.s3-accesspoint.us-east-1.amazonaws.com/myfolder/myfile.txt",
    #     "https://my-access-point-123456789012.s3-object-lambda.us-west-1.amazonaws.com/myfolder/myfile.txt",
    #     "http://mybucket.s3-website.us-east-1.amazonaws.com/myfolder/myfile.txt",
    #     "https://mycustomdomain.com/myfolder/myfile.txt"
    # ]
    # for txt in text:
    #     val = regexes.get_s3_match(txt)
    #     if val:
    #         print(f"{txt} -> {val.groupdict()}\n")
    # csp = call_api('https://floqast.app')
    # if not csp:
    #     raise ValueError('No CSP to evaluate')
    # parsed_csp = parse_csp(csp)
    # print("Parsed Content-Security-Policy:")
    # pprint(parsed_csp)
