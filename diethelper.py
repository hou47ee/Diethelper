import sqlite3
from sqlite3 import IntegrityError
import getpass

conn = sqlite3.connect('D:/NCU/senior/first/database/midterm_project/diethelper.db')
cur = conn.cursor()


def nutrient(Food): #印出食品營養素含量
    data = cur.execute("""SELECT * FROM food_nutrient WHERE Name like '{}';""".format(Food)).fetchone() #搜尋食品
    print("\n食品名稱: {}".format(data[2]))
    print("食品類別: {}".format(data[1]))
    
    print("\n\t\t每 100.0g 含量")
    print("---------------------------------")
    for j in range(3,9):
        if data[j] is None:
            d = "No Data" #若資料為 None
        else:
            d = round(data[j],1)
        if(j == 3):
            print("熱量:\t\t{}\t(kcal)".format(d))
        elif(j == 4):
            print("碳水化合物:\t{}\t(g)".format(d))
        elif(j == 5):
            print("蛋白質:\t\t{}\t(g)".format(d))
        elif(j == 6):
            print("脂肪:\t\t{}\t(g)".format(d))
        elif(j == 7):
            print("糖:\t\t{}\t(g)".format(d))
        elif(j == 8):
            print("膳食纖維:\t{}\t(g)".format(d))
    print("---------------------------------\n")
    while(1): # 依使用者輸入的公克數計算對應營養素含量
        
        try:
            weight = float(input("欲計算重量 (g) [預設 100.0g] [-1: 回上層]: "))     
        except ValueError:
            print("\n[輸入無效, 請輸入數字]")
            continue    
                
        if(weight == -1): #回上層
            break
            
        if(weight < 0):
                print("\n[輸入無效, 請輸入數字]")
                continue
        
        if(weight):
            print("\n\n\t\t每 {}g 含量".format(weight))
            print("---------------------------------")
            for j in range(3,9):
                if data[j] is None:
                    d = "No Data"
                else:
                    d = round(data[j]*weight*0.01,1)
                if(j == 3):
                    print("熱量:\t\t{}\t(kcal)".format(d))
                elif(j == 4):
                    print("碳水化合物:\t{}\t(g)".format(d))
                elif(j == 5):
                    print("蛋白質:\t\t{}\t(g)".format(d))
                elif(j == 6):
                    print("脂肪:\t\t{}\t(g)".format(d))
                elif(j == 7):
                    print("糖:\t\t{}\t(g)".format(d))
                elif(j == 8):
                    print("膳食纖維:\t{}\t(g)".format(d))
                    print("---------------------------------")
        else:
            continue
        
