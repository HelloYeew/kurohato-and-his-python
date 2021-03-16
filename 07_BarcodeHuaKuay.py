# Prog-07: EAN-13 BarKuayHuaCode
# 6310545566 Hanasakigawa Girls' High School Best Programmer Name Phawit Pornwattanakul (Class 2-A)

import math
import matplotlib.pyplot as plt


# ขีดอีกแล้ว ขีดอยู่นั่นแหละ ที่บ้านไม่มีขีดให้เล่นอ่อ
def show_barcode(digits, ean13_code):
    x = [[int(e) for e in ean13_code]]
    plt.axis('off')
    plt.imshow(x, aspect='auto', cmap='binary')
    plt.title(digits)
    plt.show()


# ขีดอีกแล้ว ขีดอยู่นั่นแหละ ที่บ้านไม่มีขีดให้เล่นอ่อ
def test1():
    digits = input('Enter a 13-digit number: ')
    codes = encode_EAN13(digits)
    if codes == '':
        print(digits, 'is not an EAN-13 number.')
    else:
        decoded_digits = decode_EAN13(codes)
        if decoded_digits == digits:
            show_barcode(digits, codes)
        else:
            print('Error in decoding.')


# ขีดอีกแล้ว ขีดอยู่นั่นแหละ ที่บ้านไม่มีขีดให้เล่นอ่อ
L_codes = ['0001101', '0011001', '0010011', '0111101', '0100011',
           '0110001', '0101111', '0111011', '0110111', '0001011']
G_codes = ['0100111', '0110011', '0011011', '0100001', '0011101',
           '0111001', '0000101', '0010001', '0001001', '0010111']
R_codes = ['1110010', '1100110', '1101100', '1000010', '1011100',
           '1001110', '1010000', '1000100', '1001000', '1110100']


# ขีดอีกแล้ว ขีดอยู่นั่นแหละ ที่บ้านไม่มีขีดให้เล่นอ่อ

def check_group1(digits):
    """
    Input : Barcode
    Return : L/G/R
    """
    first = digits[0]
    first = int(first)
    if first == 0:
        return 'LLLLLL'
    elif first == 1:
        return 'LLGLGG'
    elif first == 2:
        return 'LLGGLG'
    elif first == 3:
        return 'LLGGGL'
    elif first == 4:
        return 'LGLLGG'
    elif first == 5:
        return 'LGGLLG'
    elif first == 6:
        return 'LGGGLL'
    elif first == 7:
        return 'LGLGLG'
    elif first == 8:
        return 'LGLGGL'
    else:
        return 'LGGLGL'


def return_group1(code_check):
    """
    Input : L/G/R 6 character
    Return : First digits of barcode
    """
    if code_check == 'LLLLLL':
        return 0
    elif code_check == 'LLGLGG':
        return 1
    elif code_check == 'LLGGLG':
        return 2
    elif code_check == 'LLGGGL':
        return 3
    elif code_check == 'LGLLGG':
        return 4
    elif code_check == 'LGGLLG':
        return 5
    elif code_check == 'LGGGLL':
        return 6
    elif code_check == 'LGLGLG':
        return 7
    elif code_check == 'LGLGGL':
        return 8
    else:
        return 9


def digits_from(codes):
    """
    Input : Unicode
    Output : L/G/R to translate
    """
    index = 0
    list_code = []
    while index <= len(codes) - 1:
        list_code.append(codes[index:index + 7])
        index += 7
    result = ''
    for code in list_code:
        if code in L_codes:
            result += 'L'
        elif code in G_codes:
            result += 'G'
        elif code in R_codes:
            result += 'R'
        else:
            result = ''
    return result


def codes_of(digits, patterns):
    """
    คืน codes ของเลขแต่ละตัวใน digits ที่เข้ารหัสตามรูปแบบที่กำหนดใน patterns ตามลำดับ
    หมายเหตุ: digits และ patterns มีความยาวเท่ากันแน่ ๆ

    Doctest :
        >>> codes_of('45', 'LG')
        '01000110111001'
    """
    result = ''
    for i in range(len(patterns)):
        if patterns[i] == 'L':
            result += L_codes[int(digits[i])]
        elif patterns[i] == 'G':
            result += G_codes[int(digits[i])]
        elif patterns[i] == 'R':
            result += R_codes[int(digits[i])]
    return result


def digits_of(codes):
    """
    คืน digits ของรหัสต่าง ๆ ใน codes
    ถ้า codes ที่ได้รับมีบางรหัสภายในแปลงไม่ได้ ให้คืนสตริงว่าง

    Doctest :
        >>> digits_of('01000110111001')
        '45'
        >>> digits_of('01000111111111')
        ''
    """
    index = 0
    list_code = []
    while index <= len(codes) - 1:
        list_code.append(codes[index:index + 7])
        index += 7
    result = ''
    for code in list_code:
        if code in L_codes:
            result += str(L_codes.index(code))
        elif code in G_codes:
            result += str(G_codes.index(code))
        elif code in R_codes:
            result += str(R_codes.index(code))
        else:
            result = ''
    return result


