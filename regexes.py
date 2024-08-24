import re

def is_virtual_hosted_s3_url(url: str):
    """Check if the URL matches the virtual-hosted-style S3 URL."""
    virtual_hosted_pattern = re.compile(r"""
        https?://                                  # Match HTTP or HTTPS scheme
        (?P<bucket>[a-zA-Z0-9.\-_]+)                # Capture the bucket name
        \.s3(\.)?(?P<region>[a-zA-Z0-9-]+)?\.amazonaws\.com/     # Match the S3 service URL part with optional region
        (?P<key>[^?\s]+)                            # Capture the key (object path)
    """, re.VERBOSE)
    
    return virtual_hosted_pattern.search(url)

def is_path_style_s3_url(url: str):
    """Check if the URL matches the path-style S3 URL."""
    path_style_pattern = re.compile(r"""
        https?://                                  # Match HTTP or HTTPS scheme
        s3\.(?P<region>[a-zA-Z0-9-]+)\.amazonaws\.com/          # S3 service URL part
        (?P<bucket>[a-zA-Z0-9.\-_]+)/               # Capture the bucket name
        (?P<key>[^?\s]+)                            # Capture the key (object path)
    """, re.VERBOSE)
    
    return path_style_pattern.search(url)

def is_access_point_s3_url(url: str):
    """Check if the URL matches the S3 Access Point or Object Lambda URL."""
    access_point_pattern = re.compile(r"""
        https?://                                  # Match HTTP or HTTPS scheme
        (?P<access_point>[a-zA-Z0-9-]+)             # Capture the access point name
        -(?P<account_id>\d{12})                     # Capture the account ID
        \.s3-(?:accesspoint|object-lambda)          # Match access point or object lambda
        (?:\.[a-zA-Z0-9-]+)?\.amazonaws\.com/       # S3 service URL part
        (?P<key>[^?\s]+)                            # Capture the key (object path)
    """, re.VERBOSE)
    
    return access_point_pattern.search(url)

def is_website_s3_url(url: str):
    """Check if the URL matches the S3 Website Endpoint URL."""
    website_pattern = re.compile(r"""
        https?://                                  # Match HTTP or HTTPS scheme
        (?P<bucket>[a-zA-Z0-9.\-_]+)                # Capture the bucket name
        \.s3-website-(?P<region>[a-zA-Z0-9-]+)      # Match 's3-website-<region>' part
        \.amazonaws\.com/?$                         # Match end of the URL
    """, re.VERBOSE)
    
    return website_pattern.search(url)


def get_s3_match(url):
    match = is_virtual_hosted_s3_url(url)
    if match: return match
    match = is_path_style_s3_url(url)
    if match: return match
    match = is_access_point_s3_url(url)
    if match: return match
    match = is_website_s3_url(url)
    return match
