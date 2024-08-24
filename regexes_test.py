import pytest
from regexes import (
    get_s3_match,
    is_virtual_hosted_s3_url,
    is_path_style_s3_url,
    is_access_point_s3_url,
    is_website_s3_url,
)

# Assume the following functions are imported from your module
# from your_module import is_virtual_hosted_s3_url, is_path_style_s3_url, is_access_point_s3_url, get_s3_match


def test_virtual_hosted_s3_url():
    """Test cases for virtual-hosted-style S3 URLs."""
    valid_urls = [
        (
            "https://mybucket.s3.amazonaws.com/myfolder/myfile.txt",
            "mybucket",
            "myfolder/myfile.txt",
            None,
        ),
        (
            "https://another.bucket-name.s3.us-west-2.amazonaws.com/somefile.jpg",
            "another.bucket-name",
            "somefile.jpg",
            "us-west-2",
        ),
    ]
    for url, expected_bucket, expected_key, expected_region in valid_urls:
        match = is_virtual_hosted_s3_url(url)
        assert match is not None, f"URL should match: {url}"
        assert (
            match.group("bucket") == expected_bucket
        ), f"Expected bucket '{expected_bucket}', got '{match.group('bucket')}'"
        assert (
            match.group("key") == expected_key
        ), f"Expected key '{expected_key}', got '{match.group('key')}'"
        assert (
            match.group("region") == expected_region
        ), f"Expected region '{expected_region}', got '{match.group('region')}'"

    invalid_urls = [
        "https://s3.amazonaws.com/mybucket/myfile.txt",  # Path-style
        "https://mycustomdomain.com/myfile.txt",  # Custom domain
    ]
    for url in invalid_urls:
        match = is_virtual_hosted_s3_url(url)
        assert match is None, f"URL should not match: {url}"


def test_path_style_s3_url():
    """Test cases for path-style S3 URLs."""
    valid_urls = [
        (
            "https://s3.us-west-2.amazonaws.com/mybucket/myfolder/myfile.txt",
            "mybucket",
            "myfolder/myfile.txt",
            "us-west-2",
        ),
        (
            "https://s3.eu-central-1.amazonaws.com/another.bucket-name/somefile.jpg",
            "another.bucket-name",
            "somefile.jpg",
            "eu-central-1",
        ),
    ]
    for url, expected_bucket, expected_key, expected_region in valid_urls:
        match = is_path_style_s3_url(url)
        assert match is not None
        assert match.group("bucket") == expected_bucket
        assert match.group("key") == expected_key
        assert match.group("region") == expected_region

    invalid_urls = [
        "https://mybucket.s3.amazonaws.com/myfile.txt",  # Virtual-hosted-style
        "https://mycustomdomain.com/myfile.txt",  # Custom domain
    ]
    for url in invalid_urls:
        match = is_path_style_s3_url(url)
        assert match is None


def test_access_point_s3_url():
    """Test cases for S3 Access Point and Object Lambda URLs."""
    valid_urls = [
        (
            "https://my-access-point-123456789012.s3-accesspoint.us-east-1.amazonaws.com/myfolder/myfile.txt",
            "my-access-point",
            "123456789012",
            "myfolder/myfile.txt",
        ),
        (
            "https://other-access-point-123456789012.s3-object-lambda.us-west-1.amazonaws.com/somefile.jpg",
            "other-access-point",
            "123456789012",
            "somefile.jpg",
        ),
    ]
    for url, expected_access_point, expected_account_id, expected_key in valid_urls:
        match = is_access_point_s3_url(url)
        assert match is not None
        assert match.group("access_point") == expected_access_point
        assert match.group("account_id") == expected_account_id
        assert match.group("key") == expected_key

    invalid_urls = [
        "https://mybucket.s3.amazonaws.com/myfile.txt",  # Virtual-hosted-style
        "https://s3.amazonaws.com/mybucket/myfile.txt",  # Path-style
    ]
    for url in invalid_urls:
        match = is_access_point_s3_url(url)
        assert match is None


def test_website_s3_url():
    """Test cases for S3 Website Endpoint URLs."""
    valid_urls = [
        (
            "http://nikoraisanen.com.s3-website-us-west-1.amazonaws.com/",
            "nikoraisanen.com",
            "us-west-1",
        ),
        (
            "http://example-bucket.s3-website-eu-central-1.amazonaws.com/",
            "example-bucket",
            "eu-central-1",
        ),
    ]
    for url, expected_bucket, expected_region in valid_urls:
        match = is_website_s3_url(url)
        assert match is not None, f"URL should match: {url}"
        assert (
            match.group("bucket") == expected_bucket
        ), f"Expected bucket '{expected_bucket}', got '{match.group('bucket')}'"
        assert (
            match.group("region") == expected_region
        ), f"Expected region '{expected_region}', got '{match.group('region')}'"

    invalid_urls = [
        "https://s3.amazonaws.com/mybucket/myfile.txt",  # Path-style
        "https://mybucket.s3.amazonaws.com/myfile.txt",  # Virtual-hosted-style
        "https://mycustomdomain.com/myfile.txt",  # Custom domain
    ]
    for url in invalid_urls:
        match = is_website_s3_url(url)
        assert match is None, f"URL should not match: {url}"


def test_get_s3_match():
    """Test the general S3 URL matcher that delegates to specific match functions."""
    test_cases = [
        (
            "https://mybucket.s3.amazonaws.com/myfolder/myfile.txt",
            {"bucket": "mybucket", "key": "myfolder/myfile.txt"},
        ),
        (
            "https://s3.us-west-2.amazonaws.com/mybucket/myfolder/myfile.txt",
            {"bucket": "mybucket", "key": "myfolder/myfile.txt"},
        ),
        (
            "https://my-access-point-123456789012.s3-accesspoint.us-east-1.amazonaws.com/myfolder/myfile.txt",
            {
                "access_point": "my-access-point",
                "account_id": "123456789012",
                "key": "myfolder/myfile.txt",
            },
        ),
        (
            "http://nikoraisanen.com.s3-website-us-west-1.amazonaws.com/",
            {"bucket": "nikoraisanen.com", "region": "us-west-1"},
        ),
        ("https://non-s3.url.com/myfile.txt", None),  # Not an S3 URL
    ]
    for url, expected_result in test_cases:
        match = get_s3_match(url)
        if expected_result:
            assert match is not None
            assert all(match.group(k) == v for k, v in expected_result.items())
        else:
            assert match is None


# If you want to run the tests directly with pytest
if __name__ == "__main__":
    pytest.main()
