# Prog-08: Bag-of-Words
# 6310456855614781457254681245712457831245786 Name Kasumi Toyama or peppy

# Set the enumerate
CHAR_LIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345678"


def clear_word(word):
    """Get a word, clear a word to just a word and convert it to lowercase
    Parameter : Ugly like shit word from anywhere (Kasumi's house?)
    Return : Word as a list (because it must support if it have a separator in there)

    Doctest :
        >>> clear_word("Abc:a18")
        ['abc', 'a18']
    """
    result_list = []
    # Turn a word to lowercase
    word = word.lower()
    # Convert to list to for loop
    word_list = list(word)
    # For loop to seperate character and (if) seperator and set it to result_list
    for i in range(len(word_list)):
        if word_list[i] in CHAR_LIST:
            result_list.append(word_list[i])
        else:
            result_list.append(" ")
    # Convert result list to normal string (Make it easier to find a real 'space')
    result_list = "".join(result_list)
    # Convert back to list again but we have a real 'space' bewteen word now
    result_list = result_list.split(" ")
    # Next : We must clear some shit if a member in result list is ' ' (blank space)
    # First, we must find that how many shit space we have by using for loop.
    space_number = 0
    other_number = 0
    for member in result_list:
        if member == ' ':
            space_number += 1
        elif member == '':
            other_number += 1
    # Second, use function 'remove' to remove a shit space n times. We cannot use remove and not check a number
    # because if it not have blank space in result_list it will run to error.
    if space_number != 0:
        for i in range(space_number):
            result_list.remove(' ')
    if other_number != 0:
        for i in range(other_number):
            result_list.remove('')
    # Complete! Then, return!
    return result_list


def clear_stop_word(file_name, sentence_list):
    """Clear a stop word from list of word in sentence
    Parameter : file name that contain stop words and sentence as list
    Return : Sentence as list that already clear a stop words
    """
    duplicate_list = []
    stopwords = []
    # Open stopword file
    stopwords_file = open(file_name, "r")
    for line in stopwords_file:
        stop = line.strip().split()
        for i in stop:
            stopwords.append(i)
    stopwords_file.close()
    # Use list comprehension for finding stop words in sentence list
    for member in sentence_list:
        if member in stopwords:
            duplicate_list.append(member)
    # Remove stop word that in sentence from sentence list by use of duplicate list
    for member in duplicate_list:
        sentence_list.remove(member)
    # Return!
    return sentence_list


def sentence_to_list(sentence):
    """Convert and clean a sentence to a list for bow
    Parameter : String sentence
    Return : Clean sentence ready to use in bow
    """
    # Declare a variable zone to make a code more 'clean' not like that shit
    sentence_complete = []
    # Seperate a sentence to list
    sentence = sentence.split()
    for word in sentence:
        # Clear and spread the word by using 'clear_word' function that we write before
        sentence_complete.append(clear_word(word))
    # Convert list in list to just a word
    sentence_complete = list(map(''.join, sentence_complete))
    # Clear a stop word by using clear_stop_word function
    sentence_complete = clear_stop_word('stopwords.txt', sentence_complete)
    # Sort a list to make a result list as ordered number and word
    sentence_complete.sort()
    return sentence_complete


def bow(sentence):
    """Get a sentence and 'BoW' it
    Parameter : Sentence
    Return : BoW result

    Doctest :
        >>> bow("Shane likes football; he is a big fan of Arsenal football team.")
        [['shane', 1], ['likes', 1], ['football', 2], ['big', 1], ['fan', 1], ['arsenal', 1], ['team', 1]]
    """
    # Declare a variable zone to make a code more 'clean' not like that shit
    result = []
    word_already_append = []  # List for check if we already append it in result list to make it more convenience
    # Use sentence_to_list function to get a clean sentence ready for bow
    sentence = sentence_to_list(sentence)
    # Make a result list
    for word in sentence:
        if word not in word_already_append:
            result.append([word, 1])
            word_already_append.append(word)
        else:
            for list_in_result_index in range(len(result)):
                if result[list_in_result_index][0] == word:
                    result[list_in_result_index][1] += 1
    return result


