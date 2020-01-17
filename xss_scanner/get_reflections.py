import random
import string
import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from xss_scanner.get_reflection_context import detect_context

url_with_reflected_params = set()

def get_reflections(url):
    parsed_url = urlparse(url)
    parsed_qs = parse_qs(parsed_url.query)
    url_without_qs = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    reflections = check_reflections(url, url_without_qs, dict(parsed_qs))
    if reflections:
        url_with_reflected_params.add(url)
        return reflections

def check_reflections(url, url_without_qs, params):
    modified_params = dict()
    exist_reflected_param = False
    for k, v in params.items():
        modified_params[k] = random_string()
    
    r = requests.get(url=url_without_qs, params=modified_params, timeout=5)
    forms = get_all_forms(r.content)
    reflected_forms = check_reflection_form(forms, random_string(), url)
    reflections = []
    for k, v in modified_params.items():
        if v in r.text:
            exist_reflected_param = True
            ori_param = k + "=" + params.get(k)[0].replace(" ", "+")
            url = url.replace(ori_param, k + "=*")
            reflection = {
                "url" : url,
                "param" : k,
                "context" : detect_context(v,r.content)
            }
        reflections.append(reflection)

    for x in reflected_forms:
        reflection = {
                "url" : url,
                "form_details" : x
            }

        reflections.append(reflection)

    return reflections

def get_reflection_context():
    pass

def random_string(stringLength=15):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_all_forms(content):
    soup = BeautifulSoup(content, "lxml")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def check_reflection_form(forms, random_string, url):
    forms_vulnerables = []
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, random_string).content.decode()
        if random_string in content:
            context = detect_context(random_string, content)
            form_details['context'] = context
            forms_vulnerables.append(form_details)

    return forms_vulnerables