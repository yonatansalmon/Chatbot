import random
import pyowm
import math
from pynytimes import NYTAPI

boto_answers = ["If you want to hear a joke tell me!","To talk about your feelings tell me how you feel", "To change your sentence to pig latin write pig: 'Your sentence'", "If you want to get see the weather near you tell me!", "If you want to see the top news headline tell me!"]
animal_facts = ["The heart of a shrimp is located in its head.", "A snail can sleep for three years.", "Elephants are the only animal that can't jump.", "Nearly three percent of the ice in Antarctic glaciers is penguin urine.", " The fingerprints of a koala are so indistinguishable from humans that they have on occasion been confused at a crime scene."]
good_words = ["good", "great", "ok", "awesome", "fine"]
bad_words = ["bad", "terrible", "horrible", "not good"]
jokes_list = ['If vegetarians eat vegetables, what do humanitarians eat?', 'If tin whistles are made of tin, what are fog horns made of?',
'Why do we park our car in the driveway and drive our car on the parkway?', 'I used to be a werewoolf... But I m much better noooooooooooow !']
swear_word_list = ['fuck', 'bastard', 'ass', 'asshole', 'bitch', "shit", "idiot"]
greeting_list = ["hi", "hello", "whats up", "hey", "howdy"]
count = 0
username = ""


def pig_latin(user_input):
    sentence = user_input.split()
    sentence_slice = sentence[1:]
    for i in range(len(sentence_slice)):
        if sentence_slice[i][0] in "aeiou":
            sentence_slice[i] += 'yay'
        else:
            sentence_slice[i] = sentence_slice[i][1:] + sentence_slice[i][0]
            sentence_slice[i] += 'ay'
    sentence = ' '.join(sentence_slice)

    return sentence, "inlove"


def default_answers():
    try:
        current_answer = boto_answers.pop()
        return current_answer, "inlove"
    except IndexError:
        return "Sorry, thats all I have for you.. Have a nice day!", "inlove"



def jokes():
    current_joke = jokes_list[random.randint(0, len(jokes_list) - 1)]
    return "Here is a joke to make you laugh a bit: " + current_joke

def how_are_you_feeling(user_input):
    message_lower = user_input.lower()
    message_split = message_lower.split()
    if any((feeling_word in good_words for feeling_word in message_split)):
        return "That's great my man"
    elif any((feeling_word in bad_words for feeling_word in message_split)):
        return jokes()
    else:
        return "I didn't really understand how you are feeling"

def get_weather():
    owm = pyowm.OWM("58c5556de8c1f81edc788997cd4ba27e")
    city = "Jaffa"
    loc = owm.weather_at_place(city)
    weather = loc.get_weather()
    status = weather.get_detailed_status()
    temp = weather.get_temperature("celsius")["temp"]
    return f"The temperature in Jaffa is {temp}° celsius and the status is: {status}", "inlove"

def question():
    return "I know that you have a question but you should google it instead...", "inlove"

def swear_words(user_input):
    if "fuck" in user_input:
        return "fuck you", 'inlove'
    else:
        return "Please don't say that!", 'inlove'

def number_trick(numbers_in_string):
    double = [i * 2 for i in numbers_in_string]
    square_root = [math.sqrt(i) for i in numbers_in_string]
    return f"The double of your number is {double} and the square root is {square_root}", "inlove"


def return_name(user_input):
    global username
    message_lower = user_input.lower()
    message_split = message_lower.split()
    if "name is" in user_input:
        myindex = message_split.index("is")
        username = message_split[myindex + 1]
        return f'Hello {username}, if asfasfasfasfas ', 'inlove'
    elif len(message_split) <= 2:
        username = user_input
        return f'Hello {username}, if yasfafafsaf', 'inlove'
    else:
        return 'Hello {username}, if youasfasf', 'inlove'



def greeting():
    return "Hello nice to meet you, whats up? ", 'inlove'

def get_news():
    key = "aJDq9vqaMll0JjrRpRDRWwQnwQwPKtzZ"
    nyt = NYTAPI(key)
    top_stories = nyt.top_stories()
    return top_stories[0]["title"], "inlove"


def main_function(user_input):
    global count
    count += 1
    user_input_lower = user_input.lower()
    message_split = user_input_lower.split()

    if any((s_word in swear_word_list for s_word in message_split)):
        return swear_words(user_input)
    if "pig" in user_input_lower:
        return pig_latin(user_input)
    if "weather" in user_input_lower or "temperature" in user_input_lower or "temp" in user_input_lower:
        return get_weather()
    if count == 1 or "name is" in user_input:
        return return_name(user_input)
    if user_input_lower.endswith("?"):
        return question()
    if "joke" in user_input_lower or "bored" in user_input_lower:
        return jokes(), "inlove"
    if "i feel" in user_input_lower or "im feeling" in user_input_lower or "i am feeling" in user_input_lower:
        return how_are_you_feeling(user_input), "inlove"
    if any((my_greeting in greeting_list for my_greeting in message_split)):
        return greeting()
    numbers_in_string = [int(s) for s in message_split if s.isdigit()]
    if numbers_in_string:
        return number_trick(numbers_in_string)
    if "news" in user_input_lower:
        return get_news()

    return default_answers()









