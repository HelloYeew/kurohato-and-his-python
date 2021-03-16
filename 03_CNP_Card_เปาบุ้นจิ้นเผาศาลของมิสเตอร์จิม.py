# Prog-03: Card Game
# # 6310545566 Name เปาบุ้นจิ้นเผาศาลของมิสเตอร์จิม
import time
import random


def generate_deck(n_cards, n_shuffles):
    print('Shuffle', end='')
    deck = ''
    for suit in 'CDHS':
        for face in 'A23456789TJQK':
            deck += '|' + face + suit + '|'
    for i in range(n_shuffles):
        deck = cut(deck, random.randint(0, n_cards))
        deck = shuffle(deck)
        time.sleep(0.1)
        print('.', end='')
    print()
    return deck[:4 * n_cards]


def play(n_cards):
    print('Start a card game.')
    deck = generate_deck(n_cards, 20)

    p1, deck = deal_n_cards(deck, 5)
    p2, deck = deal_n_cards(deck, 5)
    players = [p1, p2]

    table_cards, deck = deal_n_cards(deck, 1)
    fail = False
    turn = 0

    while True:
        show_table_cards(table_cards, 10)
        show_player_cards(players[turn], turn + 1)
        k = select_card_number(players[turn])
        valid = (k != 0)
        if valid:
            cards = players[turn]
            card = peek_kth_card(cards, k)
            valid = eq_suit_or_value(card,
                                     table_cards[-4:])
            if valid:
                table_cards += card
                players[turn] = remove_kth_card(cards, k)
                fail = False
        if not valid:
            print(' ** Invalid **')
        if len(deck) == 0:
            if fail: break
        fail = True
        if len(deck) > 0:
            print(' >> get a new card')
        card, deck = deal_n_cards(deck, 1)
        players[turn] = card + players[turn]
        show_player_cards(players[turn], turn + 1)
        if len(players[turn]) == 0: break
        turn = (turn + 1) % len(players)


if len(deck) == 0:
    print('\n** No more cards **')
print('*****************')
if len(deck) == 0 and len(players[0]) == len(players[1]):
    print('Draw!!!')
elif len(players[0]) < len(players[1]):
    print('Player # 1 win!!!')
else:
    print('Player # 2 win!!!')


def eq_suit_or_value(card1, card2):
    return card1[1] == card2[1] or card1[2] == card2[2]


def show_player_cards(cards, k):
    print(' Player #', k, ':', cards)


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except:
            pass


def select_card_number(cards):
    n = len(cards) // 4
    k = input_int(' Select card # (1-' + str(n) + ') : ')
    if not (1 <= k <= n): k = 0
    return k


def peek_kth_card(cards, k):
    """cards เป็นสตริงเก็บไพ่หลายใบ (อาจจะใบเดียวก็ได้) เช่น "|2H||4S||TD||AC|"
        k เป็นจำนวนเต็ม ระบุตำแหน่งไพ่ที่สนใจใน cards (ใบซ้ายสุดคือตำแหน่งที่ 1)
        ต้องทำ: ตั้งค่าให้ตัวแปร the_kth_card เก็บสตริงที่แทนไพ่ใบที่ k ใน cards
        ตัวอย่าง: cards เก็บ "|2H||4S||TD||AC|", k เก็บ 2
        ได้ the_kth_card เก็บ "|4S|"

        Doctest :
            >>> cards = "|2H||4S||TD||AC|"
            >>> k = 2
            >>> peek_kth_card(cards, k)
            '|4S|'
            >>> k = 4
            >>> peek_kth_card(cards, k)
            '|AC|'
    """
    return cards[(4 * (k - 1)):(4 * k)]


