"""
AI Healthcare Assistant - Premium Healthcare Website GUI
Specialized healthcare agents powered by CrewAI and Gemini AI
Professional Medical Intelligence Platform using CustomTkinter 5.2.0
"""

import customtkinter as ctk
from tkinter import messagebox
from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
import threading
import time

# Load API key
load_dotenv()

# Set appearance and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Professional Healthcare Color Palette
COLORS = {
    "primary": "#0D7377",      # Deep Medical Teal
    "accent": "#14B8A6",       # Bright Teal
    "secondary": "#2E7D87",    # Professional Teal
    "success": "#10B981",      # Medical Green
    "warning": "#F59E0B",      # Attention Orange
    "danger": "#EF4444",       # Alert Red
    "bg_light": "#F8FAFC",     # Clean White
    "bg_dark": "#0F172A",      # Dark Slate
    "text_primary": "#0F172A", # Dark Text
    "text_secondary": "#64748B",# Gray Text
    "border": "#E2E8F0",       # Light Border
    "hover": "#0A5F6F",        # Darker Teal
}

class HealthcareAssistantGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MedAI - Intelligent Healthcare Platform")
        # Responsive window size tuned for 14" laptop screens (responsive)
        # Use available screen size but cap to a comfortable layout suitable for 14" displays
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        # Choose reasonable defaults but adapt to the real screen
        width = min(1200, max(1000, screen_w - 150))
        height = min(800, max(640, screen_h - 120))
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(900, 600)
        self.root.update_idletasks()

        # Determine a UI scale factor based on screen resolution so fonts/paddings shrink on smaller laptops
        # Allow a bit more shrinking on smaller displays (floor 0.72) for 14" screens
        avg_ratio = ((screen_w / 1366) + (screen_h / 768)) / 2
        self.scale = max(0.72, min(0.95, avg_ratio))

        # Helper to scale font sizes
        def sf(sz):
            return max(9, int(sz * self.scale))

        # Predefine scaled fonts used across the UI for consistent sizing
        # Increase base sizes for improved readability on laptop screens
        self.font_xlarge = ctk.CTkFont(family="Arial", size=sf(32), weight="bold")
        self.font_large = ctk.CTkFont(family="Arial", size=sf(20), weight="bold")
        self.font_med_bold = ctk.CTkFont(family="Arial", size=sf(18), weight="bold")
        self.font_med = ctk.CTkFont(family="Arial", size=sf(15))
        self.font_norm = ctk.CTkFont(family="Arial", size=sf(13))
        self.font_small = ctk.CTkFont(family="Arial", size=sf(12))
        
        # Configure window
        self.root.configure(fg_color=COLORS["bg_light"])
        
        # Check API key (if missing, continue in demo mode so layout can be tested)
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            messagebox.showwarning(
                "Warning",
                "GOOGLE_API_KEY not found in .env file — running in demo mode (consultation disabled)."
            )
            self.demo_mode = True
        else:
            self.demo_mode = False
        
        self.is_processing = False
        self.consultation_history = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the professional healthcare website-style UI"""
        
        # Configure main grid
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # ===== NAVIGATION BAR =====
        self.setup_navbar()
        
        # ===== MAIN CONTENT AREA =====
        main_container = ctk.CTkFrame(self.root, fg_color=COLORS["bg_light"])
        main_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Create tabbed interface
        self.setup_tabbed_interface(main_container)
    
    def setup_navbar(self):
        """Create professional navigation bar"""
        # Adjust navbar height relative to window height for better fit on smaller screens
        nav_height = max(56, int(self.root.winfo_height() * 0.09))
        navbar = ctk.CTkFrame(self.root, fg_color=COLORS["primary"], height=nav_height)
        navbar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        navbar.grid_propagate(False)
        
        # Logo and title area
        logo_frame = ctk.CTkFrame(navbar, fg_color=COLORS["primary"])
        logo_frame.pack(side="left", padx=25, pady=15)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🏥 MedAI",
            font=self.font_xlarge,
            text_color="white"
        )
        logo_label.pack(side="left")
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Intelligent Healthcare Platform",
            font=self.font_norm,
            text_color=COLORS["accent"]
        )
        subtitle_label.pack(side="left", padx=(15, 0))
        
        # Status indicator
        status_frame = ctk.CTkFrame(navbar, fg_color=COLORS["primary"])
        status_frame.pack(side="right", padx=25, pady=15)
        
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="● Ready",
            font=self.font_med,
            text_color=COLORS["success"]
        )
        self.status_indicator.pack()
    
    def setup_tabbed_interface(self, parent):
        """Create tabbed interface with multiple sections"""
        tabview = ctk.CTkTabview(
            parent,
            fg_color=COLORS["bg_light"],
            text_color=COLORS["text_primary"],
            border_color=COLORS["border"],
            border_width=2
        )
        # Slightly smaller padding to fit smaller screens better
        tabview.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Add tabs
        self.setup_consultation_tab(tabview.add("🩺 Consultation"))
        self.setup_health_assessment_tab(tabview.add("📊 Health Assessment"))
        self.setup_wellness_tips_tab(tabview.add("💡 Wellness Tips"))
        self.setup_doctor_profiles_tab(tabview.add("👨‍⚕️ Specialists"))
        self.setup_history_tab(tabview.add("📋 History"))
    
    def setup_consultation_tab(self, tab):
        """Main consultation interface with horizontal split layout"""
        tab.grid_rowconfigure(0, weight=0)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        # Header card
        header_card = ctk.CTkFrame(tab, fg_color="white", border_width=2, border_color=COLORS["border"])
        header_card.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        header_title = ctk.CTkLabel(
            header_card,
            text="💬 Get Medical Guidance",
            font=self.font_med_bold,
            text_color=COLORS["primary"]
        )
        header_title.pack(pady=(15, 5), padx=15)
        
        header_desc = ctk.CTkLabel(
            header_card,
            text="Consult with AI-powered medical specialists for instant healthcare guidance",
            font=self.font_small,
            text_color=COLORS["text_secondary"]
        )
        header_desc.pack(pady=(0, 15), padx=15)
        
        # Main horizontal split container
        main_container = ctk.CTkFrame(tab, fg_color=COLORS["bg_light"])
        main_container.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 8))
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # ===== LEFT SIDE - INPUT SECTION =====
        left_frame = ctk.CTkFrame(main_container, fg_color="white", border_width=1, border_color=COLORS["border"])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        left_frame.grid_rowconfigure(3, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # Specialist selection
        specialist_label = ctk.CTkLabel(
            left_frame,
            text="👨‍⚕️ Select Specialist",
            font=self.font_med_bold,
            text_color=COLORS["text_primary"]
        )
        specialist_label.pack(anchor="w", padx=10, pady=(10, 4))
        
        specialist_info = ctk.CTkLabel(
            left_frame,
            text="Choose the right healthcare expert for your needs",
            font=self.font_small,
            text_color=COLORS["text_secondary"]
        )
        specialist_info.pack(anchor="w", padx=10, pady=(0, 8))
        
        self.specialist_var = ctk.StringVar(value="Medical Advisor")
        specialists = [
            "Medical Advisor",
            "Symptom Analyzer",
            "Treatment Recommender",
            "Nutrition Specialist",
            "Mental Health Counselor",
            "Fitness Coach",
            "Disease Educator",
            "Preventive Medicine Expert",
            "Emergency Response Advisor"
        ]
        
        specialist_combo = ctk.CTkComboBox(
            left_frame,
            values=specialists,
            variable=self.specialist_var,
            state="readonly",
            font=self.font_norm,
            height=36,
            fg_color="white",
            border_color=COLORS["border"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["primary"]
        )
        specialist_combo.pack(fill="x", padx=10, pady=(0, 12))
        
        # Query input label
        query_label = ctk.CTkLabel(
            left_frame,
            text="📝 Describe Your Health Concern",
            font=self.font_med_bold,
            text_color=COLORS["text_primary"]
        )
        query_label.pack(anchor="w", padx=10, pady=(0, 6))
        
        # Query input textbox
        self.query_input = ctk.CTkTextbox(
            left_frame,
            font=self.font_norm,
            fg_color=COLORS["bg_light"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"]
        )
        self.query_input.pack(fill="both", expand=True, padx=10, pady=(0, 12))
        self.query_input.insert("1.0", "Describe your symptoms or health question in detail...")
        self.query_input.bind("<FocusIn>", self._clear_placeholder)
        self.query_input.bind("<FocusOut>", self._add_placeholder)
        
        # Action buttons
        button_frame = ctk.CTkFrame(left_frame, fg_color="white")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        button_frame.grid_columnconfigure(0, weight=1)
        
        consult_btn = ctk.CTkButton(
            button_frame,
            text="🩺 Get Guidance",
            command=self.run_consultation,
            font=self.font_med_bold,
            height=36,
            fg_color=COLORS["primary"],
            hover_color=COLORS["hover"],
            text_color="white"
        )
        consult_btn.pack(side="left", padx=(0, 8), fill="x", expand=True)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_all,
            font=self.font_med_bold,
            height=34,
            fg_color=COLORS["danger"],
            hover_color="#c82828",
            text_color="white",
            width=80
        )
        clear_btn.pack(side="left")
        
        # ===== RIGHT SIDE - OUTPUT SECTION =====
        right_frame = ctk.CTkFrame(main_container, fg_color="white", border_width=1, border_color=COLORS["border"])
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        output_label = ctk.CTkLabel(
            right_frame,
            text="💡 AI Medical Guidance",
            font=self.font_med_bold,
            text_color=COLORS["text_primary"]
        )
        output_label.pack(anchor="w", padx=15, pady=(12, 8))
        
        self.output_text = ctk.CTkTextbox(
            right_frame,
            font=self.font_small,
            fg_color=COLORS["bg_light"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"]
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 12))
        self.output_text.configure(state="disabled")
        
        # Initial placeholder
        self.output_text.configure(state="normal")
        self.output_text.insert("1.0", "🏥 Enter your health query and click 'Get Guidance' to receive AI-powered medical advice from our specialists.\n\nThis is informational only. Always consult qualified healthcare professionals for medical diagnosis and treatment.")
        self.output_text.configure(state="disabled")
    
    def setup_health_assessment_tab(self, tab):
        """Health assessment questionnaire tab"""
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            tab,
            text="📊 Health Assessment",
            font=self.font_large,
            text_color=COLORS["primary"]
        )
        header.pack(pady=(12, 8), padx=10)
        
        # Assessment sections
        assessment_frame = ctk.CTkFrame(tab, fg_color="white", border_width=1, border_color=COLORS["border"])
        assessment_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        assessment_text = ctk.CTkLabel(
            assessment_frame,
            text="""🏥 QUICK HEALTH ASSESSMENT

