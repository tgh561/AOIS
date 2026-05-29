from src.hash_row import HashRow
from src.hash_table import HashTable


def test_table_create():
    size = 23
    table = HashTable(size)

    assert len(table.rows) == size


def test_hash_func():
    table = HashTable(23)

    word = "бВ"

    word_hash1 = 33 * 1 + 2
    word_hash2 = table._calc_hash(word)

    assert word_hash1 == word_hash2


def test_search_and_insert():
    table = HashTable(23)

    table.insert("Глагол", "Действие")
    table.insert("Существительное", "Предмет")
    table.insert("Существительное", "Предмет")
    table.insert("Наречие", "Признак действия")

    assert table.search("Наречие") is not None

def delete(self, key_word: str):
    hash_value = self._calc_hash(key_word)
    hash_address = self._define_index(hash_value)

    curr_row = self.rows[hash_address]
    prev_row = None

    while curr_row:
        if curr_row.id == key_word and curr_row.d == 0:

            deleted_value = curr_row.pi

            if prev_row is None:

                if curr_row.next:
                    next_row = curr_row.next

                    curr_row.id = next_row.id
                    curr_row.pi = next_row.pi
                    curr_row.next = next_row.next
                    curr_row.c = next_row.c

                else:
                    curr_row.d = 1
                    curr_row.u = 0
                    curr_row.id = ""
                    curr_row.pi = ""

            else:
                prev_row.next = curr_row.next

            return hash_address, key_word, deleted_value

        prev_row = curr_row
        curr_row = curr_row.next

    return None