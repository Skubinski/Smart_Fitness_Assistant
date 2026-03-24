import pandas as pd

def assing_activity_factor(row):
    fitness_type = row['Fitness Type']
    goal = row['Fitness Goal']

    if fitness_type == "Cardio Fitness":
        if goal == "Weight Loss":
            return 1.55
        else:
            return 1.375
    elif fitness_type == "Muscular Fitness":
        if goal == "Weight Gain":
            return 1.725
        else:
            return 1.55

    return 1.375

def calculate_bmr(row):
    weight = row['Weight']
    height = row['Height'] * 100
    age = row['Age']
    sex = row['Sex']

    if sex == 'Male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif sex == 'Female':
        return 10 * weight + 6.25 * height - 5 * age - 161

    return -1

def calculate_tdee(row):
    bmr = row['BMR']
    act_factor = row['Activity Factor']

    tdee = bmr * act_factor

    return tdee

def calculate_target_calories(row):
    tdee = row['TDEE']
    goal = row['Fitness Goal']
    target_calories = 0

    if goal == "Weight Gain":
        target_calories = tdee + 300
    elif goal == "Weight Loss":
        target_calories = tdee - 500

    return target_calories

def encoding_gender(row):
    gender = row['Sex']

    if gender == "Male":
        return 1
    elif gender == "Female":
        return 0
    return -1

def encoding_hypertension(row):
    hypertension = row['Hypertension']

    if hypertension == "Yes":
        return 1
    elif hypertension == "No":
        return 0
    return -1
def encoding_diabetes(row):
    diabet = row['Diabetes']

    if diabet == "Yes":
        return 1
    elif diabet == "No":
        return 0
    return -1

def encoding_level(row):
    level = row['Level']

    if level == "Underweight":
        return 0
    elif level == "Normal":
        return 1
    elif level == "Overweight":
        return 2
    elif level == "Obuse":
        return 3
    return -1

def encoding_goal(row):
    goal = row['Fitness Goal']

    if goal == "Weight Loss":
        return 0
    elif goal == "Weight Gain":
        return 1
    return -1

def encoding_fitness_type(row):
    type = row['Fitness Type']

    if type == "Cardio Fitness":
        return 0
    elif type == "Muscular Fitness":
        return 1
    return -1

def encoding_exercises(row):
    exercises = row['Exercises']

    if exercises == 'Squats, deadlifts, bench presses, and overhead presses':
        return 0
    elif exercises == 'Squats, yoga, deadlifts, bench presses, and overhead presses':
        return 1
    elif exercises == 'Brisk walking, cycling, swimming, running , or dancing.':
        return 2
    elif exercises == 'Walking, Yoga, Swimming.':
        return 3
    elif exercises == 'brisk walking, cycling, swimming, or dancing.':
        return 4
    return -1



df = pd.read_csv('../Dataset/gym and diet recommendation1.csv').dropna()


df = df.drop(columns=['ID'])

act_factor = df.apply(assing_activity_factor, axis=1)
df.insert(loc=11, column='Activity Factor', value=act_factor)

bmr_values = df.apply(calculate_bmr, axis=1)
df.insert(loc=12, column='BMR', value=bmr_values)

tdee_values = df.apply(calculate_tdee, axis=1)
df.insert(loc=13, column="TDEE", value=tdee_values)

target_calories = df.apply(calculate_target_calories, axis=1)
df.insert(loc=14, column="Target Calories", value=target_calories)

df['Sex'] = df.apply(encoding_gender, axis=1)
df['Hypertension'] = df.apply(encoding_hypertension, axis=1)
df['Diabetes'] = df.apply(encoding_diabetes, axis=1)
df['Level'] = df.apply(encoding_level, axis=1)
df['Fitness Goal'] = df.apply(encoding_goal, axis=1)
df['Fitness Type'] = df.apply(encoding_fitness_type, axis=1)
df['Exercises'] = df.apply(encoding_exercises, axis=1)
df = df[df['Diet'] != 'Diet']




df.to_csv('../Dataset/processed_dataset.csv', index=False)