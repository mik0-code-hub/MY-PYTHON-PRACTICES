class Book:
    def __init__(self, title, author, ISBN, availability_status=True):
        # Written by mik0-logic™
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.status = availability_status
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        # Written by mik0-logic™
    
    def add_book(self, book):
        self.books.append(book)
    def add_member(self, member):
        self.members.append(member)
        ### === Special Methods ===
    def __str__(self):
        return f"Library with {len(self.books)} books."
    def __len__(self):
        return len(self.books)
    def __contains__(self, title):
        for books in self.books:
            if books.title.lower() == title.lower():
                return True     # Found it!
        return False     # After no match was Found.
    def __iter__(self):
        return iter(self.books)
    
my_library = Library()
while True:
    # Written by mik0-logic™
    print('===== Library Menu =====')
    print('1. Add a book')
    print('2. Register a member')
    print('3. Borrow a book')
    print('4. Return a book')
    print('5. Show library status')
    print('6. Exit')
    print('==================\n')
    try:
        choice = input('Pick a Menu Option (1 to 6): ')
    except ValueError:
        print('Please enter a Valid Number!')
    
    if choice == '1':
        print('--- ADD BOOK(S) ---')
        title = input('Enter book title: ')
        author = input('Enter book author: ')
        ISBN = input('Enter book ISBN: ')
        # Written by mik0-logic™
        # Package into a Book object
        new_book = Book(title, author, ISBN)
        my_library.add_book(new_book)
        print(f"Success!\n'{title}' has been added to the Library.")

    elif choice == '2':
        print('--- REGISTER MEMBER(S) ---')
        name = input('Enter member name: ')
        ### In the case of Invalid Characters.....
        if not name.replace(" ", "").isalpha():
            print('Invalid name! Please use letters and spaces ONLY.')
        else:
            member_id = input('Enter ID: ')
            new_member = Member(name, member_id)
            my_library.add_member(new_member)
            print(f"A member '{name}' with an ID {member_id} has been Registered Successfully!")

    elif choice == '3':
        print('--- BORROW BOOK(S) ---')
        member_id = input('Enter your Member ID: ')
        title = input('Enter the Title of the Book you wish to Borrow: ')
        found_book = None
        found_member = None
        for book in my_library.books:
            if book.title == title:
                found_book = book
                break
        for member in my_library.members:
            if member.member_id == member_id:
                found_member = member
                break
        # Written by mik0-logic™
        if found_book != None and found_member != None:
            if found_book.status == True:
                found_member.borrowed_books.append(found_book)
                found_book.status = False
                print(f"Success! {found_member.name} borrowed '{found_book.title}'.")
            else:
                print(f"Sorry, '{found_book.title}' is currently Checked Out!")
        else:
            print('ERROR! Could not find matching Member ID or Book Title.')

    elif choice == '4':
        print('--- RETURN BOOK(S) ---')
        member_id = input('Enter your Member ID: ')
        title = input('Enter Title of Book you wish to return: ')
        found_book = None
        found_member = None
        for member in my_library.members:
            if member.member_id == member_id:
                found_member = member
                break
        if found_member != None:
            for book in found_member.borrowed_books:
                if book.title == title:
                    found_book = book
                    break
        if found_member != None and found_book != None:
            found_member.borrowed_books.remove(found_book)
            found_book.status = True
            print(f"Success! {found_member.name} returned '{found_book.title}'.")
        else:
            print('ERROR: Could not process return.\nCheck Member ID or Book title.')

    elif choice == '5':
        # Written by mik0-logic™
        print('===== LIBRARY STATUS =====')
        for book in my_library.books:
            print(f"Title: {book.title} | Available: {book.status}")
            print()
            print(f"Name: {member.name} | ID: {member.member_id} | Borrowed: {len(member.borrowed_books)} books.")

    elif choice == '6':
        print('--- EXITING ---')
        print('Thank you for using the Library System.\nGoodbye!')

    else:
        print('Invalid Choice!\nPlease select an Option from (1 to 6).')

        