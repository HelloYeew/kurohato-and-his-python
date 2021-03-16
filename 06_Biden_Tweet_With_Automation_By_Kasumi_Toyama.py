# Prog-06: Kasumi Similarity
# Hanasakigawa Girls' High School Best Programmer Name Kasumi Toyama (Class 2-A)

# This 2 part will automatically do what your professor want you to do in last page. You can send this part to your
# professor and comment that Thonny is stupid. What dafaq is this? You don't want to understand it.
# Just know that it will make you automatically install must-have library to use and run a command in python shell.

# 1. This program part make you not to install nltk because it will install it for you (ฺBecause Thonny is stupid.)

try:
    # Check that you have nltk library installed on your computer if installed, import!
    import nltk
    from nltk.stem import PorterStemmer
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except:
    # You don't have it so...installed!
    import os

    os.system("pip3 install nltk")

# 2. Then make sure that it's install some command that you must run in Thonny shell. (Normally you don't want to run
# it. Just put it in your program)
nltk.download('stopwords')
nltk.download('punkt')

# import webbrowser
# from tkinter import messagebox
#
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=7aMVDDn-0us")
# webbrowser.open_new_tab("https://www.youtube.com/watch?v=_yPt5dqrwsw")
# messagebox.showinfo(title="Kasumi has taken your computer!", message="Sakuraaaaaaaaaaaa Memoriesssssssssss kimi no mono da yooooooooooooo Kono shuuuuuuuuuuuunkan mo kako moooooooooooooo zennnnnnnnnnnnnnbuuuuuuuuuuuuuuu")

# end of 2 part

STOP_WORDS = stopwords.words('english')
STEMMER = PorterStemmer()


def read_tweets():
    f = open('biden.txt', encoding='utf-8')
    tweets = [line.strip() for line in f.readlines()]
    f.close()
    return tweets


def normalize_text(text):
    words = []
    for w in word_tokenize(text.lower()):
        if w.isalnum() and w not in STOP_WORDS:
            words.append(STEMMER.stem(w))
    return get_unique(words)


def main():
    tweets = read_tweets()
    norm_tweets = []
    for t in tweets:
        norm_tweets.append(normalize_text(t))

    print_width = 48
    while True:
        query = input('Query words   : ')
        if query == '': break
        n = int(input('No. of results: '))
        norm_query = normalize_text(query)
        top_n = top_n_similarity(norm_tweets, norm_query, n)
        if len(top_n) == 0:
            print('No matches found.')
        else:
            for tid, jc_coef in top_n:
                show_tweet(tid, tweets[tid], jc_coef, print_width)
        print('-' * print_width)


# Shitty Line

def get_unique(words):
    """words เป็นลิสต์ที่เก็บสตริง
    ต้องทำ: ตั้งค่าให้ตัวแปร unique_words ที่เก็บสตริงได้มาจาก words แต่ไม่มีตัวซ้ำ (คือตัวไหนมีซ้ำใน words
    จะมีตัวนั้นแค่ตัวเดียวใน unique_words)

    Doctest :
        >>> words = ['x', 'y', 'z', 'y', 'xyz', 'z']
        >>> get_unique(words)
        ['x', 'y', 'z', 'xyz']
    """
    unique_words = []
    for i in words:
        if i not in unique_words:
            unique_words.append(i)
    return unique_words

def jaccard(words_1, words_2):
    """words_1 และ words_2 เป็นลิสต์ของคำต่าง ๆ (ไม่มีคำซ้ำใน words_1 และ ไม่มีคำซ้ำใน words_2)
    ต้องทำ: ตั้งตัวแปร jaccard_coef ให้มีค่าเท่ากับ Jaccard similarity coefficient ที่คำนวณจากค่าใน
    words_1 และ words_2 ตามสูตรที่แสดงไว้ก่อนนี้

    Doctest :
        >>> words_1 = ['x', 'y', 'z', 'xyz']
        >>> words_2 = ['y', 'x', 'w']
        >>> jaccard(words_1,words_2)
        0.4
    """
    # Check intersect
    in_other = 0
    for i in words_1:
        if i in words_2:
            in_other += 1
    # Make list of total member in both list
    both_list = []
    for i in words_1:
        if i not in both_list:
            both_list.append(i)
    for i in words_2:
        if i not in both_list:
            both_list.append(i)
    jaccard_coef = in_other / len(both_list)
    return jaccard_coef


