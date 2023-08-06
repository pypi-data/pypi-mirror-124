def adad_aval (number):
    counter = True
    for i in range(2, number):
        if number % i == 0:
            counter = False
    if counter:
        return True
    if counter == False:
        return False

def joda_cardan_argham (number):
    while number != 0:
        ragham = number % 10
        number = number // 10
        return ragham

def factorial (number):
    if number == 1:
        return number
    else:
        return number * factorial(number - 1)
    
def fibonachi (number):
    if number == 1:
        return 1
    elif number == 0:
        return 0
    else:
        return fibonachi(number - 1) + fibonachi(number - 2)
    
def maghlob (number):
    m = 0
    while number != 0:
        m = m * 10 + number % 10
        number = number // 10
    return m