def search():
    
    while(1):
        s = input("\n選擇查詢方式: 0. 輸入食品名稱 1. 食品類別 -1. 回上層\n")
        
        if(s == "0"):
            while(1):
                name = input("\n請輸入食品名稱  [-1 回上層]: ")
                
                #搜尋所有含此關鍵字的食品並放入 list All
                All = cur.execute("""SELECT Name FROM food_nutrient WHERE Name like '%{}%' ;""".format(name)).fetchall()
                
                if(name == "-1"): # 回上層
                    break
                
                if(not All): # All為空, 沒有此食品
                    print("\n[查無此物, 請重新輸入]")
                    continue
                
                if(len(All) != 1): # 如果包含此關鍵字的食品不只一個, 列出全部
                    
                    while(1):
                        print("---------------------------------")
                        for i in range(len(All)):
                            print("{}.\t{}".format(i,All[i][0]))
                        print("\n-1. 回上層")
                        print("---------------------------------")
                        print("\n請選擇欲查詢食品之號碼:\n")
                        
                        food = input() # 輸入欲查詢食品的號碼
                        
                        if(food == "-1"): # 回上層
                            break
                        
                        try:
                            if(int(food) < 0):
                                print("\n[查無此物, 請重新輸入]")
                                continue
                            nutrient(All[int(food)][0])
                            
                        except (ValueError,IndexError):
                            print("\n[查無此物, 請重新輸入]")
                            continue
                            
                else: # 若只有一項符合關鍵字, 直接印出
                    nutrient(All[0][0])
        elif(s == "1"):
            while(1): 
                # 列出所有類別
                category = cur.execute("""SELECT Category FROM food_nutrient GROUP BY Category;""").fetchall()
                print("\n---------------------------------")
                for i in range(len(category)):
                    print("{}.\t{}".format(i,category[i][0]))
                
                print("\n-1. 回上層")
                print("---------------------------------")
                print("\n請選擇欲查詢類別之號碼:\n")
                        
                cg = input() # 輸入欲查詢類別的號碼

                if(cg == "-1"): # 回上層
                    break
                
                try:
                    if(int(cg) < 0):
                        print("\n[查無此物, 請重新輸入]")
                        continue
                    All = cur.execute("""SELECT Name FROM food_nutrient WHERE Category like '{}';""".format(category[int(cg)][0])).fetchall()
                
                except (ValueError,IndexError):
                    print("\n[查無此物, 請重新輸入]")
                    continue
                
                print("\n")
                while(1):
                    print(category[int(cg)][0])
                    print("---------------------------------")
                    for i in range(len(All)):
                        print("{}.\t{}".format(i,All[i][0]))

                    print("\n-1. 回上層")
                    print("---------------------------------")
                    print("\n請選擇欲查詢食品之號碼:\n")

                    food = input() # 輸入欲查詢食品的號碼

                    if(food == "-1"): # 回上層
                        break

                    try:
                        if(int(food) < 0):
                            print("\n[查無此物, 請重新輸入]")
                            continue
                        nutrient(All[int(food)][0])

                    except (ValueError,IndexError):
                        print("\n[查無此物, 請重新輸入]")
                        continue
                    
        elif(s == "-1"):
            break
        else:
            print("\n[輸入錯誤˙n˙ , 請重新輸入]\n")
def edit(memid,time,iftimeupdate):
    while(1):
        try:
            h = float(input("身高(cm): "))
            w = float(input("體重(kg): "))
        except ValueError:
            print("\n[請輸入數字]")
            continue
            
        if(h < 0 or w < 0):
            print("\n[輸入無效, 請重新輸入]")
            continue                
        
        bmi = round(w / ((h*0.01))**2,1)
        print("\nBMI: {}".format(bmi))
        print("---------------------------------")
        print("\n0.  確認修改")
        print("1.  重新輸入")
        print("-1. 取消")

        save = input()
        
        while(save != "0" and save != "1" and save != "-1"):
            
            print("\n[無效輸入, 請重新選擇]")
            print("---------------------------------")
            print("\n0.  確認修改")
            print("1.  重新輸入")
            print("-1. 取消")

            save = input()
        
        if(save == "0"):
            if(iftimeupdate == 1):
                data = (h,w,bmi,cur.execute("""SELECT strftime('%Y-%m-%d | %H:%M:%S','now','localtime');""").fetchone()[0],memid,time)
                conn.execute("""UPDATE userdata SET height=?, weight=?, BMI=?, time=? WHERE id=? and time=?;""",data)
            elif(iftimeupdate == 0):
                data = (h,w,bmi,memid,time)
                conn.execute("""UPDATE userdata SET height=?, weight=?, BMI=? WHERE id=? and time=?;""",data)
            conn.commit()
            break
        
        elif(save == "1"):
            continue
        
        elif(save == "-1"):
            break          
        
