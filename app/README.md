# FlourishAI: The Adaptive Multi-Agent Tutor 🎓✨

> > *Track: Agents for Good*

FlourishAI is a multi-agent system designed to provide personalized, accessible education for everyone—from students with Dyslexia/ADHD to PhD researchers. It features long-term memory, multimodal grading, and a self-correcting pedagogical loop.

## 🌟 Key Features

* **🧠 Multi-Agent Orchestration:** A central brain routes tasks to 6 specialized sub-agents.
* **🛡️ The Critic Loop:** A "Pedagogical Critic" agent audits every lesson for accessibility and safety before the user sees it.
* **💾 Long-Term Memory:** Users can save their progress via a unique 5-character Access Code.
* **👁️ Multimodal Grading:** Upload handwritten homework, and the Vision Agent grades it and offers feedback.
* **🎨 Smart Personas:** Switches instantly between "Coach," "Professor," and "Visual" teaching styles.
* **📊 Visual Analytics:** Generates Python-rendered progress charts, visual lessons on demand.

## 🏗️ Architecture

The system is built using **Google's Agent Development Kit (ADK)** and **Gemini 2.5**.

| Agent | Role | Model |
| :--- | :--- | :--- |
| **Orchestrator** | Routes traffic & manages state | 
| **User Profiler** | Interviews users & builds JSON profiles | 
| **Curriculum** | Generates lessons & researches topics | 
| **Critic** | Quality control & accessibility auditor | 
| **Assessment** | Generates quizzes & mock exams | 
| **Vision** | Analyzes images & handwriting and also creates Visual learning aids|

graph LR
    %% Styles
    classDef user fill:#f9f,stroke:#333,stroke-width:2px,color:black;
    classDef brain fill:#ff9900,stroke:#333,stroke-width:2px,color:black;
    classDef swarm fill:#4285F4,stroke:#333,stroke-width:2px,color:white;
    classDef tools fill:#34A853,stroke:#333,stroke-width:2px,color:white;
    classDef memory fill:#EA4335,stroke:#333,stroke-width:2px,color:white;

    %% Nodes
    User((User)):::user
    
    subgraph "Orchestration Layer (The Brain)"
        Orch[⚡ Orchestrator Agent<br><i>Gemini 2.5 Flash</i>]:::brain
    end

    subgraph "Specialist Swarm (The Experts)"
        Profiler[👤 User Profiler<br><i>Gemini 2.5 Flash</i>]:::swarm
        Curriculum[🎓 Curriculum Generator<br><i>Gemini 2.5 Pro</i>]:::swarm
        Critic[🛡️ Pedagogical Critic<br><i>Gemini 2.5 Pro</i>]:::swarm
        Assess[📝 Assessment Engine<br><i>Gemini 2.5 Pro</i>]:::swarm
        Vision[👁️ Vision Grader<br><i>Gemini 2.0 Flash</i>]:::swarm
        Analytics[📊 Analytics Reporter<br><i>Gemini 1.5 Flash</i>]:::swarm
        Visual[🎨 Visual Teacher<br><i>Gemini 2.5 Flash</i>]:::swarm
    end

    subgraph "Capability Layer (Tools & Memory)"
        Mem[(💾 Memory Bank<br><i>JSON + Access Codes</i>)]:::memory
        Search[🔍 Google Search]:::tools
        ImgGen[🖼️ Image Generator]:::tools
        CodeExec[🐍 Python Code Exec<br><i>Matplotlib</i>]:::tools
    end

    %% Signal Flow
    User <-->|Chat & Images| Orch
    
    %% Orchestrator Routing
    Orch -->|Start/Login| Profiler
    Orch -->|Learn| Curriculum
    Orch -->|Test/Quiz| Assess
    Orch -->|Upload Img| Vision
    Orch -->|Progress| Analytics
    Orch -->|Show/Draw| Visual

    %% The Quality Loop
    Curriculum -->|Draft Lesson| Critic
    Critic -->|❌ Reject/Fix| Curriculum
    Critic -->|✅ Approve| Orch

    %% Tool Connections
    Profiler -.->|Read/Write| Mem
    Orch -.->|Read/Write| Mem
    Curriculum -.->|Research| Search
    Assess -.->|Generate Qs| Search
    Vision -.->|Grade| Mem
    Analytics -.->|Visualize| CodeExec
    Visual -.->|Create| ImgGen

    %% Analytics Flow
    CodeExec -.->|Graph Img| Analytics