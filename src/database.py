import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

try:
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    print("Connected to the database")

except mysql.connector.Error as error:
    print("Error:", error)

#
# [MARK]: READ OPERATION
#

def readUser(userId : int, userPassword : str, debug : bool = False):
    """
    Gets user data from database. Authenticates for valid userId with password

    Parameters
    ----------
    userId : int
        unique user identifier
    password : str 
        user's password
    debug : bool
        ask for the details of the execution of the query
    
    Returns
    -------
    bool
        True if the port is available.
        False if the port is not available.
    """
    debugMsg = []
    cursor = None
    result = {}
    try:
        connection.start_transaction()
        connection.close
        debugMsg.append("[TRANSACTION START]")
        cursor = connection.cursor()
        debugMsg.append("[CURSOR START]")
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (userId, ))
        debugMsg.append(f"[CURSOR EXECUTE => SELECT * FROM USERS WHERE user_id = {userId}]")            
        user = cursor.fetchone()
        if user:
            debugMsg.append(f"[CURSOR RETURN <= USER<{user[0]}> EXISTS]")
            
            # Password Authentication
            if decryptPassword(userPassword) == user[3]:
                debugMsg.append("[AUTHENTICATION PASSED]")
                result['userId'] = user[0]
                result['userName'] = user[1]
                result['userEmail'] = user[2]
                
            else: 
                debugMsg.append("[AUTHENTICATION FAILED]")
                raise Exception(f"Authentication failed expected : '{user[3]}' got : '{userPassword}'")
                
        else:
            debugMsg.append(f"[CURSOR RETURN <= USER<{userId}> DOES_NOT_EXIST]")
            raise Exception("User with given user_id does not exist") 
        connection.commit()

    except mysql.connector.Error as e:
        connection.rollback()
        debugMsg.append(f"[CONNECTION ERROR => {e}]")
        
        
    except Exception as e:
        connection.rollback()
        debugMsg.append(f"[TRANSACTION ERROR => {e}]")
        
    finally:
        if cursor is not None:
            cursor.close()
            debugMsg.append(f"[CURSOR CLOSED]")
        debugMsg.append("[TRANSACTION CLOSED]")
        if debug:
            return '\n'.join(debugMsg)
        # if result == {}:
            # result = None
        return result
       
def createUser(userData : tuple, debug : bool = False):
    """
    Creates a new user in the database.

    Parameters
    ----------
    userData : tuple
        Tuple containing user data (user_id, username, email, password)
    debug : bool
        ask for the details of the execution of the query
        
    Returns
    -------
    bool
        True if user creation is successful, False otherwise.
    """
    debugMsg = []
    cursor = None
    result = False
    # connection = get_db_connection()
    try:
        connection.start_transaction()
        debugMsg.append("[TRANSACTION START]")
        cursor = connection.cursor()
        debugMsg.append("[CURSOR START]")
        
        # Check for duplicate entry
        cursor.execute("SELECT * FROM Users WHERE email = %s", (userData[2], ))
        debugMsg.append(f"[CURSOR EXECUTE => SELECT * FROM USERS WHERE email= {userData[2]}]")
        user = cursor.fetchone()
        if user:
            raise Exception(f"USER<{userData[2]}> ALREADY EXISTS")
        
        cursor.execute("INSERT INTO Users (user_id, username, email, password) VALUES (%s, %s, %s, %s)", userData)
        debugMsg.append(f"[CURSOR EXECUTE => INSERT INTO USERS {userData}]")
        connection.commit()
        result = True
        
    except mysql.connector.Error as e:
        connection.rollback()
        debugMsg.append(f"[CONNECTION ERROR => {e}]")
        
    except Exception as e:
        connection.rollback()
        debugMsg.append(f"[TRANSACTION ERROR => {e}]")  
    
    finally:
        if cursor is not None:
            cursor.close()
            debugMsg.append(f"[CURSOR CLOSED]")
        debugMsg.append("[TRANSACTION CLOSED]")
        if debug:
            return '\n'.join(debugMsg)
        return result

def updateUser(userId : int, userPassword : str, userData : dict, debug : bool = False):
    """
    Updates user data in the database.

    Parameters
    ----------
    userId : int
        Unique user identifier
    password : str 
        user's password
    userData : dict
        update information in dictionary format. eg: {"username": "newName", ... }
    debug : bool
        ask for the details of the execution of the query
    
    Returns
    -------
    bool
        True if update is successful, False otherwise.
    """
    debugMsg = []
    cursor = None
    result = False
    try:
        connection.start_transaction()
        debugMsg.append("[TRANSACTION START]")
        cursor = connection.cursor()
        debugMsg.append("[CURSOR START]")
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (userId, ))        
        debugMsg.append(f"[CURSOR EXECUTE => SELECT * FROM USERS WHERE user_id = {userId}]") 
        user = cursor.fetchone()
        if user:
            debugMsg.append(f"[CURSOR RETURN <= USER<{userId}> EXISTS]") 
            
            # Password Authentication
            if decryptPassword(userPassword) == user[3]:
                debugMsg.append("[AUTHENTICATION PASSED]")
            else:
                debugMsg.append("[AUTHENTICATION FAILED]")
                raise Exception(f"Authentication failed expected : '{user[3]}' got : '{userPassword}'")
            
            # Update User Data 
            user = list(user)
            for field in userData.keys():
                if field == 'user_id':
                    user[0] = userData.get(field)
                elif field == 'username':
                    user[1] = userData.get(field)
                elif field == 'email':
                    user[2] = userData.get(field)
                elif field == 'password':
                    user[3] = userData.get(field)
                else:
                    pass
            user = tuple(user)[:-1]
        
            # Run query
            cursor.execute("UPDATE Users SET user_id = %s, username = %s, email = %s, password = %s WHERE user_id = %s", (*user, userId))
            debugMsg.append(f"[CURSOR EXECUTE => UPDATE USERS SET <auto> WHERE user_id = {userId}]") 
            result = True
        else:
            debugMsg.append(f"[CURSOR RETURN <= USER<{userId}> DOES_NOT_EXIST]") 
        
        connection.commit()
    
    except mysql.connector.Error as e:
        connection.rollback()
        debugMsg.append(f"[CONNECTION ERROR => {e}]")
        
    except Exception as e:
        connection.rollback()
        debugMsg.append(f"[TRANSACTION ERROR => {e}]")
        
    finally:
        if cursor is not None:
            cursor.close()
            debugMsg.append(f"[CURSOR CLOSED]")
        debugMsg.append("[TRANSACTION CLOSED]")
        if debug:
            return '\n'.join(debugMsg)
        return result

