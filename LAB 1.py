#http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
# Site used that had the quadgram text file I used  (quadgrams.txt)
#used for making random keys
import random 
#used for calculations to prevent numerical underflow of the probablity of the quadgrams
from math import log10 
#dictionary that opens the quadgram text file
dictionary = {} 
with open("quadgrams.txt", "r") as file:
    for line in file:
      #key is the quadgram and value is the count of the quadgram
      key, value = line.split(" ") 
      #typecast to int as it thinks count is a string
      dictionary[key] = int(value)

#alphabet 
alphabet = "abcdefghijklmnopqrstuvwxyz"  

#ciphers that need to be decoded 
cipher1 = "fqjcb rwjwj vnjax bnkhj whxcq nawjv nfxdu mbvnu ujbbf nnc"

cipher2 = "oczmz vmzor jocdi bnojv dhvod igdaz admno ojbzo rcvot jprvi oviyvaozmo cvooj ziejt dojig toczr dnzno jahvi fdiyv xcdzq zoczn zxjiy"

cipher3 = "ejitpspawaqlejitaiulrtwllrflrllaoatwsqqjatgackthlsiraoatwlplqjatwjufrhlhutsqataqitatsaittkstqfjcae"

cipher4 = "iyhqzewqinazqejshayzniqbeaheumhnmnjjaqiiyuexqayqknjbeuqiihedyzhniifnunsayizyudhesqshuqesqailuymqkqueaqaqmoejjshqzyujdzqadieshniznjjayzyuiqhqvayzqshsnjjejjznshnahnmytisnaesqfundqzewqieadzevqizhnjqshqzeudqaijrmtquishqifnunsiiqasuoijqqfnisyyleiszhnbhmeisquihnimnxhseadshqmrudququaqeuiisqejshnjoihyysnaxshqihelsiluymhnityz"

# First quote used for part two 
quote1 = "He who fights with monsters should look to it that he himself does not become a monster. And if you gaze long  into an abyss, the abyss also gazes into you"

# Second quote used for part two 
quote2 = "There is a theory which states that if ever anybody discovers exactly what the Universe is for and why it is here,it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened"

# Third quote used for part two 
quote3 = "Whenever I find  myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me,that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people’s hats off then, I account it high time to get to sea as soon as I can"

#function that takes the alphabet as input and returns a mixed key
def random_gen(alphabet):
   alphabet = list(alphabet)
   random.shuffle(alphabet)
   return ''.join(alphabet)

# Function that encrypts a plain text message 
# encrypt takes in a message as its first parameter and
# the modified alphabet as a key 
def encrypt(msg,key):
  # converts message to lower case
  temp = msg.lower() 
  # cipher is the decrypted message that is returned
  cipher = "" 
  # for loop that iterates through the message
  for i in temp: 
     #if the element in the message is not part of the alphabet it is outputted normally 
    if i not in alphabet:
        cipher += i
    else:
      #converts the letters in the message to the according letter in modified key
      cipher+=key[alphabet.index(i)] 
  return cipher 
	
# decrypt takes the encrypted cipher message as its first parameter and the modifed alphabet as its second parameter 
def decrypt(cipher, key):
  #text will hold the decrypted message 
  text = "" 
  #for loop iterates through the encrypted message 
  for i in cipher: 
    # if the element in the cipher isn't part of the alphabet it is outputted as it is
    if i not in alphabet: 
        text += i
    #if the element is part of the alphabet then it is converted to the according letter it should be at the matching index 
    else: 
		    text+=alphabet[key.index(i)]
  return text 

# Function for Caesar shift encryptions
def shift(cipher):
  #Iterate through every possible Caesar shift variant by looping 26 times
  for j in range(26): 
    # text will hold the decrypted message
    text = "" 
    # iterate through the cipher message 
    for i in cipher: 
      #for all the spaces output the space
      if i not in alphabet: 
        text += i
      #if it isn't a space output the possible letter it could be
      else:  
        # iteration of Caesar shifts that gets all 26 shifts 
        text += alphabet[(alphabet.index(i) + j) % 26] 
    print("Variation #" + repr(j) + ": " + text + "\n")
    

# Simple function that calls encrypt, decrypt and then prints them out 
def transform(quote, key):
  e = encrypt(quote, key)
  d = decrypt(e, key)
  print("Encrypted Message: ")
  print(e + "\n")
  print("Decrypted Message: ")
  print(d + "\n")
  print("Random generated key: "+ key + "\n")

# Function that swaps two characters in the key for the hill climbing algorithm
# the first parameter is the key which is having it's charcters switched and
# i/j are the indexes of the string that are getting swapped
def key_swap(s, i, j):
    lst = list(s)
    lst[i], lst[j] = lst[j], lst[i]
    return "".join(lst)

# Function that passes in a cipher to break into quadgrams
def quadgram_converter(cipher):
  #Replaces whitespaces in ciphers with no space 
  cipher = cipher.replace(" ","")
  # create a list that will store all quadgrams from the cipher
  quadgram_list = list()
  #for loop that iterates over the length of the cipher
  # minus 3 to get the number of quadgrams that will be in the list
  for i in range(len(cipher)-3):
    #increments and takes pieces of cipher until all quadgrams are accounted for
    quadgram_list.append(cipher[i:i+4])
  return quadgram_list

