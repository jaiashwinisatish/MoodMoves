"""
Computer Vision Engine for hand gesture detection using MediaPipe.
Detects finger counts and maps them to game controls.
"""

import cv2
import mediapipe as mp
import numpy as np
from utils import FINGER_GESTURES, GESTURE_COLOR, calculate_distance

class VisionEngine:
    """
    Computer Vision engine for hand gesture detection and finger counting.
    """
    
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initialize the vision engine with MediaPipe Hands.
        
        Args:
            min_detection_confidence (float): Minimum confidence for hand detection
            min_tracking_confidence (float): Minimum confidence for hand tracking
        """
        try:
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            
            # Initialize MediaPipe Hands
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence
            )
            
            # Gesture tracking
            self.current_gesture = "idle"
            self.gesture_confidence = 0.0
            self.gesture_history = []
            self.max_history_length = 5
            
            print("✓ Vision Engine initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing Vision Engine: {e}")
            raise
    
    def count_fingers(self, hand_landmarks):
        """
        Count the number of raised fingers based on hand landmarks.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            int: Number of raised fingers (0-5)
        """
        try:
            fingers_up = 0
            
            # Landmark indices for fingertips and MCP joints
            tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
            pip_ids = [3, 6, 10, 14, 18]  # Corresponding PIP joints
            
            # Thumb (special case - horizontal comparison)
            if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[pip_ids[0]].x:
                fingers_up += 1
            
            # Other four fingers (vertical comparison)
            for i in range(1, 5):
                tip = hand_landmarks.landmark[tip_ids[i]]
                pip = hand_landmarks.landmark[pip_ids[i]]
                
                # Check if fingertip is above PIP joint
                if tip.y < pip.y:
                    fingers_up += 1
            
            return fingers_up
        except Exception as e:
            print(f"✗ Error counting fingers: {e}")
            return 0
    
    def detect_gesture(self, frame):
        """
        Detect hand gesture from the camera frame.
        
        Args:
            frame: Camera frame (numpy array)
            
        Returns:
            dict: Gesture detection results
        """
        try:
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.hands.process(rgb_frame)
            
            gesture_result = {
                'gesture': 'idle',
                'finger_count': 0,
                'confidence': 0.0,
                'hand_detected': False,
                'landmarks': None,
                'annotated_frame': frame.copy()
            }
            
            if results.multi_hand_landmarks:
                # Get the first detected hand
                hand_landmarks = results.multi_hand_landmarks[0]
                gesture_result['hand_detected'] = True
                gesture_result['landmarks'] = hand_landmarks
                
                # Count fingers
                finger_count = self.count_fingers(hand_landmarks)
                gesture_result['finger_count'] = finger_count
                
                # Map finger count to gesture
                gesture = FINGER_GESTURES.get(finger_count, 'idle')
                gesture_result['gesture'] = gesture
                
                # Calculate confidence based on hand detection quality
                # (This is a simplified confidence calculation)
                confidence = 0.8 if finger_count > 0 else 0.5
                gesture_result['confidence'] = confidence
                
                # Draw hand landmarks on the frame
                self.mp_drawing.draw_landmarks(
                    gesture_result['annotated_frame'],
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Draw finger count
                h, w, _ = frame.shape
                cv2.putText(
                    gesture_result['annotated_frame'],
                    f"Fingers: {finger_count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    GESTURE_COLOR,
                    2
                )
                
                cv2.putText(
                    gesture_result['annotated_frame'],
                    f"Gesture: {gesture}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    GESTURE_COLOR,
                    2
                )
            
            return gesture_result
        except Exception as e:
            print(f"✗ Error detecting gesture: {e}")
            return {
                'gesture': 'idle',
                'finger_count': 0,
                'confidence': 0.0,
                'hand_detected': False,
                'landmarks': None,
                'annotated_frame': frame.copy()
            }
    
    def smooth_gesture_detection(self, gesture_result):
        """
        Apply smoothing to gesture detection to reduce jitter.
        
        Args:
            gesture_result (dict): Current gesture detection result
            
        Returns:
            str: Smoothed gesture
        """
        try:
            # Add current gesture to history
            self.gesture_history.append(gesture_result['gesture'])
            
            # Keep only recent history
            if len(self.gesture_history) > self.max_history_length:
                self.gesture_history.pop(0)
            
            # Find most common gesture in history
            if self.gesture_history:
                gesture_counts = {}
                for gesture in self.gesture_history:
                    gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
                
                # Return gesture with highest count
                smoothed_gesture = max(gesture_counts, key=gesture_counts.get)
                
                # Update current gesture if confidence is high enough
                if gesture_result['confidence'] > 0.6:
                    self.current_gesture = smoothed_gesture
                    self.gesture_confidence = gesture_result['confidence']
                
                return smoothed_gesture
            
            return 'idle'
        except Exception as e:
            print(f"✗ Error smoothing gesture detection: {e}")
            return 'idle'
    
    def get_current_gesture(self):
        """
        Get the current smoothed gesture.
        
        Returns:
            dict: Current gesture information
        """
        return {
            'gesture': self.current_gesture,
            'confidence': self.gesture_confidence
        }
    
    def reset_gesture_history(self):
        """
        Reset the gesture history for fresh detection.
        """
        self.gesture_history = []
        self.current_gesture = "idle"
        self.gesture_confidence = 0.0
    
    def draw_gesture_info(self, frame, gesture_result):
        """
        Draw gesture information on the frame.
        
        Args:
            frame: Camera frame
            gesture_result (dict): Gesture detection result
            
        Returns:
            numpy array: Frame with gesture information drawn
        """
        try:
            annotated_frame = frame.copy()
            
            if gesture_result['hand_detected']:
                # Draw gesture info box
                info_text = [
                    f"Gesture: {gesture_result['gesture']}",
                    f"Fingers: {gesture_result['finger_count']}",
                    f"Confidence: {gesture_result['confidence']:.2f}"
                ]
                
                y_offset = 10
                for text in info_text:
                    cv2.putText(
                        annotated_frame,
                        text,
                        (10, y_offset + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        GESTURE_COLOR,
                        2
                    )
                    y_offset += 25
            else:
                cv2.putText(
                    annotated_frame,
                    "No hand detected",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )
            
            return annotated_frame
        except Exception as e:
            print(f"✗ Error drawing gesture info: {e}")
            return frame
    
    def cleanup(self):
        """
        Clean up resources.
        """
        try:
            if hasattr(self, 'hands'):
                self.hands.close()
            print("✓ Vision Engine cleaned up successfully")
        except Exception as e:
            print(f"✗ Error cleaning up Vision Engine: {e}")


# Test function
def test_vision_engine():
    """
    Test the vision engine with webcam.
    """
    print("Testing Vision Engine...")
    print("Press 'q' to quit")
    
    vision = VisionEngine()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("✗ Cannot open webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect gesture
            gesture_result = vision.detect_gesture(frame)
            smoothed_gesture = vision.smooth_gesture_detection(gesture_result)
            
            # Draw results
            display_frame = vision.draw_gesture_info(frame, gesture_result)
            
            # Show frame
            cv2.imshow('Vision Engine Test', display_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"✗ Error during test: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        vision.cleanup()


if __name__ == "__main__":
    test_vision_engine()
