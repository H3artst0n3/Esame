#######     COMPITO D'ESAME PER L'APPELLO DEL 24 FEBBRAIO 2021      #######

class ExamException(Exception):
    pass


class CSVTimeSeriesFile:

    # inizializziamo l'oggetto
    def __init__ (self, name):
       self.name = name


    def get_data(self):
        
        try: # apriamo il file
            file = open(self.name, "r")
        except Exception as e: # se riscontriamo problemi allora alziamo un'eccezione
            raise ExamException('Errore apertura file: {}' .format(e))



        ### Inizializziamo array e variabile ###

        lista = [] #per comodità l'array è scritto in italiano siccome "list" è un comando
        
        epoch_prev = None #variabile che serve per "salvare" l'epoch precedente



        ### Analizziamo il file ###

        for line in file: # analizziamo riga per riga
            
            # dividiamo le righe in elementi, utilizzando la virgola come elemento separatore
            element = line.split(",")


            # ora analizziamo le righe e per quelle che presentano più di un elemento svolgiamo dei controlli
            if len(element) > 1:

                try: # convertiamo gli elementi in float (da lettura i dati risultano stringhe)
                    element[0] = float(element[0]) # corrisponde all'epoch
                    element[1] = float(element[1]) # corrisponde alla temperatura
                except Exception:
                    print('Riga non valida')


                # ora analizziamo gli elementi accertandoci che essi siano di tipo intero o float
                if isinstance(element[0], (int, float)) and isinstance(element[1], (int, float)):

                    # controlliamo ora per vedere se ci sono dati duplicati o non ordinati
                    if epoch_prev == None or element[0] > epoch_prev: # se prendiamo il primo elemento o se l'epoch preso in considerazione è più grande rispetto al precedente allora:

                        lista.append([element[0], element[1]]) # 1- salviamo la riga contenente i primi due elementi dei nuovi dati

                        epoch_prev = element[0] # 2- salviamo l'epoch corrente per utilizzarlo poi come controllo per quello successivo

                    
                    elif element[0] == epoch_prev: # se invece l'epoch preso in considerazione è uguale a quello precedente:

                        raise ExamException('Errore, dati duplicati') # stampiamo un messaggio di errore dicendo che la riga presenta dei dati duplicati


                    else: # l'ultimo caso che resta è il caso in cui l'epoch soggetto a controllo sia meniore rispetto al precedente:

                        raise ExamException('Errore, dati non ordinati') # stampiamo un messaggio di errore dicendo che la riga presenta dei dati non ordinati


            else: # se la riga invece presenta 1 elemento oppure è vuota:

                print('Riga non valida') # la riga contiene dati insufficienti e quindi non è valida

        return(lista)



def hourly_trend_changes(time_series):

    inversion = []

    control_h = None
    temp_1 = None
    temp_2 = None
    counter = 0

    if not len(time_series) == 0:
        for element in time_series:
            if round(element[0]/3600) == control_h:
                if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                    counter += 1
                
                if not temp_1 == element[1]:
                    temp_2 = temp_1
                    temp_1 = element[1]

            elif control_h == None:
                temp_1 = element[1]
                temp_2 = temp_1
                
                control_h = round(element[0]/3600)
            else: 
                inversion.append(counter)
                counter = 0
                control_h = round(element[0]/3600)
                
                if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                    counter += 1
                
                if not temp_1 == element[1]:
                    temp_2 = temp_1
                    temp_1 = element[1]
        
        inversion.append(counter)
    return(inversion)

