import mysql.connector

class Init:
    def __init__(self):
        conn = mysql.connector.connect(host = 'localhost', user = 'root', password = '12345678')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Student_Election;")
        cursor.execute("USE Student_Election;")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id varchar(10) PRIMARY KEY UNIQUE, voter_Adno char(6), status BOOLEAN DEFAULT 0);")
        cursor.execute("CREATE TABLE IF NOT EXISTS voters(barcode char(6) PRIMARY KEY UNIQUE, Name varchar(100), voting_status BOOLEAN NOT NULL DEFAULT 0);")
        cursor.execute("CREATE TABLE IF NOT EXISTS candidates(Adno char(6) PRIMARY KEY, Name varchar(100), Symbol varchar(50), Standing_For varchar(50), picture BLOB, votes INTEGER DEFAULT 0);")
        conn.commit()
        conn.close()