def remove_kth_card(cards, k):
    """cards เป็นสตริงเก็บไพ่หลายใบ (อาจจะใบเดียวก็ได้) เช่น "|2H||4S||TD||AC|"
        k เป็นจำนวนเต็ม ระบุตำแหน่งไพ่ที่สนใจใน cards (ใบซ้ายสุดคือตำแหน่งที่ 1)
        ต้องทำ: ตั้งค่าให้ตัวแปร new_cards ให้เหมือน cards แต่ไพ่ใบที่ k เดิมของ cards ถูกลบทิ้ง
        ตัวอย่าง: cards เก็บ "|2H||4S||TD||AC|", k เก็บ 2
        ได้ new_cards เก็บ "|2H||TD||AC|"

        Doctest :
            >>> cards = "|2H||4S||TD||AC|"
            >>> k = 2
            >>> remove_kth_card(cards, k)
            '|2H||TD||AC|'
            >>> cards = "|2H||4S||TD||AC|"
            >>> k = 4
            >>> remove_kth_card(cards, k)
            '|2H||4S||TD|'
    """
    new_card = cards.replace(cards[(4 * (k - 1)):(4 * k)], '')
    return new_card


def deal_n_cards(deck, n):
    """deck เป็นสตริงเก็บไพ่หลายใบ (อาจจะใบเดียวก็ได้) เช่น "|2H||4S||TD||AC||AD||AS|"
        n เป็นจำนวนเต็ม ระบุจำนวนไพ่ที่ต้องการแจกออกจาก deck (n ใบซ้าย)
        ต้องทำ: ตั้งค่าให้ตัวแปร cards เก็บสตริงที่แทนไพ่จำนวน n ใบทางซ้ายของ deck (ในลำดับเดิมที่อยู่ใน deck)
        ตั้งค่าให้ตัวแปร new_deck ให้เหมือน deck แต่ไพ่จำนวน n ใบทางซ้ายที่ k เดิมของ deck ถูกลบทิ้ง
        หมายเหตุ: ไม่ต้องสนใจกรณีที่ n มีค่ามากกว่าจำนวนไพ่ใน deck
        ตัวอย่าง: deck เก็บ "|2H||4S||TD||AC||AD||AS|", n เก็บ 4
        ได้ cards เก็บ "|2H||4S||TD||AC|" และ new_deck เก็บ "|AD||AS|"

        Doctest :
            >>> deck = "|2H||4S||TD||AC||AD||AS|"
            >>> n = 4
            >>> cards, new_deck = deal_n_cards(deck, n)
            >>> cards
            '|2H||4S||TD||AC|'
            >>> new_deck
            '|AD||AS|'
    """
    cards = deck[0:(4 * n)]
    new_deck = deck[(4 * n):]
    return cards, new_deck


def cut(deck, m):
    """deck เป็นสตริงเก็บไพ่หลายใบ เช่น "|2H||4S||TD||AC||3H||4H||5H||6H||7H||8H|"
        m เป็นจำนวนเต็ม ระบุจำนวนไพ่ที่สนใจทางซ้ายของ deck (m มีค่าได้ตั้งแต่ 0 ถึงจำนวนไพ่ใน deck)
        ต้องทำ: ตั้งค่าให้ตัวแปร new_deck เก็บสตริงจากการย้ายไพ่ m ใบทางซ้ายของ deck มาต่อท้ายทางขวาของ deck
        ตัวอย่าง: deck เก็บ "|2H||4S||TD||AC||3H||4H||5H||6H||7H||8H|", m เก็บ 4
        ได้ new_deck เก็บ "|3H||4H||5H||6H||7H||8H||2H||4S||TD||AC|"

        Doctest :
            >>> deck = "|2H||4S||TD||AC||3H||4H||5H||6H||7H||8H|"
            >>> m = 4
            >>> cut(deck, m)
            '|3H||4H||5H||6H||7H||8H||2H||4S||TD||AC|'
    """
    card_to_m = deck[0:(4 * m)]
    new_deck = deck.replace(card_to_m, '')
    return new_deck + card_to_m


