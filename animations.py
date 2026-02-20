"""
Animation system for stickman dance movements.
Defines different dance styles and their animation patterns.
"""

import math
import numpy as np
from utils import DANCE_AMPLITUDE, ANIMATION_SPEED

class AnimationSystem:
    """
    Animation system for managing stickman dance movements.
    """
    
    def __init__(self):
        """
        Initialize the animation system.
        """
        self.animation_time = 0
        self.current_dance = "normal"
        self.animation_speed = ANIMATION_SPEED
        
        # Animation parameters for different dance styles
        self.dance_patterns = {
            "normal": {
                "arm_swing": 0.3,
                "leg_lift": 0.2,
                "body_bob": 0.1,
                "head_nod": 0.15,
                "speed_multiplier": 1.0
            },
            "happy": {
                "arm_swing": 0.6,
                "leg_lift": 0.4,
                "body_bob": 0.3,
                "head_nod": 0.4,
                "speed_multiplier": 1.5
            },
            "sad": {
                "arm_swing": 0.1,
                "leg_lift": 0.05,
                "body_bob": 0.05,
                "head_nod": 0.1,
                "speed_multiplier": 0.5
            },
            "breakdance": {
                "arm_swing": 0.8,
                "leg_lift": 0.7,
                "body_bob": 0.6,
                "head_nod": 0.5,
                "speed_multiplier": 2.0
            },
            "romantic": {
                "arm_swing": 0.4,
                "leg_lift": 0.3,
                "body_bob": 0.2,
                "head_nod": 0.3,
                "speed_multiplier": 0.8
            },
            "aggressive": {
                "arm_swing": 0.7,
                "leg_lift": 0.6,
                "body_bob": 0.5,
                "head_nod": 0.6,
                "speed_multiplier": 1.8
            }
        }
    
    def update(self, dt):
        """
        Update animation time.
        
        Args:
            dt (float): Time delta in seconds
        """
        pattern = self.dance_patterns.get(self.current_dance, self.dance_patterns["normal"])
        speed_multiplier = pattern["speed_multiplier"]
        self.animation_time += dt * self.animation_speed * speed_multiplier
    
    def set_dance_style(self, dance_style):
        """
        Set the current dance style.
        
        Args:
            dance_style (str): Dance style name
        """
        if dance_style in self.dance_patterns:
            self.current_dance = dance_style
        else:
            self.current_dance = "normal"
    
    def get_arm_animation(self, is_left_arm=True):
        """
        Get arm animation offset for current frame.
        
        Args:
            is_left_arm (bool): True for left arm, False for right arm
            
        Returns:
            tuple: (x_offset, y_offset) for arm end position
        """
        pattern = self.dance_patterns.get(self.current_dance, self.dance_patterns["normal"])
        arm_swing = pattern["arm_swing"]
        
        # Create different patterns for left and right arms
        if is_left_arm:
            x_offset = math.sin(self.animation_time) * DANCE_AMPLITUDE * arm_swing
            y_offset = math.cos(self.animation_time * 2) * DANCE_AMPLITUDE * arm_swing * 0.5
        else:
            x_offset = -math.sin(self.animation_time) * DANCE_AMPLITUDE * arm_swing
            y_offset = math.cos(self.animation_time * 2 + math.pi) * DANCE_AMPLITUDE * arm_swing * 0.5
        
        return (x_offset, y_offset)
    
    def get_leg_animation(self, is_left_leg=True):
        """
        Get leg animation offset for current frame.
        
        Args:
            is_left_leg (bool): True for left leg, False for right leg
            
        Returns:
            tuple: (x_offset, y_offset) for leg end position
        """
        pattern = self.dance_patterns.get(self.current_dance, self.dance_patterns["normal"])
        leg_lift = pattern["leg_lift"]
        
        # Create walking/stepping pattern
        if is_left_leg:
            phase = self.animation_time
        else:
            phase = self.animation_time + math.pi
        
        x_offset = math.sin(phase) * DANCE_AMPLITUDE * leg_lift * 0.3
        y_offset = abs(math.sin(phase)) * DANCE_AMPLITUDE * leg_lift
        
        return (x_offset, y_offset)
    
    def get_body_animation(self):
        """
        Get body animation offset for current frame.
        
        Returns:
            tuple: (x_offset, y_offset) for body position
        """
        pattern = self.dance_patterns.get(self.current_dance, self.dance_patterns["normal"])
        body_bob = pattern["body_bob"]
        
        # Gentle bobbing motion
        x_offset = math.sin(self.animation_time * 0.5) * DANCE_AMPLITUDE * body_bob * 0.2
        y_offset = abs(math.sin(self.animation_time)) * DANCE_AMPLITUDE * body_bob
        
        return (x_offset, y_offset)
    
    def get_head_animation(self):
        """
        Get head animation offset for current frame.
        
        Returns:
            tuple: (x_offset, y_offset, rotation) for head position and rotation
        """
        pattern = self.dance_patterns.get(self.current_dance, self.dance_patterns["normal"])
        head_nod = pattern["head_nod"]
        
        # Nodding motion
        x_offset = math.sin(self.animation_time * 1.5) * DANCE_AMPLITUDE * head_nod * 0.3
        y_offset = math.sin(self.animation_time * 2) * DANCE_AMPLITUDE * head_nod * 0.2
        rotation = math.sin(self.animation_time) * 15 * head_nod  # Rotation in degrees
        
        return (x_offset, y_offset, rotation)
    
    def get_special_effects(self):
        """
        Get special effects for current dance style.
        
        Returns:
            dict: Special effects parameters
        """
        effects = {
            "particles": [],
            "color_tint": None,
            "motion_blur": False
        }
        
        if self.current_dance == "happy":
            # Add sparkles around happy dancing
            if int(self.animation_time * 10) % 3 == 0:
                effects["particles"].append({
                    "type": "sparkle",
                    "x": np.random.randint(-50, 50),
                    "y": np.random.randint(-100, 0),
                    "lifetime": 1.0
                })
        
        elif self.current_dance == "breakdance":
            # Add motion lines for breakdance
            effects["motion_blur"] = True
            effects["color_tint"] = (255, 100, 100)  # Reddish tint
        
        elif self.current_dance == "romantic":
            # Add hearts for romantic dance
            if int(self.animation_time * 5) % 2 == 0:
                effects["particles"].append({
                    "type": "heart",
                    "x": np.random.randint(-30, 30),
                    "y": np.random.randint(-80, -20),
                    "lifetime": 2.0
                })
        
        return effects
    
    def reset_animation(self):
        """
        Reset animation time to zero.
        """
        self.animation_time = 0
    
    def get_animation_info(self):
        """
        Get current animation information.
        
        Returns:
            dict: Current animation state
        """
        return {
            "current_dance": self.current_dance,
            "animation_time": self.animation_time,
            "pattern": self.dance_patterns.get(self.current_dance, {})
        }


