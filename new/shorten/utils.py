from .models import bitly
from datetime import date

def code_gen():
    import random
    shrtcd=''
    for i in range(6):
        shrtcd+= random.choice(chr(random.randint(65,90))
                               +chr(random.randint(97,122))
                               +chr(random.randint(48,57))
                               )
    return shrtcd

def create_shortcode():
    shrtcd = code_gen()
    qs = bitly.objects.filter(shortcode__iexact=shrtcd)
    if qs.exists():
        return create_shortcode()

    return shrtcd



def current_day():
    crt_date = date.today()
    return crt_date.strftime("%d-%m-%Y")
