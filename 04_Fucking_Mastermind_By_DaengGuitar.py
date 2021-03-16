# Prog-04-1: Fucking Mastermind Game Normal Version
# กูอาจารย์แดงกีตาร์จะมาสอนมึงเนื่องในโอกาสวันวาเลนไทน์เหี้ยๆนี่ Name ผมมีสองจอ ดับเบิ้ลจอ

import random
import math
# import math มาทำเหี้ยไรไม่ใช้เนี่ย

# ตัวแปรตัวใหญ่เป็น enum เอ้อ ได้อยู่
WINNING_MSG = "Congratulations! You won the game."
LOSING_MSG = "Sorry! You just lost it."

code = ''.join(random.sample('ABCDEF', 4))

print('Please guess the puzzle code using')
print('the four distinct code characters from [A to F]:')

# เขียนมาทำเหี้ยไรขีดเนี่ย

# Use for check answer when testing a program
# print(f"Answer : {code}")

code_split = list(code)
for i in range(4):
    # Same color and same position
    p = 0
    # Same color but not same position
    v = 0
    # Not fucking same! Where do you get this from?
    x = 0
    answer = input(f"Turn #{i+1} : ")
    # This list is make for mark that if it's same we are not going to check again. Just check one time.
    check_status = [' ', ' ', ' ', ' ']
    # Support when some player not use a capitalize character when play this fucking game.
    answer.upper()
    answer_split = list(answer)
    if len(answer) > 4:
        print(f"{' '*10}คิดว่าเขียนเกินแล้วเก๋าหรอไอเหี้ย")
    elif len(answer) < 4:
        print(f"{' '*10}เอ้าไอ้นี่ เกมนี้เขาให้เขียน 4 ตัวเขียนมา {len(answer)} ตัว คิดว่าเจ๋งหรอ ตกนรกนะแบบเนี้ย")
    elif answer == code:
        # Import library here? No rule about library in your sheet LMAO.
        import sys
        print("Congratulations! You won the game.")
        sys.exit()
    else:
        for j in range(4):
            if answer_split[j] == code_split[j]:
                check_status[j] = 'pass'
        for k in range(4):
            if check_status[k] == 'pass':
                p += 1
            elif answer_split[k] in code_split:
                v += 1
            else:
                x += 1
        print(f"{' '*10}P={p},V={v},X={x}")
print("Sorry! You just lost it.")
print(f"The answer is  {code}")
print("Please try again...")


