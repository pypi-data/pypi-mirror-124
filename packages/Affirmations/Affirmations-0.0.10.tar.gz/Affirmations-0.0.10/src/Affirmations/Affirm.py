from random import choice, random
try:
    from AffirmationText import affirmations as affirmations
except:
    from Affirmations.AffirmationText import affirmations as affirmations


def affirm(*args):
    if not args or args[0] > 1:
        frequency = 1
    else:
        frequency = args[0]

    def decorator(function):
        def wrapper(*args, **kwargs):
            if frequency > random():
                print(choice(affirmations))
            return function(*args, **kwargs)
        return wrapper
    return decorator



if __name__ == "__main__":
    pass
