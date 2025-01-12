from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_distinct_localizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT c.Localization  
                            FROM classification c 
                            ORDER BY c.Localization DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(localization: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *  
                        FROM classification c
                        WHERE c.Localization = %s"""
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes_w_essentiality(localization: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c.GeneID, c.Localization, g.Essential
                        FROM classification c, genes g
                        WHERE c.Localization = %s
                        and c.GeneID = g.GeneID 
                        GROUP by c.GeneID, g.Essential"""
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_chromosomes_interaction(interaction, chromosomes_map):
        cnx = DBConnect.get_connection()
        result = 0
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT g.Chromosome
                        FROM genes g 
                        WHERE g.GeneID = %s or g.GeneID = %s"""
            cursor.execute(query, (interaction.GeneID1, interaction.GeneID2))

            for row in cursor:
                result += row["Chromosome"]
            chromosomes_map[(interaction.GeneID1, interaction.GeneID2)] = result
            chromosomes_map[(interaction.GeneID2, interaction.GeneID1)] = result

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(localization: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c1.GeneID as Gene1, c2.GeneID as Gene2, SUM(DISTINCT g.Chromosome) as W
                        FROM interactions i, classification c1, classification c2, genes g
                        WHERE c1.Localization=%s and c2.Localization=c1.Localization 
                        and i.GeneID1 =c1.GeneID and i.GeneID2 =c2.GeneID and c1.GeneID<>c2.GeneID 
                        AND (g.GeneID=c1.GeneID or g.GeneID=c2.GeneID)
                        group by c1.GeneID, c2.GeneID
                        order by W asc"""
            cursor.execute(query, (localization,))

            for row in cursor:
                result.append((Classification(row["Gene1"], localization),
                               Classification(row["Gene2"], localization),
                               row["W"]))

            cursor.close()
            cnx.close()
        return result
