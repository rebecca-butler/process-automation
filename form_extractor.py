from bs4 import BeautifulSoup
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin
import webbrowser


def print_help():
    print(
    """Thank you for using the Class Schedule Checker!\n
    Please enter the subject, course number, section number, and term.\n
    For example, if you are intersted in section 3190 of ECON 101 for the 
    Fall 2021 semester, enter 'ECON', '101', '3190', and '1219'.\n""")


def get_form(url, session):
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


def get_enrolment_number(section_num):
    """Parse the HTML and print the number of empty seats in the section"""
    try:
        with open(("class_schedule.html"), "r") as f:
            # parse file
            f = f.read()
            table = etree.HTML(f).find("body/main/table/tr/td/table")
            rows = iter(table)
            headers = [col.text for col in next(rows)]

            for row in rows:
                values = [col.text for col in row]
                section_data = dict(zip(headers, values))

                # get info for given section number
                if section_data["Class"] == str(section_num):
                    cap = int(section_data["Enrl Cap"])
                    tot = int(section_data["Enrl Tot"])
                    empty_seats = cap - tot
                    print(f"Enrolment cap: {cap}")
                    print(f"Current enrolment: {tot}")
                    print(f"Seats available: {empty_seats}")
                    if (empty_seats > 0):
                        print("There is at least 1 seat available!")
                    else:
                        print("There are no seats available.")
    except Exception:
        print("Unable to parse html file")


def main():
    url = "https://classes.uwaterloo.ca/under.html"
    session = HTMLSession()

    # get the first form
    first_form = get_form(url, session)[0]

    # extract all form details
    form_details = get_form_details(first_form)

    # print help message and get user input
    print_help()
    subject = input(f"Enter the subject: ")
    course_num = input(f"Enter the course number: ")
    section_num = input(f"Enter the section number: ")
    term = input(f"Enter the term: ")


    # fill in data body we want to submit
    data = {}
    for input_tag in form_details["inputs"]:
        if input_tag["type"] == "hidden" or input_tag["name"] == None:
            # if input is hidden or None, use the default value
            data[input_tag["name"]] = input_tag["value"]
        elif input_tag["type"] != "submit":
            # set course number
            if (input_tag["name"] == "cournum"):
                data[input_tag["name"]] = course_num

    for select_tag in form_details["selects"]:
        if (select_tag["name"] == "sess"):
            data[select_tag["name"]] = term
        elif (select_tag["name"] == "subject"):
            data[select_tag["name"]] = subject

    # join the url with the action (form request URL)
    url = urljoin(url, form_details["action"])

    if form_details["method"] == "post":
        res = session.post(url, data=data)
    elif form_details["method"] == "get":
        res = session.get(url, params=data)

    # write the page content to a file
    soup = BeautifulSoup(res.content, "html.parser")
    open("class_schedule.html", "w").write(str(soup))

    # open the page on the default browser
    open_webpage = input(f"Do you want to open the webpage? yes/no: ")
    if open_webpage == "yes":
        webbrowser.open("class_schedule.html")

    # parse the file to determine number of seats available
    get_enrolment_number(section_num)


if __name__ == "__main__":
    main()