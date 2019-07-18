import mysql.connector
import collections

class my_database:
    def __init__(self):
        self.mydb=mysql.connector.connect(
                host="localhost",
                user="root",
                password="WShuaren",
                database="testdb"
            )

        #set up cursor and clear  old table
        self.mycursor=self.mydb.cursor()
        self.clearDB()

        #set up table
        self.mycursor.execute("CREATE TABLE Pills (Name VARCHAR(50), Dosage VARCHAR(255), Colour VARCHAR(200), Hue1 INTEGER(50), Hue2 INTEGER(50),Hue3 INTEGER(50), Description VARCHAR(400), CountryOfOrigin VARCHAR(200))")
        
        #must print if you fetch show tables
        self.mycursor.execute("SHOW TABLES")
        for tb in self.mycursor:
            print('table number',tb)

        self.insertDB('Hurix’s Laxative Pill','Dark Orange','5mg',35,0,0,'Bisacodyl is used on a short-term basis to treat constipation. It also is used to empty the bowels before surgery and certain medical procedures. Bisacodyl is in a class of medications called stimulant laxatives. It works by increasing activity of the intestines to cause a bowel movement','Hurix, Malaysia')
        self.insertDB('Diclofenac','Light Orange','25mg',23,0,0,'Diclofenac is used to relieve pain, swelling (inflammation), and joint stiffness caused by arthritis. Reducing these symptoms helps you do more of your normal daily activities. This medication is known as a nonsteroidal anti-inflammatory drug (NSAID).','Drug Houses of Australia Pte. Ltd.')
        self.insertDB('Salbutamol','White','2mg',0,0,0,'It is used to treat asthma, including asthma attacks, exercise-induced bronchoconstriction, and chronic obstructive pulmonary disease (COPD).','Sunward Pharmaceutical, Singapore')
        self.insertDB('Renapro Tab MultiVitamin','Brown','nicotinamide 20mgriboflavin 1.7mgfolic acid 1mgcalcium pantothenate 10mgpyridoxine HCl 10mgbiotin 300ugthiamine nitrate 1.5mgascorbic acid 97% 61.9mgcyanocobalamin 6ug',1000,0,0,'Used traditionally to relieve headache, fever, signs of colds, cough and lethargy. Multivitamins are used to provide vitamins that are not taken in through the diet. Multivitamins are also used to treat vitamin deficiencies (lack of vitamins) caused by illness, pregnancy, poor nutrition, digestive disorders, and many other conditions.','Ban Kah Chai, Malaysia')
        self.insertDB('BKC KAPSUL SELSEMA','Brown and Orange','300mg',35,1000,0,'Used traditionally to relieve headache, fever, signs of colds, cough and lethargy','Ban Kah Chai, Malaysia')
        self.insertDB('Vitamin B Forte','Dark Pink','B1 - 250mg B6 -250mg B12 - 1000mcg',345,0,0,'This product is a combination of B vitamins used to treat or prevent vitamin deficiency due to poor diet, certain illnesses, alcoholism, or during pregnancy. Vitamins are important building blocks of the body and help keep you in good health. B vitamins include thiamine, riboflavin, niacin/niacinamide, vitamin B6, vitamin B12, folic acid, and pantothenic acid.','Ban Kah Chai, Malaysia')

        # print(self.foundInDB('Salbutamol'))
        # self.removeDB('Salbutamol')
        # print(self.foundInDB('Salbutamol'))

        # self.mycursor.execute("SELECT Hue1, Hue2, Hue3 FROM Pills")
        # result=self.mycursor.fetchall()
        # print(result[0])
        # compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        # print(compare([0,35,0],result[0]))
        # self.mycursor.execute(("SELECT * FROM Pills WHERE Hue1=%s AND Hue2=%s AND Hue3=%s"),(result[0]))
        # newres=self.mycursor.fetchall()
        # print(newres)
        self.mydb.commit()

    def getMatchingPillDB(self,hsv_array):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        result=self.getListHueDB()
        for i in range(len(result)):
            print('hsv array',hsv_array,'result',result[i])
            if(compare(hsv_array,result[i])):
                self.mycursor.execute(("SELECT * FROM Pills WHERE Hue1=%s AND Hue2=%s AND Hue3=%s"),(result[i]))
                pillData=self.mycursor.fetchall()
                return pillData

        return None

    def getListHueDB(self):
        self.mycursor.execute("SELECT Hue1, Hue2, Hue3 FROM Pills")
        result=self.mycursor.fetchall()
        return result


    def insertDB(self,name,dosage,colour,hue1,hue2,hue3,description,country):
        print('insert')
        #insert into pills
        sqlFormula="INSERT INTO Pills (Name, Dosage, Colour, Hue1, Hue2, Hue3, Description, CountryOfOrigin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        pill=(name,dosage,colour,hue1,hue2,hue3,description,country)
        self.mycursor.execute(sqlFormula,pill)
        self.showTableDB()

    def searchDB(self,pillName):
        print('Pill Name:',)
        self.mycursor.execute(("SELECT * FROM Pills WHERE Name=%s"),(pillName,)) #this works

        result=self.mycursor.fetchall()
        return result

    def foundInDB(self,name):
        result=self.searchDB(name)
        print('result',result)
        if not result:
            return False
        return True

    def removeDB(self,name):
        print('remove')
        sqlFormula="DELETE FROM Pills WHERE Name=%s"
        self.mycursor.execute(sqlFormula,(name,))
        self.mydb.commit()
        self.showTableDB()
        

    def showTableDB(self):
        self.mycursor.execute('SELECT * FROM Pills')
        print('show',self.mycursor.fetchall())

    def updateDB(self):
        print('update')

    def clearDB(self):
        try:
            self.mycursor.execute("DROP TABLE testdb.Pills")
        except:
            print('Table Cleared Already')
        
if __name__ == "__main__":
    DB=my_database()