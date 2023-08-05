import os
from decouple import config 

class Core():

    myBase = "POSTGRES"
    myCulture = "es-EC"
    myDecimalSeparator = ","
    myGroupSeparator = "."
    myDateSeparator = "/"
    myShortDate = "dd/mm/YY"
    myLongDate = "dd/mm/YYYY"
    myDecimalDigits = 2
    myVariables = None
    mySession = None
    myDb = None
    myApp = None

    def __init__(self, myApp):
        self.myApp = myApp
        self.myApp.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.myApp.config['DEBUG'] = True
        self.myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.setVariables()
        self.setRegion()
        # self.setSession(session)

    """
       SETTERS


    """

    def setVariables(self):
        self.myVariables = os.environ.copy()
        env = dict(os.environ)
        for key in env:
            self.myApp.config[key] = env[key]

    def setDbCnx(self, cnx):
        self.myApp.config['SQLALCHEMY_DATABASE_URI'] = cnx
# TESTED

    def setRegion(self):
        self.myCulture = self.getVariable("myCulture")
        self.myDecimalSeparator = self.getVariable("myDecimalSeparator")
        self.myGroupSeparator = self.getVariable("myGroupSeparator")
        self.myDateSeparator = self.getVariable("myDateSeparator")
        self.myShortDate = self.getVariable("myShortDate")
        self.myLongDate = self.getVariable("myLongDate")
        self.myDecimalDigits = self.getVariable("myDecimalDigits")

    def setSession(self, session):
        self.mySession = session

    """
       GETTERS


    """

    def getVariable(self, key):
        return config(str(key).upper())

    def getAllVariables(self):
        return self.myVariables
    """
       Métodos GET ENV


    """

    def getEnvTableName(self, table):
        tableAtDomain = self.getVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        tbl = self.getVariable(domain)
        return tbl

    def getEnvCnx(self, table):
        tableAtDomain = self.getVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        cnx = self.getVariable(domain)
        self.setDbCnx(cnx)
