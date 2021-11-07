import sqlite3
# from . import dbConnect
sqliteConnection = sqlite3.connect('../../../weatherDB.db')
c = sqliteConnection.cursor()
def addToDatabase(city, data):
    # sqliteConnection = sqlite3.connect('../../../weatherDB.db')
    # c = sqliteConnection.cursor()
    sql = ''' INSERT INTO weatherDB(city, Country_Code, Coordinate, Temperature, Pressure, Humidity, Forecast, Description)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?) '''
    data_tuple = (
        city, 
        data["country_code"],
        data["coordinate"],
        data["temp"],
        data["pressure"],
        data["humidity"],
        data["main"],
        data["description"]
        )
    c.execute(sql, data_tuple)
    sqliteConnection.commit()
    return 
def getViewed():
    c.execute("select city, COUNT(city) as ct from weatherDB group by city order by ct DESC LIMIT 1")

    dt = c.fetchall()
    print(dt)
    return dt