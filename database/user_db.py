from loader import database,cursor

def add_new_work(user_id,link,numb):
    name = get_student_name(user_id)
    user_ref = get_user_ref(user_id)
    cursor.execute("INSERT INTO Works VALUES(?,?,?,?,?)",(user_id,name,link,numb,user_ref,))
    database.commit()

def check_name_in_file(name):
    with open('студенты.txt', 'r',encoding='utf_8_sig') as file:
        for line in file:
            if name in line.lower():
                return True
    return False

def get_user_ref(user_id):
    cursor.execute("SELECT ref FROM Users WHERE id=?",(user_id,))
    ref_ = cursor.fetchone()[0]
    return ref_

def check_user(user_id):
    cursor.execute("SELECT id FROM Users WHERE id=?", (user_id,))
    user_ = cursor.fetchone()
    if user_ is None:
        return False
    else:
        return True

def add_new_user(user_id,name,ref):
    user_ = check_user(user_id)
    if user_ == False:
        cursor.execute("INSERT INTO Users VALUES(?,?,?)",(user_id,name,ref,))
        database.commit()


def get_all_students(ref):
    cursor.execute("SELECT name,id FROM Users WHERE ref=?",(ref,))
    all_ = cursor.fetchall()
    return all_

def get_student_name(user_id):
    cursor.execute("SELECT name FROM Users WHERE id=?", (user_id,))
    name = cursor.fetchone()[0]
    return name

def get_user_info(user_id):
    cursor.execute("SELECT link FROM Works WHERE id=?",(user_id,))
    all_works = cursor.fetchall()
    if all_works == []:
        return False
    return all_works


def get_all_taken_user_info(ref,numb):
    cursor.execute("SELECT name,link FROM Works WHERE ref=? AND numb=?",(ref,numb,))
    all_works = cursor.fetchall()
    if all_works == []:
        return False
    return all_works