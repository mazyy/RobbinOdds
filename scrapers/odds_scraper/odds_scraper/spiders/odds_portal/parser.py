import json
import re
from base64 import b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Constants for decryption
CRYPTO_PASSWORD = "%RtR8AB&nWsh=AQC+v!=pgAe@dSQG3kQ"
CRYPTO_SALT = "orieC_jQQWRmhkPvR6u2kzXeTube6aYupiOddsPortal"

MATCH_EVENT_REACT_HEADER_COMPONENT_XPATH = '//*[@id="react-event-header"]/@data'
PAGE_VAR_XPATH = '//script[contains(text(), "var pageVar")]/text()'

#new key and old key event headers
EVENT_HEADERS_KEYS_DICT = {
    "match_id" : "id",
    "xhash" : "xhash",
    "xhashf" : "xhashf",
    "is_live" : "isLive",
    "real_live" : "realLive",
    "is_postponed" : "isPostponed",
    "is_started" : "isStarted",
    "is_finished" : "isFinished",
    "is_finished_grace_period" : "isFinishedGracePeriod",
    "sport_id" : "sportId",
    "sport_name" : "sportName",
    "sport_url" : "sportUrl",
    "home" : "home",
    "away" : "away",
    "tournament_id" : "tournamentId", 
    "tournament_name" : "tournamentName",
    "tournament_url" : "tournamentUrl",
    "country_name" : "countryName",
    "default_bet_id" : "defaultBetId",
    "user_bett_id" : "userBettId",
    "user_id" : "userId",
    "default_scope_id" : "defaultScopeId",
    "version_id" : "versionId"
}

#new key and old key event body
EVENT_BODY_KEYS_DICT = {
    "start_date" : "startDate",
    "end_date" : "endDate",
    "home_result" : "homeResult",
    "away_result" : "awayResult",
    "partial_result" : "partialresult",
    "event_stage_name" : "eventStageName",
    "event_stage_id" : "eventStageId",
    "ft_only" : "ftOnly",
    "ft_only_text" : "ftOnlyText",
    "ft_only_text_short" : "ftOnlyTextShort",
    "venue" : "venue",
    "venue_town" : "venueTown",
    "venue_country" : "venueCountry",
    "additional_odds_info" : "additionalOddsInfo",
    "providers_names" : "providersNames",
    "providers_is_betting_exchange" : "providersIsBettingExchange",
    "request_pre_match" : "requestPreMatch",
    "request_base_pre_match" : "requestBasePreMatch",
    "update_score_request" : "updateScoreRequest",
    "updatescore_request_base" : "updateScoreRequestBase",
    "request_match_facts" : "requestMatchFacts",
    "request_event_data" : "requestEventData",
    "request_last_results" : "requestLastResults",
    "request_betting_exchanges" : "requestBettingExchanges"
}

#new key and old key page var
PAGE_VAR_KEYS_DICT = {
    "default_betting_type" : "betting_type_id",
    "default_scope" : "scope_id",
    "nav" : "navigation",
    "nav_filtered" : "filtered_navigation"
}

def load_json_str(dict_str):
    if dict_str:
        try:
            # Try to parse as JSON for prettier formatting
            data_json = json.loads(dict_str)
            return data_json
        except Exception as e:
            # If parsing fails, save as raw text
            print(f"Failed to parse JSON data: {e}")

def add_json_value_to_itemloader(itemloader, json_data, keymaps=None):
    if keymaps:
        for k, v in keymaps.items():
            if v in json_data:
                json_data[k] = json_data.pop(v)

    item_fields = list(itemloader.item.fields.keys())
    for k, v in json_data.items():
        if k in item_fields:
            itemloader.add_value(k, v)
    return itemloader

def extract_pagevar_data(response, page_var_xpath):
    # Try to find pageVar in script tags
    pagevar_script = response.xpath(page_var_xpath).get()
    pagevar_data = {}
    
    if pagevar_script:
        # Try different patterns to extract the data
        patterns = [
            r'var\s+pageVar\s*=\s*\'(.*?)\'\s*;',  # Single quotes
            r'var\s+pageVar\s*=\s*"(.*?)"\s*;',    # Double quotes
            r'var\s+pageVar\s*=\s*(\{.*?\})\s*;'   # Direct JSON
        ]
        
        for pattern in patterns:
            match = re.search(pattern, pagevar_script, re.DOTALL)
            if match:
                pagevar_str = match.group(1)
                pagevar_data = load_json_str(pagevar_str)
    else:
        print("No pageVar script found")
    
    # Extract structured data from pageVar
    extracted = {}
    if pagevar_data:
        extracted = {
            'default_settings': {
                'betting_type_id': pagevar_data.get('defaultBettingType'),
                'scope_id': pagevar_data.get('defaultScope')
            },
            'navigation': pagevar_data.get('nav', {}),
            'filtered_navigation': pagevar_data.get('navFiltered', {})
        }
    return extracted

def decrypt_data_PBKDF2HMAC(encrypted_data):
    # First base64 decode
    decoded = b64decode(encrypted_data).decode('utf-8')
    
    # Split on colon
    parts = decoded.split(':')
    if len(parts) != 2:
        print("Invalid format after base64 decode")
        return None
    
    encrypted_b64 = parts[0]
    iv_hex = parts[1]
    
    # Convert IV from hex to bytes
    iv = bytes.fromhex(iv_hex)
    
    # Convert encrypted data from base64 to bytes
    encrypted_bytes = b64decode(encrypted_b64)
    
    # Derive key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits for AES-256
        salt=CRYPTO_SALT.encode('utf-8'),
        iterations=1000,
    )
    key = kdf.derive(CRYPTO_PASSWORD.encode('utf-8'))
    
    # Decrypt using AES-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
    
    # Remove PKCS7 padding
    padding_length = decrypted_padded[-1]
    decrypted_data = decrypted_padded[:-padding_length]
    
    # Decode to text
    plaintext = decrypted_data.decode('utf-8')
    
    # Parse JSON
    return json.loads(plaintext)