def top_n_similarity(norm_tweets, norm_query, n):
    """norm_tweets เป็นลิสต์ที่ภายในเก็บลิสต์ของคำต่าง ๆ [ [w00,w01,...], [w10,w11,...], ... ]
    norm_query เป็นลิสต์ของคำต่าง ๆ
    n เป็นจำนวนเต็ม
    ต้องทำ: ตั้งค่าให้ตัวแปร top_n ที่เก็บลิสต์ขนาดไม่เกิน n ช่อง
    แต่ละช่องเก็บลิสต์ย่อยขนาดสองช่อง [ [tweet_id, jaccard], ... ]
    tweet_id คือเลขอินเด็กซ์ของทวีตใน norm_tweets
    jaccard คือค่า Jaccard coefficient ของ norm_tweets[tweet_id] กับ norm_query
    โดยจะเลือกทวีตที่มีค่า Jaccard มากกว่า 0 และติดอันดับมากสุด n ตัวแรก
    ในกรณีที่มีค่า Jaccard เท่ากัน ให้เลือกอันที่มี tweet_id น้อยกว่าก่อน
    """
    index_list = []
    jaccard_list = []
    for i in range(len(norm_tweets)):
        index_list.append(i + 1)
        jaccard_list.append(jaccard(norm_tweets[i], norm_query))
    top_n = []
    result_list = []
    number_list = []
    sort_jaccard = sorted(jaccard_list, reverse=True)
    for i in range(len(sort_jaccard)):
        for j in range(len(jaccard_list)):
            if (sort_jaccard[i] == jaccard_list[j]) and (jaccard_list[j] != 0) and (j not in number_list):
                number_list.append(j)
                result_list.append([j, sort_jaccard[i]])
    for i in range(n):
        top_n.append(result_list[i])
    return top_n


def show_tweet(tweet_id, tweet_content, jc_coef, print_width):
    """tweet_id เป็นจำนวนเต็มแทนเลขอินเด็กซ์ของทวีต
    tweet_content เป็นสตริงเก็บข้อความของทวีตที่ต้องการแสดง
    jc_coef เป็นจำนวนจริงแทนค่า Jaccard coefficient
    print_width เป็นจำนวนเต็มแทนจำนวนตัวอักษรที่แสดงได้ในหนึ่งบรรทัด
    ต้องทำ: นำข้อมูลทั้งหลายที่ได้รับมาแสดงทางจอภาพในรูปแบบที่แสดงในตัวอย่าง ฟังก์ชันนี้ไม่คืนผลอะไร

    Doctest :
        >>> t = 'I promise you that as president, I will always appeal to the best  in us.'
        >>> show_tweet(1076, t, 0.222222, 40)
        <BLANKLINE>
        #1076 (0.22)
          I promise you that as president, I
          will always appeal to the best  in us.
        >>> show_tweet(1076, t, 0.222222, 30)
        <BLANKLINE>
        #1076 (0.22)
          I promise you that as
          president, I will always
          appeal to the best  in us.
        >>> show_tweet(1076, t, 0.222222, 20)
        <BLANKLINE>
        #1076 (0.22)
          I promise you that
          as president, I
          will always appeal
          to the best  in
          us.
    """
    print()
    print(f"#{tweet_id} ({round(jc_coef, 2)})")
    word_list = tweet_content.split(" ")
    print_list = []
    word_to_print = ""
    for i in range(len(word_list)):
        if i == len(word_list) - 1:
            if (len(word_to_print + word_list[i]) + 2) <= print_width:
                word_to_print += f"{word_list[i]} "
                print_list.append(word_to_print)
                continue
            else:
                print_list.append(word_to_print)
                print_list.append(f"{word_list[i]} ")
                continue
        elif (len(word_to_print + word_list[i]) + 2) <= print_width:
            word_to_print += f"{word_list[i]} "
        else:
            print_list.append(word_to_print)
            word_to_print = f"{word_list[i]} "
    for word in print_list:
        print(f"  {word[:-1]}")


# Shitty Line
main()
