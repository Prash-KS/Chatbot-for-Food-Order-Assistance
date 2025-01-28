import aiomysql


async def insert_order_tracking(order_id, status):
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="root",
        db="food_db",
        minsize=1,
        maxsize=5
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
            await cursor.execute(query, (order_id, status))
            await conn.commit()

    pool.close()
    await pool.wait_closed()


async def get_total_order_price(order_id):
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="root",
        db="food_db",
        minsize=1,
        maxsize=5
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            query = f"SELECT get_total_order_price({order_id})"
            await cursor.execute(query)
            result = await cursor.fetchone()

    pool.close()
    await pool.wait_closed()

    if result:
        return result[0]
    return 0


async def insert_order_item(food_item: str, quantity: int, order_id: int):
    try:
        pool = await aiomysql.create_pool(
            host="localhost",
            user="root",
            password="root",
            db="food_db",
            minsize=1,
            maxsize=5
        )

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.callproc('insert_order_item', (food_item, quantity, order_id))
                await conn.commit()

        pool.close()
        await pool.wait_closed()

        return 1

    except aiomysql.Error as err:
        print(f"Error inserting order item: {err}")
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1


async def get_next_order_id():
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="root",
        db="food_db",
        minsize=1,
        maxsize=5
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            query = "SELECT MAX(order_id) FROM orders"
            await cursor.execute(query)
            result = await cursor.fetchone()

    pool.close()
    await pool.wait_closed()

    if result and result[0]:
        return result[0] + 1
    return 1


async def get_order_status(order_id: int):
    pool = await aiomysql.create_pool(
        host="localhost",
        user="root",
        password="root",
        db="food_db",
        minsize=1,
        maxsize=5
    )

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            query = "SELECT status FROM order_tracking WHERE order_id = %s"
            await cursor.execute(query, (order_id,))
            result = await cursor.fetchone()

    pool.close()
    await pool.wait_closed()

    if result:
        return result[0]
    return None
