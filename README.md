# ML-DM
An AI-driven tool designed for Dungeon Masters (DMs) in tabletop role-playing games. 

## Project description
Proposal: AI-Powered Dungeon Master Assistant with RAG
High-Level Concept: An AI-driven tool designed for Dungeon Masters (DMs) in tabletop role-playing games. The tool will leverage LangChain's Retrieval-Augmented Generation (RAG) to fetch relevant information from a campaign database and enhance storytelling in real-time. Using LLMs, the assistant will generate narrative suggestions, enemy encounters, and loot tailored to the game's current state based on prior campaign history and player choices.
Front End: A Flask web interface enables Dungeon Masters to manage game sessions, import custom maps, and view AI-generated suggestions in real-time. The interface will allow for intuitive interaction, such as token placement on a visual map and dialogue generation for non-player characters (NPCs).
Database:
*	Player Profiles: Stores character information 
    * Stats, Skills, Background
    * Inventory
    * Actions
*	Campaign Logs: 
    * Stores the narrative history, encounters, and NPC details.

## Retrieval-Augmented Generation (RAG) 
 - The model will retrieve relevant parts of the campaign history to generate contextually appropriate suggestions for ongoing gameplay.
Tools:
*	LangChain: To query the campaign database using RAG and generate context-aware narratives based on the retrieved information.
    *	Example:
            “Jenny (Witch in the woods):  I have a request for you complete. I need a live troll to study their habits, and to fortify the defenses of the kingdom” 
*	Langflow: 
        * To integrate the LLM with the database and ensure smooth retrieval of campaign data in real time.
    *	Example: 
        * A player defeats a key NPC, which is stored in the database. When the DM asks for a follow-up encounter, the LLM knows not to suggest that NPC, thanks to the real-time update. This can also come up as a negative later on if the players defeat enough NPCs to trigger consequences in the campaign. It should also be able to move some story beats to other living NPC’s. 