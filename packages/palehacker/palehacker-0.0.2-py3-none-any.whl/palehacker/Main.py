import requests

# --- #


def Get_HTTP():
    HTTP_Proxies = requests.get(
        "https://palehacker-api.cf/proxies/http").text.replace("<pre>", "").replace("</pre>", "")


def Get_HTTPS():
    HTTPS_Proxies = requests.get(
        "https://palehacker-api.cf/proxies/https").text.replace("<pre>", "").replace("</pre>", "")


def Get_Socks4():
    Socks4_Proxies = requests.get(
        "https://palehacker-api.cf/proxies/socks4").text.replace("<pre>", "").replace("</pre>", "")


def Get_Socks5():
    Socks5_Proxies = requests.get(
        "https://palehacker-api.cf/proxies/socks5").text.replace("<pre>", "").replace("</pre>", "")

# --- #
