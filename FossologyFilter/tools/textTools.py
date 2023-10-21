import string

delete_char_set = set(string.punctuation)


def clearn_refer_text(text: str) -> str:
    text = text.lower()
    text = text.replace("\n", " ")
    for i in delete_char_set:
        text.replace(i, "")
    return text


def check_is_independent_token(whole_text: str,
                               sub_text: str):
    """
    检测sub_text在whole_text中是否是一个独立的单词
    :param whole_text:
    :param sub_text:
    :return:
    """
    flag = False
    index = whole_text.index(sub_text)
    while True:
        try:
            if index == 0:
                left_pass = True
            else:
                left_char = whole_text[index - 1]
                if left_char not in string.ascii_letters:
                    left_pass = True
                else:
                    left_pass = False

            if index + len(sub_text) == len(whole_text):
                right_pass = True
            else:
                right_char = whole_text[index + len(sub_text)]
                if right_char not in string.ascii_letters:
                    right_pass = True
                else:
                    right_pass = False
            if left_pass and right_pass:
                flag = True
                break

            index = whole_text.index(sub_text, index + 1)
        except ValueError:
            break
    return flag


if __name__ == '__main__':
    assert check_is_independent_token("under mit", "mit")
    assert not check_is_independent_token("under lmit", "mit")
    assert not check_is_independent_token("under mitl", "mit")
    assert check_is_independent_token("mit under", "mit")
    assert not check_is_independent_token("mitd under", "mit")
    assert not check_is_independent_token("qmit under", "mit")
    assert check_is_independent_token("z mit under", "mit")
    assert not check_is_independent_token("z amit under", "mit")
    assert not check_is_independent_token("z mita under", "mit")
    assert check_is_independent_token("z mita under mit", "mit")
