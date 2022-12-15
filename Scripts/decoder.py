import base64
import hashlib
import html
import urllib
import urllib.parse


class Encode:

    @staticmethod
    def url_encode(String):
        return urllib.parse.quote_plus(String)

    @staticmethod
    def base64_encode(String):
        String = String.Encode('utf-8')
        return base64.b64encode(String).decode('utf-8')

    @staticmethod
    def base32_encode(String):
        String = String.Encode('utf-8')
        return base64.b32encode(String).decode()

    @staticmethod
    def md5_encode(String):
        return hashlib.md5(String.Encode()).hexdigest()

    @staticmethod
    def sha1_encode(String):
        return hashlib.sha1(String.Encode()).hexdigest()

    @staticmethod
    def sha256_encode(String):
        return hashlib.sha256(String.Encode()).hexdigest()

    @staticmethod
    def sha512_encode(String):
        return hashlib.sha512(String.Encode()).hexdigest()

    @staticmethod
    def html_encode(String):
        return html.escape(String)


class Decode:
    @staticmethod
    def url_decode(String):
        return urllib.parse.unquote_plus(String)

    @staticmethod
    def base64_decode(String):
        String += '=' * (len(String) % 4)
        return base64.b64decode(String).decode()

    @staticmethod
    def base32_decode(String):
        return base64.b32decode(String).decode()

    @staticmethod
    def html_decode(String):
        return html.unescape(String)
