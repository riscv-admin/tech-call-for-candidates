import os
from datetime import datetime, timedelta

import requests
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/call-submit', methods=['POST'])
def submit_form():
    # Collect form data
    data = request.form

    # Check for GitHub token and user
    github_token = os.getenv('GITHUB_TOKEN')

    if not github_token:
        flash("ERROR: Could NOT Open GitHub Issue. \n Please try again or contact help@riscv.org.", "error")
        return redirect(url_for('index'))

    # Prepare data for GitHub issue
    title = f"Call for {data['positions']} - {data['groupName']}"

    # Current date
    current_date = datetime.now()

    # Add 14 days to the current date
    future_date = current_date + timedelta(days=14)

    # Format the future date as "DAY, DAY OF WEEK, Month YEAR"
    formatted_future_date = future_date.strftime("%A, %B %d, %Y")

    body = f"""
Basic Information:
- Contact Email: {data['requestorEmail']}
- Group Name: {data['groupName']}
- Group Type: {data['groupType']}
- Positions: {data['positions']}
- Governing Committee: {data['governingCommittee']}
- Dotted-Line Governing Committee: {data['dottedLineCommittee']}
- Required Technical Qualifications: {data.get('techQuali', '')}
- Group Charter: {data.get('groupCharter', '')}

TODO:
- [ ] Review carefully for correctness the Draft Email with the group and the Governing and Dotted-line committed Chairs. Update as needed. (You)
- [ ] Send the email to the following mailing lists (Governing HC/IC Chair):
    - [ ] tech-announce@lists.riscv.org (which is moderated)
    - [ ] governing IC/HC mailing list ({data['governingCommittee']})
    - [ ] all dotted-line committees ({data['dottedLineCommittee']})
    - [ ] the group mailing list ({data['groupName']})
- [ ] Create the Candidates document (RVI TPMs)
- [ ] Collect the candidate(s) (RVI TPMs)
- [ ] Interview the candidate(s) (HC/IC Chair(s))
- [ ] Select the nominee(s) (HC/IC Chair(s))
- [ ] Seek approval of the nominees(s) per the process (RVI TPMs)

Contact help@riscv.org if you have any questions.

---------------------------------------------

Sample Call for {data['positions']} Email:

Subject:

Call for {data['positions']} - {data['groupName']}

Body:

Dear RISC-V Technical Community,

This is a Call for {data['positions']}  for the {data['groupName']}.

If you're interested in participating or know a suitable candidate, we encourage you to reach out. Please email help@riscv.org with the candidate’s details, including their name, membership affiliation, qualifications, a brief biography, and a statement of intent. Ensure that both the bio and statement are concise, each under 250 words.

Please note, all candidate submissions, comprising a biography and a statement of intent, must be received by {formatted_future_date}. For a comprehensive understanding of this process, refer to the [Groups & Chairs policy](https://docs.google.com/document/d/1_0Mnd5sXn8KcyOUI4-qvCdG7ITPY6vSAIhFc5Iy-URI/edit) which outlines the necessary guidelines and details.

Group's Charter: 
{data.get('groupCharter', '')}

The list of qualification includes the following but is not limited to:
{data.get('techQuali', '')}

Additional duties as Chair/Vice-Chair include:

- Collaboration with existing task groups within the RISC-V Foundation.
- Seek contributions/collaborations while keeping focus on TG charter.
- Publish meeting minutes.
- Serve as an editor for some of the proposals.
- Community interactions through meetings, mail list, GitHub, Wiki.
- Respond to queries within 48 hours.
- Manage and run regular meetings as per the group charter.
- Attend weekly tech-chairs meetings.
- See the Chairs Best Practices document for more details.

Best Regards,

[REPLACE WITHE THE GOVERNING COMMITTEE CHAIR NAME], {data['governingCommittee']} Chair

---------------------------------------------
"""
    # Use GitHub API to create an issue
    url = "https://api.github.com/repos/riscv-admin/help/issues"
    headers = {
        "Authorization": "token " + github_token,
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body,
        "labels": ["call-for-candidates"]
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        flash("Your submission was successful!", "success") 
        return redirect('/')
    else:
        # Handle other status codes
        flash(f"ERROR: Could NOT Open GitHub Issue. Status Code: {response.status_code}. \n Please try again or contact help@riscv.org.", "error")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)