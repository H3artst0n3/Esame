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

                    # controlliamo per vedere se sono presenti eventuali dati duplicati o non ordinati
                    if epoch_prev == None or element[0] > epoch_prev: # se prendiamo il primo elemento o se l'epoch preso in considerazione è maggiore rispetto al precedente allora:

                        lista.append([element[0], element[1]]) # 1- salviamo i primi due elementi

                        epoch_prev = element[0] # 2- salviamo l'epoch corrente per utilizzarlo poi come controllo per quello successivo

                    
                    elif element[0] == epoch_prev: # se invece l'epoch preso in considerazione è uguale a quello precedente:

                        raise ExamException('Errore, dati duplicati') # stampiamo un messaggio di errore dicendo che la riga presenta dei dati duplicati


                    else: # l'ultimo caso che resta da analizzare è quello in cui l'epoch soggetto a controllo è miniore rispetto al precedente:

                        raise ExamException('Errore, dati non ordinati') # in questo caso stampiamo un messaggio di errore dicendo che la riga presenta dei dati non ordinati


            else: # se la riga invece presenta 1 elemento oppure è vuota:

                print('Riga non valida') # la riga contiene dati insufficienti e quindi non è valida

        return(lista)



def hourly_trend_changes(time_series):



    ### Inizializziamo array e variabili ###

    inversion = [] # array dove verranno salvate le inversioni di trend

    control_h = None # variabile che serve per "salvare" l'ora precedente e che ci servirà come controllo


    # per comodità salviamo le due misurazioni precedenti, a quella presa in considerazione, così da poter stabilire se c'è un'inversione di trend o meno; in questo caso possiamo dire che la temperatura della riga interessata, element[1], la possiamo definire come un valore "N";


    temp_1 = None # questa variabile corrisponderebbe al valore "N - 1"
    
    temp_2 = None # questa variabile corrisponderebbe al valore "N - 2"
    
    counter = 0 # variabile che andrà a salvare il numero di inversioni di ogni ora



    ### Analizziamo i dati ###

    # dobbiamo controllare che il file non sia un file vuoto
    if not len(time_series) == 0: # perciò si pone la sua lunghezza diversa da zero

        for element in time_series: # per ogni elemento nel file facciamo un controllo

            # prima di tutto dobbiamo controllare che i dati siano relativi alla stessa ora
            if round(element[0]/3600) == control_h: # prendiamo in considerazione l'epoch corrente e lo dividiamo per 3600 (numero di secondi in un'ora), per vedere se la temperatura registrata appartiene alla stessa ora della misurazione registrata precedentemente, infine, arrotondiamo il risultato con il metodo round, come richiesto dalle specifiche presenti nel tema d'esame. Nel caso, invece, non si volesse arrotondare il valore, allora il controllo verrebbe: if (element[0]//3600) == control_h dove "//" indica la divisione con risultato intero e troncato della parte decimale.

                # ora passato il controllo dobbiamo stabilire se è presente un'inversione di trend o meno. L'idea è che se tre valori, a, b, c, sono crescenti, allora questi sono: a < b < c; perciò abbiamo un'inversione nel caso b > c; 
                # analogamente per il caso di decrescenza dove avremo a > b > c ottenendo un'inversione nel caso b < c

                if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                    
                    # nel caso si presentasse un' inversione di trend:
                    counter += 1 # incrementiamo il contatore di uno
                
                # facciamo un'ulteriore controllo:
                if not temp_1 == element[1]:

                    # nel caso "N - 1" e "N" siano diversi, allora:
                    temp_2 = temp_1 # 1- salviamo il valore di "N - 1" per utilizzarlo come "N - 2"

                    temp_1 = element[1] # 2- salviamo la temperatura corrente per utilizzarla poi successivamente come "N - 1"


            elif control_h == None: # nel caso in cui l'epoch sia il primo non esistono valori con cui confrontarlo precedentemente quindi:

                temp_1 = element[1] # 1- salviamo la temperatura corrente per utilizzarla poi successivamente come "N - 1"  

                temp_2 = temp_1 #2- poniamo "N - 2" = "N - 1" così da avere tutti i dati necessari per il controllo di quelli successivi
                
                control_h = round(element[0]/3600) # 3- salviamo l'ora corrente, approssimata, per utilizzarla successivamente come controllo
            
            
            else: #se invece i dati appartengono ad ore diverse:

                inversion.append(counter) # 1- salviamo il contatore nella lista

                counter = 0 # 2- azzeriamo il contatore

                control_h = round(element[0]/3600) # 3- salviamo l'ora corrente, approssimata, per utilizzarla successivamente come controllo 

                
                if (temp_2 < temp_1 and temp_1 > element[1]) or (temp_2 > temp_1 and temp_1 < element[1]):
                    
                    # nel caso si presentasse un' inversione di trend al "cambio" dell'ora:
                    counter += 1 # incrementiamo il contatore di uno
                

                if not temp_1 == element[1]:
                    
                    # nel caso "N - 1" e "N" siano diversi, allora:
                    temp_2 = temp_1 # 1- salviamo il valore di "N - 1" per utilizzarlo come "N - 2"
                    
                    temp_1 = element[1] # 2- salviamo la temperatura corrente per utilizzarla  successivamente come "N - 1"
        
        inversion.append(counter) # salviamo il valore del contatore

    return(inversion)