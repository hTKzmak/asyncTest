import pytest
import asyncio
import aiohttp
import sqlite3
import threading

# 1. Напишите асинхронный тест, который проверяет, что функция,
# которая возвращает promise(future), разрешается с ожидаемым значением.
# Используйте фикстуру event_loop для создания цикла событий и
# декоратор pytest.mark.asyncio для пометки теста как асинхронного.
async def async_func():
    await asyncio.sleep(1)
    return 'smth'

@pytest.mark.asyncio
async def test_resolve(event_loop):
    result = await async_func()
    assert result == 'smth'


# 2. Напишите асинхронный тест, который проверяет, что функция,
# которая возвращает промис, отклоняется с ожидаемым исключением.
# Используйте фикстуру event_loop для создания цикла событий и
# декоратор pytest.mark.asyncio для пометки теста как асинхронного.
async def also_my_function():
    await asyncio.sleep(1)
    raise ValueError("Expected exception")

@pytest.mark.asyncio
async def test_future_resolution(event_loop):
    with pytest.raises(ValueError) as exc_info:
        await also_my_function()
    assert str(exc_info.value) == "Expected exception"


# 3. Напишите асинхронный тест, который проверяет, что функция,
# которая выполняет HTTP-запрос к внешнему API, возвращает
# корректный ответ. Используйте библиотеку aiohttp для выполнения
# асинхронных HTTP-запросов и фикстуру event_loop для создания цикла событий.

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/photos/1') as response:
            return await response.json()

@pytest.mark.asyncio
async def test_http_request(event_loop):
    data = await fetch_data()
    assert data['title'] == "accusamus beatae ad facilis cum similique qui sunt"
    assert data['url'] == "https://via.placeholder.com/600/92c952"



# 4. Напишите асинхронный тест, который проверяет, что функция,
# которая работает с базой данных, корректно добавляет новую запись.
# Используйте библиотеку aiopg(aiocpg) для работы с PostgreSQL или aiosqlite
# для работы с SQLite 3 и фикстуру event_loop для создания цикла событий.

async def insert_data():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tablePeople (name TEXT, age INT)")
    cursor.execute("INSERT INTO tablePeople (name, age) VALUES ('Jade', 23)")
    conn.commit()
    conn.close()

@pytest.mark.asyncio
async def test_database_insert(event_loop):
    await insert_data()
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tablePeople WHERE name='Jade' AND age=23")
    result = cursor.fetchone()
    conn.close()
    assert result is not None

# 5. Напишите асинхронный тест, который проверяет, что функция,
# которая запускает другую асинхронную функцию в отдельном потоке,
# корректно возвращает результат. Используйте библиотеку asyncio
# для работы с асинхронностью и фикстуру event_loop для создания цикла событий.


async def sync_func():
    await asyncio.sleep(1)
    return "asynchrony"

def run_async_function():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(sync_func())
    loop.close()
    return result

def test_run_async_function(event_loop):
    result = run_async_function()
    assert result == "asynchrony"