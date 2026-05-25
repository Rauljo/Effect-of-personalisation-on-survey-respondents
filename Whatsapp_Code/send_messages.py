#Uses selenium in Whatsapp web to send messages to a list of contacts in a csv file. Uses different types of messages and languages depending on the contact. Creates a new csv file with the time at which the message was sent. 
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# --------------------
# Chrome configuration
# --------------------
options = Options()
options.add_argument("--window-size=960,1080")
options.add_argument("--window-position=0,0")
options.add_argument("user-data-dir=/home/rauls/chrome-whatsapp-profile")
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --------------------
# Messages dictionaries
# --------------------
links = {
    "Spanish": "https://docs.google.com/forms/d/e/1FAIpQLSffk5jw0yHtL44rNxRjKUmqVzE4ejdWTgCXSdqTb9I5Tfp6PQ/viewform?usp=pp_url&entry.322075881={codigo}",
    "Turkish": "https://docs.google.com/forms/d/e/1FAIpQLSeUN6ozmgxKIBkvGHvC1rIOTZCGqzQCuGu210N-2bDKDG4GsQ/viewform?usp=pp_url&entry.1980778738={codigo}",
    "English": "https://docs.google.com/forms/d/e/1FAIpQLSevzZ_5NYdHkyo6HdBdMEtw0UG6xhaYR11NRNpW4NYc9jDfJQ/viewform?usp=pp_url&entry.1355964674={codigo}"
}


messages_by_language_without_customisation = {
    "Spanish": "Hola, estoy recopilando datos para un proyecto de mi Máster. Necesito gente para rellenar un pequeño formulario, no debería llevar mas de un minuto. ¿Te importaría rellenarlo en el siguiente enlace? \n {link}",
    "English": "Hi, I am currently collecting data for an MSc project and I am looking for participants to fill out a google forms. It takes less than 1 minute. Could you please fill it out at this link? \n {link}",
    "Turkish": "Selam, şu anda yüksek lisans projem için veri topluyorum ve Google Form'u dolduracak katılımcılar arıyorum. 1 dakikadan az sürüyor. Lütfen bu bağlantıdan formu doldurabilir misin? \n {link}"
}

messages_by_language_personalized = {
    "English": "Hey {nombre}. Quick favor—I'm working on my MSc project right now and I really need your help gathering some data. I want to understand how certain habits change depending on nationality and culture, and I really need a diverse range of people to make the results meaningful. The form is super short (literally less than a minute). Would you be able to help me out? Thanks! \n\n Here's the link: {link}",
    "Spanish": "Hola {nombre}. Te puedo pedir un favor?? Estoy trabajando en un proyecto para el Máster y necesitaría tu ayuda para conseguir datos. Quiero estudiar cómo distintos hábitos cambian dependiendo de la nacionalidad y la cultura, y necesito una gran diversidad de gente para obtener resultados significativos. El formulario es súper corto (literal menos de un minuto) Te importaría rellenarlo? Gracias! \n\n Aquí tienes el enlace: {link}",
    "Turkish": "Selam {nombre}. Küçük bir ricam olacak — şu anda yüksek lisans projem için veri topluyorum ve gerçekten yardımına ihtiyacım var. Farklı milletler ve kültürler arasında bazı günlük alışkanlıkların nasıl değiştiğini anlamaya çalışıyorum; bu yüzden farklı kişilerden yanıt almak benim için çok önemli. Form çok kısa (gerçekten 1 dakikadan bile kısa). Müsaitsen bu formu doldurabilir misin? Şimdiden çok teşekkür ederim! \n\n İşte bağlantı: {link}"
}

def open_chat_by_number(number):
    """
    Search for and open a chat using the telephone number.
    """
    time.sleep(1)
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    time.sleep(0.1)
    search_box.click()
    time.sleep(0.1)

    # Clear bar
    search_box.send_keys(Keys.CONTROL + "a")
    time.sleep(0.1)
    search_box.send_keys(Keys.BACKSPACE)
    time.sleep(0.1)

    # Write number
    search_box.send_keys(number)
    time.sleep(1)

    # Select the first result in the list
    try:
        first_result = driver.find_element(By.XPATH, '(//div[contains(@class,"_ak8j")])[1]')
        first_result.click()
        time.sleep(0.5)
        return True
    except:
        print(f"❌ No chat was found for number: {number}")
        return False

# --------------------
# Open WhatsApp Web
# --------------------
driver.get("https://web.whatsapp.com")
print("Open WhatsApp Web and scan the QR code if needed. Waiting for 20 seconds...")
time.sleep(20)

# --------------------
# Read CSV and send messages
# --------------------
with open('Friends_list.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader, 1):
        number = row['Number']
        name = row.get('Name', 'friend')
        language = row["Language"].strip()
        message_type = row.get("MessageType", "Basic").strip()  # Basico por defecto

        # Elegir mensaje según tipo
        if message_type == "Personalised":
            mensaje_base = messages_by_language_personalized[language]
            mensaje = mensaje_base.format(nombre=name, link=links[language].format(codigo=row['codigo']))
        else:
            mensaje = messages_by_language_without_customisation[language]
            mensaje = mensaje.format(link=links[language].format(codigo=row['codigo']))

        if open_chat_by_number(number):
            try:
                message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                message_box.click()
                time.sleep(0.2)
                message_box.send_keys(mensaje)
                time.sleep(0.2)
                message_box.send_keys(Keys.ENTER)
                print(f"[{i}] Mensaje ({message_type}) enviado a {name} ({number}) en {language}")

                # create new csv with code and time sent
                with open('sent_messages.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Number', 'Name', 'codigo', 'MessageType', 'TimeSent']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    writer.writerow({
                        'Number': number,
                        'Name': name,
                        'code': row['code'],
                        'MessageType': message_type,
                        'TimeSent': time.strftime("%Y-%m-%d %H:%M:%S")
                    })

                time.sleep(1)
            except Exception as e:
                print(f"[{i}] ERROR al enviar mensaje a {name} ({number}): {e}")

print("✔ All messages have been processed. Please check 'sent_messages.csv' for details.")
input("Press Enter to close the browser...")
driver.quit()