# Calculate the total number quadgrams in text file  
total = sum(dictionary.values())

# Calculates the total fitness of a quadgram list that is returned from
# quadgram_converter using log probablity to counter numerical underflow 
def fitness(quadgram_list):
  # temp will store the vale of the cipher's fitness 
  temp = 0.00
  # iterate through the list of quadgrams 
  for i in range(len(quadgram_list)):
    # if the quadgram is in the quadgram.txt file divide it by the count of the total quadgrams and then take the log10 of it to account for numerical underflow to find it's log probablity
    # if the quadgram is in the dictionary 
    if quadgram_list[i] in dictionary:  
      temp += log10(float(dictionary.get(quadgram_list[i]))/total)
    else:
      # if the quadgram isn't in the text file assign it a negative value 
      # so we don't get log10(0) which would be negative infinity 
      temp += -9.40018764963
  return temp


# Hill climbing algorithm that takes a cipher as its parameter
# Start with a random key and test its score
# then slightly change the key by switching characters randomly
# and test the score again if new score is better set it as the new score and key 
# Swap characters in the new key again and test the score once again 
# It eventually reaches a local maximum after 1000 iterations and it can not further decrypt
# Used for cipher3 and cipher4 
def crackSub(cipher):
  #starting score to compare to score calculated from hill climb
  small_score = -1000000
  # Attempts of trying to get correct decryption
  attempts = 0
  #first loop
  while attempts < 125:
    #iterations is the number of times we switch key values
    iterations = 0 
    attempts = attempts + 1
    #Generate a random key from alphabet
    key = random_gen(alphabet)
    #Attempt a decryption of cipher using new key
    dec_attempt = decrypt(cipher,key)
    #Convert the cipher into quadgrams and store them in a list
    qlist = quadgram_converter(dec_attempt)
    #Pass the qlist into the fitness function to get its score
    original_score = fitness(qlist)
    #Second loop that iterates for finding a better score than the original score 
    while iterations < 1000:
      #swap values that hold random index between 0-25 for swapping characters in key
      swap1 = random.randrange(0,25)
      swap2 = random.randrange(0,25)
      #Don't increment the iterations if swaps are the same index so loop again
      if swap1 != swap2:
        #Call key swap function that moves two characters in our key to find better key and store in new_key
        new_key = key_swap(key,swap1, swap2) 
        #decrypt again with modified key
        dec_attempt = decrypt(cipher,new_key)
        #Conver the cipher into quadgrams and store in list again 
        qlist = quadgram_converter(dec_attempt)
        #find the new score of decrypted phrase 
        new_score = fitness(qlist)
        # If the new key gave a better score than the original_score
        # update the original_score to new score and new key
        # iteration set to 0 since we're headed toward a better decryption 
        if new_score > original_score:
          original_score = new_score
          key = new_key
          iterations = 0
          # If the score isn't improving increment iterations 
        iterations = iterations + 1
    #After the second while loop ends compare the original score of decryption with the small score which is a large negative number 
    if original_score > small_score:
      # since the new score is larger than the small score replace small score with original score 
      small_score = original_score
      print("Attempt #" + str(attempts))
      print("Attempted decryption: " + dec_attempt + "\n")
      print("Key: " + key + "\n")
      print("Score: " + str(original_score) + "\n")

#Menu for choosing which problems you want to see decrypted/encrypted
choice = 0
while choice != 6:
    print ("""\nWhich question do you want to pick?\n
    ----Symmetric Cryptography----
    1.Cipher 1 Decryption (Caesar Cipher)
    2.Cipher 2 Decryption (Caesar Cipher)
    3.Cipher 3 Decryption (Hill Climb) 
    4.Cipher 4 Decryption (Hill Climb) 
    5.Part Two Encryption 
    6. Quit Menu 
    """)
    choice = input("Enter your choice: \n") 
    if choice=="1": 
      #whats in a name a rose by any other name would smell as sweet
      print ("\nFirst Decryption:\n")
      shift(cipher1)
    elif choice=="2":
      #there are two things to aim at in life first to get what you want and after that to enjoy it Only the wisest of mankind achieve the second
      print ("\nSecond Decryption: \n")
      shift(cipher2)
    elif choice=="3":
      #contrariwise continued tweedle dee if it was so it might be and if it were so it would be but as it isnt it aint thats logic
      print ("\nThird Decryption: \n") 
      crackSub(cipher3)
    elif choice=="4":
      #so he waxes in wealth no wise can harm him illness or age no evil cares shadow his spirit no sword hate threatens from ever an enemy all the world wends at his will no worse he knoweth till all within him obstinate pride waxes and wakes while the warden slumbers the spirits sentry sleep is too fast which masters his might and the murderer nears stealthily shooting the shafts from his bow
     print ("\nFourth Decryption: \n") 
     crackSub(cipher4)
    elif choice=="5":
     print ("Part Two Simple Sub Encrypter: \n")
     print("Quote 1 \n")
     transform(quote1, random_gen(alphabet))
     print("Quote 2 \n")
     transform(quote2, random_gen(alphabet))
     print("Quote 3 \n")
     transform(quote3, random_gen(alphabet))
    elif choice=="6":
     print ("\nGoodbye!\n")
     file.close()
     break
    elif choice !="":
      print("\nNot Valid Choice Try again") 