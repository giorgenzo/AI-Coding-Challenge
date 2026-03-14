import os
import subprocess
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("self-healing")

load_dotenv()

class SelfHealingEngine:
    """
    Motore di auto-correzione che esegue codice Python,
    rileva errori e chiede a un LLM di ripararli.
    """
    
    def __init__(self, model_id="gpt-4o-mini", max_retries=5):
        api_key_val = os.getenv("OPENROUTER_API_KEY")
        self.model = ChatOpenAI(
            api_key=api_key_val,
            base_url="https://openrouter.ai/api/v1",
            model=model_id,
            temperature=0.2
        )
        self.max_retries = max_retries

    def run_and_heal(self, file_path):
        """Esegue il file e tenta di ripararlo fino a max_retries in caso di errore."""
        attempt = 0
        while attempt < self.max_retries:
            attempt += 1
            logger.info(f"Esecuzione {file_path} - Tentativo {attempt}/{self.max_retries}")
            
            result = subprocess.run(["python3", file_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Codice eseguito con successo!")
                print(result.stdout)
                return True
            
            # Errore rilevato
            error_msg = result.stderr
            logger.error(f"❌ Errore rilevato:\n{error_msg}")
            
            if attempt < self.max_retries:
                logger.info("🔧 Richiesta di riparazione all'AI...")
                self._heal(file_path, error_msg)
            else:
                logger.error("🚫 Massimo numero di tentativi raggiunto. Impossibile riparare.")
        
        return False

    def _heal(self, file_path, error_msg):
        """Chiede all'LLM di riparare il file basandosi sull'errore."""
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        prompt = f"""
        Il seguente codice Python è fallito con un errore.
        
        CODICE:
        ```python
        {code}
        ```
        
        ERRORE:
        ```
        {error_msg}
        ```
        
        Per favore, restituisci l'INTERO codice corretto, pronto per essere sovrascritto nel file.
        Non includere spiegazioni, solo il blocco di codice tra triple backticks.
        """
        
        messages = [
            SystemMessage(content="Sei un esperto sviluppatore Python specializzato nel debugging e nel self-healing code."),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        new_code = response.content.strip()
        
        # Estrai codice se l'LLM ha usato backticks
        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()
        elif "```" in new_code:
            new_code = new_code.split("```")[1].split("```")[0].strip()
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_code)
        
        logger.info(f"File {file_path} aggiornato con la correzione suggerita.")

# --- Test ---
if __name__ == "__main__":
    # Crea un file con un errore intenzionale
    buggy_file = "execution/buggy_script.py"
    with open(buggy_file, "w") as f:
        f.write("print('Hello World')\nresult = 10 / 0  # ZeroDivisionError")

    engine = SelfHealingEngine()
    engine.run_and_heal(buggy_file)
