# Pubblica 3.17 — compilazione Java Android

## Specifica

- R1: aggiungere una voce Java Android nel sottomenu Compila.
- R2: accettare uno ZIP Android Studio con `settings.gradle`, `build.gradle`, un modulo Android e sorgenti Java/Kotlin.
- R3: generare un workflow Gradle dedicato senza alterare i workflow esistenti (eccetto conferma per il medesimo file).
- R4: utilizzare il flusso Pubblica su GitHub già disponibile e lasciare all'utente l'ultima conferma.
- R5: conservare tutte le funzioni precedenti, l'offline e le impostazioni salvate.
- R6: compilare APK debug via GitHub Actions e renderlo disponibile come artifact.

## Piano e attività

1. Menu e vista dedicata con controllo ZIP (R1,R2).
2. Generazione ZIP con workflow Gradle `build-java-apk.yml` (R3,R6).
3. Collegamento all'esistente vista Pubblica e istruzioni (R4).
4. Incremento versione a 3.17.0 e conservazione service worker (R5).
5. Test sintassi, struttura ZIP e test manuale della compilazione da GitHub.

## Verifica

| Criterio | Stato | Evidenza / limite |
|---|---|---|
| R1 | verificato | pulsante e vista presenti nel codice |
| R2 | parziale | controlli implementati; test interattivo browser non eseguito |
| R3 | verificato staticamente | file GitHub Actions dedicato; conferma prima di sostituire un omonimo |
| R4 | verificato staticamente | navigazione alla vista Pubblica senza scritture automatiche |
| R5 | parziale | versione/cache aggiornate, JS compilabile; regressioni UI da collaudare |
| R6 | non verificabile | compilazione GitHub richiede pubblicazione autorizzata e run GitHub Actions |

## Limiti noti

- È un flusso in due passi: scarica ZIP preparato e pubblica il nuovo ZIP con Pubblica.
- Non firma release; per aggiornamenti affidabili serve un keystore protetto e persistente.
- ZIP massimo 40 MiB, workflow impostato per JDK 17 e Gradle 8.9 se manca il wrapper.
- Non sostituisce la compilazione Gradle direttamente sul telefono.
- Repository Android già esistenti possono richiedere JDK/Gradle specifici o ulteriori dipendenze.
