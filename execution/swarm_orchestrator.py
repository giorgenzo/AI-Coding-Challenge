import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("swarm")

load_dotenv()

class SwarmOrchestrator:
    """
    Coordina un gruppo di agenti esperti per analizzare un caso
    e raggiungere un consenso o una sintesi finale.
    """
    
    def __init__(self, model_id="gpt-4o-mini"):
        api_key_val = os.getenv("OPENROUTER_API_KEY")
        self.model = ChatOpenAI(
            api_key=api_key_val,
            base_url="https://openrouter.ai/api/v1",
            model=model_id,
            temperature=0.7
        )
        
        self.experts = {
            "temporal": "Esperto di trend temporali e ritmi circadiani.",
            "physical": "Esperto di attività fisica e bio-metrica.",
            "social": "Esperto di isolamento sociale e pattern di mobilità."
        }

    def analyze_case(self, case_data):
        """Coordina gli esperti per analizzare il caso."""
        logger.info("Iniziando analisi Swarm...")
        
        expert_opinions = {}
        for role, desc in self.experts.items():
            logger.info(f"Consultando esperto: {role}")
            opinion = self._get_expert_opinion(role, desc, case_data)
            expert_opinions[role] = opinion
            
        logger.info("Sintetizzando le opinioni...")
        final_decision = self._synthesize(expert_opinions, case_data)
        
        return {
            "opinions": expert_opinions,
            "final_decision": final_decision
        }

    def _get_expert_opinion(self, role, description, case_data):
        prompt = f"""
        Sei un {description}
        Analizza i seguenti dati e identifica eventuali anomalie dal tuo punto di vista specialistico.
        
        DATI:
        {case_data}
        
        Fornisci un'analisi concisa (max 3 righe).
        """
        messages = [HumanMessage(content=prompt)]
        response = self.model.invoke(messages)
        return response.content.strip()

    def _synthesize(self, opinions, case_data):
        opinions_text = "\n".join([f"- {role.upper()}: {text}" for role, text in opinions.items()])
        
        prompt = f"""
        Sei l'Orchestratore del Mirror Project.
        Hai ricevuto le seguenti opinioni dagli esperti dello sciame:
        
        {opinions_text}
        
        DATI ORIGINALI:
        {case_data}
        
        Sulla base di questi input, fornisci una VALUTAZIONE FINALE strutturata in JSON:
        {{
            "anomaly_level": "Basso|Medio|Alto",
            "justification": "...",
            "recommended_action": "..."
        }}
        """
        messages = [
            SystemMessage(content="Rispondi solo in formato JSON valido."),
            HumanMessage(content=prompt)
        ]
        
        response = self.model.invoke(messages)
        return response.content.strip()

# --- Test ---
if __name__ == "__main__":
    test_case = "Utente di 75 anni. Attività fisica calata del 60% negli ultimi 3 giorni. Sonno irregolare. Nessuna uscita di casa segnalata dal GPS."
    swarm = SwarmOrchestrator()
    result = swarm.analyze_case(test_case)
    
    print("\n--- OPINIONI ESPERTI ---")
    for role, op in result['opinions'].items():
        print(f"[{role}]: {op}")
        
    print("\n--- DECISIONE FINALE ---")
    print(result['final_decision'])
