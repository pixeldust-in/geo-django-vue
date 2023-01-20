from django.contrib.sites.models import Site


def build_domain_url(path=None):
    url = f"https://{Site.objects.get_current().domain}"
    if not path:
        return f"{url}/"
    return f"{url}{path}"


def mask_str(string, skip_count=3, mask_char="*"):
    return string[-skip_count:].rjust(len(string), mask_char)
