import datetime
import random
import json
from transformers import pipeline
class StudBud:
    """
    AI-Powered Personalized Study Planner utilizing BERT.
    """

    def __init__(self, student_name="Student", model_name="bert-base-uncased"):
        """
        Initializes the StudBud object.

        Args:
            student_name (str, optional): The name of the student. Defaults to "Student".
            model_name (str, optional): The name of the BERT model to use. Defaults to "bert-base-uncased".
        """
        self.student_name = student_name
        self.study_plan = {}
        self.nlp_model = pipeline("text-classification", model=model_name) # Load BERT model
        self.subjects = []  # Store subjects for the student

    def gather_student_info(self):
        """
        Gathers information about the student's goals, strengths, weaknesses, and preferences.
        This implementation uses simple input prompts. A real-world implementation
        would involve a more sophisticated UI or API integration.
        """
        print(f"Hello {self.student_name}!  Let's create your personalized study plan.\n")

        self.subjects = input("Enter the subjects you are studying (comma-separated): ").split(",")
        self.subjects = [s.strip() for s in self.subjects]  # Clean up whitespace

        self.goals = input("What are your academic goals? (e.g., 'Get an A in Math', 'Improve my understanding of History'): ")

        self.strengths = {}
        self.weaknesses = {}

        for subject in self.subjects:
            self.strengths[subject] = input(f"What are your strengths in {subject}? (e.g., 'Problem-solving', 'Memorization'): ")
            self.weaknesses[subject] = input(f"What are your weaknesses in {subject}? (e.g., 'Calculus', 'Essay writing'): ")


        self.study_preferences = {
            "study_time": input("What time of day do you prefer to study? (e.g., 'Morning', 'Evening'): "),
            "study_duration": int(input("How many hours do you want to study per day? (e.g., 2): ")),
            "study_environment": input("Where do you prefer to study? (e.g., 'Library', 'Quiet room'): "),
            "study_methods": input("What study methods do you find effective? (e.g., 'Flashcards', 'Practice problems'): ").split(",")
        }
        self.study_preferences["study_methods"] = [method.strip() for method in self.study_preferences["study_methods"]]


    def analyze_student_data(self):
      """
      Analyzes the collected data to identify key areas for focus.
      This implementation is a placeholder. A more sophisticated implementation
      would leverage the BERT model to analyze the student's text input and
      extract key concepts, sentiment, and areas of concern.
      """

      print("\nAnalyzing your information...\n")
      self.areas_to_focus = {}
      for subject in self.subjects:
          # This is a very basic example.  BERT could be used to analyze the weakness
          # description and identify specific concepts within that weakness that need
          # more attention.  It could also be used to identify the general sentiment
          # of the response and adapt the study plan accordingly (e.g. if the student
          # seems particularly anxious about a subject).

          self.areas_to_focus[subject] = self.weaknesses[subject] # Placeholder - focus on weaknesses

    def generate_study_plan(self, start_date=None, num_days=7):
        """
        Generates a personalized study plan.

        Args:
            start_date (datetime.date, optional): The start date for the study plan. Defaults to today.
            num_days (int, optional): The number of days to generate the study plan for. Defaults to 7.
        """
        if not self.subjects:
            print("No subjects defined. Please gather student info first.")
            return

        if start_date is None:
            start_date = datetime.date.today()

        current_date = start_date
        for day in range(num_days):
            self.study_plan[current_date.strftime("%Y-%m-%d")] = self.generate_daily_plan(current_date)
            current_date += datetime.timedelta(days=1)

    def generate_daily_plan(self, date):
        """
        Generates a study plan for a specific day.

        Args:
            date (datetime.date): The date for the study plan.

        Returns:
            dict: A dictionary representing the daily study plan.
        """
        daily_plan = {}
        available_time = self.study_preferences["study_duration"] # in hours
        study_blocks = []

        # Distribute study time across subjects (simple example)
        time_per_subject = available_time / len(self.subjects)
        time_per_subject = max(0.5, time_per_subject) # Minimum 30 minutes per subject

        for subject in self.subjects:
            # Simple Task allocation based on Weaknesses and Study Methods
            task = f"Review {self.areas_to_focus[subject]} using {random.choice(self.study_preferences['study_methods'])}"
            study_blocks.append({
                "subject": subject,
                "time": time_per_subject,
                "task": task,
                "priority": self.prioritize_task(subject, task) # Prioritize based on a basic "urgency"
            })


        daily_plan["date"] = date.strftime("%Y-%m-%d")
        daily_plan["study_blocks"] = study_blocks
        daily_plan["environment"] = self.study_preferences["study_environment"]
        daily_plan["preferred_time"] = self.study_preferences["study_time"]

        return daily_plan

    def prioritize_task(self, subject, task_description):
        """
        Prioritizes a task based on sentiment analysis and subject difficulty.

        Args:
            subject (str): The subject the task belongs to.
            task_description (str): A description of the task.

        Returns:
            str: "High", "Medium", or "Low" priority.
        """

        # Use BERT for Sentiment Analysis of the Task Description.
        # Ideally, this would analyze the student's weaknesses in relation to the subject as well.
        try:
            result = self.nlp_model(task_description) # Get sentiment analysis result
            sentiment = result[0]["label"]
            score = result[0]["score"]
        except Exception as e:
            print(f"Error performing sentiment analysis: {e}.  Defaulting to medium priority.")
            return "Medium"

        # Adjust priority based on sentiment and subject (simplified rules)
        if sentiment == "NEGATIVE" and score > 0.7:
            return "High" # Prioritize if strongly negative feelings about task

        if self.weaknesses[subject] in task_description:
            return "Medium" # Medium if task directly addresses weakness

        return "Low" # Default to low priority

    def display_study_plan(self):
        """
        Displays the generated study plan in a readable format.
        """

        if not self.study_plan:
            print("No study plan generated. Please generate a study plan first.")
            return

        print(f"\n{self.student_name}'s Personalized Study Plan:\n")

        for date, daily_plan in self.study_plan.items():
            print(f"--- {date} ---")
            print(f"  Environment: {daily_plan['environment']}")
            print(f"  Preferred Study Time: {daily_plan['preferred_time']}")

            for block in daily_plan["study_blocks"]:
                print(f"    Subject: {block['subject']}")
                print(f"    Time: {block['time']} hours")
                print(f"    Task: {block['task']}")
                print(f"    Priority: {block['priority']}")
                print("")

    def save_study_plan(self, filename="study_plan.json"):
        """
        Saves the study plan to a JSON file.

        Args:
            filename (str, optional): The name of the file to save the study plan to. Defaults to "study_plan.json".
        """
        with open(filename, "w") as f:
            json.dump(self.study_plan, f, indent=4)

        print(f"Study plan saved to {filename}")

    def load_study_plan(self, filename="study_plan.json"):
        """
        Loads a study plan from a JSON file.

        Args:
            filename (str, optional): The name of the file to load the study plan from. Defaults to "study_plan.json".
        """
        try:
            with open(filename, "r") as f:
                self.study_plan = json.load(f)
            print(f"Study plan loaded from {filename}")
        except FileNotFoundError:
            print(f"File not found: {filename}")

    # Future Enhancements
    def get_resources(self, subject, topic):
        """
        Retrieves relevant study resources (placeholder).
        In a real application, this could involve querying external APIs or databases.
        """
        # TODO: Implement resource retrieval using web scraping or API calls.
        print(f"Finding resources for {subject} - {topic}... (Not Implemented)")
        return []

# Example Usage
if __name__ == "__main__":
    studbud = StudBud(student_name="Alice")  # Initialize StudBud
    studbud.gather_student_info()    # Gather student information
    studbud.analyze_student_data()   # Analyze the data to find focus areas.
    studbud.generate_study_plan(num_days=5)  # Generate a study plan for 5 days
    studbud.display_study_plan()    # Display the plan
    studbud.save_study_plan("alice_study_plan.json") # Save the plan to a file

    # Load the study plan from file
    studbud_loaded = StudBud(student_name="Alice")
    studbud_loaded.load_study_plan("alice_study_plan.json")
    studbud_loaded.display_study_plan() # Display the loaded plan to ensure it works