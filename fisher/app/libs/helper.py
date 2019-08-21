# 判断是否为isbn
def is_isbn_or_key(word):
    """
    isbn13 13个由0到9的数组组成
    isbn10 10个由0到9的数组组成，含有一些'-'
    """

    isbn_or_key = False

    # 判断是否为isbn13
    if len(word) == 13 and word.isdigit():
        isbn_or_key = True

    # 判断是否为isbn10
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = True

    return isbn_or_key
