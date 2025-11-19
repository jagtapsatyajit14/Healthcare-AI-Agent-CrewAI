"""
AI Healthcare Assistant - Interactive CLI
Specialized healthcare agents powered by CrewAI and Gemini AI
"""

from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

def print_header():
    """Display welcome header"""
    print("\n" + "=" * 80)
    print("🏥 AI HEALTHCARE ASSISTANT")
    print("Medical Guidance | Health Information | Wellness Support")
    print("=" * 80)
    print("⚠️  DISCLAIMER: For informational purposes only")
    print("Always consult qualified healthcare professionals for medical advice")
    print("=" * 80)
    print()

def get_healthcare_specialist():
    """Let user select healthcare specialist"""
    print("👨‍⚕️ SELECT HEALTHCARE SPECIALIST:")
    print()
    
    specialists = {
        '1': ('Medical Advisor', 'General medical information and guidance'),
        '2': ('Symptom Analyzer', 'Analyze symptoms and suggest possible conditions'),
        '3': ('Treatment Recommender', 'Evidence-based treatment options and lifestyle changes'),
        '4': ('Nutrition Specialist', 'Dietary guidance and nutritional advice'),
        '5': ('Mental Health Counselor', 'Mental health support and coping strategies'),
        '6': ('Fitness Coach', 'Exercise guidance and fitness recommendations'),
        '7': ('Disease Educator', 'Disease information, prevention, and management')
    }
    
    for key, (role, desc) in specialists.items():
        print(f"  {key}. {role:<25} - {desc}")
    
    print()
    choice = input("Enter your choice (1-7): ").strip()
    
    if choice in specialists:
        role, description = specialists[choice]
        return role, description
    else:
        print("⚠️  Invalid choice. Using default 'Medical Advisor'")
        return specialists['1']

def get_health_query():
    """Get health query from user"""
    print("\n" + "-" * 80)
    print("📝 DESCRIBE YOUR HEALTH QUERY")
    print("-" * 80)
    print()
    print("Examples:")
    print("  • I have a persistent headache and sensitivity to light")
    print("  • What are healthy meal options for managing diabetes?")
    print("  • I feel anxious and stressed lately, what can I do?")
    print("  • Best exercises for lower back pain")
    print()
    print("Your query (press Enter twice when done):")
    print()
    
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            if lines:
                break
    
    return ' '.join(lines)

def consult_healthcare_agent(specialist, description, query, api_key):
    """Execute healthcare consultation"""
    print("\n" + "=" * 80)
    print(f"🔍 {specialist.upper()} IS ANALYZING YOUR QUERY...")
    print("=" * 80)
    print()
    
    try:
        # Agent configurations
        agent_configs = {
            "Medical Advisor": {
                "goal": "Provide accurate medical information and guidance",
                "backstory": """You are an experienced medical advisor with extensive knowledge 
                of various medical conditions, symptoms, and treatments. You provide clear, 
                evidence-based medical information while always emphasizing the importance 
                of consulting healthcare professionals for diagnosis and treatment."""
            },
            "Symptom Analyzer": {
                "goal": "Analyze symptoms and suggest possible conditions",
                "backstory": """You are a symptom analysis expert trained to identify patterns 
                in patient-reported symptoms. You provide possible explanations for symptoms, 
                assess severity, and recommend when immediate medical attention is needed. 
                You never provide definitive diagnoses."""
            },
            "Treatment Recommender": {
                "goal": "Suggest evidence-based treatment options and lifestyle changes",
                "backstory": """You are a treatment specialist knowledgeable about various 
                medical treatments, medications, therapies, and lifestyle modifications. 
                You provide comprehensive treatment information while emphasizing proper 
                medical supervision."""
            },
            "Nutrition Specialist": {
                "goal": "Provide dietary guidance and nutritional advice",
                "backstory": """You are a certified nutritionist with expertise in therapeutic 
                nutrition, dietary management of diseases, and healthy eating. You provide 
                personalized nutritional guidance based on health conditions and goals."""
            },
            "Mental Health Counselor": {
                "goal": "Provide mental health support and coping strategies",
                "backstory": """You are a compassionate mental health counselor trained in 
                psychology and therapeutic techniques. You provide emotional support, coping 
                strategies, and guidance for mental health concerns while recognizing when 
                professional help is needed."""
            },
            "Fitness Coach": {
                "goal": "Provide exercise guidance and fitness recommendations",
                "backstory": """You are a certified fitness coach with expertise in exercise 
                physiology, rehabilitation, and physical wellness. You create safe, effective 
                exercise recommendations tailored to individual health conditions and fitness levels."""
            },
            "Disease Educator": {
                "goal": "Educate about diseases, prevention, and management",
                "backstory": """You are a health educator specializing in disease information, 
                prevention strategies, and self-management techniques. You explain complex 
                medical concepts in clear, understandable language."""
            }
        }
        
        config = agent_configs.get(specialist, agent_configs["Medical Advisor"])
        
        # Create LLM
        llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.7,
            api_key=api_key
        )
        
        # Create healthcare agent
        agent = Agent(
            role=specialist,
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=False,
            llm=llm
        )
        
        # Create task
        task = Task(
            description=f"""
            As a {specialist}, analyze the following health query and provide helpful guidance:
            
            QUERY: {query}
            
            INSTRUCTIONS:
            1. Provide clear, accurate information
            2. If symptoms are mentioned, explain possible conditions (not diagnoses)
            3. Suggest when to seek immediate medical attention
            4. Provide practical recommendations
            5. Include relevant health tips
            6. Always remind that this is informational, not medical advice
            7. Be compassionate and supportive in tone
            
            Provide a comprehensive, well-structured response.
            """,
            agent=agent,
            expected_output="Comprehensive healthcare guidance with clear explanations"
        )
        
        # Create and run crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        
        return True, str(result)
        
    except Exception as e:
        return False, f"Error: {str(e)}\nPlease check your internet connection and API key."

def display_consultation_result(success, result, specialist):
    """Display the consultation response"""
    print("\n" + "=" * 80)
    if success:
        print(f"💡 {specialist.upper()} RESPONSE:")
    else:
        print("❌ ERROR:")
    print("=" * 80)
    print()
    print(result)
    print()
    print("=" * 80)
    if success:
        print("⚠️  DISCLAIMER: This information is for educational purposes only.")
        print("Always consult qualified healthcare professionals for medical advice.")
        print("=" * 80)

def main():
    """Main program loop"""
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY not found!")
        print("\nPlease ensure .env file exists with your API key.")
        print("Format: GOOGLE_API_KEY=your-key-here")
        return
    
    print_header()
    
    while True:
        # Get specialist
        specialist, description = get_healthcare_specialist()
        print(f"\n✅ Selected: {specialist}")
        print(f"   {description}")
        
        # Get query
        query = get_health_query()
        
        if not query.strip():
            print("\n⚠️  No query entered. Please try again.")
            continue
        
        # Run consultation
        success, result = consult_healthcare_agent(specialist, description, query, api_key)
        
        # Display result
        display_consultation_result(success, result, specialist)
        
        # Ask to continue
        print("\n" + "-" * 80)
        continue_choice = input("Would you like another consultation? (yes/no): ").strip().lower()
        
        if continue_choice not in ['yes', 'y']:
            print("\n👋 Thank you for using AI Healthcare Assistant!")
            print("Stay healthy and take care!")
            print("=" * 80)
            break
        
        print("\n\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Take care!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
