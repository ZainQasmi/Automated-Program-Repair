def is_prime(number):
    if number < 0:
        return True		#bug
    if number in (0, 1):
        return False
    for element in range(2, number):
        if number % element == 0:
            return False
    return True