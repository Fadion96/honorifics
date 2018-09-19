class TextSwapperInMark(object):
    """Swap text in mark A|text|B|text|C , default to {*}text{*text}"""

    def __init__(self, begin_mark: str = '{*}', middle_mark: str = '{*', end_mark: str = '}'):
        self.begin_mark = begin_mark
        self.middle_mark = middle_mark
        self.end_mark = end_mark

    def __swap_in_mark(self, text: str, pos: int) -> (str, int):
        # Prefixes s_ - start of, e_ - end_of
        e_begin_mark = pos + len(self.begin_mark)

        s_middle_mark = text.find(self.middle_mark, e_begin_mark)
        e_middle_mark = s_middle_mark + len(self.middle_mark)

        s_end_mark = text.find(self.end_mark, e_middle_mark)
        e_end_mark = s_end_mark + len(self.end_mark)

        swapped = self.begin_mark + text[e_middle_mark:s_end_mark] + self.middle_mark + \
                  text[e_begin_mark:s_middle_mark] + self.end_mark

        return swapped, e_end_mark

    def swap(self, text: str) -> str:
        pos = 0
        new_text = []

        while True:
            begin_mark = text.find(self.begin_mark, pos)
            if begin_mark != -1:
                (swapped, end_mark) = self.__swap_in_mark(text, begin_mark)

                new_text.append(text[pos:begin_mark])
                new_text.append(swapped)

                pos = end_mark
            else:
                break

        return ''.join(new_text) + text[pos:]