• Vital Signs Check
  - Blood Pressure, Heart Rate, Temperature
  - Oxygen Level, Respiratory Rate

• Medical History Review
  - Past conditions and treatments
  - Current medications
  - Allergies and sensitivities

• Lifestyle Evaluation
  - Sleep patterns and quality
  - Exercise and physical activity
  - Diet and nutrition habits
  - Stress levels and mental health

• Symptom Analysis
  - Current health concerns
  - Duration and severity
  - Associated factors

Click the Consultation tab to discuss any specific health concerns with our AI specialists.
Our medical experts can provide personalized guidance based on your assessment.""",
            font=self.font_norm,
            text_color=COLORS["text_primary"],
            justify="left"
        )
        assessment_text.pack(fill="both", expand=True, padx=12, pady=12)
    
    def setup_wellness_tips_tab(self, tab):
        """Wellness and health tips tab"""
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            tab,
            text="💡 Wellness & Prevention Tips",
            font=self.font_large,
            text_color=COLORS["primary"]
        )
        header.pack(pady=(12, 8), padx=10)
        
        # Tips content
        tips_frame = ctk.CTkScrollableFrame(tab, fg_color="white", border_width=1, border_color=COLORS["border"])
        tips_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        tips_content = [
            ("🥗 Nutrition", "Eat balanced meals with fruits, vegetables, and lean proteins. Stay hydrated with 8+ glasses of water daily."),
            ("🏃 Exercise", "Aim for 150 minutes of moderate exercise weekly. Include strength training 2-3 times per week."),
            ("😴 Sleep", "Maintain 7-9 hours of quality sleep. Keep consistent sleep schedule for better health."),
            ("🧘 Stress Management", "Practice meditation, yoga, or deep breathing. Take regular breaks and maintain work-life balance."),
            ("🚫 Avoid Bad Habits", "Limit alcohol, avoid smoking, and reduce sugar intake. These significantly impact long-term health."),
            ("🏥 Regular Check-ups", "Visit healthcare providers annually. Early detection prevents serious conditions."),
            ("💚 Mental Health", "Maintain social connections. Seek professional help when needed. Mental health is crucial."),
            ("🧠 Brain Health", "Stay mentally active with reading and learning. Social engagement keeps mind sharp.")
        ]
        
        for title, content in tips_content:
            tip_item = ctk.CTkFrame(tips_frame, fg_color=COLORS["bg_light"], border_width=1, border_color=COLORS["border"])
            tip_item.pack(fill="x", padx=8, pady=6)
            
            tip_title = ctk.CTkLabel(
                tip_item,
                text=title,
                font=self.font_med_bold,
                text_color=COLORS["primary"]
            )
            tip_title.pack(anchor="w", padx=10, pady=(8, 4))

            tip_text = ctk.CTkLabel(
                tip_item,
                text=content,
                font=self.font_small,
                text_color=COLORS["text_secondary"],
                justify="left",
                wraplength=420
            )
            tip_text.pack(anchor="w", padx=10, pady=(0, 8))
    
    def setup_doctor_profiles_tab(self, tab):
        """Healthcare specialists profiles"""
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            tab,
            text="👨‍⚕️ Our Healthcare Specialists",
            font=self.font_large,
            text_color=COLORS["primary"]
        )
        header.pack(pady=(20, 10), padx=15)
        
        # Specialists info
        specialists_frame = ctk.CTkScrollableFrame(tab, fg_color="white", border_width=1, border_color=COLORS["border"])
        specialists_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        specialists_data = [
            ("Medical Advisor", "🏥", "General medical consultation and guidance"),
            ("Symptom Analyzer", "🔍", "Detailed symptom analysis and assessment"),
            ("Treatment Recommender", "💊", "Evidence-based treatment options"),
            ("Nutrition Specialist", "🥗", "Personalized nutrition and diet plans"),
            ("Mental Health Counselor", "🧠", "Mental health support and wellness"),
            ("Fitness Coach", "💪", "Exercise programs and fitness guidance"),
            ("Disease Educator", "📚", "Disease information and management"),
            ("Preventive Medicine", "🛡️", "Prevention strategies and wellness"),
            ("Emergency Advisor", "🚨", "Emergency response and crisis management")
        ]
        
        for name, icon, desc in specialists_data:
            specialist_card = ctk.CTkFrame(specialists_frame, fg_color=COLORS["bg_light"], border_width=2, border_color=COLORS["accent"])
            specialist_card.pack(fill="x", padx=10, pady=8)
            
            title_frame = ctk.CTkFrame(specialist_card, fg_color=COLORS["bg_light"])
            title_frame.pack(fill="x", padx=12, pady=(10, 5))
            
            spec_icon = ctk.CTkLabel(
                title_frame,
                text=f"{icon} {name}",
                font=self.font_med_bold,
                text_color=COLORS["primary"]
            )
            spec_icon.pack(anchor="w")
            
            spec_desc = ctk.CTkLabel(
                specialist_card,
                text=desc,
                font=self.font_small,
                text_color=COLORS["text_secondary"],
                justify="left",
                wraplength=500
            )
            spec_desc.pack(anchor="w", padx=12, pady=(0, 10))
    
    def setup_history_tab(self, tab):
        """Consultation history tab"""
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            tab,
            text="📋 Consultation History",
            font=self.font_large,
            text_color=COLORS["primary"]
        )
        header.pack(pady=(20, 10), padx=15)
        
        # History content
        self.history_text = ctk.CTkTextbox(
            tab,
            font=self.font_small,
            fg_color=COLORS["bg_light"],
            text_color=COLORS["text_primary"],
            border_width=1,
            border_color=COLORS["border"]
        )
        self.history_text.pack(fill="both", expand=True, padx=15, pady=15)
        self.history_text.configure(state="disabled")
        
        self.update_history_display()
    
    def _clear_placeholder(self, event):
        """Clear placeholder text"""
        placeholder = "Describe your symptoms or health question in detail..."
        if self.query_input.get("1.0", "end-1c") == placeholder:
            self.query_input.delete("1.0", "end")
    
    def _add_placeholder(self, event):
        """Add placeholder text back if empty"""
        if not self.query_input.get("1.0", "end-1c").strip():
            placeholder = "Describe your symptoms or health question in detail..."
            self.query_input.insert("1.0", placeholder)
    
    def clear_all(self):
        """Clear input and output"""
        self.query_input.delete("1.0", "end")
        placeholder = "Describe your symptoms or health question in detail..."
        self.query_input.insert("1.0", placeholder)
        
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        
        self.status_indicator.configure(text="● Ready", text_color=COLORS["success"])
    
    def run_consultation(self):
        """Handle consultation request"""
        if self.is_processing:
            messagebox.showwarning("Processing", "AI is already analyzing your query!")
            return

        # If running in demo mode (no API key), block consultation runs
        if getattr(self, 'demo_mode', False):
            messagebox.showinfo(
                "Demo Mode",
                "Consultation is disabled in demo mode. Set GOOGLE_API_KEY in your .env to enable full functionality."
            )
            return
        
        # Get query
        query = self.query_input.get("1.0", "end-1c").strip()
        placeholder = "Describe your symptoms or health question in detail..."
        
        if not query or query == placeholder:
            messagebox.showwarning("Input Required", "Please describe your health query!")
            return
        
        # Clear output
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", "🔄 AI specialist is analyzing your query...")
        self.output_text.configure(state="disabled")
        
        # Update status
        self.is_processing = True
        self.status_indicator.configure(text="● Analyzing", text_color=COLORS["warning"])
        
        # Run in thread
        thread = threading.Thread(target=self.execute_consultation, args=(query,))
        thread.daemon = True
        thread.start()
    
    def execute_consultation(self, query):
        """Execute consultation in background thread"""
        try:
            specialist = self.specialist_var.get()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Agent configurations
            agent_configs = {
                "Medical Advisor": {
                    "role": "Medical Advisor",
                    "goal": "Provide accurate medical information and comprehensive guidance",
                    "backstory": """You are an experienced medical advisor with extensive knowledge 
                    of various medical conditions, symptoms, and treatments. You provide clear, 
                    evidence-based medical information while emphasizing the importance of consulting 
                    healthcare professionals for diagnosis and treatment."""
                },
                "Symptom Analyzer": {
                    "role": "Symptom Analyzer",
                    "goal": "Analyze symptoms and suggest possible conditions",
                    "backstory": """You are a symptom analysis expert trained to identify patterns 
                    in patient-reported symptoms. You provide possible explanations for symptoms, 
                    assess severity, and recommend when immediate medical attention is needed."""
                },
                "Treatment Recommender": {
                    "role": "Treatment Recommender",
                    "goal": "Suggest evidence-based treatment options",
                    "backstory": """You are a treatment specialist knowledgeable about various 
                    medical treatments, medications, and therapies. You provide comprehensive 
                    treatment information while emphasizing proper medical supervision."""
                },
                "Nutrition Specialist": {
                    "role": "Nutrition Specialist",
                    "goal": "Provide dietary guidance and nutritional advice",
                    "backstory": """You are a certified nutritionist with expertise in therapeutic 
                    nutrition and dietary management of diseases. You provide personalized 
                    nutritional guidance based on health conditions."""
                },
                "Mental Health Counselor": {
                    "role": "Mental Health Counselor",
                    "goal": "Provide mental health support and coping strategies",
                    "backstory": """You are a compassionate mental health counselor trained in 
                    psychology and therapeutic techniques. You provide emotional support, coping 
                    strategies, and guidance for mental health concerns."""
                },
                "Fitness Coach": {
                    "role": "Fitness Coach",
                    "goal": "Provide exercise guidance and fitness recommendations",
                    "backstory": """You are a certified fitness coach with expertise in exercise 
                    physiology and rehabilitation. You create safe, effective exercise recommendations 
                    tailored to individual health conditions."""
                },
                "Disease Educator": {
                    "role": "Disease Educator",
                    "goal": "Educate about diseases, prevention, and management",
                    "backstory": """You are a health educator specializing in disease information 
                    and prevention strategies. You explain complex medical concepts in clear language."""
                },
                "Preventive Medicine Expert": {
                    "role": "Preventive Medicine Expert",
                    "goal": "Provide prevention strategies and wellness recommendations",
                    "backstory": """You are a preventive medicine expert focused on disease prevention 
                    and health promotion. You provide actionable recommendations for maintaining health."""
                },
                "Emergency Response Advisor": {
                    "role": "Emergency Response Advisor",
                    "goal": "Provide emergency guidance and critical response information",
                    "backstory": """You are an emergency medicine advisor trained in crisis management. 
                    You provide immediate guidance for emergencies and identify when to call emergency services."""
                }
            }
            
            config = agent_configs.get(specialist, agent_configs["Medical Advisor"])
            
            # Create LLM
            llm = LLM(
                model="gemini/gemini-2.5-flash",
                temperature=0.7,
                api_key=self.api_key
            )
            
            # Create agent
            agent = Agent(
                role=config["role"],
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
                3. Suggest when to seek medical attention
                4. Provide practical recommendations
                5. Always remind this is informational, not medical advice
                6. Be compassionate and supportive
                
                Provide a comprehensive, well-structured response.
                """,
                agent=agent,
                expected_output="Comprehensive healthcare guidance"
            )
            
            # Create crew and execute
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=False
            )
            
            result = crew.kickoff()
            
            # Format result
            formatted_result = f"""
┌─────────────────────────────────────────────────────────┐
│ 🏥 {specialist.upper()}
└─────────────────────────────────────────────────────────┘
📅 Consultation Date: {timestamp}

{result}

─────────────────────────────────────────────────────────

⚠️  MEDICAL DISCLAIMER
This guidance is informational only and not a substitute for 
professional medical advice. Always consult qualified healthcare 
professionals for diagnosis, treatment, and emergency situations.

─────────────────────────────────────────────────────────"""
            
            # Add to history
            history_entry = f"\n[{timestamp}] {specialist}: {query[:100]}...\n"
            self.consultation_history.append(history_entry)
            
            # Display result
            self.root.after(0, self.display_result, formatted_result)
            
        except Exception as e:
            # Log exception to console for debugging
            print("Consultation error:", repr(e))

            # Provide a friendly fallback (demo) response so the UI stays usable
            simulated_result = f"""
┌─────────────────────────────────────────────────────────┐
│ 🏥 {specialist.upper()} (Demo Response)
└─────────────────────────────────────────────────────────┘
📅 Consultation Date: {timestamp}

It appears the live AI consultation failed to complete (network or API error).
Below is a simulated guidance response so you can continue testing the application layout and flow.

-- SAMPLE GUIDANCE START --

Thank you for describing your concern. Based on the symptoms you've provided, here are some possibilities and suggestions:

- Common causes may include muscle strain, overuse, or minor nerve irritation.
- If you have sudden severe pain, numbness, weakness, or loss of function, seek immediate medical attention.
- For mild to moderate pain: rest, ice, compression, elevation (RICE) and use over-the-counter analgesics as appropriate.
- Monitor for worsening symptoms and consult a healthcare professional if symptoms persist beyond a few days.

-- SAMPLE GUIDANCE END --

⚠️ Note: This is a simulated message. The real AI consultation failed with error: {str(e)}

"""

            # Add to history with an indicator that this was a fallback
            history_entry = f"\n[{timestamp}] {specialist} (demo fallback): {query[:100]}...\n"
            self.consultation_history.append(history_entry)

            # Display the simulated result instead of an error popup
            self.root.after(0, self.display_result, simulated_result)
    
    def display_result(self, result):
        """Display consultation result"""
        try:
            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
            self.output_text.see("1.0")  # Ensure text is visible
            self.output_text.configure(state="disabled")
            
            self.is_processing = False
            self.status_indicator.configure(text="● Complete", text_color=COLORS["success"])
            self.update_history_display()
        except Exception as e:
            print(f"Error displaying result: {e}")
            self.is_processing = False
            self.status_indicator.configure(text="● Error", text_color=COLORS["danger"])
    
    def display_error(self, error_msg):
        """Display error message"""
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", error_msg)
        self.output_text.configure(state="disabled")
        
        self.is_processing = False
        self.status_indicator.configure(text="● Error", text_color=COLORS["danger"])
        messagebox.showerror("Error", "Consultation failed. Check output for details.")
    
    def update_history_display(self):
        """Update consultation history display"""
        if hasattr(self, 'history_text'):
            self.history_text.configure(state="normal")
            self.history_text.delete("1.0", "end")
            
            if self.consultation_history:
                header = "📋 YOUR CONSULTATION HISTORY\n" + "="*50 + "\n\n"
                self.history_text.insert("1.0", header)
                for entry in reversed(self.consultation_history):
                    self.history_text.insert("end", entry)
            else:
                self.history_text.insert("1.0", "No consultations yet.\n\nUse the Consultation tab to start your first medical consultation.")
            
            self.history_text.configure(state="disabled")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = HealthcareAssistantGUI()
    app.run()
