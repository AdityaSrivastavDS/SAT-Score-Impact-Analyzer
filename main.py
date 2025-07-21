# main.py - This is our main program that runs the SAT score analysis

# We're importing our custom helper function to read JSON files easily
from utils import load_json

# Bringing in our SAT scoring engine that converts raw scores to scaled scores
from scorer import SATScorer

# Importing our what-if analyzer that figures out which questions would boost scores the most
from analyzer import WhatIfAnalyzer


# Time to load up all our data files - think of this as opening our filing cabinet
# First, we grab the official SAT scoring rubric that tells us how raw scores become scaled scores
scoring_data = load_json("data/scoring_DSAT_v2.json")


# Now we load the first student's test attempt - all their answers and whether they got them right or wrong
student1_data = load_json("data/67f2aae2c084263d16dbe462user_attempt_v2.json")


# And here's our second student's test data - same format as the first student
student2_data = load_json("data/66fece285a916f0bb5aea9c5user_attempt_v3.json")


# Let's create our scoring machine - this will handle all the complex math of converting scores
scorer = SATScorer(scoring_data)


# Now we build our analyzer - this is like having a smart tutor who can predict score improvements
analyzer = WhatIfAnalyzer(scorer)


# Time to analyze our first student! Let's see how they did and what they could improve
print("===== Student 1 =====")

# We're asking our analyzer to crunch all the numbers for this student's performance
result1 = analyzer.analyze_student(student1_data)

# Now let's go through each subject (Math and Reading & Writing) and see the results
for subject, summary in result1.items():
    # Print a nice header for each subject so we can tell them apart
    print(f"\n--- {subject} ---")
    # Show the student's current scaled score (what colleges see) and raw score (number correct)
    print(f"Current Scaled Score: {summary['current_scaled']} (Raw: {summary['current_raw']})")
    # Tell us whether they got the harder or easier version of module 2 based on module 1 performance
    print(f"Module 2 Type: {summary['module2_type']}")
    # Here come the money shots - which questions would help the most if they got them right
    print("\nTop What-if Fixes:")
    # We only want to see the top 5 most impactful questions, not overwhelm with all of them
    for fix in summary['what_if'][:5]:  # top 5
        # For each high-impact question, show the ID, topic, how many points they'd gain, and if it changes their module 2 difficulty
        print(f" - QID: {fix['question_id']} | Topic: {fix['topic']} | Gain: +{fix['improvement']} | Module Flip: {fix['caused_module_flip']}")



# Now let's do the exact same analysis for our second student
print("\n\n===== Student 2 =====")

# Run the same comprehensive analysis on student 2's data
result2 = analyzer.analyze_student(student2_data)

# Again, loop through each subject to display their results
for subject, summary in result2.items():
    # Same format as before - clean subject header
    print(f"\n--- {subject} ---")
    # Display student 2's current performance - both the scaled score and raw score
    print(f"Current Scaled Score: {summary['current_scaled']} (Raw: {summary['current_raw']})")
    # Show what difficulty level they got for module 2 (this matters a lot for scoring!)
    print(f"Module 2 Type: {summary['module2_type']}")
    # Time to reveal the strategic insights - which questions are worth focusing on
    print("\nTop What-if Fixes:")
    # Just like with student 1, we'll show the top 5 most valuable questions to review
    for fix in summary['what_if'][:5]:  # top 5
        # Each line shows: question ID, the topic it covers, potential point gain, and whether fixing it would change their module 2 difficulty
        print(f" - QID: {fix['question_id']} | Topic: {fix['topic']} | Gain: +{fix['improvement']} | Module Flip: {fix['caused_module_flip']}")
