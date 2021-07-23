# Write your code here
import random
import sqlite3

class Card: 
    balance = 0
    
    def __init__(self, conn, cursor):
        self.card_number = None
        self.pin =  None 
        self.number_input = None
        self.pin_input = None
        self.card_info = None
        self.luhn_answer = None
        self.card_input = None
        self.conn = conn
        self.cursor = cursor
        
    def default_mode(self): #default mode, you can create an account and log into it
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        action_input = int(input())
        if action_input == 1: 
            Card.create_card(self)
        elif action_input == 2: 
            Card.logging_in(self)
        elif action_input == 0: 
            print('Bye!')
            exit()
            
    def luhn_algo(self): #Luhn algorithm. It creates card number that passes Luhn algorithm
        card_n = 400000000000000 + random.randint(100000000,199999999)
        total_number = 0
        card_num = [int(x) for x in str(card_n)] #card that we've generated in list
        l_number = [int(x) for x in str(card_n)] #list for algorithm
        second_list = []
        for i in range(0, len(l_number), 2): #here the algorithm begins
            l_number[i] *= 2
        for i in l_number: 
            if i > 9: 
                i = i - 9
                second_list.append(i)
            else: 
                second_list.append(i)
        for i in second_list: 
            total_number += i
        required_number = 10 - ((total_number)%10) #here it ends
        if required_number != 10: #here we choose the last number so the card will be valid according to algorithm
            card_num.append(required_number)
            l_num = ''.join(map(str, card_num))
            self.card_number = int(l_num)
        elif required_number == 10: 
            card_num.append(0)
            l_num = ''.join(map(str, card_num))
            self.card_number = int(l_num)            
        
    def create_card(self): #we create card
        password = random.sample(range(1,10), 4)
        pincode = map(str, password)
        pincod = ''.join(pincode)
        self.pin = int(pincod)
        Card.luhn_algo(self)
        self.cursor.execute('INSERT INTO card(number, pin) VALUES (?, ?)',(self.card_number, self.pin))
        self.conn.commit()
        print('Your card has been created')
        print('Your card number:')
        print(self.card_number)
        print('Your card PIN:')
        print(self.pin)
        print()
        Card.default_mode(self)
        
    def logging_in(self): #log into the system
        print('Enter your card number:')
        self.number_input = input()
        print('Enter your card PIN')
        self.pin_input = input()
        Card.checking_card(self)
        
    def checking_card(self): #check that card exists in database
        self.cursor.execute('SELECT number, pin FROM card WHERE number = ? AND pin = ?',(self.number_input, self.pin_input))
        self.conn.commit()
        if self.cursor.fetchone():
            print('You have successfully logged in!')
            Card.logged_in(self)
        elif self.cursor.fetchone() == None:
            print('Wrong card number or PIN!')
            Card.default_mode(self)



    def logged_in(self): #menu of our account
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            action_input_2 = int(input())
            if action_input_2 == 1: #check the balance
                print('Balance: ' + self.cursor.execute('SELECT balance FROM card WHERE number = ?'),(self.number_input,))
                self.conn.commit()
                Card.logged_in(self)
            elif action_input_2 == 2: #adding the income to balance
                print('Enter income')
                income_input = int(input())
                self.cursor.execute('UPDATE card SET balance = balance + ? WHERE number = ?',(income_input, self.number_input))
                self.conn.commit()
                print('Income was added!')
                Card.logged_in(self)
            elif action_input_2 == 3: #transfering money
                Card.money_transfering(self)
            elif action_input_2 == 4: #deleting account from database
                self.cursor.execute('DELETE FROM card WHERE number = ?',(self.card_number,))
                self.conn.commit()
                Card.logged_in(self)
            elif action_input_2 == 5: #log out of account
                print('You have successfully logged out')
                Card.default_mode(self)
            elif action_input_2 == 0: #exit the program
                print('Bye!')
                exit()

    def luhn_algo_check(self, card_check): #we check that card passes the lugn algo (the card that was not created by algo)
        card_num = [int(x) for x in str(card_check)]
        l_number = [int(x) for x in str(card_check)]
        l_number.pop()
        total_number = 0
        second_list = []
        for i in range(0, len(l_number), 2):
            l_number[i] *= 2
        for i in l_number:
            if i > 9:
                i = i - 9
                second_list.append(i)
            else:
                second_list.append(i)
        for i in second_list:
            total_number += i
        checksum = total_number + card_num[-1]
        if checksum % 10 == 0:
            self.luhn_answer = 'yes'
        else:
            self.luhn_answer = 'no'



    def money_transfering(self): #transfer the money
        print('Enter card number:')
        self.card_input = int(input())
        card_in = self.card_input
        Card.luhn_algo_check(self, card_in)
        if self.luhn_answer == 'no': #card doesn't pass luhn, it means that somewhere there is a typo
            print('Probably you made a mistake in the card number. Please try again!')
            Card.logged_in(self)
        if self.luhn_answer == 'yes':
            self.cursor.execute('SELECT number FROM card WHERE number = ?', (self.card_input,))
            self.conn.commit()
            if self.cursor.fetchone(): #card is in database, we transfer money
                print('Enter how much money you want to transfer:')
                money_to_transfer = int(input())
                self.cursor.execute('SELECT balance FROM card WHERE number = ?',(self.number_input,))
                self.conn.commit()
                card_balance = self.cursor.fetchone()
                if card_balance[0] >= money_to_transfer: #everything's okay, we transfer money
                    print('Success!')
                    self.cursor.execute('UPDATE card SET balance = balance - ? WHERE number = ?',(money_to_transfer, self.number_input))
                    conn.commit()
                    self.cursor.execute('UPDATE card SET balance = balance + ? WHERE number = ?',(money_to_transfer, self.card_input))
                    conn.commit()
                    Card.logged_in(self)
                elif card_balance[0] < money_to_transfer: #there is no money to transfer
                    print('Not enough money!')
                    Card.logged_in(self)
            elif self.cursor.fetchone() == None: #card is not in our database
                print('Such a card does not exist.')
                Card.logged_in(self)


#we create the base
conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()
         
#launching our program
card = Card(conn,cursor)
card.default_mode()

