# import random
# import json
# import torch
# import webbrowser
# import requests
# from bs4 import BeautifulSoup
# from model import NeuralNet
# from nltk_utils import tokenize, bag_of_words
# import re
# import csv


# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/intents.json'
# def load_data(file_path):
#     with open(file_path, 'r') as f:
#         intents = json.load(f)
#     return intents

# def load_products_from_csv(file_path):
#     products = []
#     with open(file_path, mode='r', encoding='utf-8') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             products.append(row)
#     return products
# def get_product_by_id(products, product_id):
#     for product in products:
#         if product['id'] == str(product_id):
#             return product
#     return None
# def compare_products(product_A, product_B):
#     if not product_A or not product_B:
#         return "One or both products not found."

#     criteria = ['price', 'rating', 'ratingTotal', 'discount']
#     scores = { 'A': 0, 'B': 0 }
#     comparison_result = f"Comparison Result:\n\n"
    
#     for criterion in criteria:
#         value_A = product_A.get(criterion, "N/A")
#         value_B = product_B.get(criterion, "N/A")
        
#         if value_A != "N/A" and value_B != "N/A":
#             if criterion in ['price', 'discount']:
#                 value_A = float(value_A)
#                 value_B = float(value_B)
#                 if value_A < value_B:
#                     scores['A'] += 1
#                 else:
#                     scores['B'] += 1
#             else:
#                 value_A = float(value_A)
#                 value_B = float(value_B)
#                 if value_A > value_B:
#                     scores['A'] += 1
#                 else:
#                     scores['B'] += 1

#         comparison_result += f"{criterion.capitalize()}:\n"
#         comparison_result += f"Product A: {value_A}\n"
#         comparison_result += f"Product B: {value_B}\n\n"
    
#     comparison_result += f"Product A URL: {product_A['purl']}\n"
#     comparison_result += f"Product B URL: {product_B['purl']}\n\n"
    
#     if scores['A'] > scores['B']:
#         better_product = 'Product A'
#     elif scores['B'] > scores['A']:
#         better_product = 'Product B'
#     else:
#         better_product = 'Neither, it\'s a tie'

#     comparison_result += f"Based on the criteria, {better_product} is better."
    
#     return comparison_result


# def load_model(file_path):
#     try:
#         data = torch.load(file_path)
#         input_size = data['input_size']
#         hidden_size = data['hidden_size']
#         output_size = data['output_size']
#         all_words = data['all_words']
#         tags = data['tags']
#         model_state = data['model_state']

#         model = NeuralNet(input_size, hidden_size, output_size).to(device)
#         model.load_state_dict(model_state)
#         model.eval()
#         print(f'Model loaded from {file_path}')
#         return model, all_words, tags

#     except Exception as e:
#         print(f'Error loading the model: {e}')
#         return None, None, None

# def get_response(sentence, model, all_words, tags, intents):
#     if isinstance(sentence, str):
#         processed_sentence = sentence
#     elif isinstance(sentence, list):
#         processed_sentence = ' '.join(sentence)
#     else:
#         return "I do not understand..."

#     sentence = tokenize(processed_sentence)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     with torch.no_grad():
#         output = model(X)
#         _, predicted = torch.max(output, dim=1)
#         tag = tags[predicted.item()]

#         probs = torch.softmax(output, dim=1)
#         prob = probs[0][predicted.item()]

#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent['tag']:
#                 response = random.choice(intent['responses'])

#                 if tag == "compare_products":
#                     response = compare_products_response(processed_sentence)  # Pass processed_sentence

#                 elif tag == "top_products":
#                     response = get_top_products()

#                 elif tag == "support_details":
#                     response = get_support_details()

#                 elif tag in ["men_section", "women_section", "footwear_section", "kids_section"]:
#                     get_section_info(tag)  # Call function to open section URL
#                     response = "Opening section..."

#                 return response
#     else:
#         return "I do not understand..."

# def compare_products_response(sentence):
#     products = extract_products(sentence)

#     if not products or len(products) < 2:
#         return "Please provide two valid product names or links to compare."

#     product_A = products[0]
#     product_B = products[1]

#     comparison_result = fetch_and_compare(product_A, product_B)

#     return comparison_result

# def fetch_and_compare(product_A, product_B):
#     product_A_data = fetch_product_data(product_A)
#     product_B_data = fetch_product_data(product_B)

#     if not product_A_data or not product_B_data:
#         return "Could not fetch data for comparison."

#     better_product = compare_products_data(product_A_data, product_B_data)

#     comparison_result = f"Comparing {product_A_data['url']} and {product_B_data['url']}. Based on price and sales, {better_product} is better."

#     return comparison_result

