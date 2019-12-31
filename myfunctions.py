swear_word_list = ['fuck', 'bastard', 'ass', 'asshole', 'bitch', "shit"]
greeting_list = ["hi", "hello", "whats up", "howdy"]
count = 0
username = ""


def greeting(message):
    return "Hello"


def swear_words(message):
    if "fuck" in message:
        return "fuck you"
    else:
        return "Please don't say that!"


def return_name(message):
    global username
    message_lower = message.lower()
    message_split = message_lower.split()
    if "name is" in message:
        myindex = message_split.index("is")
        username = message_split[myindex + 1]
        return f"Hello {username} "
    elif len(message_split) <= 2:
        username = message
        return f"Hello {username} "


def main_function(message):
    global count
    count += 1
    message_lower = message.lower()
    message_split = message_lower.split()
    if any((my_greeting in greeting_list for my_greeting in message_split)):
        return greeting(message)
    if any((s_word in swear_word_list for s_word in message_split)):
        return swear_words(message)
    if count == 1:
        return return_name(message)

    return message









