# **Primordia Engine**

Primordia Engine is a grid-based artificial life simulation built in Python using Pygame.  
It simulates a world where multiple agents coexist, move, interact, and follow deterministic rules for resolving movement and collisions.  
The engine is designed from the ground up to support future features like food, energy, hunger, reproduction, predators, and evolving ecosystems.

Primordia Engine emphasizes **fairness, simultaneity, and clean world-state updates**, ensuring every agent acts independently with no bias caused by update order.  
This makes it ideal for artificial life experiments, evolutionary simulations, and emergent behavior studies.

---

# **Day 1 — Core Engine Implementation**

### **Grid Rendering**
A complete visual grid was implemented using Pygame.  
Each cell represents a discrete space in the world, with clear boundaries and adjustable cell size.  
The grid refreshes every frame, ensuring a stable visual foundation for all agent interactions.

### **Agent Architecture**
Agents were implemented as independent entities with:
- A grid position (row, col)
- A unique color
- A draw method for visual rendering
- A propose_move method defining their next action

Agents move in cardinal directions and remain bounded within world limits.

### **Movement Proposal System**
Instead of moving immediately, each agent generates a *proposal* for its next move.  
This proposal system allows:
- Simultaneous movement  
- Fair behavior  
- No order-dependent logic  

Every agent first decides where it *wants* to go before any movement is processed.

### **Grouping Proposals**
Proposals are grouped by target tile.  
This is crucial for detecting:
- Conflicts  
- Collisions  
- Multiple agents attempting the same tile  
- Whether a current occupant wants to stay  

This grouping is the core structure required for correct conflict resolution.

### **Conflict Resolution System**
A full tile-based resolution system was developed:
- If the current occupant of a tile chooses to **stay**, the tile becomes locked to them for the tick.
- If a tile is free and only one agent proposes it, the move is approved.
- If multiple agents propose the same free tile, a random winner is selected.
- All other agents attempting that tile are denied for that tick.

This prevents overlapping and ensures deterministic, unbiased behavior.

### **Simultaneous Movement Application**
After resolving all proposals:
1. All approved movements are stored.
2. All agents update their positions in one atomic step.

This makes every tick fair, consistent, and synchronous—like a real simulation should be.

---

# **Current Status (End of Day 1)**

Primordia Engine now features:
- A fully functional grid-based world  
- Independent multi-agent movement  
- Random-walk agent behavior  
- A robust propose → resolve → apply cycle  
- A complete conflict-resolution engine  
- Perfectly simultaneous movement  
- No overlapping, clipping, or ordering bias  

This foundation enables richer behaviors and future ecosystem mechanics to be built cleanly on top of it.

---

# **Project Vision**
Primordia Engine aims to grow into a sandbox for artificial life, emergent behavior, and evolutionary simulations.  
Future days will introduce:
- Food, hunger, and energy  
- Death & natural selection  
- Basic AI behaviors  
- Reproduction & mutation  
- Predator-prey dynamics  
- Ecosystem stability experiments  
- Agent stats, UI overlays, and analytics  

Primordia Engine is designed as a long-term evolving project, starting from simple grid motion and growing into a living digital world.

