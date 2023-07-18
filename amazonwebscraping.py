# from bs4 import BeautifulSoup
# import requests

# def search_and_check(value):
#     # Set the URL for the search endpoint
#     search_url = "https://www.amazon.com/s"

#     # Set the query parameters
#     params = {
#         "k": value,
#         "ref": "nb_sb_noss"
#     }

#     # Construct the URL
#     url = search_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
#     print("Search URL:", url)

#     HEADERS = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
#         'Accept-Language': 'en-US, en;q=0.5'
#     }

#     webpage = requests.get(url=url, headers=HEADERS)
#     HTML = BeautifulSoup(webpage.content, 'html.parser')

#     # Get the result element
#     result_element = HTML.select_one('.a-size-medium-plus.a-color-base')

#     if result_element:
#         result = result_element.text
#         if "Results" in result:
#             return 1
#         elif "Need help?" in result:
#             return 0
#     return None

# # Take user input
# user_input = input("Enter a value: ")

# # Call the search_and_check function with the user input
# search_result = search_and_check(user_input)
# print(search_result)


from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_and_check():
    number = request.args.get('number')

    # Set the URL for the search endpoint
    search_url = "https://www.amazon.com/s"

    # Set the query parameters
    params = {
        "k": number,
        "ref": "nb_sb_noss"
    }

    # Construct the URL
    url = search_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

    # Fetch the HTML content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(url, headers=headers)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get the result element
    result_element = soup.select_one('.a-size-medium-plus.a-color-base')
    result_text = result_element.text if result_element else ''

    # Check the result and return the response
    if 'Results' in result_text:
        return jsonify({'result': 1})
    elif 'Need help?' in result_text:
        return jsonify({'result': 0})
    else:
        return jsonify({'result': None})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
