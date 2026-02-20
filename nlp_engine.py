"""
NLP Engine for analyzing text input and determining dance styles.
Uses NLTK VADER sentiment analyzer and keyword detection.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from utils import SENTIMENT_DANCES, KEYWORD_DANCES

class NLPEngine:
    """
    Natural Language Processing engine for text analysis and dance style determination.
    """
    
    def __init__(self):
        """
        Initialize the NLP engine with VADER sentiment analyzer.
        """
        try:
            # Download VADER lexicon if not already downloaded
            nltk.download('vader_lexicon', quiet=True)
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            print("✓ NLP Engine initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing NLP Engine: {e}")
            raise
    
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Sentiment scores and classification
        """
        try:
            # Get sentiment scores
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Determine sentiment category
            compound_score = scores['compound']
            
            if compound_score >= 0.05:
                sentiment = "positive"
            elif compound_score <= -0.05:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                'sentiment': sentiment,
                'scores': scores,
                'compound': compound_score
            }
        except Exception as e:
            print(f"✗ Error analyzing sentiment: {e}")
            return {
                'sentiment': 'neutral',
                'scores': {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0},
                'compound': 0
            }
    
    def detect_keywords(self, text):
        """
        Detect dance-related keywords in the text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            list: List of detected keywords
        """
        try:
            # Convert to lowercase for case-insensitive matching
            text_lower = text.lower()
            
            # Remove punctuation and split into words
            words = re.findall(r'\b\w+\b', text_lower)
            
            # Find keywords
            detected_keywords = []
            for word in words:
                if word in KEYWORD_DANCES:
                    detected_keywords.append(word)
            
            return detected_keywords
        except Exception as e:
            print(f"✗ Error detecting keywords: {e}")
            return []
    
    def determine_dance_style(self, text):
        """
        Determine the dance style based on sentiment and keywords.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dance style information
        """
        try:
            # Analyze sentiment
            sentiment_result = self.analyze_sentiment(text)
            
            # Detect keywords
            keywords = self.detect_keywords(text)
            
            # Determine dance style
            dance_style = None
            dance_source = None
            
            # Priority 1: Keywords (highest priority)
            if keywords:
                # Use the first detected keyword
                keyword = keywords[0]
                dance_style = KEYWORD_DANCES[keyword]
                dance_source = f"keyword: {keyword}"
            
            # Priority 2: Sentiment (fallback if no keywords)
            if dance_style is None:
                sentiment = sentiment_result['sentiment']
                dance_style = SENTIMENT_DANCES[sentiment]
                dance_source = f"sentiment: {sentiment}"
            
            return {
                'dance_style': dance_style,
                'source': dance_source,
                'sentiment': sentiment_result['sentiment'],
                'sentiment_scores': sentiment_result['scores'],
                'keywords': keywords,
                'original_text': text
            }
        except Exception as e:
            print(f"✗ Error determining dance style: {e}")
            return {
                'dance_style': 'normal',
                'source': 'error_fallback',
                'sentiment': 'neutral',
                'sentiment_scores': {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0},
                'keywords': [],
                'original_text': text
            }
    
    def get_dance_description(self, dance_style):
        """
        Get a description of the dance style.
        
        Args:
            dance_style (str): Dance style name
            
        Returns:
            str: Description of the dance style
        """
        descriptions = {
            'happy': "Joyful and energetic dance with upbeat movements",
            'sad': "Slow and melancholic dance with gentle swaying",
            'normal': "Casual dance with balanced movements",
            'breakdance': "Dynamic breakdance with acrobatic moves",
            'romantic': "Graceful and flowing romantic dance",
            'aggressive': "Intense and powerful dance with strong movements"
        }
        return descriptions.get(dance_style, "Unknown dance style")
    
    def process_text_input(self, text):
        """
        Process text input and return complete analysis.
        
        Args:
            text (str): Input text from user
            
        Returns:
            dict: Complete analysis result
        """
        if not text or not text.strip():
            return {
                'dance_style': 'normal',
                'source': 'empty_input',
                'sentiment': 'neutral',
                'sentiment_scores': {'pos': 0, 'neg': 0, 'neu': 1, 'compound': 0},
                'keywords': [],
                'original_text': text,
                'description': "Normal dance - no specific emotion detected"
            }
        
        result = self.determine_dance_style(text)
        result['description'] = self.get_dance_description(result['dance_style'])
        
        return result


# Test function
def test_nlp_engine():
    """
    Test the NLP engine with sample inputs.
    """
    print("Testing NLP Engine...")
    
    nlp = NLPEngine()
    
    test_texts = [
        "I am so happy today!",
        "I feel very sad and lonely",
        "Let's have a party tonight",
        "I love you so much",
        "I am angry about this situation",
        "Just a normal day"
    ]
    
    for text in test_texts:
        print(f"\nText: '{text}'")
        result = nlp.process_text_input(text)
        print(f"Dance Style: {result['dance_style']}")
        print(f"Source: {result['source']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Keywords: {result['keywords']}")
        print(f"Description: {result['description']}")


if __name__ == "__main__":
    test_nlp_engine()