class DanceTransition:
    """
    Handles smooth transitions between dance styles.
    """
    
    def __init__(self, transition_duration=1.0):
        """
        Initialize dance transition system.
        
        Args:
            transition_duration (float): Duration of transition in seconds
        """
        self.transition_duration = transition_duration
        self.transition_time = 0
        self.is_transitioning = False
        self.from_dance = "normal"
        self.to_dance = "normal"
    
    def start_transition(self, from_dance, to_dance):
        """
        Start a transition between dance styles.
        
        Args:
            from_dance (str): Current dance style
            to_dance (str): Target dance style
        """
        self.from_dance = from_dance
        self.to_dance = to_dance
        self.transition_time = 0
        self.is_transitioning = True
    
    def update(self, dt):
        """
        Update transition progress.
        
        Args:
            dt (float): Time delta in seconds
        """
        if self.is_transitioning:
            self.transition_time += dt
            if self.transition_time >= self.transition_duration:
                self.is_transitioning = False
                self.transition_time = 0
    
    def get_transition_factor(self):
        """
        Get current transition factor (0 to 1).
        
        Returns:
            float: Transition factor
        """
        if not self.is_transitioning:
            return 1.0
        
        # Smooth easing function
        t = self.transition_time / self.transition_duration
        return t * t * (3.0 - 2.0 * t)  # Smoothstep function
    
    def is_complete(self):
        """
        Check if transition is complete.
        
        Returns:
            bool: True if transition is complete
        """
        return not self.is_transitioning


# Test function
def test_animation_system():
    """
    Test the animation system.
    """
    print("Testing Animation System...")
    
    anim_system = AnimationSystem()
    transition = DanceTransition()
    
    # Test different dance styles
    dance_styles = ["normal", "happy", "sad", "breakdance", "romantic", "aggressive"]
    
    for i, dance in enumerate(dance_styles):
        print(f"\nTesting {dance} dance...")
        anim_system.set_dance_style(dance)
        
        # Simulate a few animation frames
        for frame in range(10):
            anim_system.update(0.033)  # ~30 FPS
            
            # Get animation values
            left_arm = anim_system.get_arm_animation(True)
            right_arm = anim_system.get_arm_animation(False)
            left_leg = anim_system.get_leg_animation(True)
            right_leg = anim_system.get_leg_animation(False)
            body = anim_system.get_body_animation()
            head = anim_system.get_head_animation()
            effects = anim_system.get_special_effects()
            
            print(f"Frame {frame}: Arms({left_arm:.1f}, {right_arm:.1f}) "
                  f"Legs({left_leg:.1f}, {right_leg:.1f}) "
                  f"Body{body:.1f} Head{head[:2]:.1f}")
    
    print("\n✓ Animation System test completed")


if __name__ == "__main__":
    test_animation_system()
