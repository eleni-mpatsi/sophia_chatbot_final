# Rasa Chatbot – Task-Oriented Dialogue System

## Overview

This project implements a task-oriented conversational assistant using Rasa, designed as a proof of concept (PoC) for hands-free communication in motorcycle helmet telecommunication systems.

The assistant aims to support users in motion through structured, voice-driven interactions, enabling safe and efficient task execution without manual input.

### Core Features
- Structured multi-turn interactions via forms  
- Slot filling with validation  
- Handling interruptions during task execution  
- Experimentation with dialogue policies  
- Extensibility toward additional use cases and integrations

The system supports tasks such as:
- Initiating phone calls (via contact information collection)  
- Managing structured interactions through guided dialogue flows  
- Answering general queries and handling fallback scenarios  

Additionally, the system is designed to be easily extensible, as demonstrated by the music interaction module.

---

## Limitations and Notes

- During development, a persistent Rasa error  
  (`GraphComponentException: Error running graph component for node train_TEDPolicy0`)  
  significantly limited experimentation time. This issue appears unresolved in the Rasa community.
- As a result, the implementation prioritizes stability and completeness over complexity.
- Example dialogues and policy experiments are available in:  
  `/rasa_example_dialogs`
- Bot responses are highlighted in bold in the examples.

---

## Core Functionality

### 1. Form-Based Dialogue Management

The chatbot uses Rasa Forms to guide structured interactions.

---

### A. Contact Form (Call Someone)

The bot collects:
- First name  
- Last name  

#### Features:
- Input validation:
  - Minimum length of 3 characters  
  - Alphabetic characters only  
- Error handling:
  - Invalid inputs trigger clarification prompts  
- Interruption handling:
  - Chitchat (e.g., "are you a bot?") does not break the form flow  

---

### B. Music Form (Extensibility Demonstration)

The music interaction module is implemented as a **proof-of-concept for extending the system with additional task-oriented flows**.

The bot collects:
- Song title  
- Artist  

#### Purpose and Design:
- Demonstrates how new domains can be integrated using the same form-based architecture  
- Serves as a template for future integrations (e.g., media control, recommendations, external services)  
- Validates that the system can support **multiple independent task flows within a unified dialogue framework**

#### Current Implementation:
- Uses a small predefined list of songs/artists for demonstration purposes  
- Includes full validation and interruption handling logic  
- Maintains consistent conversational behavior with the rest of the system  

This module is intentionally designed as a **scalable placeholder**, showcasing how the assistant can be expanded beyond its core functionality without requiring architectural changes.

---

### C. External API Integration (Optional)

- Integration with NewsAPI  
- Retrieves and displays the top 2 news articles  

This demonstrates:
- API usage within `actions.py`  
- Dynamic response generation  

---

### D. Fallback Handling

- Custom fallback action implemented  
- When intent confidence is low:
  - The bot responds with: "please rephrase that"  

---

## Dialogue Policy Experiments

### Policies Evaluated

- RulePolicy  
- MemoizationPolicy  
- TEDPolicy  

---

### Key Findings

#### RulePolicy
- Increasing `core_fallback_threshold` (0.3 → 0.8):
  - Led to excessive fallback usage  
  - Reduced performance even for known intents  

Default configuration performed better.

---

#### MemoizationPolicy
- Tested `max_history = 3` and `5`  
- No significant difference observed  
- Struggled with paraphrased inputs  

---

#### TEDPolicy
- Compared default configuration with extended transformer setup  
- No significant performance improvement observed  
- Simpler configuration preferred  

---

## Best Performing Configuration

The most effective setup was:

- TEDPolicy + RulePolicy  

This combination achieved:
- Correct intent handling  
- Stable form completion  
- Robust interruption recovery  
- Natural conversational flow 
