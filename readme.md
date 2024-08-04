# Conversational Multi-Agent AI Chatbot for Engineering Simulations using AutoGen + GPT-4o + Chainlit UI

![Graphical Abstract](https://github.com/karthik-codex/autogen_graphRAG/blob/main/images/1721017707759.jpg?raw=true](https://github.com/karthik-codex/autogen_FEA/blob/main/Article%202%20-%20Mech%20Agents/graphical%20abstract.png)

The application constructs a network of LLM-powered AI agents that autonomously create models and simulate problems in solid mechanics and fluid dynamics with minimal human input. The framwork consists of a team of conversational agents using Microsoft AutoGen, each a specialist in roles like planning, problem formulation, writing, debugging and executing codes, plotting and analysis, and result critique. They will work autonomously, correcting each other as needed to create and simulate FEA and CFD models using open-source Python libraries. OpenAI's GPT-4 is the powerhouse behind this. The framework is wrapped within a user interface using the Chainlit app.

The core of this implementation involves enabling AI agents to utilize open-source Python libraries and tools. To solve FEA or CFD problems, we need tools to script the geometry, solve it using numerical algorithms, and visualize the results. Libraries like gmsh, a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities, are used to create geometry or meshes. FEniCS, an open-source computing platform for solving partial differential equations (PDEs), is employed to formulate and run numerical simulations. For visualization, matplotlib is used for 2D geometries and pyvista for 3D geometries. Additional required libraries are listed in the requirements.txt.

## Useful Links 🔗

- **Medium Article:** Engineering with Next-Gen AI: Autonomous LLM Agents Solving Solid Mechanics & Fluid Dynamics [Medium.com](https://medium.com/@karthik.codex/autonomous-llm-agents-solving-solid-mechanics-fluid-dynamics-496cedf96073?source=friends_link&sk=85a2ed7a060aa5613907b5f1b15a1e39) 📚

## 📦 Installation and Setup

Follow these steps to set up and run the multi-agent Chainlit application:

1. **Create conda environment and install packages:**
    ```bash
    conda create -n fea_agents -c conda-forge fenics mshr
    conda activate fea_agents
    git clone https://github.com/karthik-codex/autogen_FEA.git
    cd autogen_FEA
    pip install -r requirements.txt    
    ```           
2. **Export OpenAI API key to environment**
    ```bash
    export API_KEY=<your_key_xxxxxx>
    ```    
3. **Run app:**
    ```bash
    chainlit run appUI.py
    ```                
