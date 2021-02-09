from bs4 import BeautifulSoup
import urllib3
import json
import pprint
from selenium import webdriver

#   consts
FILE_PATH = "fonts.json"
PAGE = "https://coolsymbol.com/cool-fancy-text-generator.html"
ALPHABETS = {
    "nums": [0,1,2,3,4,5,6,7,8,9],
    "ru": [
        "А","а","Б","б","В","в","Г","г","Д","д","Е","е",
        "Ё","ё","Ж","ж","З","з","И","и","Й","й","К","к",
        "Л","л","М","м","Н","н","О","о","П","п","Р","р",
        "С","с","Т","т","У","у","Ф","ф","Х","х","Ц","ц",
        "Ч","ч","Ш","ш","Щ","щ","Ъ","ъ","Ы","ы","Ь","ь",
        "Э","э","Ю","ю","Я","я"],
    "eng": [
        "A","a","B","b","C","c","D","d","E","e","F","f",
        "G","g","H","h","I","i","J","j","K","k","L","l",
        "M","m","N","n","O","o","P","p","Q","q","R","r",
        "S","s","T","t","U","u","V","v","W","w","X","x",
        "Y","y","Z","z"],
    "rutoeng": [
        "A","a","B","b","V","v","G","g","D","d","E","e",
        "Yo","yo","Zh","zh","Z","z","I","i","Y","y","K",
        "k","L","l","M","m","N","n","O","o","P","p","R",
        "r","S","s","T","t","U","u","F","f","Kh","kh","Ts",
        "ts","Ch","ch","Sh","sh","Shch","shch","","","Y","y",
        "'","'","E","e","Yu","yu","Ya","Ya"]
}
#   Сюда вставьте нужные id инпутов с https://coolsymbol.com/cool-fancy-text-generator.html
FAVOUTIRE_FONTS = [
    "manga","fantasy","currency",
    "fancySymbols","square",
    "rusify","h4k3r","fancyStyle19","cloudy"
]

#   update json file
def json_update():
    with open(FILE_PATH, 'w') as json_file:
        json.dump(data, json_file)
#   get char
def get_char(font_char,input_char,font_id):
    inputbox.clear()
    inputbox.send_keys(input_char)
    data["fonts"][font_id]["characters"][font_char] = driver.find_element_by_id(FAVOUTIRE_FONTS[i]).get_attribute("value")

    
#   MAIN
#   load json data
file = open(FILE_PATH)
data = {"fonts":[]}
#   set driver & set input field
driver = webdriver.Firefox()
driver.get(PAGE)
inputbox = driver.find_element_by_id("converting_text")

for i in range(len(FAVOUTIRE_FONTS)):
    data["fonts"].append({"title":f"{FAVOUTIRE_FONTS[i].capitalize()} font","characters":{}})
    for char in ALPHABETS["nums"]:
        get_char(char,char,i)
    for char in ALPHABETS["eng"]:
        get_char(char,char,i)
    for char_i in range(len(ALPHABETS["ru"])):
        get_char(ALPHABETS["ru"][char_i],ALPHABETS["rutoeng"][char_i],i)


driver.quit()
json_update()