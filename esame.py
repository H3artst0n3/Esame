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

                try:
                    element[0] = round(float(element[0]))
                    element[1] = float(element[1])
                except:
                    print('Riga non valida')

                if isinstance(element[0], (int, float)) and isinstance(element[1], (int, float)):

                    if epochprec == None or element[0] > epochprec:
                        lista.append([element[0], element[1]])
                        epochprec = element[0]
                    elif element[0] == epochprec:
                        raise ExamException('Errore, dati duplicati')
                    else:
                        raise ExamException('Errore, dati non ordinati')

        return(lista)

def hourly_trend_changes(time_series):

    inversion = []

    control_h = None
    temp_1 = None
    temp_2 = None
    counter = 0

    for element in time_series:
        if element[0]/3600 == control_h:
            if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                counter += 1
            
            if not temp_1 == element[1]:
                temp_2 = temp_1
                temp_1 = element[1]

        elif control_h == None:
            temp_1 = element[1]
            temp_2 = temp_1
            
            control_h = element[0]/3600
        else: 
            inversion.append(counter)
            counter = 0
            control_h = element[0]/3600
            
            if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                counter += 1
            
            if not temp_1 == element[1]:
                temp_2 = temp_1
                temp_1 = element[1]
    
    return(inversion)


oggetto = CSVTimeSeriesFile('data.csv')

print('         Errori        ')
print('-----------------------')

value = hourly_trend_changes(oggetto.get_data())

print('  Ora  |  Inversioni  ')
print('----------------------')
i = 0
for element in value:
    i += 1
    print('  {}   |  {}  ' .format(i, element))