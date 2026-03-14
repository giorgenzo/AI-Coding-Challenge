# 📖 Glossario Tecnico — Progetto Mirror (Aggiornato)

> Tutti i termini tecnici usati nel progetto, spiegati in modo semplice e in italiano.

---

## 🤖 Machine Learning & Anomaly Detection

| Termine | Spiegazione |
|---------|-------------|
| **IsolationForest** | Algoritmo di ML che impara come si comporta un gruppo "normale" (classe 0). Se un nuovo dato è troppo diverso dal gruppo, lo segnala come anomalia. |
| **L0 Engine (llm)** | Motore del Layer 0 che usa un LLM "Nano" invece dell'IsolationForest. È più lento e ha un costo in token, ma è più preciso nel filtrare i falsi positivi iniziali. |
| **One-Class Classification** | Tecnica dove il modello impara solo una classe (quella "buona"). Tutto ciò che non rientra viene considerato anomalo. |
| **Inlier** | Un dato che il modello considera "normale" — rientra nella zona di benessere. |
| **Outlier** | Un dato che il modello considera "anomalo" e viene passato al Layer 1 per verifica. |
| **Anomaly Score** | Punteggio numerico che indica quanto un dato è "strano". Più è alto, più è anomalo. |
| **Contamination** | Percentuale stimata di dati anomali nel training set. Influisce sulla sensibilità del Layer 0. |

---

## 📈 Feature Engineering

| Termine | Spiegazione |
|---------|-------------|
| **Feature Engineering** | Creazione di nuovi indicatori partendo dai dati grezzi (es. calcolare la media dell'attività fisica). |
| **Cross-feature Interaction** | Indicatori nati combinando due metriche diverse (es. `activity_sleep_ratio`). Servono a catturare malesseri complessi. |
| **Sliding Window** | Finestra temporale (3 o 7 giorni) che scorre sui dati per calcolare trend e statistiche locali. |
| **ACF (Autocorrelation)** | Analisi dei ritardi temporali per scoprire i ritmi naturali (e le anomalie nei ritmi) di un cittadino. |
| **Location Entropy** | Misura della varietà dei luoghi visitati. Un calo improvviso può indicare isolamento o problemi di mobilità. |
| **Acceleration** | Tasso di cambiamento del trend. Se l'attività fisica cala *sempre più velocemente*, l'accelerazione è negativa e pericolosa. |

---

## 🧠 Multi-Agent System (Swarm)

| Termine | Spiegazione |
|---------|-------------|
| **Swarm (Sciame)** | Gruppo di agenti che lavorano insieme su un caso. Ogni agente vota e l'opinione finale è la sintesi del gruppo. |
| **RoleCoordinator** | L'agente "capo" che gestisce un gruppo specifico (es. esperti temporali) e decide quanti agenti attivare. |
| **Complexity Score** | Grado di incertezza di un caso. Se è alto, il sistema attiva più agenti (fino a 5) per quello sciame. |
| **Agreement Ratio** | Quanto gli esperti sono d'accordo tra loro. Un basso accordo indica un caso molto difficile da interpretare. |
| **Staggered Temperatures** | Tecnica che dà temperature diverse agli agenti dello sciame per forzare punti di vista differenti ed evitare il pensiero di gruppo. |
| **Orchestrator** | L'agente di Layer 2 che legge i risultati di tutti gli sciami e prende la decisione finale di supporto. |

---

## 🔤 LLM & Configurazione

| Termine | Spiegazione |
|---------|-------------|
| **API Quota Deadlock** | Situazione in cui il sistema si ferma perché ha esaurito i crediti o le chiamate gratuite giornaliere (429 Rate Limit) per i modelli API. |
| **Clinical Thresholds** | Soglie mediche fisse (es. PAI < 30) inserite nei prompt per dare agli agenti un riferimento oggettivo di pericolo. |
| **Smart / Cheap Model** | Utilizzo di modelli potenti (es. Gemini Ultra) per le decisioni finali e modelli veloci (es. Gemini Flash) per l'analisi preliminare. |
| **JSON Mode** | Forza l'LLM a rispondere solo con dati strutturati, evitando chiacchiere e facilitando il lavoro del codice. |
| **Tenacity (Retry)** | Sistema che riprova automaticamente le chiamate LLM fallite per rate limiting o errori di rete. |

---

## 📦 RAG & Memoria

| Termine | Spiegazione |
|---------|-------------|
| **RAG (Retrieval-Augmented Generation)** | Permette agli agenti di "ricordare" casi passati simili prima di rispondere. Migliora la coerenza delle decisioni. |
| **Online RAG Learning** | Caricamento di nuovi casi nella memoria RAG *durante* l'esecuzione della valutazione, non solo nel training. |
| **Few-Shot Examples** | Esempi concreti passati inseriti nel prompt per spiegare all'agente "cosa cercare" nel caso attuale. |
| **ChromaDB** | Il database locale che funge da memoria a lungo termine del progetto Mirror. |

---

## 🔭 Observability

| Termine | Spiegazione |
|---------|-------------|
| **Langfuse** | Portale web usato per monitorare le chiamate LLM, i costi e il ragionamento logico di ogni singolo agente. |
| **Session ID** | Codice univoco che raggruppa tutte le attività di una corsa del pipeline, permettendo di vederle come un unico flusso su Langfuse. |
| **Trace** | Il "filo di Arianna" che permette di risalire dalla decisione dell'Orchestrator fino alla singola riga di log di ogni sottocomponente. |

---

## 🛠️ Architettura e Sistema di Generazione

| Termine | Spiegazione |
|---------|-------------|
| **Meta-Architect** | Sistema auto-generante principale che ingloba contesto (PDF e dati) e costruisce, testa e corregge autonomamente l'intero pipeline. |
| **Builder LLM** | Il Modello Linguistico a cui il Meta-Architect affida il compito di scrivere e riparare attivamente il codice Python. |
| **Self-Healing Loop** | Ciclo autonomo iterativo (fino a 15 volte) in cui il Meta-Architect esegue il codice, legge i log di errore e li usa per chiedere al Builder LLM di correggersi. |
| **CUSUM (Cumulative Sum)** | Algoritmo che accumula il "debito" anomalo nel tempo per individuare degradazioni progressive invece che falsi allarmi puntuali. |
| **Exponential Decay** | Decadimento temporale applicato al CUSUM per ogni evento normale (es. ridotto del 30%), che permette alle anomalie isolate di essere assorbite. |
| **Zero-Shot Entity Pre-Filtering** | Filtro matematico che salta intere analisi LLM per cittadini estremamente stabili (CV < 15%), riducendo chiamate e costi per entità palesemente sane. |
