from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Circuito import Circuito


class DAO():
    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                select distinct r.`year` 
                from races r 
                order by r.`year` asc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct c.*
                from circuits c """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuito(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEges(annoMax,annoMin,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select a1.circuitId as circuito1, a2.circuitId as circuito2, tb1.n + tb2.n as peso
    from (select distinct c.circuitId 
          from circuits c, races r 
          where c.circuitId = r.circuitId and r.year < %s and r.year > %s
          ) as a1,
         (select distinct c.circuitId 
          from circuits c, races r 
          where c.circuitId = r.circuitId and r.year < %s and r.year > %s
          ) as a2,
         (select r2.circuitId, count(*) as n
          from results r, races r2 
          where r2.raceId = r.raceId 
          and r.time != '\\\\N'
          and r2.year < %s and r2.year > %s
          group by r2.circuitId) as tb1,
         (select r2.circuitId, count(*) as n
          from results r, races r2 
          where r2.raceId = r.raceId 
          and r.time != '\\\\N'
          and r2.year < %s and r2.year > %s
          group by r2.circuitId) as tb2
    where a1.circuitId > a2.circuitId 
      and a1.circuitId = tb1.circuitId 
      and a2.circuitId = tb2.circuitId 
             
                     """
        cursor.execute(query,(annoMax,annoMin,annoMax,annoMin,annoMax,annoMin,annoMax,annoMin))

        res = []
        for row in cursor:
            res.append(Arco(idMap[row["circuito1"]],idMap[row["circuito2"]],row["peso"]))

        cursor.close()
        cnx.close()
        return res
