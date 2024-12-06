from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

# Access the system
search_url = "https://www.amazon.com/s?k=pet+food&crid=1IZVVRSKGLN6U&sprefix=pet+food%2Caps%2C138&ref=nb_sb_noss_1"
driver.get(search_url)
time.sleep(60)

all_products = []

def grab_product_info():
    products = []
    try:
        product_elements = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item[data-asin]"))
        )
        for product in product_elements:
            try:
                # Access Product Name and Link
                name_element = product.find_element(By.CSS_SELECTOR, "h2 a.a-link-normal")
                name = name_element.text
                link = name_element.get_attribute("href")

                # Access Product Price
                try:
                    price_whole = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    price = f"${price_whole}.{price_fraction}"
                except:
                    price = "Price unavailable"

                driver.execute_script("window.open(arguments[0]);", link)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)

                # Access Product Rating
                try:
                    rating_element = driver.find_element(By.ID, "acrPopover")
                    rating = rating_element.get_attribute("title")
                except:
                    rating = "Rating unavailable"

                # Access Brand Information
                try:
                    brand_element = driver.find_element(By.XPATH,
                                                        "//tr[@class='a-spacing-small po-brand']//td[@class='a-span9']/span")
                    brand = brand_element.text
                except:
                    brand = "Brand unavailable"

                # Access Age Range
                try:
                    age_range_element = driver.find_element(By.XPATH,
                                                            "//tr[@class='a-spacing-small po-age_range_description']//td[@class='a-span9']/span")
                    age_range = age_range_element.text
                except:
                    age_range = "Age Range unavailable"

                # Access Ingredients
                try:
                    expand_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Ingredients')]")
                    expand_button.click()
                    time.sleep(3)

                    ingredients = driver.find_element(By.CSS_SELECTOR, "div#nic-ingredients-content").text
                except:
                    ingredients = "Ingredients unavailable"

                # Access Sales
                try:
                    sale_element = driver.find_element(By.CSS_SELECTOR, "span.social-proofing-faceout-title-text span")
                    sales = sale_element.text
                except:
                    sales = "Sales unavailable"

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Insert into the dictionary
                product_info = {
                    "Product": name,
                    "Price": price,
                    "Link": link,
                    "Rating": rating,
                    "Brand": brand,
                    "Age Range": age_range,
                    "Ingredients": ingredients,
                    "Sales": sales
                }
                products.append(product_info)

                print(f"Product: {product_info['Product']}")
                print(f"Price: {product_info['Price']}")
                print(f"Link: {product_info['Link']}")
                print(f"Rating: {product_info['Rating']}")
                print(f"Brand: {product_info['Brand']}")
                print(f"Age Range: {product_info['Age Range']}")
                print(f"Ingredients: {product_info['Ingredients']}")
                print(f"Sales: {product_info['Sales']}")
                print("-" * 40)

            except Exception as e:
                print(f"Failed to retrieve product details: {e}")
    except Exception as e:
        print(f"Product list not found: {e}")
    return products

# Iterate 6 pages (Amazon shows 6 pages for the maximum settings)
for page_num in range(6):
    print(f"\nGrabbing product information from page {page_num + 1}...\n")
    page_products = grab_product_info()
    all_products.extend(page_products)

    if page_num < 5:
        try:
            next_page_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//a[contains(@class, 's-pagination-next') and not(contains(@class, 's-pagination-disabled'))]"))
            )
            next_page_button.click()
            time.sleep(10)
        except Exception as e:
            print("Next page button not found or unable to click:", e)
            break

driver.quit()

# Test the dic
print("\nAll Products Information:")
for product in all_products:
    print(f"Product: {product['Product']}, Price: {product['Price']}, Link: {product['Link']}, "
          f"Rating: {product['Rating']}, Brand: {product['Brand']}, Age Range: {product['Age Range']}, "
          f"Ingredients: {product['Ingredients']}, Sales: {product['Sales']}")

# Output the csv file
output_path = 'amazon_pet_food.csv'
df = pd.DataFrame(all_products)
df.to_csv(output_path, index=False, encoding='utf-8')