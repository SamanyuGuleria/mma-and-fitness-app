import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import math
from gtts import gTTS
import tempfile

# -------------------------
# LOAD API KEY
# -------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

st.set_page_config(page_title="Elite AI Performance Lab", layout="centered")

st.title("🏆 Elite AI Performance Lab")
st.write("AI-Powered Training | MMA | Strength | Nutrition | Science-Based Programming")

# -------------------------
# USER INPUTS
# -------------------------
goal = st.selectbox(
    "Primary Goal:",
    ["Muscle Gain", "Fat Loss", "Strength", "Athletic Performance", "MMA Conditioning"]
)

experience = st.selectbox(
    "Training Experience:",
    ["Beginner (0-1 yr)", "Intermediate (1-3 yrs)", "Advanced (3+ yrs)"]
)

days = st.selectbox("Training Days per Week:", [3,4,5,6])

weight = st.number_input("Bodyweight (kg)", 40,150,70)
height = st.number_input("Height (cm)",140,210,170)
age = st.number_input("Age",15,50,20)

# -------------------------
# CALORIE CALCULATIONS
# -------------------------
bmr = 10 * weight + 6.25 * height - 5 * age + 5
maintenance = bmr * 1.5

if goal == "Muscle Gain":
    calories = maintenance + 300
elif goal == "Fat Loss":
    calories = maintenance - 400
else:
    calories = maintenance

protein = round(weight * 1.8,1)
fats = round(weight * 0.8,1)
carbs = round((calories - (protein*4 + fats*9))/4,1)

# -------------------------
# FALLBACK PLAN
# -------------------------
def fallback_plan():

    base_strength = """
### 🏋 Strength Foundation

Barbell Squat – 4x5  
Bench Press – 4x6  
Deadlift – 3x5  
Pull-ups – 3x8
"""

    mma_block = """
### 🥊 MMA Conditioning

Heavy Bag Rounds – 5x3 min  
Sprawl Drills – 4x10  
Shadowboxing – 3x5 min  
Russian Twists – 3x20
"""

    nutrition_block = f"""
### 🥗 Nutrition

Calories: {round(calories)} kcal  
Protein: {protein} g  
Carbs: {carbs} g  
Fats: {fats} g
"""

    progression = """
### 📈 Progression

Add 2.5kg weekly  
Deload every 6-8 weeks  
Sleep 7-9 hours
"""

    if goal == "MMA Conditioning":
        return base_strength + mma_block + nutrition_block + progression
    else:
        return base_strength + nutrition_block + progression


# -------------------------
# PLAN GENERATOR
# -------------------------
if st.button("Generate Elite Plan"):

    try:

        if not client:
            raise Exception("API key missing")

        prompt = f"""
Create a detailed {days}-day training program.

Goal: {goal}
Experience: {experience}

Include:
- Exercises
- Sets and reps
- Rest time
- Nutrition
- Recovery
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are an elite strength and MMA coach."},
                {"role":"user","content":prompt}
            ]
        )

        st.success("Elite Plan Generated")
        st.write(response.choices[0].message.content)

    except Exception:
        st.warning("AI unavailable, using fallback plan.")
        st.write(fallback_plan())


# -------------------------
# AI EXERCISE FORM COACH
# -------------------------

st.markdown("---")
st.subheader("🏋 AI Exercise Technique Coach")

exercise = st.text_input("Enter an exercise (Squat, Deadlift, Jab Cross, etc)")

if st.button("Explain Technique"):

    if exercise.strip() == "":
        st.warning("Enter an exercise name.")

    else:
        try:
            if client is None:
                raise Exception("No API key")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an elite strength coach and biomechanics expert."},
                    {"role": "user", "content": f"Explain perfect form for {exercise}. Include cues, mistakes and injury prevention."}
                ],
                temperature=0.5
            )

            explanation = response.choices[0].message.content
            st.write(explanation)

        except Exception:
            st.warning("AI unavailable. Showing offline coaching cues.")

            exercise_lower = exercise.lower()

            if "squat" in exercise_lower:
                st.write("""
**Squat Form**
- Keep chest up and spine neutral
- Push hips back before bending knees
- Knees should track over toes
- Drive through mid-foot
- Common mistake: knees collapsing inward
""")
            elif "deadlift" in exercise_lower:
                st.write("""
**Deadlift Form**
- Keep bar close to shins
- Maintain a neutral spine
- Brace core before lifting
- Push the floor away
- Common mistake: rounding lower back
""")
            elif "jab" in exercise_lower or "cross" in exercise_lower:
                st.write("""
**Boxing Punch Form**
- Keep chin tucked and guard high
- Rotate hips and shoulders into the punch
- Snap the punch back to guard quickly
- Stay balanced on your feet
- Common mistake: dropping the non-punching hand
""")
            else:
                st.write("""