# def fetch_product_data(product_name_or_link):
#     if product_name_or_link.startswith("https://www.myntra.com/"):
#         product_url = product_name_or_link
#     else:
#         search_url = f"https://www.myntra.com/s/{product_name_or_link}"
#         product_url = fetch_product_url_from_search(search_url)

#     if not product_url:
#         return None

#     product_data = scrape_product_page(product_url)
#     return product_data

# def fetch_product_url_from_search(search_url):
#     try:
#         response = requests.get(search_url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         product_link = soup.find('a', {'class': 'product-productLink'}).get('href')
#         return f"https://www.myntra.com{product_link}"
#     except Exception as e:
#         print(f"Error fetching product URL: {e}")
#         return None

# def scrape_product_page(product_url):
#     try:
#         response = requests.get(product_url)
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         price_element = soup.find('span', {'class': 'pdp-price'})
#         price = float(price_element.text.strip().replace('₹', '').replace(',', ''))

#         product_data = {
#             'url': product_url,
#             'price': price,
#             # Add more details as needed
#         }

#         return product_data

#     except Exception as e:
#         print(f"Error scraping product page: {e}")
#         return None

# def extract_products(sentence):
#     urls = re.findall(r'(https?://\S+)', sentence)

#     if urls:
#         return urls
#     else:
#         product_urls = fetch_product_urls_from_myntra(sentence)
#         if product_urls:
#             return product_urls
#         else:
#             return [sentence]
# def fetch_product_urls_from_myntra(query):
#     try:
#         search_url = f"https://www.myntra.com/s/{query}"
#         response = requests.get(search_url)
#         print(response)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         product_links = soup.find_all('a', {'class': 'product-productLink'})
        
#         if product_links:
#             product_urls = [link.get('href') for link in product_links]
#             full_product_urls = [f"https://www.myntra.com{url}" for url in product_urls]
#             return full_product_urls[:2]  # Return up to 2 product URLs
#         else:
#             return []
#     except Exception as e:
#         print(f"Error fetching product URLs from Myntra: {e}")
#         return []

# def compare_products_data(product_A_data, product_B_data):
#     if product_A_data['price'] < product_B_data['price']:
#         return product_A_data['url']
#     else:
#         return product_B_data['url']

# def fetch_product_data(product_url):
#     try:
#         response = requests.get(product_url)
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Example: Extracting price and rating from Myntra page
#         price_element = soup.find('span', {'class': 'pdp-price'})
#         price = float(price_element.text.strip().replace('₹', '').replace(',', ''))

#         rating_element = soup.find('div', {'class': 'pdp-rating'})
#         rating = float(rating_element['data-rating'])

#         rating_total_element = soup.find('span', {'class': 'pdp-review-total'})
#         rating_total = int(rating_total_element.text.strip().replace('(', '').replace(')', ''))

#         discount_element = soup.find('span', {'class': 'pdp-discount'})
#         discount = float(discount_element.text.strip().replace('%', ''))

#         product_data = {
#             'url': product_url,
#             'price': price,
#             'rating': rating,
#             'ratingTotal': rating_total,
#             'discount': discount,
#             # Add more details as needed
#         }

#         return product_data

#     except Exception as e:
#         print(f"Error fetching product data: {e}")
#         return None

# def compare_products(product_A, product_B):
#     if not product_A or not product_B:
#         return "One or both products not found."

#     criteria = ['price', 'rating', 'ratingTotal', 'discount']
#     scores = { 'A': 0, 'B': 0 }
#     comparison_result = f"Comparison Result:\n\n"
    
#     for criterion in criteria:
#         value_A = product_A.get(criterion, "N/A")
#         value_B = product_B.get(criterion, "N/A")
        
#         if value_A != "N/A" and value_B != "N/A":
#             if criterion in ['price', 'discount']:
#                 value_A = float(value_A)
#                 value_B = float(value_B)
#                 if value_A < value_B:
#                     scores['A'] += 1
#                 else:
#                     scores['B'] += 1
#             else:
#                 value_A = float(value_A)
#                 value_B = float(value_B)
#                 if value_A > value_B:
#                     scores['A'] += 1
#                 else:
#                     scores['B'] += 1

#         comparison_result += f"{criterion.capitalize()}:\n"
#         comparison_result += f"Product A: {value_A}\n"
#         comparison_result += f"Product B: {value_B}\n\n"
    
#     comparison_result += f"Product A URL: {product_A['url']}\n"
#     comparison_result += f"Product B URL: {product_B['url']}\n\n"
    
#     if scores['A'] > scores['B']:
#         better_product = 'Product A'
#     elif scores['B'] > scores['A']:
#         better_product = 'Product B'
#     else:
#         better_product = 'Neither, it\'s a tie'

#     comparison_result += f"Based on the criteria, {better_product} is better."
    
#     return comparison_result

