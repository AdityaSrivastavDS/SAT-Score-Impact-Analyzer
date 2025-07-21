# scorer.py - This file contains our SAT scoring engine that handles all the complex score calculations

class SATScorer:
    def __init__(self, scoring_data):
        """
        Initialize scorer with the full SAT scoring data
        """
        # We're building a lookup table from the scoring data - think of it as a conversion chart
        # Each subject (Math, Reading & Writing) gets its own mapping of raw scores to scaled scores
        self.scoring_map = {
            entry['key']: entry['map']  # 'key' is the subject name, 'map' is the conversion table
            for entry in scoring_data  # We loop through each subject in our scoring data
        }

    def get_scaled_score(self, subject, raw_score, difficulty='hard'):
        """
        Convert raw score to scaled score using the map
        """
        # First, we grab the conversion table for this specific subject (Math or Reading & Writing)
        mapping = self.scoring_map.get(subject, [])
        # Now we search through the table to find the row that matches our raw score
        for entry in mapping:
            # When we find the matching raw score, we return the scaled score for the given difficulty level
            if entry['raw'] == raw_score:
                return entry[difficulty]  # This gives us either the 'easy' or 'hard' scaled score
        # If somehow we can't find the raw score in our table, we return the minimum possible SAT score
        return 200  # default fallback (minimum)

    def determine_module2_difficulty(self, correct_count, total, threshold=0.5):
        """
        Decide module 2 difficulty (easy/hard) based on threshold
        """
        # This is where the SAT's adaptive logic kicks in - if you do well on module 1, you get harder module 2
        # We calculate the percentage of questions they got right in module 1
        # If they got 50% or more correct, they get the hard version of module 2
        # If they got less than 50%, they get the easier version (but with lower possible scores)
        return 'hard' if (correct_count / total) >= threshold else 'easy'
