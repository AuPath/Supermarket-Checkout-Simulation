# Supermarket Checkout Simulation

## Obiettivo finale

Confronti tra diverse configurazioni delle casse per un
supermercato. Valutazione del tempo di attesa per i clienti,
flusso in uscita dei clienti.

## Tipologie di casse

- Cassa "normale"
  - con coda dedicata
  - con coda condivisa (tipo decathlon)

- Cassa self-service
  Limitato per numero di articoli.
  Con coda condivisa.

- Cassa self-scan
    Soggetta a controlli a campione. Controlli parziali o totali.
  
## Tipologie di agenti
    
- Clienti
  
  Ogni cliente è a conoscenza della dimensione del proprio basket.
  Appena entrato nel negozio sa se usare la tipologia di cassa self-scan.

- Casse

Non è un agente ma per il negozio è definito il numero di cassieri.

## Comportamento degli agenti
    
- Cliente

Ogni cliente entra nel negozio, per ogni cliente viene stabilito 
una basket-size in base ad una legge ricavata dai dati del paper (giorno ed ora).
Il cliente spende un tempo proporzionale al basket-size per la fase di acquisizione dei prodotti, poi si presenta in cassa.

Se precedentemente aveva scelto di fare self-scan allora va self-scan.
Altrimenti deve decidere tipologia di cassa e tra queste scegliere una coda
da seguire.

Il cliente ad ogni step può decidere di cambiare la coda.
    
### Strategie scelta coda
    
1. Coda con meno gente
2. Coda con meno articoli
3. Coda con minor tempo atteso, prodotto numero clienti * tempo servizio medio
4. Coda con minor tempo atteso, prodotto numero clienti * somma expected transactions and break time

### Cambio di coda (Jockeying)
    
Trovare strategie.

Se il cliente può migliorare il proprio tempo di attesa 
in un certo range allora cambia cassa (si considerano solo casse adiacenti). 
    
## Fase di transazione
    
Definita da:

1. Scanning
   
   Per cassa self-scan 0, incorporato nella spesa.
   Per le altre calcolato nella stessa maniera, proporzionale a basket size.
   
2. Payment
   
   Uguale per tutti. tempo costante.
   
3. Bagging
   
   Nella self-scan incorporato nella spesa.
   Nella normale 0 in quanto incorporato nello scanning.
   Nella self service lo fa il cliente, proporzionale alla basket size.

## Cose da mettere nella relazione
    
Andamento simulazione per vari tipi di coda, tipi di scelta della
coda, con e senza jockeying.  Note sul tempo di attesa per clienti.
    
## Cose random
    
Break time AKA tempo tra una transazione e l'altra.

## Struttura dell supermercato
Ogni supermercato saraà composto necessariamente da 3 zone:
1. **Zona di entrata**: Non cambia mai. Costituita da un rettangolo in alto
2. **Zona di shopping**: Non cambia mai. Costituita da un rettangolo a destra
3. **Zonda delle casse**: Questa zona è dinamica. Si può scegliere al momento della costruzione del supermercato come costruirlo. In questa zona è possibile inserire i diversi tipi di cassa e coda in modo tale da simulare diversi tipi di struttura del negozio.