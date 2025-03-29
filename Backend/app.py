from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import random

app = Flask(__name__, static_folder="../")  
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5503"}})  # Allow frontend on port 5503

# Serve the chatbot frontend
@app.route("/")
def serve_chatbot():
    return send_from_directory(app.static_folder, "index.html")

# Serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Chatbot API
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '').lower()

    bot_responses = {
        "eligibility": "The Candidate should be an Indian National; Passed HSC or its equivalent examination with Physics and Mathematics as compulsory subjects along with one of the Chemistry or Biotechnology or Biology or Technical or Vocational subjects and obtained at least 45% marks (at least 40% marks, in case of Backward class categories and Persons with Disability candidates belonging to Maharashtra State only) in the above subjects taken together and Obtained non-zero score in MHT-CET 2023 for Maharashtra State Candidates (or in JEE(Main) Paper I for AI Seats which are available only in CAP Rounds).",
        "apply": "Candidates must register on the DTE Maharashtra website, fill out the application form, upload necessary documents, and select KJSIT as their preferred institute. After the CAP rounds, remaining vacant seats are filled at the Institute level by inviting applications on the portal.",
        "fee": "The fees for B.Tech programs for the academic year 2023-24 will be displayed after approval from the Fees Regulating Authority, Government of Maharashtra. In 2022-23, tuition and development fees varied based on category and eligibility. Hostel fees, if applicable, are separate and depend on the campus location.",
        "dates": "The MHT-CET exam is scheduled between April 15-30, 2024. CAP registration will take place from June 10-30, 2024. Candidates must stay updated with notifications from DTE Maharashtra for further details.",
        "established": "KJSIT was established in the year 2001 by the Somaiya Trust at the Ayurvihar campus, Sion, to impart quality education in modern fields of Information Technology and Engineering.",
        "popular_name": "K. J. Somaiya Institute of Technology is popularly referred to as KJSIT by students, faculty, alumni, and staff.",
        "location": "KJSIT is situated near Sion railway station (Central Line) and Chunabhatti railway station (Harbour Line). The college is close to the Eastern Express Highway, making it easily accessible by road.",
        "why kjsit": "KJSIT is conferred with 'Fresh Autonomous Status' by UGC and is permanently affiliated with the University of Mumbai. It has received 'A' grade accreditation from NAAC and NBA accreditation for its Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology programs. The institute is recognized for academic excellence, research initiatives, and holistic student development.",
        "courses": "KJSIT offers undergraduate programs in B.Tech (Computer Engineering, Information Technology, Electronics & Telecommunication Engineering, Artificial Intelligence & Data Science), a postgraduate M.Tech program in Artificial Intelligence, and Ph.D. programs in Computer Engineering, Information Technology, and Electronics & Telecommunication Engineering.",
        "admission_process": "Admissions are conducted through the Centralized Admission Process (CAP) by the State CET Cell, Maharashtra. Candidates must apply through CAP to be eligible for admission. Vacant seats after CAP rounds are filled at the institute level by inviting applications.",
        "documents": "Documents required for admission include SSC (Std X) mark sheet, HSC (Std XII) mark sheet, MHT-CET Score Card, School Leaving Certificate, Certificate of Indian Nationality, Migration Certificate (if applicable), Gap affidavit (if required), and True copy of Aadhar card.",
        "minority_seat": "51% of the total seats at KJSIT are reserved for candidates belonging to the Gujarati Linguistic Minority category. These seats are filled through the CAP process.",
        "fee_concession": "All types of fee concessions declared by the Government of Maharashtra are available for CAP-admitted students. However, candidates securing admission against vacant seats remaining after CAP rounds will not be eligible for fee concessions.",
        "cutoff": "Cutoffs for previous years varied by branch. In 2022-23, the CAP cutoff based on MHT-CET for Computer Engineering was 95.60, Information Technology was 94.87, Electronics & Telecommunication Engineering was 89.52, and Artificial Intelligence & Data Science was 94.07.",
        "placement": "KJSIT has an approximately 80% placement rate, with the highest CTC offered being ₹13.5 LPA. Companies visiting the campus include top IT firms and multinational corporations.",
        "hostel": "Hostel accommodation is available for outstation students on a first-come-first-serve basis at Somaiya Vidyavihar and Ayurvihar campuses. Bus facilities are provided for students staying in the hostel.",
        "transfer": "If a candidate is allotted a different branch in subsequent counseling rounds conducted by the institute, they must cancel their previous admission. The previously paid fees will be adjusted towards the new admission as per ARA guidelines.",
        "cancellation": "Admission can be canceled by applying online and submitting the required cancellation form along with receipts. Fees will be refunded after deducting cancellation charges as per ARA rules.",
        "nr_quota": "No, KJSIT does not have an NRI quota for admissions.",
        "autonomous": "Yes, KJSIT is an autonomous institute affiliated with the University of Mumbai and approved by AICTE.",
        "accreditation": "KJSIT is accredited by NAAC with an 'A' grade. The Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology departments are accredited by NBA.",
        "awards": "KJSIT was awarded 'Best College' in the urban region by Mumbai University in 2018-19 and has received multiple recognitions from professional bodies.",
        "iic": "KJSIT’s Institution Innovation Council (IIC) has been recognized as a Top Performing IIC for four consecutive years: 2018-19, 2019-20, 2020-21, and 2021-22.",
        "research": "KJSIT provides financial assistance for innovative student and faculty projects through its research funding programs.",
        "robotics": "KJSIT actively participates in national-level robotics competitions like e-Yantra and ROBOCON, ranking among the top teams in India over the past five years."
    }

    default_responses = [
        "Could you please provide more details about your query?",
        "I'm here to help with admission information. What would you like to know?",
        "Feel free to ask about eligibility, application process, or fee structure.",
        "I didn't understand that. Can you try asking in a different way?"
    ]

    def get_response(query):
        response = bot_responses.get(query, random.choice(default_responses))
        return response

    response = get_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
