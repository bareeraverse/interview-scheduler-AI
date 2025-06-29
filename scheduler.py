def schedule_interviews(data):
    candidates = [p for p in data if p['role'] == 'Candidate']
    interviewers = [p for p in data if p['role'] == 'Interviewer']

    schedule = []
    used_slots = set()
    used_interviewers = set()
    matched_candidates = set()

    # Sort candidates by priority: 1 = High, 5 = Low
    candidates = sorted(candidates, key=lambda x: x['priority'])

    for candidate in candidates:
        matched = False
        for slot in candidate['availability']:
            for interviewer in interviewers:
                if (
                    slot in interviewer['availability']
                    and slot not in used_slots
                    and interviewer['name'] not in used_interviewers
                ):
                    # Match found — assign interviewer to this candidate
                    schedule.append({
                        'candidate': candidate['name'],
                        'interviewer': interviewer['name'],
                        'slot': slot,
                        'priority': candidate['priority'],
                        'status': 'Scheduled'
                    })
                    used_slots.add(slot)
                    used_interviewers.add(interviewer['name'])
                    matched_candidates.add(candidate['name'])
                    matched = True
                    break
            if matched:
                break

        if not matched:
            # Could not schedule this candidate
            schedule.append({
                'candidate': candidate['name'],
                'interviewer': 'Not Assigned',
                'slot': 'N/A',
                'priority': candidate['priority'],
                'status': 'Unscheduled'
            })

    # Any interviewer not used goes here
    for interviewer in interviewers:
        if interviewer['name'] not in used_interviewers:
            schedule.append({
                'candidate': 'N/A',
                'interviewer': interviewer['name'],
                'slot': 'N/A',
                'priority': '—',
                'status': 'Unscheduled'
            })

    return schedule
