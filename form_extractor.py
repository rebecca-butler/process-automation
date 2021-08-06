from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser

# initialize an HTTP session
session = HTMLSession()


def get_form(url):
    """Return all form tags found on web page"""
    res = session.get(url)
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """Return HTML details of form (action, method, inputs, selects"""
    details = {}

    # get the form action (requested URL)
    action = form.attrs.get("action").lower()

    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()

    # get all form inputs
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    # get all form selects
    selects = []
    for select_tag in form.find_all("select"):
        select_name = select_tag.attrs.get("name", "text")
        selects.append({"name": select_name})

    # put everything into dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    details["selects"] = selects
    return details


def main():
    url = "https://classes.uwaterloo.ca/under.html"

    # get the first form
    first_form = get_form(url)[0]

    # extract all form details
    form_details = get_form_details(first_form)
    pprint(form_details)

    # fill in data body we want to submit
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden" or input_tag["name"] == None:
            # if input is hidden or None, use the default value
            data[input_tag["name"]] = input_tag["value"]
        elif input_tag["type"] != "submit":
            # for all others except submit, prompt the user to set
            value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
            data[input_tag["name"]] = value
            print(f"'{input_tag['name']}' has been set to {value}")

    for select_tag in form_details["selects"]:
        value = input(f"Enter the value of the field '{select_tag['name']}': ")
        data[select_tag["name"]] = value
        print(f"'{select_tag['name']}' has been set to {value}")

    # join the url with the action (form request URL)
    url = urljoin(url, form_details["action"])

    if form_details["method"] == "post":
        res = session.post(url, data=data)
    elif form_details["method"] == "get":
        res = session.get(url, params=data)

    # replace relative URLs with absolute ones
    soup = BeautifulSoup(res.content, "html.parser")
    for link in soup.find_all("link"):
        try:
            link.attrs["href"] = urljoin(url, link.attrs["href"])
        except:
            pass
    for script in soup.find_all("script"):
        try:
            script.attrs["src"] = urljoin(url, script.attrs["src"])
        except:
            pass
    for img in soup.find_all("img"):
        try:
            img.attrs["src"] = urljoin(url, img.attrs["src"])
        except:
            pass
    for a in soup.find_all("a"):
        try:
            a.attrs["href"] = urljoin(url, a.attrs["href"])
        except:
            pass

    # write the page content to a file
    open("class_schedule.html", "w").write(str(soup))

    # open the page on the default browser
    webbrowser.open("class_schedule.html")


if __name__ == "__main__":
    main()