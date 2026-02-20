"""
Main entry point for the AI Stickman Dancing Game.
Integrates NLP,Computer Vision, and Animation systems.
"""

import cv2
import time
import threading
import queue
import sys
from datetime import datetime

from nlp_engine import NLPEngine
from vision_engine import VisionEngine
from stickman import Stickman
from utils import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, FPS,
    draw_text_with_background
)

class StickmanDancingGame:
    """
    Main game class that orchestrates all systems.
    """
    
    def __init__(self):
        """
        Initialize the game and all subsystems.
        """
        print("🎮 Initializing AI Stickman Dancing Game...")
        
        # Initialize subsystems
        try:
            self.nlp_engine = NLPEngine()
            self.vision_engine = VisionEngine()
            self.stickman = Stickman()
            
            # Game state
            self.running = True
            self.paused = False
            self.current_text_input = ""
            self.nlp_result = None
            
            # Timing
            self.clock = cv2.TickMeter()
            self.last_time = time.time()
            
            # Threading for text input
            self.input_queue = queue.Queue()
            self.input_thread = None
            
            # Camera
            self.cap = None
            
            print("✓ Game initialized successfully!")
        except Exception as e:
            print(f"✗ Failed to initialize game: {e}")
            sys.exit(1)
    
    def initialize_camera(self):
        """
        Initialize the webcam camera.
        """
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Cannot open webcam")
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, FPS)
            
            print("✓ Camera initialized successfully")
        except Exception as e:
            print(f"✗ Failed to initialize camera: {e}")
            raise
    
    def get_user_text_input(self):
        """
        Get text input from user in a separate thread.
        """
        def input_worker():
            while self.running:
                try:
                    user_input = input("\nEnter text for dance analysis (or 'quit' to exit): ")
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        self.running = False
                        break
                    elif user_input.strip():
                        self.input_queue.put(user_input)
                except EOFError:
                    self.running = False
                    break
                except Exception as e:
                    print(f"Input error: {e}")
        
        self.input_thread = threading.Thread(target=input_worker, daemon=True)
        self.input_thread.start()
    
    def process_text_input(self):
        """
        Process pending text input from the queue.
        """
        try:
            while not self.input_queue.empty():
                text = self.input_queue.get_nowait()
                self.current_text_input = text
                
                # Process with NLP engine
                self.nlp_result = self.nlp_engine.process_text_input(text)
                
                # Update stickman dance style
                dance_style = self.nlp_result['dance_style']
                self.stickman.set_dance_style(dance_style)
                
                print(f"\n📝 Text: '{text}'")
                print(f"💃 Dance Style: {dance_style}")
                print(f"🎭 Source: {self.nlp_result['source']}")
                print(f"😊 Sentiment: {self.nlp_result['sentiment']}")
                print(f"📊 Keywords: {self.nlp_result['keywords']}")
                print(f"📖 Description: {self.nlp_result['description']}")
                
        except queue.Empty:
            pass
        except Exception as e:
            print(f"✗ Error processing text input: {e}")
    
    def handle_gesture_input(self, gesture_result):
        """
        Handle gesture input from vision engine.
        
        Args:
            gesture_result (dict): Gesture detection result
        """
        try:
            gesture = gesture_result['gesture']
            
            # Map gestures to stickman actions
            if gesture == "move_left":
                self.stickman.move_left()
            elif gesture == "move_right":
                self.stickman.move_right()
            elif gesture == "special_dance":
                self.stickman.special_dance()
            elif gesture == "idle":
                self.stickman.stop_moving()
            
        except Exception as e:
            print(f"✗ Error handling gesture input: {e}")
    
    def create_display_frame(self, camera_frame, gesture_result):
        """
        Create the main display frame combining camera and game elements.
        
        Args:
            camera_frame: Raw camera frame
            gesture_result (dict): Gesture detection result
            
        Returns:
            numpy array: Combined display frame
        """
        # Create main display frame
        display_frame = cv2.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        display_frame[:] = BACKGROUND_COLOR
        
        # Resize and place camera feed
        if camera_frame is not None:
            camera_resized = cv2.resize(camera_frame, (320, 240))
            
            # Place camera feed in top-left corner
            display_frame[10:250, 10:330] = camera_resized
            
            # Draw border around camera feed
            cv2.rectangle(display_frame, (10, 10), (330, 250), (100, 100, 100), 2)
        
        # Draw stickman
        self.stickman.draw(display_frame)
        
        # Draw UI elements
        self._draw_ui(display_frame, gesture_result)
        
        return display_frame
    
    def _draw_ui(self, frame, gesture_result):
        """
        Draw UI elements on the frame.
        
        Args:
            frame: Display frame
            gesture_result (dict): Gesture detection result
        """
        # Title
        title_text = "AI Stickman Dancing Game"
        cv2.putText(frame, title_text, (WINDOW_WIDTH // 2 - 150, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Instructions
        instructions = [
            "Hand Gestures:",
            "1 finger: Idle",
            "2 fingers: Move right",
            "3 fingers: Move left",
            "5 fingers: Special dance",
            "",
            "Type text and press Enter to change dance style"
        ]
        
        y_offset = 350
        for instruction in instructions:
            draw_text_with_background(frame, instruction, (350, y_offset), 0.5, 1)
            y_offset += 25
        
        # Current text input
        if self.current_text_input:
            text_preview = f"Text: {self.current_text_input[:50]}..."
            draw_text_with_background(frame, text_preview, (10, 270), 0.6, 1)
        
        # NLP result
        if self.nlp_result:
            nlp_info = [
                f"Dance: {self.nlp_result['dance_style'].upper()}",
                f"Sentiment: {self.nlp_result['sentiment']}",
                f"Source: {self.nlp_result['source']}"
            ]
            
            y_offset = 320
            for info in nlp_info:
                draw_text_with_background(frame, info, (10, y_offset), 0.6, 1)
                y_offset += 25
        
        # Gesture info
        if gesture_result['hand_detected']:
            gesture_info = [
                f"Gesture: {gesture_result['gesture']}",
                f"Fingers: {gesture_result['finger_count']}",
                f"Confidence: {gesture_result['confidence']:.2f}"
            ]
            
            y_offset = WINDOW_HEIGHT - 100
            for info in gesture_info:
                draw_text_with_background(frame, info, (WINDOW_WIDTH - 200, y_offset), 0.5, 1)
                y_offset += 25
        
        # FPS counter
        fps_text = f"FPS: {int(self.clock.getFPS())}"
        draw_text_with_background(frame, fps_text, (WINDOW_WIDTH - 100, 30), 0.6, 1)
        
        # Time
        current_time = datetime.now().strftime("%H:%M:%S")
        draw_text_with_background(frame, current_time, (WINDOW_WIDTH - 100, 60), 0.6, 1)
    
    def run(self):
        """
        Main game loop.
        """
        print("\n🚀 Starting AI Stickman Dancing Game...")
        print("📝 Enter text to control the stickman's dance style")
        print("🤚 Use hand gestures to control movement")
        print("👋 Press 'q' in the camera window or type 'quit' to exit\n")
        
        try:
            # Initialize camera
            self.initialize_camera()
            
            # Start text input thread
            self.get_user_text_input()
            
            # Main game loop
            while self.running:
                self.clock.start()
                
                # Calculate delta time
                current_time = time.time()
                dt = current_time - self.last_time
                self.last_time = current_time
                
                # Read camera frame
                ret, camera_frame = self.cap.read()
                if ret:
                    # Flip frame horizontally for mirror effect
                    camera_frame = cv2.flip(camera_frame, 1)
                    
                    # Detect gestures
                    gesture_result = self.vision_engine.detect_gesture(camera_frame)
                    smoothed_gesture = self.vision_engine.smooth_gesture_detection(gesture_result)
                    
                    # Handle gesture input
                    self.handle_gesture_input(gesture_result)
                else:
                    gesture_result = {
                        'gesture': 'idle',
                        'finger_count': 0,
                        'confidence': 0.0,
                        'hand_detected': False
                    }
                
                # Process text input
                self.process_text_input()
                
                # Update stickman
                self.stickman.update(dt)
                
                # Create display frame
                display_frame = self.create_display_frame(camera_frame, gesture_result)
                
                # Show display frame
                cv2.imshow('AI Stickman Dancing Game', display_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 'q' or ESC
                    self.running = False
                elif key == ord(' '):  # Spacebar to pause
                    self.paused = not self.paused
                
                self.clock.stop()
                
        except KeyboardInterrupt:
            print("\n👋 Game interrupted by user")
        except Exception as e:
            print(f"✗ Game error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources.
        """
        print("\n🧹 Cleaning up...")
        
        try:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            self.vision_engine.cleanup()
            print("✓ Cleanup completed")
        except Exception as e:
            print(f"✗ Cleanup error: {e}")


def main():
    """
    Main entry point.
    """
    print("=" * 60)
    print("🎮 AI STICKMAN DANCING GAME")
    print("Using NLP and Computer Vision")
    print("=" * 60)
    
    try:
        game = StickmanDancingGame()
        game.run()
    except Exception as e:
        print(f"✗ Failed to start game: {e}")
        sys.exit(1)
    
    print("\n👋 Thanks for playing!")


if __name__ == "__main__":
    main()
