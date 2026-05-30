from .hash_row import HashRow

class HashTable:
    def __init__(self, size: int = 20):
        self.size = size
        self.rows = [HashRow(i) for i in range(self.size)]

    def _calc_hash(self, key_word: str) -> int:
        if len(key_word) < 2:
            key_word += "а" * (2 - len(key_word))

        rus_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

        char1_index = max(rus_alphabet.find(key_word[0].lower()), 0)
        char2_index = max(rus_alphabet.find(key_word[1].lower()), 0)

        return char1_index * 33 + char2_index

    def _define_index(self, hash: int) -> int:
        return hash % self.size

    def _fill_row(self, row, id, value):
        """Заполняет новую строку (по умолчанию терминальная)."""
        row.id = id
        row.c = 0
        row.u = 1
        row.t = 1          # новая строка всегда терминальная (next == None)
        row.l = 0
        row.d = 0
        row.pi = value
        row.next = None
        return row

    def insert(self, key_word: str, value: str):
        hash_value = self._calc_hash(key_word)
        hash_address = self._define_index(hash_value)

        curr_row = self.rows[hash_address]

        # Строка свободна
        if curr_row.u == 0:
            self._fill_row(curr_row, key_word, value)
            return hash_address, key_word, value

        # Ищем конец цепочки и проверяем наличие дубликата
        temp = curr_row
        while temp:
            if temp.id == key_word and temp.d == 0:
                return None               # ключ уже существует
            if temp.next is None:
                break
            temp = temp.next

        # Сейчас temp указывает на последний элемент цепочки
        # Он перестаёт быть терминальным, т.к. мы добавим новый
        if temp.t == 1:
            temp.t = 0

        new_row = HashRow(hash_address)
        self._fill_row(new_row, key_word, value)
        new_row.c = 1                     # признак коллизии
        temp.next = new_row

        return hash_address, key_word, value

    def search(self, key_word: str):
        hash_value = self._calc_hash(key_word)
        hash_address = self._define_index(hash_value)

        curr_row = self.rows[hash_address]

        while curr_row:
            if curr_row.id == key_word and curr_row.d == 0:
                return hash_address, curr_row.id, curr_row.pi
            curr_row = curr_row.next

        return None

    def delete(self, key_word: str):
        hash_value = self._calc_hash(key_word)
        hash_address = self._define_index(hash_value)

        curr_row = self.rows[hash_address]
        prev_row = None

        while curr_row:
            if curr_row.id == key_word and curr_row.d == 0:
                # Нашли удаляемый элемент
                if prev_row is None:
                    # Удаляем первый элемент в цепочке
                    if curr_row.next:
                        # Есть следующий — копируем его содержимое в текущий
                        next_row = curr_row.next
                        curr_row.id = next_row.id
                        curr_row.pi = next_row.pi
                        curr_row.next = next_row.next
                        curr_row.c = next_row.c
                        # Пересчитываем терминальный флаг для curr_row
                        curr_row.t = 1 if curr_row.next is None else 0
                    else:
                        # Цепочка состояла из одного элемента — помечаем как удалённый
                        curr_row.d = 1
                        curr_row.u = 0
                        curr_row.id = ""
                        curr_row.pi = ""
                        curr_row.t = 0    # неактивная строка — не терминальная
                        curr_row.c = 0
                else:
                    # Удаляем не первый элемент
                    prev_row.next = curr_row.next
                    # Если после удаления prev_row стал последним — обновляем его t
                    if prev_row.next is None:
                        prev_row.t = 1
                return hash_address, key_word, curr_row.pi

            prev_row = curr_row
            curr_row = curr_row.next

        return None

    def get_fill_factor(self) -> float:
        filled = sum([1 for row in self.rows if row.u == 1])
        return filled / self.size