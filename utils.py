"""
Utility functions and constants for the AI Stickman Dancing Game.
"""

import cv2
import numpy as np

# Game constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 30
BACKGROUND_COLOR = (20, 20, 30)
STICKMAN_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)
GESTURE_COLOR = (255, 0, 255)

# Stickman dimensions
HEAD_RADIUS = 20
BODY_LENGTH = 60
ARM_LENGTH = 40
LEG_LENGTH = 50
SHOULDER_WIDTH = 30

# Animation constants
ANIMATION_SPEED = 0.15
DANCE_AMPLITUDE = 30
WALK_SPEED = 5

# Finger gesture mappings
FINGER_GESTURES = {
    0: "idle",
    1: "idle", 
    2: "move_right",
    3: "move_left",
    4: "idle",
    5: "special_dance"
}

# Sentiment to dance mappings
SENTIMENT_DANCES = {
    "positive": "happy",
    "negative": "sad", 
    "neutral": "normal"
}

# Keyword to dance mappings
KEYWORD_DANCES = {
    "party": "breakdance",
    "love": "romantic",
    "angry": "aggressive",
    "happy": "happy",
    "sad": "sad",
    "dance": "normal",
    "excited": "happy",
    "celebration": "breakdance"
}

def draw_text_with_background(img, text, position, font_scale=1, thickness=2):
    """
    Draw text with a background for better visibility.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    
    # Draw background rectangle
    bg_top_left = (position[0] - 5, position[1] - text_size[1] - 5)
    bg_bottom_right = (position[0] + text_size[0] + 5, position[1] + 5)
    cv2.rectangle(img, bg_top_left, bg_bottom_right, (0, 0, 0), -1)
    
    # Draw text
    cv2.putText(img, text, position, font, font_scale, TEXT_COLOR, thickness)

def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def smooth_interpolation(current, target, factor=0.1):
    """
    Smooth interpolation between current and target values.
    """
    return current + (target - current) * factor

def clamp(value, min_val, max_val):
    """
    Clamp a value between min and max.
    """
    return max(min_val, min(max_val, value))