**General Form Advice**
- Use controlled movement
- Maintain proper posture
- Avoid ego lifting
- Use full range of motion
- Stop if form breaks down
""")


# -------------------------
# WEEKLY TRACKER
# -------------------------
st.markdown("---")
st.subheader("✅ Weekly Training Tracker")

for i in range(1, days+1):
    st.checkbox(f"Completed Day {i}")


# -------------------------
# AI RECOVERY ADVISOR
# -------------------------

st.markdown("---")
st.subheader("🧠 AI Recovery & Injury Prevention Advisor")

fatigue = st.selectbox(
    "Current Fatigue Level",
    ["Low", "Moderate", "High"]
)

sleep = st.slider("Hours of Sleep Last Night", 3, 10, 7)

if st.button("Generate Recovery Advice"):

    try:
        if client is None:
            raise Exception("No API key")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sports scientist specializing in athletic recovery."},
                {"role": "user", "content": f"""
Athlete fatigue level: {fatigue}
Sleep last night: {sleep} hours

Provide recovery advice including:
- Mobility work
- Nutrition
- Hydration
- Sleep optimization
- Injury prevention
"""}
            ],
            temperature=0.6
        )

        advice = response.choices[0].message.content
        st.write(advice)

    except Exception:
        st.warning("AI unavailable. Showing offline recovery advice.")

        if fatigue == "High" or sleep <= 5:
            st.write("""
**Recovery Priority: High**
- Reduce training intensity for 1–2 days
- Sleep 8–9 hours tonight
- Increase water and electrolytes
- Focus on mobility and stretching
- Keep protein intake high
""")
        elif fatigue == "Moderate" or sleep == 6:
            st.write("""
**Recovery Priority: Moderate**
- Keep training but reduce volume slightly
- Add 10–15 minutes mobility work
- Hydrate consistently through the day
- Eat balanced meals with protein and carbs
""")
        else:
            st.write("""
**Recovery Status: Good**
- Maintain your current routine
- Keep sleep above 7 hours
- Stay hydrated
- Continue mobility and warm-up work
""")

# -------------------------
# AI DAILY MEAL PLANNER
# -------------------------

st.markdown("---")
st.subheader("🍛 AI Smart Meal Planner")

diet = st.selectbox(
    "Diet Preference",
    ["Mixed", "Vegetarian", "High Protein Athlete"]
)

# Correct macro calculations
protein_macro = round(weight * 1.8)
fat_macro = round(weight * 0.8)
carb_macro = round((calories - (protein_macro * 4 + fat_macro * 9)) / 4)
water_intake = round(weight * 35)

st.markdown(f"""
### Daily Macro Targets

Protein: **{protein_macro} g**  
Carbohydrates: **{carb_macro} g**  
Fats: **{fat_macro} g**  
Water Intake: **{water_intake} ml**
""")

if st.button("Generate Daily Meal Plan"):

    try:
        if client is None:
            raise Exception("No API key")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional sports nutritionist."},
                {"role": "user", "content": f"""
Create a daily meal plan for an athlete.

Calories: {round(calories)}
Protein target: {protein_macro} g
Carbs target: {carb_macro} g
Fat target: {fat_macro} g
Diet type: {diet}

Include:
- Breakfast
- Lunch
- Snack
- Dinner
- Hydration advice
- Micronutrient tips
"""}
            ],
            temperature=0.7
        )

        meal_plan = response.choices[0].message.content
        st.write(meal_plan)

    except Exception:

        st.warning("AI unavailable. Showing offline meal plan.")

        if diet == "Vegetarian":
            st.write(f"""
**Vegetarian Athlete Meal Plan**

Breakfast:
Oats + milk + banana + peanut butter

Lunch:
Rice + dal + paneer + vegetables

Snack:
Greek yogurt + almonds

Dinner:
Roti + tofu/paneer + vegetables

Daily Targets:
Calories: {round(calories)} kcal  
Protein: {protein_macro} g  
Carbs: {carb_macro} g  
Fats: {fat_macro} g  

Water Intake: {water_intake} ml
""")

        elif diet == "High Protein Athlete":
            st.write(f"""
**High Protein Athlete Meal Plan**

Breakfast:
Eggs + oats + fruit

Lunch:
Chicken breast + rice + vegetables

Snack:
Greek yogurt or whey protein shake

Dinner:
Fish or chicken + potatoes/rice + salad

Daily Targets:
Calories: {round(calories)} kcal  
Protein: {protein_macro} g  
Carbs: {carb_macro} g  
Fats: {fat_macro} g  

Water Intake: {water_intake} ml
""")

        else:
            st.write(f"""
**Balanced Mixed Diet Plan**

Breakfast:
Eggs or paneer + oats + fruit

Lunch:
Rice + dal + chicken/paneer + vegetables

Snack:
Nuts + yogurt

Dinner:
Roti + protein source + vegetables

Daily Targets:
Calories: {round(calories)} kcal  
Protein: {protein_macro} g  
Carbs: {carb_macro} g  
Fats: {fat_macro} g  