def patterns_of(codes):
    """
    คืน patterns ของรหัสต่าง ๆ ใน codes
    ถ้า codes ที่ได้รับมีรหัสที่ไม่อยู่ในรูปแบบใด ให้คืนสตริงว่าง

    Doctest :
        >>> patterns_of('01000110111001')
        'LG'
        >>> patterns_of('01000111111111')
        ''
    """
    code_1 = codes[0:7]
    code_2 = codes[7:]
    list_code = [code_1, code_2]
    result = ''
    for code in list_code:
        if code in L_codes:
            result += 'L'
        elif code in G_codes:
            result += 'G'
        elif code in R_codes:
            result += 'R'
        else:
            result = ''
    return result


def check_digit(digits):
    """
    คืน check digit ที่คำนวณจากเลข 12 หลักที่ได้รับใน digits ตามมาตรฐานของ EAN-13
    หมายเหตุ: digits เป็นสตริงที่มี 12 หลักแน่ ๆ

    Doctest :
        >>> check_digit('321029204519')
        '2'
        >>> check_digit('123456789018')
        '0'
    """
    digits_list = list(digits)
    second_digits = []
    for i in range(6):
        second_digits.append(1)
        second_digits.append(3)
    summation = 0
    for i in range(len(digits_list)):
        calculate = int(digits_list[i]) * int(second_digits[i])
        summation += calculate
    if summation % 10 == 0:
        multiply_ten = summation
    else:
        multiply_ten = ((summation // 10) + 1) * 10
    return str(multiply_ten - summation)


def encode_EAN13(digits):
    """
    คืนสตริงของ 0 และ 1 ความยาว 95 ตัว ที่ได้มาจากการเข้ารหัสเลขใน digits แบบ EAN-13
    ถ้าเกิดกรณีต่อไปนี้ ให้คืนสตริงว่าง
     พบตัวที่ไม่ใช่ตัวเลขใน digits
     digits มีไม่ครบ 13 หลัก
     check digit ใน digits ไม่ตรงกับที่ควรจะเป็น

    Doctest :
        >>> encode_EAN13('1234')
        ''
        >>> encode_EAN13('one-two-33333')
        ''
        >>> encode_EAN13('1111111111111')
        ''
        >>> encode_EAN13('3210292045192')
        '10100100110011001010011100110110010111001001101010111001010111001001110110011011101001101100101'
    """
    result = ''
    try:
        if len(digits) != 13:
            return ''
        elif check_digit(digits[0:12]) != digits[-1]:
            return ''
        else:
            result += '101'
            letter_group1 = check_group1(digits)
            result += codes_of(digits[1:7], letter_group1)
            result += '01010'
            result += codes_of(digits[7:13], 'RRRRRR')
            result += '101'
            return result
    except:
        return ''


def decode_EAN13(codes):
    """
    คืนสตริงของเลขที่ได้จากการถอดรหัสจากสตริง 0/1 ที่เก็บใน codes แบบ EAN-13
    ถ้าเกิดกรณีต่อไปนี้ ให้คืนสตริงว่าง (สาเหตุเหล่านี้มักมาจากเครื่องอ่านบาร์โค้ดอ่านรหัส 0 และ 1 มาผิด)
     codes เก็บจำนวนบิต หรือรูปแบบไม่ตรงข้อกำหนด
     รหัสบางส่วนแปลงเป็นตัวเลขไม่ได้
     เลขหลักที่ 13 ที่อ่านได้ ไม่ตรงกับค่า check digit ที่คำนวณได้
    หมายเหตุ: เป็นไปได้ว่า ผู้ใช้เครื่องบาร์โค้ด อาจสแกนบาร์โค้ดที่วางกลับหัวก็ได้ ฟังก์ชันนี้ก็ต้องรองรับกรณีเช่นนี้ด้วย

    Doctest :
        >>> c = '10100100110011001010011100110110010111001001101010111001010111001001110110011011101001101100101'
        >>> decode_EAN13(c)
        '3210292045192'
        >>> c = '10111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111101'
        >>> decode_EAN13(c)
        ''
    """
    result = ''
    try:
        if len(codes) != 95:
            return ''
        else:
            number_group1 = digits_of(codes[3:45])
            code_group1 = digits_from(codes[3:45])
            number_group2 = digits_of(codes[50:-3])
            code_group2 = digits_from(codes[50:-3])
            if code_group2 == 'RRRRRR':
                result = str(return_group1(code_group1)) + number_group1 + number_group2
            elif code_group1 == 'RRRRRR':
                result = str(return_group1(code_group1)) + number_group1 + number_group2
            else:
                # Support when barcode reader read a barcode upside down
                reverse_codes = codes
                reverse_codes.reverse()
                number_group1 = digits_of(codes[3:45])
                code_group1 = digits_from(codes[3:45])
                number_group2 = digits_of(codes[50:-3])
                code_group2 = digits_from(codes[50:-3])
                if code_group2 == 'RRRRRR':
                    result = str(return_group1(code_group1)) + number_group1 + number_group2
                elif code_group1 == 'RRRRRR':
                    result = str(return_group1(code_group1)) + number_group1 + number_group2
            return result
    except:
        return ''


# ขีดอีกแล้ว ขีดอยู่นั่นแหละ ที่บ้านไม่มีขีดให้เล่นอ่อ
test1()
