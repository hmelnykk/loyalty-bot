import pymysql
import aiomysql

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='loyaltyBot@localhost',
    password='beLoyalBeHumble',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with connection.cursor() as cursor:
        # Create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS loyalty_bot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        # Select the database
        cursor.execute("USE loyalty_bot_db;")
        
        # Create the users table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            chatId INT,
            name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            surname VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            studentCardPhotoId LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            loyaltyLevel INT,
            loyaltyPoints INT,
            isVerified BOOLEAN
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        cursor.execute(create_table_query)

    connection.commit()
    print("Database and table created successfully.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    connection.close()


async def add_new_user(new_user):
    async with aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='loyaltyBot@localhost',
        password='beLoyalBeHumble',
        db='loyalty_bot_db',
        charset='utf8mb4'
    ) as pool:
        
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                sql = """
                INSERT INTO `users` (name, surname, chatId, studentCardPhotoId, loyaltyLevel, loyaltyPoints, isVerified) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                data = (new_user['name'], new_user['surname'], new_user['chat_id'], 
                        new_user['studentCardPhotoId'], 0, 0, False)
                
                try:
                    await cursor.execute(sql, data)
                    await connection.commit()
                    print("New user added successfully.")
                except aiomysql.MySQLError as e:
                    print(f"Error: {e}")

async def is_user_in_database(chat_id):
    ...

async def get_unverified():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='loyaltyBot@localhost',
        password='beLoyalBeHumble',
        database='loyalty_bot',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Execute the query to fetch unverified users
            sql = "SELECT * FROM `users` WHERE 'isVerified' = %s"
            cursor.execute(sql, (0,))  # Parameterized query to prevent SQL injection
            
            # Fetch all results
            users = cursor.fetchall()
            
            print(users)
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None
    finally:
        connection.close()