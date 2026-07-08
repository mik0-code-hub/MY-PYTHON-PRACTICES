# student_list = []
# student_count = 0
# # ADD STUDENT*****
# while True:
#     print('===== Student Management System =====')
#     print('\n1. ADD STUDENT')
#     user_name = input('Enter Name: ')
#     user_id = input('Enter ID: ')
#     user_dept = input('Enter Department: ')
#     user_score = float(input('Enter Score: '))
    
#     student_dict = {
#         'student_name':   user_name,
#         'student_id':   user_id,
#         'student_dept':   user_dept,
#         'student_score':   user_score
#     }
#     student_list.append(student_dict)
#     student_count += 1
#     if student_count == 3:
#         break
#     print('Student added successfully!..')

# # REMOVE STUDENT*****
# print('\n=== REMOVE A STUDENT ===')
# remove_student = input('Enter the Student you wish to remove: ')

# for student in student_list:
#     if student['student_name'] == remove_student:
#         student_list.remove(student)
#         print(f"The Student {student} has been removed Successfully..")
#         break

# # SEARCH STUDENT*****
# print()
# print(f"---> CONFIRM THAT THE STUDENT {remove_student} HAS BEEN REMOVED.")
# for student in student_list:
#     if student['student_name'] == remove_student:
#         print('STATUS: Student Found.')
#         break
# else:
#     print('STATUS: Student Not Found.')

# # DISPLAY ALL STUDENTS
# print('\n==== DISPLAY ALL REMAINING STUDENT ====')
# for student in student_list:
#     print(student)

# # CALCULATING AVG. SCORE
# print()
# print('===== THE AVG. SCORE OF THE STUDENTS =====')
# total_score = 0
# for student in student_list:
#     score = student['student_score']
#     total_score += score
# avg_score = total_score / len(student_list)
# print(f"Their Average Score is: {avg_score}.")
# print('\nEXITING SYSTEM. GoodBye.')

################################
################################

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. Search Student")
    print("4. Display All Students")
    print("5. Calculate Average Score & Exit\n")
    student_master_list = []
    
    choice = input("Enter your Choice (1-5): ")
    if choice =='1':
        name = input('Enter Name: ')
        id = input('Enter ID: ')
        dept = input('Enter your Department: ')
        score = input('Enter your Score: ')
        student_card = {
            'student_name':   name,
            'student_id':   id,
            'student_dept':   dept,
            'student score':   score 
        }
        student_master_list.append(student_card)
        print('Student has been added Successfully.\n')
    elif choice == '2':
        remove_student = input('Enter the name of Student you wish to Remove: ')
        for student in student_master_list:
            if student['student_name'] == remove_student:
                student_master_list.remove(student)
                print(f"The student {student} has been Removed Successfully.")
        else:
            print('STATUS: Student Not Found.\n')
    elif choice == '3':
        search_student = input('Enter the Student you want to Search: ')
        for student in student_master_list:
            if student['student_name'] == search_student:
                print('\n----- Student Found! -----')
                print(f"Name: {student['student_name']}")
                print(f"ID: {student['student_id']}")
                print(f"Department: {student['student_dept']}")
                print(f"Score: {student['student_score']}")
                break
        else:
            print("\nSTATUS: Student Not Found in Our Database.")
            print()
    elif choice == '4':
        print('==== ALL REGISTERED STUDENTS ====')
        for student in student_master_list:
            print(student)
            print()
    elif choice == '5':
        total_score = 0
        student_count = 0
        for student in student_master_list:
            # TODO: A for loop to loop thru stud_mast_list
            # TODO: Add up the Scores and count student inside the loop
            # TODO: Out of this loop, divide total/count, Print average