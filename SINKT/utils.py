import unicodedata
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from enum import Enum
from langchain.chat_models import init_chat_model, BaseChatModel

def normalize_id(s: str) -> str:
    """Standardizes IDs to match between Relations and Questions"""
    if not s: return ""
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(char for char in s if not unicodedata.combining(char))
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'[^\w_]', '', s)
    return s.lower()

def normalize_filename(s: str) -> str:
    """
    Remove accents, replace underscores and remove non-alphanumeric characters.
    
    :param s: String to be normalized
    """
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(char for char in s if not unicodedata.combining(char))
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'[^\w_]', '', s)
    return s.lower()

def prettify_xml(elem: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.
    Strips the annoying extra newlines minidom likes to add.
    
    :param elem: Element (``ET.Element``)
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Filter out lines that are purely whitespace
    return '\n'.join([line for line in reparsed.toprettyxml(indent="   ").split('\n') if line.strip()])

class Models(str, Enum):
    GPT4_o = "openai:gpt-4o"
    GPT5_1 = "openai:gpt-5.1"
    CLAUDE4_5 = "anthropic:claude-opus-4-5"

def get_llm(model_name: Models) -> BaseChatModel:
    return init_chat_model(model_name.value)


