from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker()

# Define all the functions
def random_integer(max_value):
    return random.randint(0, max_value)

def fake_email():
    return fake.email()

def fake_first_name():
    return fake.first_name()

def fake_last_name():
    return fake.last_name()

def fake_address():
    return fake.street_address()

def fake_city():
    return fake.city()

def fake_country():
    return fake.country()

def fake_postcode():
    return fake.postcode()

def random_zip():
    return str(random.randint(10000, 99999))

def generalize_daterange():
    return '2020-01-01 to 2020-12-31'

def generalize_numrange():
    return '1 to 100'

def generalize_timestamp():
    return '2020-01-01 00:00:00'

def partial_masking(data):
    return data[:4] + '*' * (len(data) - 4)

def full_masking(data):
    return '*' * len(data)

def randomized_date():
    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2020-12-31', '%Y-%m-%d')
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime('%Y-%m-%d')

def convert_to_Confidential(data):
    return 'Confidential'

def random_mobile_number():
    return ''.join(random.choices('0123456789', k=10))

def Random_String():
    return fake.random_letters(length=10)

def Random_In(data):
    return random.choice(data)

# Test each function
print("Testing random_integer:")
print(random_integer(100))

print("\nTesting fake_email:")
print(fake_email())

print("\nTesting fake_first_name:")
print(fake_first_name())

print("\nTesting fake_last_name:")
print(fake_last_name())

print("\nTesting fake_address:")
print(fake_address())

print("\nTesting fake_city:")
print(fake_city())

print("\nTesting fake_country:")
print(fake_country())

print("\nTesting fake_postcode:")
print(fake_postcode())

print("\nTesting random_zip:")
print(random_zip())

print("\nTesting generalize_daterange:")
print(generalize_daterange())

print("\nTesting generalize_numrange:")
print(generalize_numrange())

print("\nTesting generalize_timestamp:")
print(generalize_timestamp())

print("\nTesting partial_masking:")
print(partial_masking("SensitiveData"))

print("\nTesting full_masking:")
print(full_masking("SensitiveData"))

print("\nTesting randomized_date:")
print(randomized_date())

print("\nTesting convert_to_Confidential:")
print(convert_to_Confidential("SensitiveData"))

print("\nTesting random_mobile_number:")
print(random_mobile_number())

print("\nTesting Random_String:")
print(Random_String())

print("\nTesting Random_In:")
print(Random_In(["Option1", "Option2", "Option3"]))
