import random
import pyowm
import math
from pynytimes import NYTAPI

boto_answers = ["If you want to hear a joke tell me!", "If you want me to tell you an interesting animal fact, tell me that you love animals!", 'To change your sentence to pig latin write pig: "Your sentence"',
                "If you want to see the weather forecast near you tell me!", "If you want to see the top news headline tell me!", "I a mathematician, I can do fun stuff with numbers, write a number and see what happens. "]
animal_facts = ["The heart of a shrimp is located in its head.", "A snail can sleep for three years.", "Elephants are the only animal that can't jump.",
                "Nearly three percent of the ice in Antarctic glaciers is penguin urine.", " The fingerprints of a koala are so indistinguishable from humans that they have on occasion been confused at a crime scene."]
good_words = ["good", "great", "ok", "awesome", "fine"]
bad_words = ["bad", "terrible", "horrible", "not"]
jokes_list = ["What’s the difference between a good joke and a bad joke timing.", "Do I lose when the police officer says papers and I say scissors?",
"Moses had the first tablet that could connect to the cloud.", "The Journal of Medicine reports that 9 out of 10 doctors agree that 1 out of 10 doctors is an idiot.",
              "The first computer dates back to Adam and Eve. It was an Apple with limited memory, just one byte. And then everything crashed."]
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
    return sentence, "confused"


def facts():
    try:
        current_fact = animal_facts.pop(random.randint(0, len(animal_facts)-1))
        return current_fact, "dog"
    except ValueError:
        return "Sorry, those are all the facts I have...", "heartbroke"


def default_answers():
    try:
        current_answer = boto_answers.pop(random.randint(0, len(boto_answers)-1))
        return current_answer, "excited"
    except ValueError:
        return "Sorry, that's all I have for you, Ill see you in the future, when I am smarter and wiser!", "takeoff"


def jokes():
    try:
        current_joke = jokes_list.pop(random.randint(0, len(jokes_list) - 1))
        return current_joke, "laughing"
    except ValueError:
        return "Sorry, those are all the jokes I have...", "heartbroke"


def how_are_you_feeling(user_input):
    message_lower = user_input.lower()
    message_split = message_lower.split()
    if any((feeling_word in bad_words for feeling_word in message_split)):
        current_joke = jokes_list[random.randint(0, len(jokes_list) - 1)]
        return f"Oh no! Here's a joke to make you feel better: {current_joke}", "crying"
    elif any((feeling_word in good_words for feeling_word in message_split)):
        return "That's great! Since you're in a good mood, ask me to tell you a joke! ", "giggling"
    else:
        return "I didn't really understand how you are feeling, tell me in other words... I feel..", "no"


def get_weather():
    owm = pyowm.OWM("58c5556de8c1f81edc788997cd4ba27e")
    city = "Jaffa"
    loc = owm.weather_at_place(city)
    weather = loc.get_weather()
    status = weather.get_detailed_status()
    temp = weather.get_temperature("celsius")["temp"]
    return f"The temperature in Jaffa is {temp}° celsius and the status is: {status}", "ok"


def question():
    return "I know that you have a question but I am not very smart...", "bored"


def swear_words(user_input):
    if "fuck" in user_input:
        return "Hey! I can also be nasty! Fuck you!", "money"
    else:
        return "Whoah! Someone's got a filthy mouth... ", "afraid"


def math_operations(numbers_in_string):
    squared = [math.pow(i, 2) for i in numbers_in_string]
    square_root = [round(math.sqrt(i), 1) for i in numbers_in_string]
    sine = [round(math.sin(i), 1) for i in numbers_in_string]
    return f"Your number/s squared is{squared}, the square root is {square_root}, and the sine of your number is{sine}", "dancing"


def return_name(user_input):
    global username
    message_lower = user_input.lower()
    message_split = message_lower.split()
    if "name is" in user_input:
        try:
            is_index = message_split.index("is")
            firstname = message_split[is_index + 1]
            lastname = message_split[is_index + 2]
            return f"Hello {firstname} {lastname}, how are you feeling today?", "waiting"
        except IndexError:
            return (f"Hello {firstname}, how are you feeling today?", "waiting")
    elif len(message_split) <= 2:
        username = user_input
        return f"Hello {username}, how are you feeling today?", "ok"
    else:
        return "Hello how are you feeling?", "waiting"


def greeting():
    return "Hello nice to meet you, how are you feeling? ", "inlove"


def get_news():
    key = "aJDq9vqaMll0JjrRpRDRWwQnwQwPKtzZ"
    nyt = NYTAPI(key)
    top_stories = nyt.top_stories()
    return top_stories[random.randint(1, 11)]["title"], "excited"


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
        return jokes()
    if count == 2 or "i feel" in user_input_lower or "im feeling" in user_input_lower or "i am feeling" in user_input_lower:
        return how_are_you_feeling(user_input)
    if any((my_greeting in greeting_list for my_greeting in message_split)):
        return greeting()
    numbers_in_string = [int(s) for s in message_split if s.isdigit()]
    if numbers_in_string:
        return math_operations(numbers_in_string)
    if "news" in user_input_lower:
        return get_news()
    if "animal" in user_input_lower or "animals" in user_input_lower:
        return facts()
    return default_answers()