def fhash(word, M):
    """Just fhash
    Parameter : word, M
    Return : fhash result

    Doctest :
        >>> fhash('big', 4)
        2
    """
    # Calculate fhash formular
    G = 37
    result = 0
    word = list(word)
    for i in range(len(word)):
        if i == 0:
            result += ord(word[i])
        else:
            result += ord(word[i]) * (G ** i)
    return result % M


def bow_fhash(sentence, M):
    """Bow with fhash
    Parameter : sentence, M
    Return : List result of bow with fhash

    Doctest :
        >>> bow_fhash("Shane likes football; he is a big fan of Arsenal football team.", 4)
        [[0, 1], [1, 1], [2, 2], [3, 4]]
    """
    # Declare a variable zone to make a code more 'clean' not like that shit
    result = []
    fhash_list = []
    already_append = []  # List for check if we already append it in result list to make it more convenience
    # Use sentence_to_list function to get a clean sentence ready for bow
    sentence = sentence_to_list(sentence)
    for word in sentence:
        fhash_list.append(fhash(word, M))
    # Sort a list to make a result list as ordered number
    fhash_list.sort()
    # Make a result list
    for fhash_number in fhash_list:
        if fhash_number not in already_append:
            result.append([fhash_number, 1])
            already_append.append(fhash_number)
        else:
            for list_in_result_index in range(len(result)):
                if result[list_in_result_index][0] == fhash_number:
                    result[list_in_result_index][1] += 1
    return result


def count(file_name, fhash=False, M=0):
    """Count and print all
    Parameter : file name, fhash True or False as a boolean (Default is False), M if fhash is True
    Return : Nothing
    """
    # Declare a variable
    char_count = 0
    alphanumberic_count = 0
    word_count = 0
    file_list = []
    line_list = []
    word_list = []
    clear_word_list = []
    # Open file and readline
    file = open(file_name, "r")
    # Append each line of file to list
    for x in file:
        file_list.append(x)
    # We get line_count from how many list that it append in for loop
    line_count = len(file_list)
    # Next, for loop each line to make a list of line and a list of word
    for line in file_list:
        line_list.append(line.strip())
        word_list.append(line.strip().split())
    # Use a line list that we just make to count a character and alphanumberic
    for line in line_list:
        char_count += len(line)
        for character in line:
            if character in CHAR_LIST:
                alphanumberic_count += 1
    # Clear a word list by using a clear_word function
    for word in word_list:
        clear_word_list.append(clear_word(str(word)))
    # After we get a clean word now, count it.
    for member in clear_word_list:
        word_count += len(member)
    # Print a result
    print("-------------------")
    print(f"char count = {char_count}")
    print(f"alphanumberic count = {alphanumberic_count}")
    print(f"line count = {line_count}")
    print(f"word_count = {word_count}")
    sentence = ""
    for line in line_list:
        sentence += line
        sentence += " "
    # We set 2 parameter (fhash and M) to an enum to so you can use this function if you don't have fhash and M to.
    if fhash == False:
        print(f"BoW = {bow(sentence)}")
    else:
        print(f"BoW = {bow_fhash(sentence, M)}")


# Run Program
file_name = input("File name = ")
while True:
    hashing_or_not = input("Use feature hashing ? (y,Y,n,N) ")
    if hashing_or_not == "Y" or hashing_or_not == "y":
        M = int(input("M = "))
        # Turn fhash mode on and put M in function
        count(file_name, fhash=True, M=M)
        break
    elif hashing_or_not == "N" or hashing_or_not == "n":
        # Use this function normally, fhash mode of and not input M because we don't require M
        count(file_name)
        break
    else:
        print("Try again.")
