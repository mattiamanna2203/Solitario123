import numpy as np 

# Mazzo italiano base senza semi di 40 carte (creato una sola volta)
## Con np.arange(1, 11) si crea un vettore da 1 a 10.
## Con np.tile( X ,4) si ripete il vettore X 4 volte per arrivare alle 40 carte.
MAZZO_BASE = np.tile(np.arange(1, 11), 4)  # Creo questa al di fuori della function dato che è sempre la stessa non verrà ricreata ogni volta che la funzione  viene chiamata

def  __simulazione_solitario123__():
   """Funzione per effettuare una simulazione di una singola partita."""
   
   # Creo il mazzo di carte virtuale, non servono le figure. Solo i numeri da 1 a 10.
   carte = [i for _ in range(4) for i in range(1,11)]   
   
   # Mescolo il mazzo di carte 
   carte_mescolate = np.array(carte)    # trasformo la lista in un numpy array
   np.random.shuffle(carte_mescolate)   # faccio lo shuffle (equivale a mischiare il mazzo di carte)
   
  
   carta_perdente = 1 # Per tenere traccia di quale sia la carta perdente
   
   # Simulo l'estrazione dal mazzo. Devo estrarre per 40 volte
   for index in range(0,40):
      
      # Se la carta estratta corrisponde a quella perdente interrompere
      if carte_mescolate[index] == carta_perdente:
         return 0 # Sconfitta
      
      # Se la carta perdente è il 3 ripartire da 1
      if carta_perdente == 3:
         carta_perdente = 1 
         
      # Se la carta perdente è < 3 allora +1 così da aggiornare  e proseguire secondo la sequenza: 1 -> 2 -> 3
      else:
         carta_perdente += 1

   return 1 # Vittoria

def __simulazione_solitario123_vettorializzata__(n_prove = 1,seed = None):
    """ Versione di __simulazione_solitario123__ vettorizzata (più veloce).
        Usa più numpy ed evita loop per quanto possibile.
        
        Input:
            - n_prove (int, default 1): Numero di volte che il solitario viene giocato (prove effettuate);
            - seed (None, default None): Seed per il generatore randomico che mescola i mazzi.
    """
    # region InputCheck
    if not isinstance(n_prove,int):
        raise TypeError("'n_prove' deve essere un numero intero")    
    
    if not isinstance(seed,(type(None),int)):
        raise TypeError("'seed' deve essere un numero intero o None")    
    # endregion
         
    # region Mescolare il mazzo generando il numero di prove richieste
    rng = np.random.default_rng(seed=seed) # Per generare numeri randomici, usa il seed in input

    indici = np.argsort(rng.random((n_prove, 40)), axis=1) # Genero indici casuali per ogni riga, ovvero ogni singola prova

    # Applicare al mazzo base gli indici randomici. In questo modo:
    ## 1. Vengono creati tanti mazzi quanto il numero di prove richiester
    ## 2. Vengono mescolati singolarmente
    mazzi = MAZZO_BASE[indici]
    # endregion
    
    # region Risultato partite
    ## Generare la sequenza della carta perdente: 1,2,3,1,2,3,...
    sequenza_sconfitta = (np.arange(40) % 3) + 1 # Lista da 0 a 40, operatore resto 3. 0 % 3 -> 0, 1 % 3 -> 1, 2 % 3 -> 2 Poi aggiungo 1 a tutto ed ottengo la sequenza 1,2,3
    numero_sconfitte = np.sum((mazzi == sequenza_sconfitta).any(axis=1))
    numero_successi = n_prove - numero_sconfitte

    # region Dettaglio del codice per migliore leggibilità
    # Confronto vettoriale, confronta la sequenza_sconfitta con ogni prova (mazzo mescolato)
    # Se hanno un elemento in comune significa che c'è 1 ove l'1 perde, stessa cosa per 2 e 3.
    # Quando accade questo compare un True
    #perdite = (mazzi == sequenza_sconfitta)

    # Una partita è persa se almeno un match, ovvero se c'è almeno un Ture
    #sconfitte = perdite.any(axis=1) # any restituisce True se c'è almeno un True

    #numero_sconfitte = np.sum(sconfitte) # True corrisponde ad 1, perciò le sconfitte ottengo il numero di sconfitte totale.
    # endregion

    # endregion

    return numero_successi

if __name__ == "__main__":
   numero_prove = 1000
   vittorie = 0
   for _ in range(numero_prove):
      vittorie += __simulazione_solitario123__() # restituisce 1 se ha successo 0 se non lo ha. Basta quindi sommare per tenere traccia dei successi

   # Calcolo il tasso di successo
   tasso_di_successo = (vittorie/numero_prove)*100

   # Creo un output testuale descrivente i risultati per la i-esima simulazione con le N prove specificate
   risultato_testuale = f"Su {numero_prove} prove il solitario è stato vinto {vittorie} volte.\nTasso di successo {tasso_di_successo}\n"
   
   vittorie = __simulazione_solitario123_vettorializzata__(numero_prove)
   tasso = (vittorie / numero_prove) * 100
   print(f"Tasso di successo con solitario vettorializzato: {tasso_di_successo}%")


   