class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__ (self, name):
       self.name = name

    def get_data(self):
        
        try: 
            file = open(self.name, "r")
        except Exception as e:
            raise ExamException('Errore apertura file: {}' .format(e))

        lista = []

        epochprec = None

        for line in file:
            element = line.split(",")

            if len(element) > 1:
                if isinstance(element[0], (int, float)) and isinstance(element[1], (int, float)):
                    element[0] = round(element[0])

                    if element[0] > epochprec:
                        lista.append([element[0], element[1]])
                        epochprec = element[0]
                    elif element[0] = epochprec:
                        raise ExamException('Errore, dati duplicati')
                    else:
                        raise ExamException('Errore, dati non ordinati')

        return(lista)

def hourly_trend_changes(time_series):

    #controllare epoch stessa ora e inversioni, poi contarle