# analyzer.py - This is our smart what-if analysis engine that predicts score improvements

# We need our scoring engine to do all the score calculations
from scorer import SATScorer

class WhatIfAnalyzer:
    def __init__(self, scorer):
        # We're connecting our analyzer to the scoring engine - like giving it a calculator
        self.scorer = scorer

    def analyze_student(self, responses):
        """
        Analyze one student's responses and calculate current score + what-if gains
        """
        # First, let's organize this student's responses by subject - SAT has Math and Reading & Writing
        sections = {'Math': [], 'Reading and Writing': []}
        # We go through every single question the student answered
        for q in responses:
            # We check which subject this question belongs to and put it in the right bucket
            subject = q['subject']['name']
            sections[subject].append(q)

        # This will store all our analysis results for both subjects
        result = {}

        # Now we analyze each subject separately (Math gets scored differently than Reading & Writing)
        for subject, questions in sections.items():
            # The SAT has two modules per subject - module 1 is always medium difficulty, module 2 adapts based on module 1 performance
            module1 = [q for q in questions if q['section'] == 'Static']  # Module 1 questions (always same difficulty)
            module2 = [q for q in questions if q['section'] != 'Static']  # Module 2 questions (adaptive difficulty)

            # Let's count how many they got right in each module
            correct1 = sum(q['correct'] for q in module1)  # Total correct answers in module 1
            correct2 = sum(q['correct'] for q in module2)  # Total correct answers in module 2
            total1 = len(module1)  # How many questions were in module 1 (usually around 22)

            # Based on their module 1 performance, figure out if they got easy or hard module 2
            module2_type = self.scorer.determine_module2_difficulty(correct1, total1)

            # Calculate their current overall performance
            raw_score = correct1 + correct2  # Total questions they got right across both modules
            scaled_score = self.scorer.get_scaled_score(subject, raw_score, module2_type)  # Convert to the 200-800 scale

            # Start building the results for this subject
            result[subject] = {
                "current_raw": raw_score,  # How many they got right total
                "current_scaled": scaled_score,  # Their actual SAT score (200-800)
                "module2_type": module2_type,  # Whether they got easy or hard module 2
                "what_if": []  # This will hold all the what-if scenarios
            }

            # Here's where the magic happens - we test what would happen if they got each wrong module 1 question right
            for i, q in enumerate(module1):  # Go through every question in module 1
                if q['correct'] == 1:
                    continue  # Skip this one - they already got it right, so no point in analyzing it

                # Time to simulate an alternate reality where they got this question right
                new_correct1 = correct1 + 1  # Add one more correct answer to their module 1 score
                # Check if this extra correct answer would change their module 2 difficulty level
                new_module2_type = self.scorer.determine_module2_difficulty(new_correct1, total1)

                # Calculate what their new total raw score would be
                new_raw = raw_score + 1  # One more question correct overall
                # And convert that to a scaled score using the potentially new module 2 difficulty
                new_scaled = self.scorer.get_scaled_score(subject, new_raw, new_module2_type)

                # The moment of truth - how many points would this question be worth?
                delta = new_scaled - scaled_score

                # Store all the juicy details about this what-if scenario
                result[subject]["what_if"].append({
                    "question_id": q['question_id'],  # Which specific question we're talking about
                    "unit": q['unit']['name'],  # What unit/chapter this question covers
                    "topic": q['topic']['name'],  # The specific topic within that unit
                    "difficulty": q['compleixty'],  # How hard this question was rated
                    "improvement": delta,  # The actual point increase they'd get (this is the gold!)
                    "caused_module_flip": new_module2_type != module2_type  # Did fixing this question change their module 2 difficulty?
                })

            # Time to rank these opportunities - put the biggest point gains at the top
            result[subject]["what_if"].sort(key=lambda x: x['improvement'], reverse=True)

        # Send back all our analysis for both subjects
        return result
