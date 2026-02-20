"""
Stickman character rendering and animation system.
Draws and animates the stickman character based on dance styles and user input.
"""

import cv2
import numpy as np
import math
from utils import (
    HEAD_RADIUS, BODY_LENGTH, ARM_LENGTH, LEG_LENGTH, SHOULDER_WIDTH,
    STICKMAN_COLOR, BACKGROUND_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT,
    WALK_SPEED, clamp, draw_text_with_background
)
from animations import AnimationSystem, DanceTransition

class Stickman:
    """
    Stickman character class for rendering and animation.
    """
    
    def __init__(self, x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2):
        """
        Initialize the stickman character.
        
        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        
        # Animation system
        self.animation_system = AnimationSystem()
        self.transition_system = DanceTransition()
        
        # Movement
        self.velocity_x = 0
        self.facing_right = True
        
        # Visual properties
        self.color = STICKMAN_COLOR
        self.thickness = 3
        
        # State
        self.current_dance = "normal"
        self.is_moving = False
        
        print("✓ Stickman character initialized")
    
    def update(self, dt):
        """
        Update stickman state and animations.
        
        Args:
            dt (float): Time delta in seconds
        """
        # Update position with smooth movement
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1
        
        # Keep stickman within screen bounds
        self.x = clamp(self.x, 50, WINDOW_WIDTH - 50)
        self.y = clamp(self.y, 100, WINDOW_HEIGHT - 100)
        
        # Update animations
        self.animation_system.update(dt)
        self.transition_system.update(dt)
        
        # Update facing direction based on movement
        if abs(self.velocity_x) > 0.1:
            self.facing_right = self.velocity_x > 0
    
    def set_dance_style(self, dance_style):
        """
        Set the dance style with smooth transition.
        
        Args:
            dance_style (str): Dance style name
        """
        if dance_style != self.current_dance:
            # Start transition
            self.transition_system.start_transition(self.current_dance, dance_style)
            self.current_dance = dance_style
            self.animation_system.set_dance_style(dance_style)
    
    def move_left(self):
        """
        Move stickman to the left.
        """
        self.target_x -= WALK_SPEED
        self.velocity_x = -WALK_SPEED
        self.is_moving = True
    
    def move_right(self):
        """
        Move stickman to the right.
        """
        self.target_x += WALK_SPEED
        self.velocity_x = WALK_SPEED
        self.is_moving = True
    
    def stop_moving(self):
        """
        Stop stickman movement.
        """
        self.velocity_x = 0
        self.is_moving = False
    
    def special_dance(self):
        """
        Trigger special dance animation.
        """
        self.set_dance_style("breakdance")
        # Add some visual flair
        self.color = (255, 100, 100)  # Red tint for special dance
    
    def reset_to_normal(self):
        """
        Reset stickman to normal state.
        """
        self.set_dance_style("normal")
        self.color = STICKMAN_COLOR
        self.stop_moving()
    
    def get_body_positions(self):
        """
        Calculate all body part positions based on current animation state.
        
        Returns:
            dict: Dictionary containing all body part positions
        """
        # Get animation offsets
        body_offset = self.animation_system.get_body_animation()
        head_offset = self.animation_system.get_head_animation()
        left_arm_offset = self.animation_system.get_arm_animation(True)
        right_arm_offset = self.animation_system.get_arm_animation(False)
        left_leg_offset = self.animation_system.get_leg_animation(True)
        right_leg_offset = self.animation_system.get_leg_animation(False)
        
        # Apply facing direction
        direction_multiplier = 1 if self.facing_right else -1
        
        # Base positions
        head_pos = (
            int(self.x + body_offset[0] + head_offset[0] * direction_multiplier),
            int(self.y - BODY_LENGTH + body_offset[1] + head_offset[1])
        )
        
        neck_pos = (
            int(self.x + body_offset[0]),
            int(self.y - BODY_LENGTH + body_offset[1])
        )
        
        shoulder_pos = (
            int(self.x + body_offset[0]),
            int(self.y - BODY_LENGTH * 0.7 + body_offset[1])
        )
        
        hip_pos = (
            int(self.x + body_offset[0]),
            int(self.y + body_offset[1])
        )
        
        # Arms
        left_shoulder = (
            int(shoulder_pos[0] - SHOULDER_WIDTH * direction_multiplier),
            shoulder_pos[1]
        )
        
        right_shoulder = (
            int(shoulder_pos[0] + SHOULDER_WIDTH * direction_multiplier),
            shoulder_pos[1]
        )
        
        left_hand = (
            int(left_shoulder[0] + left_arm_offset[0] * direction_multiplier),
            int(left_shoulder[1] + ARM_LENGTH + left_arm_offset[1])
        )
        
        right_hand = (
            int(right_shoulder[0] + right_arm_offset[0] * direction_multiplier),
            int(right_shoulder[1] + ARM_LENGTH + right_arm_offset[1])
        )
        
        # Legs
        left_foot = (
            int(hip_pos[0] - 10 * direction_multiplier + left_leg_offset[0] * direction_multiplier),
            int(hip_pos[1] + LEG_LENGTH + left_leg_offset[1])
        )
        
        right_foot = (
            int(hip_pos[0] + 10 * direction_multiplier + right_leg_offset[0] * direction_multiplier),
            int(hip_pos[1] + LEG_LENGTH + right_leg_offset[1])
        )
        
        return {
            'head': head_pos,
            'neck': neck_pos,
            'shoulder': shoulder_pos,
            'hip': hip_pos,
            'left_shoulder': left_shoulder,
            'right_shoulder': right_shoulder,
            'left_hand': left_hand,
            'right_hand': right_hand,
            'left_foot': left_foot,
            'right_foot': right_foot,
            'head_rotation': head_offset[2] if len(head_offset) > 2 else 0
        }
    
    def draw(self, frame):
        """
        Draw the stickman on the given frame.
        
        Args:
            frame: OpenCV image frame to draw on
        """
        positions = self.get_body_positions()
        
        # Draw body parts
        # Head
        cv2.circle(frame, positions['head'], HEAD_RADIUS, self.color, self.thickness)
        
        # Face (simple eyes and smile)
        eye_offset = 8 if self.facing_right else -8
        cv2.circle(frame, 
                  (positions['head'][0] + eye_offset, positions['head'][1] - 5), 
                  3, self.color, -1)
        cv2.circle(frame, 
                  (positions['head'][0] - eye_offset, positions['head'][1] - 5), 
                  3, self.color, -1)
        
        # Smile
        smile_start = (positions['head'][0] - 10, positions['head'][1] + 5)
        smile_end = (positions['head'][0] + 10, positions['head'][1] + 5)
        cv2.arc(frame, positions['head'], 12, 0, 180, self.color, 2)
        
        # Body
        cv2.line(frame, positions['neck'], positions['hip'], self.color, self.thickness)
        
        # Arms
        cv2.line(frame, positions['left_shoulder'], positions['left_hand'], self.color, self.thickness)
        cv2.line(frame, positions['right_shoulder'], positions['right_hand'], self.color, self.thickness)
        
        # Legs
        cv2.line(frame, positions['hip'], positions['left_foot'], self.color, self.thickness)
        cv2.line(frame, positions['hip'], positions['right_foot'], self.color, self.thickness)
        
        # Draw special effects
        self._draw_special_effects(frame)
        
        # Draw status text
        self._draw_status(frame)
    
    def _draw_special_effects(self, frame):
        """
        Draw special effects based on current dance style.
        
        Args:
            frame: OpenCV image frame to draw on
        """
        effects = self.animation_system.get_special_effects()
        
        # Draw particles
        for particle in effects.get('particles', []):
            if particle['type'] == 'sparkle':
                # Draw sparkle
                x = self.x + particle['x']
                y = self.y + particle['y']
                cv2.drawMarker(frame, (int(x), int(y)), (255, 255, 0), 
                             cv2.MARKER_STAR, 10, 2)
            
            elif particle['type'] == 'heart':
                # Draw simple heart shape
                x = self.x + particle['x']
                y = self.y + particle['y']
                cv2.putText(frame, '♥', (int(x), int(y)), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 100), 2)
        
        # Apply color tint if specified
        if effects.get('color_tint'):
            # This would require more complex image manipulation
            # For now, we'll just change the stickman color temporarily
            pass
    
    def _draw_status(self, frame):
        """
        Draw status information on the frame.
        
        Args:
            frame: OpenCV image frame to draw on
        """
        # Dance style indicator
        dance_text = f"Dance: {self.current_dance.upper()}"
        draw_text_with_background(frame, dance_text, (10, WINDOW_HEIGHT - 60), 0.7, 2)
        
        # Movement indicator
        if self.is_moving:
            move_text = f"Moving: {'→' if self.facing_right else '←'}"
            draw_text_with_background(frame, move_text, (10, WINDOW_HEIGHT - 30), 0.7, 2)
    
    def get_info(self):
        """
        Get current stickman information.
        
        Returns:
            dict: Current state information
        """
        return {
            'position': (self.x, self.y),
            'dance_style': self.current_dance,
            'is_moving': self.is_moving,
            'facing_right': self.facing_right,
            'animation_info': self.animation_system.get_animation_info()
        }


# Test function
def test_stickman():
    """
    Test the stickman rendering system.
    """
    print("Testing Stickman System...")
    
    # Create a stickman
    stickman = Stickman()
    
    # Create a test frame
    frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
    frame.fill(30)  # Dark background
    
    # Test different dance styles
    dance_styles = ["normal", "happy", "sad", "breakdance", "romantic", "aggressive"]
    
    for i, dance in enumerate(dance_styles):
        print(f"Testing {dance} dance...")
        
        # Set dance style
        stickman.set_dance_style(dance)
        
        # Update animation
        for frame_num in range(30):  # 1 second at 30 FPS
            stickman.update(0.033)
            
            # Clear frame
            frame.fill(30)
            
            # Draw stickman
            stickman.draw(frame)
            
            # Show frame
            cv2.imshow(f'Stickman Test - {dance}', frame)
            
            if cv2.waitKey(33) & 0xFF == ord('q'):
                break
        
        cv2.destroyWindow(f'Stickman Test - {dance}')
    
    print("✓ Stickman test completed")


if __name__ == "__main__":
    test_stickman()
