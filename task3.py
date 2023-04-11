
import os
from datetime import datetime

LOG_FILE_NAME = "main.log"

def logger(old_function):

    def new_function(*args, **kwargs):
        with open(LOG_FILE_NAME, 'a', encoding="utf-8") as f:
            f.write(f"{old_function} called at {datetime.now()}\n")
            for a in args:
                f.write(f"{str(a)}\n")
            for k in kwargs.keys():
                f.write(f'"{str(k)}": {str(kwargs[k])}\n')
#            f.write(*args)
            result = old_function(*args, **kwargs)
            f.write(f"{str(result)}\n")
        return result

    return new_function

@logger
def flat_list(lst, res):
    [flat_list(i, res) for i in lst] if isinstance(lst, list) else res.append(lst)

class FlatIterator:

    def __init__(self, list_of_list):
        res = []
        flat_list(list_of_list, res)
        self.list_of_list = iter(res)

    def __iter__(self):
        # ...
        return self

    def __next__(self):
        item = next(self.list_of_list)
        return item


def test_3():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()