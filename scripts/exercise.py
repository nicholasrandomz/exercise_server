import json
import random


class Exercise:
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.link = ""

    def print_exercise(self) -> None:
        print("Exercise Name: ", self.name)
        print("Exercise Type: ", self.type)
        print("Exercise Link: ", self.link)


class ExerciseDatabase:
    exercise_dictionary = []
    exercise_count = 0

    def __init__(self, file: str):
        with open(file) as f:
            database = json.load(f)
        print("Retrieving Exercises from", file, "- date created: ", database['date_created'])

        for ex in database['exercise_list']:
            tempex = Exercise(ex['name'])
            tempex.type = ex['type']
            tempex.link = ex['link']
            self.exercise_count += 1
            self.exercise_dictionary.append(tempex)

    """ Prints Exercises in Exercise Dictionary """

    def print_exercise(self):
        for ex in self.exercise_dictionary:
            ex.print_exercise()

    @staticmethod
    def GetRandomExercise() -> Exercise:
        return random.choice(ExerciseDatabase.exercise_dictionary)


class Challenge:
    def __init__(self):
        self.isCompleted = False
        self.leaderboard = {}
        self.exercise_target = 0
        self.exercise_amount = 0
        self.exercise_challenge = None
        self.GetRandomChallenge()

    def GetRandomChallenge(self):
        self.leaderboard.clear()
        self.exercise_challenge = ExerciseDatabase.GetRandomExercise()
        if 'Cardio' not in self.exercise_challenge.type:
            self.exercise_target = random.choice([50, 100, 1000, 5000])
        else:
            self.exercise_target = random.randrange(10, 50, 5)

    # AMOUNT RELATED
    def CalculatePercentage(self) -> float:
        return float(self.exercise_amount / self.exercise_target * 100)

    def SubtractAmount(self, user: str, amt: float) -> None:
        """ Subtract Amount for PARTICIPATING users """
        if user in self.leaderboard:
            self.leaderboard[user] -= amt

        self.exercise_amount -= amt
        if self.exercise_amount < self.exercise_target:
            self.isCompleted = False

    def SetAmount(self, amt) -> None:
        self.exercise_amount = amt

    def AddAmount(self, user: str, amt: float) -> None:
        if user in self.leaderboard:
            self.leaderboard[user] += amt
        else:
            self.leaderboard[user] = amt

        self.exercise_amount += amt
        if self.exercise_amount >= self.exercise_target:
            self.isCompleted = True
            self.exercise_amount = self.exercise_target

    def UpdateAmount(self, user: str, amt: float) -> None:
        if user in self.leaderboard:
            wrong_amt = self.leaderboard[user]
            self.SubtractAmount(user, wrong_amt)
            self.AddAmount(user, amt)

    # TEXT RELATED
    def challenge_text(self) -> str:
        return "CHALLENGE THIS WEEK: " + str(self.exercise_target) + " " + str(self.exercise_challenge.name) + "\n" \
                                                                                                               "Link: " + str(
            self.exercise_challenge.link)

    def status_text(self) -> str:
        if self.exercise_amount < self.exercise_target:
            return "Challenge Status: " + str(self.exercise_amount) + "/" + str(self.exercise_target) + " " + \
                   str(self.exercise_challenge.name) + " (" + "{:.2f}".format(self.CalculatePercentage()) + "%)"
        else:
            return "CHALLENGE COMPLETE"

    def leaderboard_text(self) -> str:
        if len(self.leaderboard) == 0:
            return "No Leaderboard"

        text = self.status_text()
        text += "\n"
        for everyone in self.leaderboard:
            print("DEBUG:", everyone, self.leaderboard[everyone])
            text += everyone + ": " + str(self.leaderboard[everyone]) + " (" + "{:.2f}".format(
                (self.leaderboard[everyone] / self.exercise_target * 100)) + "%)\n"
        return text
