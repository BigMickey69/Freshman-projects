from random import choice, randint




def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    #raise NotImplementedError("Can't find code QQ")

    if lowered == "hello" or lowered == "hi" or lowered == "hello!" or lowered == "hi!":
        return "Greetings, how may I be of service?"
    elif lowered == "are you online?" or lowered == "are you online":
        return "Yes I am! I am current online and ready to be at your service. :) "
    elif lowered == "self introduction":
        return 'Hello, I am José the butler. I am a Bot created by 石維廉 in charge of encrypting, decrypting, storing splitting and overall management of all files on "Discord Clouding!'
    elif lowered == "roll a dice" or lowered == "roll dice":
        return f"Sure, You rolled a {randint(1,6)}!"
    elif lowered == "doggo":
        return f"Woof woof!"
    else:
        return choice(["Sorry, I didn't quite get that",
                       "Hmm, I'm having issue understanding, maybe try something else?",
                       "Apologies, I can't comprehend what you're saying"
                       ])