# def load_products_from_csv(file_path):
#     products = []
#     with open(file_path, mode='r', encoding='utf-8') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             products.append(row)
#     return products

# def get_product_by_id(products, product_id):
#     for product in products:
#         if product['id'] == str(product_id):
#             return product
#     return None

# def main():
#     file_path = 'products.csv'  # path to your CSV file
#     products = load_products_from_csv(file_path)

#     # Example product URLs to compare
#     product_A_url = 'https://www.myntra.com/product1'
#     product_B_url = 'https://www.myntra.com/product2'

#     product_A = fetch_product_data(product_A_url)
#     product_B = fetch_product_data(product_B_url)

#     if product_A and product_B:
#         result = compare_products(product_A, product_B)
#         print(result)
#     else:
#         print("Failed to fetch product data for comparison.")

# if __name__ == "__main__":
#     main()


# def get_top_products():
#     try:
#         url = "https://www.myntra.com/s/top-products"  
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         products = soup.find_all('li', class_='product-base')

#         response = "Here are the top products:\n"

#         for idx, product in enumerate(products[:3], start=1):  
#             product_name = product.find('h3', class_='product-title').text.strip()
#             product_price = product.find('span', class_='product-discountedPrice').text.strip()
#             product_rating = product.find('span', class_='product-rating').text.strip()

#             response += f"{idx}. {product_name} - Price: {product_price}, Rating: {product_rating}\n"

#         return response

#     except Exception as e:
#         print(f"Error fetching top products: {e}")
#         return "Sorry, I couldn't fetch the top products at the moment."

# def get_support_details():
#     support_details = {
#         "email": "support@myntra.com",
#         "phone": "+1-800-123-4567",
#         "hours": "Mon-Fri 9:00 AM to 5:00 PM (GMT)"
#     }

#     response = f"For support, contact us at:\n"
#     response += f"Email: {support_details['email']}\n"
#     response += f"Phone: {support_details['phone']}\n"
#     response += f"Hours: {support_details['hours']}\n"

#     return response

# def get_section_info(tag):
#     url = ""
#     if tag == "men_section":
#         url = "https://www.myntra.com/shop/men"
#     elif tag == "women_section":
#         url = "https://www.myntra.com/shop/women"
#     elif tag == "footwear_section":
#         url = "https://www.myntra.com/shop/footwear"
#     elif tag == "kids_section":
#         url = "https://www.myntra.com/shop/kids"

#     if url:
#         try:
#             webbrowser.open(url)
#         except Exception as e:
#             print(f"Error opening URL: {e}")

# if __name__ == "__main__":
#     file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/intents.json'  # Update with your actual file path
#     model_file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/data.pth'  # Update with your actual model file path

#     intents = load_data(file_path)
#     model, all_words, tags = load_model(model_file_path)

#     if model is None:
#         print('Cannot load the model. Exiting...')
#         exit()

#     print("Let's chat! Type 'quit' to exit.")
#     while True:
#         sentence = input("You: ")
#         if sentence.lower() == 'quit':
#             break

#         response = get_response(sentence, model, all_words, tags, intents)
#         print(f"Luno: {response}")
import random
import json
import torch
import webbrowser
import requests
from bs4 import BeautifulSoup
from model import NeuralNet
from nltk_utils import tokenize, bag_of_words
import re
import csv
import speech_recognition as sr

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

bot_name = "Luno"

def load_data(file_path):
    with open(file_path, 'r') as f:
        intents = json.load(f)
    return intents

def load_model(file_path):
    try:
        data = torch.load(file_path)
        input_size = data['input_size']
        hidden_size = data['hidden_size']
        output_size = data['output_size']
        all_words = data['all_words']
        tags = data['tags']
        model_state = data['model_state']

        model = NeuralNet(input_size, hidden_size, output_size).to(device)
        model.load_state_dict(model_state)
        model.eval()
        print(f'Model loaded from {file_path}')
        return model, all_words, tags

    except Exception as e:
        print(f'Error loading the model: {e}')
        return None, None, None

