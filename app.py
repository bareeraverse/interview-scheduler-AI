from scheduler import schedule_interviews
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

interview_data = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        availability = request.form.getlist('availability')
        priority = int(request.form['priority']) if request.form['role'] == 'Candidate' else None


        interview_data.append({
    'name': name,
    'role': role,
    'availability': availability,
    'priority': priority
})


    return render_template('index.html', interviews=interview_data)

@app.route('/schedule')
def show_schedule():
    from scheduler import schedule_interviews
    final_schedule = schedule_interviews(interview_data)

    total = len([p for p in interview_data if p['role'] == 'Candidate'])
    scheduled = len([s for s in final_schedule if s['status'] == 'Scheduled' and s['candidate'] != 'N/A'])
    unscheduled = total - scheduled
    used_slots = list(set([s['slot'] for s in final_schedule if s['slot'] != 'N/A']))

    return render_template('schedule.html', schedule=final_schedule, total=total,
                           scheduled=scheduled, unscheduled=unscheduled, slots=used_slots)



if __name__ == '__main__':
    app.run(debug=True)
