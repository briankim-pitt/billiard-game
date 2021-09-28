# billiard-game
 
**Project Description:**
- Pool game with various difficulty options and game modes
  
**Competitive Analysis:**  
- Most of the pool games online offer a similar approach for user interface, specifically how the user will control the angle and power of the cue, where the position of the mouse determines the angle and power. Also, they offer the choice between single and multiplayer. My project would implement these similar core mechanics. To differ from competitors, I will be allowing the user to choose from different difficulty options that limit hints to the angle and power the ball as you increase difficulty, and game modes, such as versing against an opponent, presenting obstacles on the table, and modifying the balls to have different properties.  
  
  
**Structural Plan:**
- The balls and the cue are organized as objects
- The different types of balls (Cue ball, Striped and Plain balls) are organized as
subclasses
- Different game modes will be made in separate files in order to keep the project
organized
  
**Algorithmic Plan:**
- Ball collisions:
- Based on storing direction(angle) of each instance of a ball as they move
- If two balls collide, the impact point between the two balls will determine the
angles they bounce off of
- The bounce angle will be the opposite of the angle from the center of the
ball to the impact point - Collisions with walls:
- Angle of bounce will be the opposite reference angle from wall
- Distribution of energy:
- Transfer of speed from one ball to the other will be divided by a specific
constant
