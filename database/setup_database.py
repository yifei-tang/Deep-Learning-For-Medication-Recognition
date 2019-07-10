import mysql.connector

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
        self.mycursor.execute("CREATE TABLE Pills (Name VARCHAR(50), Dosage VARCHAR(255), Colour VARCHAR(200), Hue INTEGER(50), Description VARCHAR(400), CountryOfOrigin VARCHAR(200))")
        
        #must print if you fetch show tables
        self.mycursor.execute("SHOW TABLES")
        for tb in self.mycursor:
            print('table number',tb)

        self.insertDB('Hurix’s Laxative Pill','Light Orange','5mg',35,'Bisacodyl is used on a short-term basis to treat constipation. It also is used to empty the bowels before surgery and certain medical procedures. Bisacodyl is in a class of medications called stimulant laxatives. It works by increasing activity of the intestines to cause a bowel movement','Hurix, Malaysia')
        self.insertDB('Diclofenac','Dark Orange','25mg',23,'Diclofenac is used to relieve pain, swelling (inflammation), and joint stiffness caused by arthritis. Reducing these symptoms helps you do more of your normal daily activities. This medication is known as a nonsteroidal anti-inflammatory drug (NSAID).','Drug Houses of Australia Pte. Ltd.')
        self.insertDB('Salbutamol','White','2mg',0,'It is used to treat asthma, including asthma attacks, exercise-induced bronchoconstriction, and chronic obstructive pulmonary disease (COPD).','Sunward Pharmaceutical, Singapore')
        self.insertDB('Renapro Tab MultiVitamin','Brown','nicotinamide 20mgriboflavin 1.7mgfolic acid 1mgcalcium pantothenate 10mgpyridoxine HCl 10mgbiotin 300ugthiamine nitrate 1.5mgascorbic acid 97% 61.9mgcyanocobalamin 6ug',0,'Used traditionally to relieve headache, fever, signs of colds, cough and lethargy. Multivitamins are used to provide vitamins that are not taken in through the diet. Multivitamins are also used to treat vitamin deficiencies (lack of vitamins) caused by illness, pregnancy, poor nutrition, digestive disorders, and many other conditions.','Ban Kah Chai, Malaysia')
        self.insertDB('BKC KAPSUL SELSEMA','Brown and Orange','300mg',35,'Used traditionally to relieve headache, fever, signs of colds, cough and lethargy','Ban Kah Chai, Malaysia')
        self.insertDB('Vitamin B Forte','Dark Pink','B1 - 250mg B6 -250mg B12 - 1000mcg',350,'This product is a combination of B vitamins used to treat or prevent vitamin deficiency due to poor diet, certain illnesses, alcoholism, or during pregnancy. Vitamins are important building blocks of the body and help keep you in good health. B vitamins include thiamine, riboflavin, niacin/niacinamide, vitamin B6, vitamin B12, folic acid, and pantothenic acid.','Ban Kah Chai, Malaysia')

        # print(self.foundInDB('Salbutamol'))
        # self.removeDB('Salbutamol')
        # print(self.foundInDB('Salbutamol'))


        #find something

        # sqlFormula="INSERT INTO students (name, age) VALUES (%s, %s)"
        # student1=("Jenny",22)
        # mycursor.execute(sqlFormula,student1))
        
        #this command will save the table
        #mydb.commit()

    def insertDB(self,name,dosage,colour,hue,description,country):
        print('insert')
        #insert into pills
        sqlFormula="INSERT INTO Pills (Name, Dosage, Colour, Hue, Description, CountryOfOrigin) VALUES (%s,%s,%s,%s,%s,%s)"
        pill=(name,dosage,colour,hue,description,country)
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