Water Intake: {water_intake} ml
""")

# -------------------------
# AI FIGHT COACH
# -------------------------

st.markdown("---")
st.subheader("🥊 AI Fight Coach")

fight_problem = st.text_area(
    "Describe your problem (example: I drop my left hand when throwing a jab)"
)

if st.button("Get Coaching Advice"):

    if fight_problem.strip() == "":
        st.warning("Describe the issue you're facing.")

    else:
        try:
            if client is None:
                raise Exception("No API key")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional MMA striking coach specializing in boxing, Muay Thai, and kickboxing."},
                    {"role": "user", "content": f"My issue in training is: {fight_problem}. Give corrections, drills, and tips."}
                ],
                temperature=0.6
            )

            advice = response.choices[0].message.content
            st.success("Coaching Advice:")
            st.write(advice)

        except Exception:
            st.warning("AI unavailable. Showing offline coaching advice.")

            problem = fight_problem.lower()

            if "drop" in problem and "hand" in problem:
                st.write("""
**Guard Discipline Fix**
- Return every punch straight back to guard
- Shadowbox slowly with focus on hand return
- Keep chin tucked
- Practice jab-cross while watching your non-punching hand
""")
            elif "gas" in problem or "tired" in problem or "cardio" in problem:
                st.write("""
**Fight Conditioning Advice**
- Add interval rounds: 5 x 3 min hard work
- Improve breathing rhythm
- Use bag work, sprawls, and shadowboxing
- Pace yourself instead of exploding every exchange
""")
            else:
                st.write("""
**Basic Fight Coaching Advice**
- Keep your guard high
- Stay balanced when throwing strikes
- Use footwork before power
- Drill technique slowly before sparring fast
""")



        # -------------------------
# AI INJURY PREVENTION ADVISOR
# -------------------------

st.markdown("---")
st.subheader("🛡 AI Injury Prevention Advisor")

exercise = st.text_input("Exercise you are worried about injuring yourself in:")

if st.button("Get Injury Prevention Tips"):

    if exercise.strip() == "":
        st.warning("Please enter an exercise.")
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a sports physiotherapist."},
                    {"role": "user", "content": f"Explain how to prevent injury when performing {exercise}. Include warmup tips and technique advice."}
                ]
            )

            tips = response.choices[0].message.content
            st.success("Injury Prevention Tips")
            st.write(tips)

        except Exception:
            st.warning("AI unavailable. Basic advice:")
            st.write("Warm up properly, maintain correct form, and avoid excessive weight.")
            # -------------------------
# WEEKLY PROGRESS ANALYZER
# -------------------------

st.markdown("---")
st.subheader("📊 Weekly Progress Analyzer")

workouts_completed = st.slider("Workouts completed this week", 0, 7, 3)
energy_level = st.slider("Average energy level", 1, 10, 6)

if st.button("Analyze Weekly Progress"):

    # Try AI analysis first
    try:
        if client is None:
            raise Exception("No API key")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a strength coach analyzing athlete performance."},
                {"role":"user","content":f"""
Workouts completed: {workouts_completed}
Energy level: {energy_level}

Give feedback on training consistency and improvements.
"""}
            ]
        )

        feedback = response.choices[0].message.content
        st.success("AI Performance Analysis")
        st.write(feedback)

    # If AI fails, run local logic
    except Exception:

        st.warning("⚠ AI unavailable. Using local performance analysis.")

        if workouts_completed >= 5 and energy_level >= 7:
            st.success("Excellent week. Training volume and recovery are strong.")

        elif workouts_completed >= 3 and energy_level >= 5:
            st.info("Decent consistency. Focus on improving recovery and pushing intensity.")

        elif workouts_completed <= 2:
            st.error("Low training consistency. Try scheduling workouts earlier in the week.")

        if energy_level <= 4:
            st.write("Your energy levels are low. Consider improving sleep, hydration, and nutrition.")
# AI MOTIVATION COACH
# -------------------------

st.markdown("---")
st.subheader("🔥 AI Motivation Coach")

if st.button("Give Me Motivation"):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are an intense MMA coach motivating an athlete."},
                {"role":"user","content":"Give a short motivational speech for training hard."}
            ]
        )

        speech = response.choices[0].message.content
        st.success("Coach Says:")
        st.write(speech)

    except Exception:
        st.write("Discipline beats motivation. Show up and do the work.")
        # -------------------------
# -------------------------
# AI VOICE COACH
# -------------------------

st.markdown("---")
st.subheader("🎙 AI Voice Coach")

voice_prompt = st.text_area("Ask the AI coach something")

if st.button("Ask Voice Coach"):

    try:

        if client is None:
            raise Exception("No API key")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are an elite MMA and strength coach."},
                {"role":"user","content":voice_prompt}
            ]
        )

        answer = response.choices[0].message.content

        st.write(answer)

        tts = gTTS(text=answer, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_file = open(fp.name, "rb")
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

    except Exception:

        fallback = "Stay disciplined. Train consistently and focus on proper technique."

        st.write(fallback)

        tts = gTTS(text=fallback, lang="en")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_file = open(fp.name, "rb")
            audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")