def shuffle(deck):
    """deck เป็นสตริงเก็บไพ่หลายใบ เช่น "|2H||3H||4H||5H||6H||7H||8H||9H||TH||JH||QH||KH||AH|"
        ต้องทำ: ตั้งค่าให้ตัวแปร new_deck เก็บสตริงจากการนำไพ่ครึ่งซ้ายและครึ่งขวาของ deck มาวางสลับกันทีละใบ
        ตัวอย่าง: deck เก็บ "|2H||3H||4H||5H||6H||7H||8H||9H||TH||JH||QH||KH||AH|"
        ได้ new_deck เก็บ "|2H||9H||3H||TH||4H||JH||5H||QH||6H||KH||7H||AH||8H|"
        หมายเหตุ: ในกรณีที่จำนวนไพ่ใน deck เป็นจำนวนคี่ ให้ครึ่งซ้ายมีจำนวนมากกว่าครึ่งขวา (ดูตัวอย่าง)

        Doctest :
        >>> deck = '|2H||3H||4H||5H||6H||7H||8H||9H||TH||JH||QH||KH||AH|'
        >>> shuffle(deck)
        '|2H||9H||3H||TH||4H||JH||5H||QH||6H||KH||7H||AH||8H|'
        >>> deck = '|2H||3H||4H||5H||6H||7H||8H||9H||TH||JH||QH||KH||AH||1S|'
        >>> shuffle(deck)
        '|2H||9H||3H||TH||4H||JH||5H||QH||6H||KH||7H||AH||8H||1S|'
        """

    # ตรงนี้งงไม่แปลงบอกเลย กูก็ไม่รู้เหมือนกันเขียนไรไป

    if (len(deck) / 4) % 2 != 0:
        num_card_left = int((len(deck) / 4) / 2) + 1
        num_card_right = int((len(deck) / 4) / 2)
    else:
        num_card_left = int((len(deck) / 4) / 2)
        num_card_right = int((len(deck) / 4) / 2)
    card_stay = deck[0:(num_card_left * 4)]
    card_move = deck[num_card_left * 4:]
    card_left = []
    while_card_left = 0
    while while_card_left < (num_card_left * 4):
        card_left.append(card_stay[while_card_left:while_card_left + 4])
        card_left.append("Yeah")
        while_card_left += 4
    card_right = []
    while_card_right = 0
    while while_card_right < (num_card_right * 4):
        card_right.append(card_move[while_card_right:while_card_right + 4])
        while_card_right += 4
    for i in range(0, len(card_right)):
        card_left[((i + 1) * 2) - 1] = card_right[i]
    if card_left[-1] == 'Yeah':
        card_left.remove('Yeah')
    return ''.join(card_left)


def show_table_cards(cards, m):
    """cards เป็นสตริงเก็บไพ่หลายใบ (อาจจะใบเดียวก็ได้) เช่น "|2H||4S||TD||AC|"
        m เป็นจำนวนเต็ม ระบุจำนวนไพ่ที่สนใจทางขวาของ cards ที่จะนำมาแสดง
        ต้องทำ: นำไพ่ใน cards ทางขวา m ใบมาแสดง (ถ้ามีน้อยกว่าก็แสดงเท่าที่มี)
        ในกรณีที่มีมากกว่า m ใบ ต้องแสดง .... ทางซ้ายด้วย ดูรายละเอียดของรูปแบบการแสดงในตัวอย่าง
        ฟังก์ชันนี้ไม่มีการคืนค่าใด ๆ

        Doctest :
        >>> cards = "|2H||3H||4H||5H|"
        >>> show_table_cards(cards, 5)
        -----------------------
        Table: |2H||3H||4H||5H|
        -----------------------
        >>> show_table_cards(cards, 4)
        -----------------------
        Table: |2H||3H||4H||5H|
        -----------------------
        >>> show_table_cards(cards, 3)
        -----------------------
        Table: ....|3H||4H||5H|
        -----------------------
        >>> show_table_cards(cards, 2)
        -------------------
        Table: ....|4H||5H|
        -------------------
    """
    if len(cards) / 4 <= m:
        dot_num = 7 + len(cards)
        print(f"{'-' * dot_num}\nTable: {cards}\n{'-' * dot_num}")
    else:
        print_cards = cards[len(cards) - (m * 4):]
        dot_num = 11 + len(print_cards)
        print(f"{'-' * dot_num}\nTable: ....{print_cards}\n{'-' * dot_num}")


play(51)

# If you want to run doctest run 'python3 -m doctest <filename>.py' to check your function (mean you don't want to
# make a new file LOL)

# มีโค้ดที่จารให้มาเราก็อปผิดนิดหน่อย ไปแก้ด้วย ไม่งั้นรันไม่ได้
