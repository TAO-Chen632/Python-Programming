def encrypt_it(string):
    '''
    This is the function that takes an input string, and returns the encrypted version of it.
    
    Input:
        string (str): the string of the original text

    Output:
        string (str): the string of the encrypted text
    '''
    # Convert the input string to `list` type, each element of which represents a word in this string
    str_list = string.split(' ')
    n = len(str_list)
    # Turn all the occurrences of the word 'I' into lowercase 'i'
    str_list = [word if word != 'I' else 'i' for word in str_list]
    # Re-order the words in the sentence
    for i in range(n):
        if i % 2 == 1:
            str_list[i - 1], str_list[i] = str_list[i], str_list[i - 1]
    # Take the first letters of all the words
    first_letters = [word[0] for word in str_list]
    # Replace the first letter of each word with the first letter of the previous word
    for i in range(n):
        if i > 0:
            str_list[i] = first_letters[i - 1] + str_list[i][1: ]
        else:
            str_list[i] = first_letters[n - 1] + str_list[i][1: ]
    # Reverse the order of all the letters excluding the first letter in each word
    str_list = [(word[0] + word[ :0 :-1]) for word in str_list]
    # Join every word in the `str_list` to construct the complete encrypted string
    string = ' '.join(str_list)
    return string


def decrypt_it(string):
    '''
    This is the function that takes an input encrypted string, and returns the unencrypted version of it.
    
    Input:
        string (str): the string of the encrypted text

    Output:
        string (str): the string of the original unencrypted text
    '''
    # Convert the input string to `list` type, each element of which represents a word in this string
    str_list = string.split(' ')
    n = len(str_list)
    # Reverse the order of all the letters excluding the first letter
    # in each word again to restore the original order
    str_list = [(word[0] + word[ :0 :-1]) for word in str_list]
    # Take the first letters of all the words
    first_letters = [word[0] for word in str_list]
    # Replace the first letter of each word with the first letter of
    # the subsequent word to restore the original word
    for i in range(n):
        if i < n - 1:
            str_list[i] = first_letters[i + 1] + str_list[i][1: ]
        else:
            str_list[i] = first_letters[0] + str_list[i][1: ]
    # Re-order the words in the sentence again to restore the original order of the words
    for i in range(n):
        if i % 2 == 1:
            str_list[i - 1], str_list[i] = str_list[i], str_list[i - 1]
    # Turn all the occurrences of the word 'i' into uppercase 'I'
    str_list = [word if word != 'i' else 'I' for word in str_list]
    # Join every word in the `str_list` to construct the complete unencrypted string
    string = ' '.join(str_list)
    return string


# Testing examples

# The original message from the future
print(decrypt_it('pcimedna peh Te blli w!noo srev omla cpee Kyojn edn an ignimmargor p!nohty'))

# The testing examples in the `README.md`
print(encrypt_it('This course is fun, but I am tired of programming in Python!'))
print(decrypt_it('iesruo csih T,nu fs i itu bderi tm agnimmargor pf o!nohty Pn'))

print(decrypt_it('mevo l ihti wuo yy mll a i!ylle bo tdetna wtrae hya sy mtu bs iylle b.reggi bhcu'))
print(decrypt_it('tesua cemo Srevereh wssenippa h;o gyeh treveneh wemo s.o gyeh'))

# Other more examples for testing

# The sentences with odd words
print(encrypt_it('If you wish to succeed, you should use persistence as your friend, experience as your reference, prudence as your brother and hope as your sentry.'))
print(decrypt_it('suo yf Io thsi wuo y,deeccu ses udluoh ss aecnetsisre p,dneir fruo ys aecneirepx e,ecnerefe rruo ys aecnedur prehtor bruo yepo hdn aruo ys a.yrtne'))
print(encrypt_it('I love it when I catch you looking at me, and then you smile and look away.'))
print(decrypt_it('aevo l ineh wt ihcta c ignikoo luo y,e mt aneh tdn aelim suo ykoo ldn a.yaw'))

# The sentences with even words
print(encrypt_it('One needs three things to be truly happy living in the world: some thing to do, some one to love and some thing to hope for.'))
print(decrypt_it('hsdee nen Osgnih teerh te bo typpa hylur tn ignivi l:dlro weh tgnih temo s,o do ten oemo sevo lo temo sdn ao tgnih t.ro fepo'))
print(encrypt_it('Accept what was and what is, and you will have more positive energy to pursue what will be.'))
print(decrypt_it('wtah wtpecc Adn asa w,s itah wuo ydn aeva hlli wevitiso pero mo tygren etah weusru p.e blli'))

# Some edge cases - the strings with only a single letter, only one word or only two words
print(encrypt_it('I'))
print(decrypt_it('i'))
print(encrypt_it('x'))
print(decrypt_it('x'))
print(encrypt_it('encrypt'))
print(decrypt_it('etpyrcn'))
print(encrypt_it('Brilliant invention'))
print(decrypt_it('Bnoitnevn itnaillir'))
