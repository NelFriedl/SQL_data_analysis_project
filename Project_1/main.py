"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Nela Friedlová
email: nela.friedl@gmail.com
"""
TEXTS = [
    '''Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30 and the Union Pacific Railroad,
    which traverse the valley.''',
    '''At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.''',
    '''The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.'''
]
users = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}
separator = "-" * 50
#login
username = input("Enter username: ")
password = input("Enter password: ")
print(separator)

#login verification
if username in users and password == users[username]:
  print(f'Hi, {username.title()}!\nWe have 3 texts to be analyzed.')
  print(separator)

# text selection and validation
  text_index = input("Select text by entering a number (1-3): ")
  if not text_index.isdigit() or not(1 <= int(text_index) <= 3):
    print("Wrong value!Must be in the range 1-3.")
  else:
    for index, text in enumerate(TEXTS, start=1):
      if int(text_index) == index:
        chosen_text = text

# text analysis       
  words_number = len(chosen_text.split())
  capital_letter = 0
  capitals = 0
  lower_word = 0
  numbers = 0
  sum = 0
  for word in chosen_text.split():
    if word.istitle():
      capital_letter += 1
    elif word.isupper():
        capitals += 1
    elif word.islower():
      lower_word +=1
    elif int(word):
      numbers += 1
      sum = sum + int(word)
  print(separator)
  statistics = f'''
    There are {words_number} words in the selected text.
    There are {capital_letter} titlecase words.
    There are {capitals} uppercase words.
    There are {lower_word} lowercase words.
    There are {numbers} numeric strings.
    The sum of all the numbers is {sum}
    '''
  print(statistics)
  print(separator)
  
  # graph creating
  words_length = {} 
  for word in chosen_text.split():
    word_length = len(word)
    if word_length in words_length:
      words_length[word_length] += 1
    else:
      words_length[word_length] = 1
  print(f'LEN| OCCURENCES       |NR. ')
  for word_length in sorted(words_length):
    print(f'{word_length:>3}|{'*' * words_length[word_length]:<18}| {words_length[word_length]}')

# unregistered user
else:
  print(f'username:{username}\npassword:{password}\nunregistered user, terminating the program..')