def get_response(sentence, model, all_words, tags, intents, products):
    if isinstance(sentence, str):
        processed_sentence = sentence
    elif isinstance(sentence, list):
        processed_sentence = ' '.join(sentence)
    else:
        return "I do not understand..."

    sentence = tokenize(processed_sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    with torch.no_grad():
        output = model(X)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                response = random.choice(intent['responses'])

                if tag == "compare_products":
                    response = compare_products_response(processed_sentence, products)

                elif tag == "top_products":
                    response = get_top_products()

                elif tag == "support_details":
                    response = get_support_details()

                elif tag in ["men_section", "women_section", "footwear_section", "kids_section"]:
                    response = get_section_info(tag)
                
                return response

    return "I do not understand..."

def compare_products_response(sentence, products):
    product_ids = extract_product_ids(sentence)
    if len(product_ids) != 2:
        return "Please provide two valid product IDs."

    product_A = get_product_by_id(products, product_ids[0])
    product_B = get_product_by_id(products, product_ids[1])

    if not product_A or not product_B:
        return "One or both products not found."

    comparison_result = compare_products(product_A, product_B)

    return comparison_result

def extract_product_ids(sentence):
    try:
        ids = re.findall(r'\b\d+\b', sentence)
        return [int(id) for id in ids]
    except:
        return []

def compare_products(product_A, product_B):
    criteria = ['price', 'rating', 'ratingTotal', 'discount']
    scores = {'A': 0, 'B': 0}
    comparison_result = f"Comparison Result:\n\n"

    for criterion in criteria:
        value_A = product_A.get(criterion, "N/A")
        value_B = product_B.get(criterion, "N/A")

        if value_A != "N/A" and value_B != "N/A":
            if criterion in ['price', 'discount']:
                value_A = float(value_A)
                value_B = float(value_B)
                if value_A < value_B:
                    scores['A'] += 1
                else:
                    scores['B'] += 1
            else:
                value_A = float(value_A)
                value_B = float(value_B)
                if value_A > value_B:
                    scores['A'] += 1
                else:
                    scores['B'] += 1

        comparison_result += f"{criterion.capitalize()}:\n"
        comparison_result += f"Product A: {value_A}\n"
        comparison_result += f"Product B: {value_B}\n\n"

    comparison_result += f"Product A URL: {product_A['purl']}\n"
    comparison_result += f"Product B URL: {product_B['purl']}\n\n"

    if scores['A'] > scores['B']:
        better_product = 'Product A'
    elif scores['B'] > scores['A']:
        better_product = 'Product B'
    else:
        better_product = 'Neither, it\'s a tie'

    comparison_result += f"Based on the criteria, {better_product} is better."

    return comparison_result

def load_products_from_csv(file_path):
    products = []
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            products.append(row)
    return products

def get_product_by_id(products, product_id):
    for product in products:
        if product['id'] == str(product_id):
            return product
    return None

def get_top_products():
    try:
        url = "https://www.myntra.com/s/top-products"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('li', class_='product-base')

        response = "Here are the top products:\n"

        for idx, product in enumerate(products[:3], start=1):
            product_name = product.find('h3', class_='product-title').text.strip()
            product_price = product.find('span', class_='product-discountedPrice').text.strip()
            product_rating = product.find('span', class_='product-rating').text.strip()

            response += f"{idx}. {product_name} - Price: {product_price}, Rating: {product_rating}\n"

        return response

    except Exception as e:
        print(f"Error fetching top products: {e}")
        return "Sorry, I couldn't fetch the top products at the moment."

def get_support_details():
    support_details = {
        "email": "support@myntra.com",
        "phone": "+1-800-123-4567",
        "hours": "Mon-Fri 9:00 AM to 5:00 PM (GMT)"
    }

    response = f"For support, contact us at:\n"
    response += f"Email: {support_details['email']}\n"
    response += f"Phone: {support_details['phone']}\n"
    response += f"Hours: {support_details['hours']}\n"

    return response

def get_section_info(tag):
    url = ""
    if tag == "men_section":
        url = "https://www.myntra.com/shop/men"
    elif tag == "women_section":
        url = "https://www.myntra.com/shop/women"
    elif tag == "footwear_section":
        url = "https://www.myntra.com/shop/footwear"
    elif tag == "kids_section":
        url = "https://www.myntra.com/shop/kids"

    if url:
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL: {e}")

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        sentence = recognizer.recognize_google(audio)
        print(f"You said: {sentence}")
        return sentence
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return ""

def main():
    intents_file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/intents.json'  # Update with your intents JSON file path
    model_file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/data.pth'  # Update with your model file path
    products_file_path = 'C:/Users/manya/OneDrive/Desktop/myntraweforshe/products.csv'  # Update with your products CSV file path

    intents = load_data(intents_file_path)
    model, all_words, tags = load_model(model_file_path)
    products = load_products_from_csv(products_file_path)

    if model is None:
        print('Cannot load the model. Exiting...')
        exit()

    print("Let's chat! Type 'quit' to exit.")
    while True:
        print("Do you want to type or speak? (type/speak)")
        input_mode = input("You: ").strip().lower()

        if input_mode == 'quit':
            break
        elif input_mode == 'speak':
            sentence = recognize_speech()
        else:
            sentence = input("You: ")

        if sentence.lower() == 'quit':
            break

        response = get_response(sentence, model, all_words, tags, intents, products)
        print(f"Luno: {response}")

if __name__ == "__main__":
    main()
