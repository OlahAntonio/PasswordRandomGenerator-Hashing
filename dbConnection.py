import mysql.connector
import bcrypt

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Passwords",
    )

def hash_password(password):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")

def save_password(password):
    password_hash = hash_password(password)
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO user_passwords (password, password_hash)
        VALUES (%s, %s)
        """,
        (password, password_hash),
    )
    connection.commit()
    inserted_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return inserted_id, password_hash

def delete_password(password_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        DELETE FROM user_passwords
        WHERE id = %s
        """,
        (password_id,),
    )
    deleted_rows = cursor.rowcount
    if deleted_rows > 0:
        cursor.execute(
            """
            UPDATE user_passwords 
            SET id = id - 1 
            WHERE id > %s
            """,
            (password_id,),
        )

        cursor.execute("SELECT MAX(id) FROM user_passwords")
        result = cursor.fetchone()
        max_id = result[0] if result[0] is not None else 0
        next_id = max_id + 1
        cursor.execute(f"ALTER TABLE user_passwords AUTO_INCREMENT = {next_id}")
    connection.commit()
    cursor.close()
    connection.close()
    return deleted_rows