def bodydata(work,memid,time):
    
    if(work == "0"):
        while(1):
            try:
                h = float(input("身高(cm): "))
                w = float(input("體重(kg): "))
            except ValueError:
                print("\n[請輸入數字]")
                
            if(h < 0 or w < 0):
                print("\n[輸入無效, 請重新輸入]")
                continue
            else:
                break
        
        bmi = round(w / ((h*0.01))**2,1) # 體重(公斤) / 身高**2(公尺)
        
        data= (memid,h,w,bmi,cur.execute("""SELECT strftime('%Y-%m-%d | %H:%M:%S','now','localtime');""").fetchone()[0]) 
        conn.execute("""INSERT INTO userdata(id,height,weight,BMI,time) VALUES (?,?,?,?,?)""",data)
        conn.commit()
        
    elif(work == "1"):
        edit(memid,time,1)
    
    elif(work == "2"):
        
        while(1):
            
            All = cur.execute("""SELECT time,height,weight,BMI FROM userdata WHERE id == '{}';""".format(memid)).fetchall()
            print("\n編號\t時間\t\t\t身高(cm)\t體重(kg)\tBMI\n")
            print("----------------------------------------------------------------------")
            for i in range(len(All)):
                print("{}\t{}\t {}\t\t {}\t      {}".format(i,All[i][0],All[i][1],All[i][2],All[i][3]))
            
            print("----------------------------------------------------------------------")
            print("0.  修改資料")
            print("1.  刪除資料")
            print("\n-1. 回上層")
            print("---------------------------------")
            chose = input()
            
            if(chose == "-1"):
                break
            elif(chose == "0"):
                while(1):
                    try:
                        change = int(input("請選擇欲修改編號 : "))
                        
                    except ValueError:
                        print("\n[輸入無效, 請重新輸入]")
                    
                    if(len(All) < change < 0):
                        print("\n[查無會員, 請重新輸入]")
                        continue
                    else:
                        break
                    
                edit(memid,All[change][0],0)
            
            elif(chose == "1"):
                while(1):
                    try:
                        delete = int(input("\n欲刪除編號: "))
                        
                    except ValueError:
                        print("\n[輸入無效, 請重新輸入]")
                        continue
                    
                    if(len(All) < delete < 0):
                        print("\n[查無會員, 請重新輸入]")
                        continue
                    else:
                        break
                        
                d = input("\n確認刪除(y/n): ")
                
                
                if d == "y":
                    conn.execute("""DELETE FROM userdata WHERE id=? and time=?;""",(memid,All[delete][0]))
                    conn.commit()
            
                elif d == "n":
                    None
                else:
                    print("\n[輸入無效]")
                    break
            else:
                print("\n[輸入無效]")
                
def body(memid):
    
    while(1):

        memdata = cur.execute("""SELECT height,weight,BMI,time FROM membership INNER JOIN userdata ON membership.id=userdata.id WHERE membership.id == '{}' ORDER BY time DESC LIMIT 1;""".format(memid)).fetchone()
    
        print("\n=================================")
        if memdata is None:
            print("時間: {}".format(cur.execute("""SELECT strftime('%Y-%m-%d | %H:%M:%S','now','localtime');""").fetchone()[0]))
            print("=================================")
            print("身高: No Data")
            print("體重: No Data")
            print("BMI: No Data")
        else:
            print("時間: {}".format(memdata[3]))
            print("=================================")
            print("身高: {}".format(memdata[0]))
            print("體重: {}".format(memdata[1]))
            print("BMI: {}".format(memdata[2]))
        print("=================================")      
        print("\n0.  新增資料")
        print("1. 修改資料")
        print("2. 查詢過去紀錄\n")
        print("-1. 回上層\n")
        print("---------------------------------")
        choose = input("請輸入選項: ")
        
        if(choose == "-1"):
            break
        if(choose != "0" and choose != "1" and choose != "2"):
            print("\n[無此選項, 請重新輸入]")
            continue
        
        if(memdata is None):
            if(choose != "0"):
                print("\n[尚無資料, 請先新增資料]")
                continue
            elif(choose =="0"):    
                bodydata(choose,memid,0)
        else:
            bodydata(choose,memid,memdata[3])
            
