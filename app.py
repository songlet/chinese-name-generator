from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random
import os

app = Flask(__name__)

# Surname database
SURNAMES = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]

# Male names database
MALE_NAMES = ["伟", "强", "勇", "杰", "涛", "明", "超", "浩", "宇", "鑫"]

# Female names database
FEMALE_NAMES = ["丽", "敏", "静", "秀", "娟", "艳", "芳", "玲", "娜", "婷"]

# Names based on interests
INTEREST_NAMES = {
    "sports": ["健", "翔", "跃", "飞"],
    "music": ["韵", "歌", "乐", "音"],
    "art": ["雅", "艺", "绘", "墨"],
    "reading": ["书", "文", "博", "智"],
    "travel": ["远", "航", "游", "景"]
}

# English to Chinese name mapping
ENGLISH_TO_CHINESE = {
    'a': '安', 'b': '本', 'c': '凯', 'd': '德', 'e': '伊',
    'f': '弗', 'g': '格', 'h': '赫', 'i': '艾', 'j': '杰',
    'k': '克', 'l': '勒', 'm': '姆', 'n': '恩', 'o': '欧',
    'p': '佩', 'q': '丘', 'r': '尔', 's': '斯', 't': '特',
    'u': '尤', 'v': '维', 'w': '威', 'x': '克斯', 'y': '伊',
    'z': '兹'
}

def translate_english_name(name):
    """Convert English name to phonetically similar Chinese characters"""
    name = name.lower()
    chinese_chars = []
    for char in name:
        if char in ENGLISH_TO_CHINESE:
            chinese_chars.append(ENGLISH_TO_CHINESE[char])
    return ''.join(chinese_chars)

def generate_chinese_name(gender, interests, birthdate, english_name):
    # Generate surname from English name (1 character)
    surname = translate_english_name(english_name[:1])
    if not surname:
        surname = random.choice(SURNAMES)
    surname = surname[0]  # Ensure single character
    
    # Select name based on birth month
    birth_month = datetime.strptime(birthdate, "%Y-%m-%d").month
    seasonal_names = {
        1: ["冬", "寒", "雪"],
        2: ["春", "晓", "萌"],
        3: ["春", "雨", "风"],
        4: ["春", "花", "燕"],
        5: ["夏", "阳", "荷"],
        6: ["夏", "雨", "晴"],
        7: ["夏", "炎", "蝉"],
        8: ["秋", "叶", "枫"],
        9: ["秋", "月", "桂"],
        10: ["秋", "霜", "菊"],
        11: ["冬", "梅", "寒"],
        12: ["冬", "雪", "冰"]
    }
    
    # Select name based on interests
    interest_name = ""
    for interest in INTEREST_NAMES:
        if interest in interests.lower():
            interest_name = random.choice(INTEREST_NAMES[interest])
            break
            
    # Select name based on gender (1 character)
    if gender == "male":
        given_name = random.choice(MALE_NAMES)[0]
    else:
        given_name = random.choice(FEMALE_NAMES)[0]
        
    # Combine name components
    if interest_name:
        name = f"{surname}{interest_name}{given_name}"
        explanation = f"""
        Your Chinese name {name} was generated based on:
        - Surname: {surname} (1 character derived from your English name)
        - Middle character: {interest_name} (based on your interests: {interests})
        - Last character: {given_name} (1 character based on your gender)
        """
    else:
        seasonal_char = random.choice(seasonal_names[birth_month])
        name = f"{surname}{seasonal_char}{given_name}"
        explanation = f"""
        Your Chinese name {name} was generated based on:
        - Surname: {surname} (1 character derived from your English name)
        - Middle character: {seasonal_char} (based on your birth month)
        - Last character: {given_name} (1 character based on your gender)
        """
    
    return name, explanation

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            surname = request.form.get('surname', '').strip()
            given_name = request.form.get('given_name', '').strip()
            gender = request.form.get('gender', '').strip()
            interests = request.form.get('interests', '').strip()
            birthdate = request.form.get('birthdate', '').strip()
            
            if not all([surname, given_name, gender, interests, birthdate]):
                return render_template('index.html', error="Please fill in all fields")
            
            english_name = f"{surname} {given_name}"
                
            chinese_name, explanation = generate_chinese_name(gender, interests, birthdate, english_name)
            return render_template('index.html', 
                                name=chinese_name,
                                explanation=explanation,
                                original_name=english_name,
                                gender=gender.capitalize(),
                                interests=interests,
                                birthdate=birthdate)
            
        except Exception as e:
            return render_template('index.html', error=f"Error generating Chinese name: {str(e)}")
    
    return render_template('index.html')

# For PythonAnywhere deployment
application = app

# For local development
if __name__ == '__main__':
    app.run(debug=True)
