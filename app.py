from flask import Flask, request, render_template
from math import log10

app = Flask(__name__)

def calculate_body_fat(gender, age, height_cm, weight_kg, measurements):
    height_in = height_cm / 2.54  # Convert height from cm to inches
    weight_lb = weight_kg * 2.20462  # Convert weight from kg to lbs

    if gender.lower() == 'male':
        abdomen_in = measurements['abdomen'] / 2.54
        neck_in = measurements['neck'] / 2.54
        body_fat = 86.010 * log10(abdomen_in - neck_in) - 70.041 * log10(height_in) + 36.76
    else:
        waist_in = measurements['waist'] / 2.54
        hip_in = measurements['hip'] / 2.54
        neck_in = measurements['neck'] / 2.54
        body_fat = 163.205 * log10(waist_in + hip_in - neck_in) - 97.684 * log10(height_in) - 78.387

    return body_fat

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bodyfat', methods=['GET', 'POST'])
def bodyfat():
    if request.method == 'POST':
        try:
            gender = request.form['gender']
            age = int(request.form['age'])
            height_cm = float(request.form['height'])
            weight_kg = float(request.form['weight'])
            nationality = request.form['nationality']

            measurements = {
                'abdomen': float(request.form['abdomen']) if gender.lower() == 'male' else None,
                'neck': float(request.form['neck']),
                'waist': float(request.form['waist']) if gender.lower() == 'female' else None,
                'hip': float(request.form['hip']) if gender.lower() == 'female' else None
            }

            body_fat_percentage = calculate_body_fat(gender, age, height_cm, weight_kg, measurements)

            return render_template('result.html', age=age, nationality=nationality, 
                                   gender=gender, body_fat=body_fat_percentage)
        except ValueError:
            return "Invalid input. Please ensure all fields are correctly filled."
    return render_template('bodyfat_form.html')

if __name__ == '__main__':
    app.run(debug=True)