def memberdata(m):

    while(1):
        print("\n[會員資料]")
        print("\nUser Name: {}".format(m[1]))
        print("---------------------------------")
        print("0.  About Body")
        print("1.  Diet Record")
        print("2.  Search for Food Nutrient")
        print("-1. Logout")
        print("---------------------------------")
        choose = input("請輸入項目: ")
        if(choose == "0"):
            body(m[0])
            break
        elif(choose == "2"):
            search()
        elif(choose == "-1"):
            break

def login():
    alluser = cur.execute("""SELECT username FROM membership;""").fetchall()
    if(len(alluser)==0):
        return 1
    
    print("---------------------------------")
    for i in range(len(alluser)):
        print("{}. {}".format(i,alluser[i][0]))
    print("---------------------------------")
    
    while(1):
        member = input("\n請選擇會員:  [-1 取消]: ")
        if(member == "-1"): # 回上層
            return 2
        
        try:
            if(int(member) < 0):
                print("\n[查無會員, 請重新輸入]")
                continue
            mem = cur.execute("""SELECT id,username,password FROM membership WHERE username like '{}';""".format(alluser[int(member)][0])).fetchone() 
            print("\nHi! {}".format(alluser[int(member)][0]))
        
        except (ValueError,IndexError):
            print("\n[查無會員, 請重新輸入]")
            continue
            
        del member
    

        pw = getpass.getpass("\n請輸入密碼: ")     
        
        count = 0
        while(pw != mem[2]):
            
            count += 1
            if(count == 3):
                return 0
            
            print("\n[密碼錯誤, 錯誤累積 {} 次]".format(count))
            pw = input("\n請輸入密碼: ")
        print("---------------------------------")
        print("\n{} 歡迎回來! ƪ(•◡•ƪ)".format(mem[1]))    
        return (mem[0],mem[1])

def register():
    
    print("\n[註冊會員]")
    while(1):
        username = input("\n會員名稱  [-1 取消]: ")
        if(username == "-1"):
            break
        
        Insert_query="""SELECT username FROM membership WHERE username=?"""
        
        exist = cur.execute(Insert_query,(username,)).fetchall()
        if(exist):
            print("\n[會員名稱已存在, 請重新輸入]")
            continue
        password = input("密碼:   [-1 取消]: ")
        if(password == "-1"):
            break
        check = input("\n確認送出(y/n): ")
        
        

        if(check == "y"):
            conn.execute("""INSERT INTO membership(username,password) VALUES (?,?)""",(username,password))
            conn.commit()
            break
        elif(check == "n"):
            None
            break
        else:
            print("\n[輸入無效]")
        
if __name__ == "__main__":
    '''
    # create membership table

    cur.execute('DROP TABLE IF EXISTS membership')
    
    cur.execute("""CREATE TABLE IF NOT EXISTS membership
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE,
                   password TEXT)""")
                  
    # create userdata table

    cur.execute('DROP TABLE IF EXISTS userdata')
    
    cur.execute("""CREATE TABLE IF NOT EXISTS userdata
                  (id INTEGER,
                   height REAL,
                   weight REAL,
                   BMI REAL,
                   time TEXT)""")
    '''            
    print("\nHi! 歡迎使用 DietHelper (●ゝω)ノヽ(∀＜●)\n")
    
    while(1):
        
        status = input("\n請輸入數字: 0. 會員登入 1. 加入會員 2. 訪客查詢 -1. 離開\n")
    
        if(status == "0"):
            member = login()
            
            if(member == 0):
                print("\n[已達密碼錯誤次數上限, 請稍後再試]\n")
            elif(member == 1):
                print("\n[尚無會員]")
            elif(member == 2):
                None
            else:
                memberdata(member)
            
        elif(status == "1"):
            
            register()
            
        elif(status == "2"):
            search()
            
        elif(status == "-1"):
            break
            
        else:
            print("\n[輸入錯誤˙n˙ , 請重新輸入]\n")
    conn.close()