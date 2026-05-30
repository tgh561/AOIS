import pytest
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


def test_hash_func_short_word():
    table = HashTable(20)
    assert table._calc_hash("а") == 0
    assert table._calc_hash("") == 0


def test_hash_func_non_rus_chars():
    table = HashTable(20)
    assert table._calc_hash("xyz") == 0


def test_search_and_insert():
    table = HashTable(23)
    table.insert("Глагол", "Действие")
    table.insert("Существительное", "Предмет")
    
    assert table.insert("Глагол", "Новое Действие") is None
    
    table.insert("Наречие", "Признак действия")
    assert table.search("Наречие") is not None


def test_collision_insertion_and_duplicate():
    table = HashTable(20)
    
    res1 = table.insert("Кот", "Животное 1")
    res2 = table.insert("Кошка", "Животное 2")
    
    assert res1 is not None
    assert res2 is not None
    
    assert res1[0] == res2[0] 
    
    assert table.insert("Кошка", "Дубликат") is None


def test_search_not_found():
    table = HashTable(20)
    table.insert("Кот", "Животное")
    
    assert table.search("Собака") is None
    
    assert table.search("Корабль") is None


def test_delete_scenarios():
    table = HashTable(20)
    
    table.insert("Яблоко", "Фрукт")
    del_res = table.delete("Яблоко")
    assert del_res is not None
    assert del_res[1] == "Яблоко"
    assert table.search("Яблоко") is None  
    
    table.insert("Дом", "Строение")
    table.insert("Дорога", "Путь")
    table.insert("Дочь", "Человек")
    
    del_res_first = table.delete("Дом")
    assert del_res_first is not None
    assert table.search("Дом") is None
    assert table.search("Дорога") is not None  
    assert table.search("Дочь") is not None
    
    del_res_last = table.delete("Дочь")
    assert del_res_last is not None
    assert table.search("Дочь") is None
    assert table.search("Дорога") is not None


def test_delete_not_found():
    table = HashTable(20)
    table.insert("Книга", "Источник знаний")
    assert table.delete("Блокнот") is None


def test_get_fill_factor():
    table = HashTable(10)
    
    assert table.get_fill_factor() == 0.0
    
    table.insert("Мама", "Слово")
    assert table.get_fill_factor() == 0.1
    
    table.insert("Машина", "Транспорт")
    assert table.get_fill_factor() == 0.1