def deleteUser(userId : int, userPassword: str, debug=False):
    """
    Deletes a user from the database.

    Parameters
    ----------
    userId : int
        Unique user identifier
    password : str 
        user's password
    debug : bool
        ask for the details of the execution of the query
    Returns
    -------
    bool
        True if deletion is successful, False otherwise.
    """
    debugMsg = []
    cursor = None
    result = False
    try:
        connection.start_transaction()
        debugMsg.append("[TRANSACTION START]")
        cursor = connection.cursor()
        debugMsg.append("[CURSOR START]")
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (userId, ))
        debugMsg.append(f"[CURSOR EXECUTE => SELECT * FROM USERS WHERE user_id = {userId}]") 
        user = cursor.fetchone()
        if user:
            debugMsg.append(f"[CURSOR RETURN <= USER<{userId}> EXISTS]") 
                        
            # Password Authentication
            if decryptPassword(userPassword) == user[3]:
                debugMsg.append("[AUTHENTICATION PASSED]")
            else:
                debugMsg.append("[AUTHENTICATION FAILED]")
                raise Exception(f"Authentication failed expected : '{user[3]}' got : '{userPassword}'")
            
            # Main delete query
            cursor.execute("DELETE FROM Users WHERE user_id = %s AND password = %s", (userId, userPassword))
            debugMsg.append(f"[CURSOR EXECUTE => DELETE FROM USERS WHERE user_id = {userId}]") 
            result = True
        else:
            debugMsg.append(f"[CURSOR RETURN <= USER<{userId}> DOES_NOT_EXIST]") 
        
        connection.commit()
    
    except mysql.connector.Error as e:
        connection.rollback()
        debugMsg.append(f"[CONNECTION ERROR => {e}]")
        
    except Exception as e:
        connection.rollback()
        debugMsg.append(f"[TRANSACTION ERROR => {e}]")
        
    finally:
        if cursor is not None:
            cursor.close()
            debugMsg.append(f"[CURSOR CLOSED]")
        debugMsg.append("[TRANSACTION CLOSED]")
        if debug:
            return '\n'.join(debugMsg)
        return result

def closeConnection():
    # Close connection
    try:
        if connection.is_connected():
            connection.close()
            print("Connection closed")
    except mysql.connector.Error as error:
        print("Error:", error)
        
def startConnection():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("Connected to the database")

    except mysql.connector.Error as error:
        print("Error:", error)
        
def test_read(debug):
    # NORMAL
    print(readUser(1, "password123", debug))

    # USER_DOES_NOT_EXIST
    print(readUser(12, "password123", debug))

    # AUTH FAIL
    print(readUser(1, "password23", debug))

    # TRANSACTION ERROR
    # unexpected error

    # CONNECTION ERROR
    # closeConnection()
    # print(readUser(1, "password123"))
    
def getAllUsers():
    cursor = None
    users = None
    try:
        connection.start_transaction()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, username, email FROM Users")
        users = cursor.fetchall()
        print()
        print("+","-"*len(str(users[0])))
        for user in users:
            print("|", user)
        print("+","-"*len(str(users[0])))
        print()
        connection.commit()        
        
    except Exception as e:
        print(e)
        connection.rollback()
        
    finally:
        cursor.close()
        return users

def decryptPassword(password : str, secretKey : str = ""):
    return password
    
def encryptPassword(password : str, publicKey : str = ""):
    return password

def test_create_del(debug):
    u1 = (101, "Foreman", "foreman.md@house.com", "foreman.md")
    print("Test Create: ", createUser(u1, debug))
    
    getAllUsers()
    
    print("Test Delete:", deleteUser(101, "foreman.md", debug))


# print("Test Delete:", deleteUser(1001, "foreman.md", True))
# print("Test Delete:", deleteUser(1001, "foreman.md", True))

# test_create_del(True)
# getAllUsers()

updateDict1 = {"email" : "john_doe@example.com", "password" : "password123", "name" : "test"}
updateDict2 = {"email" : "test@example.com", "password" : "password1234", "name" : "test"}
# print(updateUser(1, "password1234", updateDict1, True))

# test_read(True)

getAllUsers()
closeConnection()


# TODO: Add server codes to return 
# """
# TODO: Add input data security
# TODO: Decrypt the password
# """