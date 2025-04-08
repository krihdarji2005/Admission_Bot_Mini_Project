# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import os
# import random

# app = Flask(__name__, static_folder="../")  
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5503"}})  # Allow frontend on port 5503

# # Serve the chatbot frontend
# @app.route("/")
# def serve_chatbot():
#     return send_from_directory(app.static_folder, "index.html")

# # Serve static files (CSS, JS, images)
# @app.route('/<path:filename>')
# def serve_static_files(filename):
#     return send_from_directory(app.static_folder, filename)

# # Chatbot API
# @app.route('/api/chat', methods=['POST'])
# def chat():
#     data = request.json
#     query = data.get('message', '').lower()

#     bot_responses = {
#         "eligibility": "The Candidate should be an Indian National; Passed HSC or its equivalent examination with Physics and Mathematics as compulsory subjects along with one of the Chemistry or Biotechnology or Biology or Technical or Vocational subjects and obtained at least 45% marks (at least 40% marks, in case of Backward class categories and Persons with Disability candidates belonging to Maharashtra State only) in the above subjects taken together and Obtained non-zero score in MHT-CET 2023 for Maharashtra State Candidates (or in JEE(Main) Paper I for AI Seats which are available only in CAP Rounds).",
#         "apply": "Candidates must register on the DTE Maharashtra website, fill out the application form, upload necessary documents, and select KJSIT as their preferred institute. After the CAP rounds, remaining vacant seats are filled at the Institute level by inviting applications on the portal.",
#         "fee": "The fees for B.Tech programs for the academic year 2023-24 will be displayed after approval from the Fees Regulating Authority, Government of Maharashtra. In 2022-23, tuition and development fees varied based on category and eligibility. Hostel fees, if applicable, are separate and depend on the campus location.",
#         "dates": "The MHT-CET exam is scheduled between April 15-30, 2024. CAP registration will take place from June 10-30, 2024. Candidates must stay updated with notifications from DTE Maharashtra for further details.",
#         "established": "KJSIT was established in the year 2001 by the Somaiya Trust at the Ayurvihar campus, Sion, to impart quality education in modern fields of Information Technology and Engineering.",
#         "popular_name": "K. J. Somaiya Institute of Technology is popularly referred to as KJSIT by students, faculty, alumni, and staff.",
#         "location": "KJSIT is situated near Sion railway station (Central Line) and Chunabhatti railway station (Harbour Line). The college is close to the Eastern Express Highway, making it easily accessible by road.",
#         "why kjsit": "KJSIT is conferred with 'Fresh Autonomous Status' by UGC and is permanently affiliated with the University of Mumbai. It has received 'A' grade accreditation from NAAC and NBA accreditation for its Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology programs. The institute is recognized for academic excellence, research initiatives, and holistic student development.",
#         "courses": "KJSIT offers undergraduate programs in B.Tech (Computer Engineering, Information Technology, Electronics & Telecommunication Engineering, Artificial Intelligence & Data Science), a postgraduate M.Tech program in Artificial Intelligence, and Ph.D. programs in Computer Engineering, Information Technology, and Electronics & Telecommunication Engineering.",
#         "admission_process": "Admissions are conducted through the Centralized Admission Process (CAP) by the State CET Cell, Maharashtra. Candidates must apply through CAP to be eligible for admission. Vacant seats after CAP rounds are filled at the institute level by inviting applications.",
#         "documents": "Documents required for admission include SSC (Std X) mark sheet, HSC (Std XII) mark sheet, MHT-CET Score Card, School Leaving Certificate, Certificate of Indian Nationality, Migration Certificate (if applicable), Gap affidavit (if required), and True copy of Aadhar card.",
#         "minority_seat": "51% of the total seats at KJSIT are reserved for candidates belonging to the Gujarati Linguistic Minority category. These seats are filled through the CAP process.",
#         "fee_concession": "All types of fee concessions declared by the Government of Maharashtra are available for CAP-admitted students. However, candidates securing admission against vacant seats remaining after CAP rounds will not be eligible for fee concessions.",
#         "cutoff": "Cutoffs for previous years varied by branch. In 2022-23, the CAP cutoff based on MHT-CET for Computer Engineering was 95.60, Information Technology was 94.87, Electronics & Telecommunication Engineering was 89.52, and Artificial Intelligence & Data Science was 94.07.",
#         "placement": "KJSIT has an approximately 80% placement rate, with the highest CTC offered being ₹13.5 LPA. Companies visiting the campus include top IT firms and multinational corporations.",
#         "hostel": "Hostel accommodation is available for outstation students on a first-come-first-serve basis at Somaiya Vidyavihar and Ayurvihar campuses. Bus facilities are provided for students staying in the hostel.",
#         "transfer": "If a candidate is allotted a different branch in subsequent counseling rounds conducted by the institute, they must cancel their previous admission. The previously paid fees will be adjusted towards the new admission as per ARA guidelines.",
#         "cancellation": "Admission can be canceled by applying online and submitting the required cancellation form along with receipts. Fees will be refunded after deducting cancellation charges as per ARA rules.",
#         "nr_quota": "No, KJSIT does not have an NRI quota for admissions.",
#         "autonomous": "Yes, KJSIT is an autonomous institute affiliated with the University of Mumbai and approved by AICTE.",
#         "accreditation": "KJSIT is accredited by NAAC with an 'A' grade. The Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology departments are accredited by NBA.",
#         "awards": "KJSIT was awarded 'Best College' in the urban region by Mumbai University in 2018-19 and has received multiple recognitions from professional bodies.",
#         "iic": "KJSIT’s Institution Innovation Council (IIC) has been recognized as a Top Performing IIC for four consecutive years: 2018-19, 2019-20, 2020-21, and 2021-22.",
#         "research": "KJSIT provides financial assistance for innovative student and faculty projects through its research funding programs.",
#         "robotics": "KJSIT actively participates in national-level robotics competitions like e-Yantra and ROBOCON, ranking among the top teams in India over the past five years."
#     }

#     default_responses = [
#         "Could you please provide more details about your query?",
#         "I'm here to help with admission information. What would you like to know?",
#         "Feel free to ask about eligibility, application process, or fee structure.",
#         "I didn't understand that. Can you try asking in a different way?"
#     ]

#     def get_response(query):
#         response = bot_responses.get(query, random.choice(default_responses))
#         return response

#     response = get_response(query)
#     return jsonify({"response": response})

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# here
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import random
import re

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

    # Enhanced keyword-to-response mapping with multiple keywords for each response
    bot_responses = {
        # Basic Information
        "established": [
            "KJSIT was established in the year 2001 by the Somaiya Trust at the Ayurvihar campus, Sion, to impart quality education in modern fields of Information Technology and Engineering."
        ],
        "popular_name": [
            "K. J. Somaiya Institute of Technology is popularly referred to as KJSIT by students, faculty, alumni, and staff."
        ],
        "location": [
            "KJSIT is situated near Sion railway station (Central Line) and Chunabhatti railway station (Harbour Line). The college is close to the Eastern Express Highway, making it easily accessible by road. Students coming by bus can get down at Everard Nagar Bus stop from where it is a 5 minutes' walk to reach KJSIT."
        ],
        "why kjsit": [
            "KJSIT is conferred with 'Fresh Autonomous Status' by UGC and is permanently affiliated with the University of Mumbai. It has received 'A' grade accreditation from NAAC and NBA accreditation for its Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology programs. The institute was awarded 'Best college' by Mumbai University in urban region in 2018-19. KJSIT extends over sprawling 5 acres of land and is located at the heart of Mumbai city, with state-of-the-art amenities and infrastructure for holistic student development."
        ],
        
        # Admissions Information
        "eligibility": [
            "The Candidate should be an Indian National; Passed HSC or its equivalent examination with Physics and Mathematics as compulsory subjects along with one of the Chemistry or Biotechnology or Biology or Technical or Vocational subjects and obtained at least 45% marks (at least 40% marks, in case of Backward class categories and Persons with Disability candidates belonging to Maharashtra State only) in the above subjects taken together and Obtained non-zero score in MHT-CET 2023 for Maharashtra State Candidates (or in JEE(Main) Paper I for AI Seats which are available only in CAP Rounds)."
        ],
        "apply": [
            "Candidates must register on the DTE Maharashtra website, fill out the application form, upload necessary documents, and select KJSIT as their preferred institute. After the CAP rounds, remaining vacant seats are filled at the Institute level by inviting applications on the portal."
        ],
        "admission_process": [
            "Admissions are conducted through the Centralized Admission Process (CAP) by the State CET Cell, Maharashtra. The process involves: 1) Appearing for MHT-CET, 2) Applying for CAP, 3) Document verification, 4) Merit list generation, 5) Seat allocation, 6) Admission confirmation by reporting to the institute. Vacant seats after CAP rounds are filled at the institute level by inviting applications."
        ],
        "documents": [
            "Documents required for admission include: 1) CAP Allotment letter, 2) Receipt-cum Acknowledgement from FC/ARC, 3) SSC (Std X) mark sheet, 4) HSC (Std XII) mark sheet, 5) MHT-CET Score Card, 6) School Leaving Certificate, 7) Certificate of Indian Nationality, 8) Migration Certificate (if applicable), 9) Gap affidavit (if required), and 10) True copy of Aadhar card."
        ],
        "minority_seat": [
            "51% of the total seats at KJSIT are reserved for candidates belonging to the Gujarati Linguistic Minority category. Documents required for minority seats include: a) School Leaving Certificate mentioning Gujarati Language as mother tongue OR Certificate issued by registered community regarding mother tongue of the candidate, b) Affidavit on stamp paper of Rs. 100/- in prescribed format, and c) Domicile Certificate of Maharashtra State (Compulsory)."
        ],
        "cutoff": [
            "For 2022-23, the CAP cutoffs based on MHT-CET were: Computer Engineering (95.60), Information Technology (94.87), Electronics & Telecommunication Engineering (89.52), and Artificial Intelligence & Data Science (94.07). Minority cutoffs were: Computer Engineering (88.49), Information Technology (86.20), Electronics & Telecommunication Engineering (17.43), and AI & Data Science (82.19)."
        ],
        "seats": [
            "Sanctioned intake: Computer Engineering (120 seats), Information Technology (60 seats), Electronics & Telecommunication Engineering (120 seats), and Artificial Intelligence & Data Science (60 seats). Each program also has TFWS and J&K seats. For M.Tech in Artificial Intelligence, there are 18 seats. PhD programs have 15 seats each for Computer Engineering and Information Technology, and 20 seats for Electronics & Telecommunication Engineering."
        ],
        "transfer": [
            "If a candidate is allotted a different branch in subsequent counseling rounds conducted by the institute, they must cancel their previous admission. The previously paid fees will be adjusted towards the new admission as per ARA guidelines. In transfer cases, the candidate will have to pay the cancellation charges as specified by ARA in the admission brochure."
        ],
        "cancellation": [
            "To cancel admission: 1) Apply online for cancellation, 2) Fill proforma O for Cancellation in duplicate, 3) Attach a copy of retention certificate and photocopies of receipts, 4) Submit the form in the Admission Cell, 5) Collect original documents. Fees will be refunded after deducting cancellation charges as per ARA rules."
        ],
        "nri_quota": [
            "No, KJSIT does not have an NRI quota for admissions."
        ],
        
        # Program Information
        "courses": [
            "KJSIT offers undergraduate B.Tech programs in Computer Engineering (120 seats), Information Technology (60 seats), Electronics & Telecommunication Engineering (120 seats), and Artificial Intelligence & Data Science (60 seats). The institute also offers an M.Tech program in Artificial Intelligence (18 seats) and Ph.D. programs in Computer Engineering, Information Technology, and Electronics & Telecommunication Engineering."
        ],
        "career_opportunities": [
            "Career opportunities vary by program. For Computer Engineering/IT: Software Engineer, Data Scientist, Web Developer, System Administrator, Cyber Security Analyst. For Electronics & Telecommunications: Network Engineer, Telecommunications Engineer, Hardware Engineer, System Designer. For AI & Data Science: AI Engineer, Data Architect, Machine Learning Engineer, Data Scientist. For M.Tech AI: Data Scientist, AI Architect, ML Engineer, Algorithm Specialist."
        ],
        
        # Financial Information
        "fee": [
            "The fees for B.Tech programs are determined by the Fees Regulating Authority, Government of Maharashtra. They vary based on category (Open, SC/ST, OBC, etc.) and admission type (CAP, DSE, etc.). Updated fee structure will be displayed after approval for the current academic year."
        ],
        "fee_concession": [
            "All types of fee concessions declared by the Government of Maharashtra are available for CAP-admitted students. However, candidates securing admission against vacant seats remaining after CAP rounds will not be eligible for fee concessions."
        ],
        "financial_aid": [
            "KJSIT offers 'Helping Hand – KJSIT': A Financial Aid Scheme for needy and meritorious students of EXTC branch. Additionally, the institute provides research funding to support innovative student projects."
        ],
        
        # Campus Life and Facilities
        "hostel": [
            "Hostel accommodation is available for outstation students on a first-come-first-serve basis at Somaiya Vidyavihar and Ayurvihar campuses. The hostels provide hygienic/nutritional food and recreation facilities. Bus facilities are provided for students staying in the Vidyavihar campus hostel. For hostel enquiry, contact Mrs. Kavita S. Kadam (kavita.sk@somaiya.edu)."
        ],
        "campus_activities": [
            "KJSIT offers various campus activities including: Innovative project development, Software Development Cell (SDC), Research Innovation Incubation and Design Lab (RiiDL), NPTEL certification courses, Professional body student chapters (IEEE, CSI, IETE, etc.), Training & Placement Cell, Annual festivals (RENAISSANCE, SURGE, SCORE), Student clubs (Robocon Cell, Programming Club, etc.), NSS, Industry-Institute Interaction, and Centers of Excellence in AI, ML & DL."
        ],
        "facilities": [
            "KJSIT provides state-of-the-art facilities including: Wi-Fi enabled campus, CC Camera Surveillance, Ample parking space, Spacious garden, Well-lit classrooms, Fire Fighting and Safety Devices, 24-hour internet with 150 Mbps bandwidth, Digital library, Open Gymnasium, Sports grounds, and Bus facility between campuses."
        ],
        
        # Achievements and Recognition
        "autonomous": [
            "Yes, KJSIT is an autonomous institute conferred with 'Fresh Autonomous Status' by University Grants Commissions (UGC) and permanently affiliated to University of Mumbai."
        ],
        "accreditation": [
            "KJSIT is accredited by NAAC with an 'A' grade. Three programs - Computer Engineering, Electronics & Telecommunication Engineering, and Information Technology - are accredited by the National Board of Accreditation (NBA)."
        ],
        "awards": [
            "KJSIT was awarded 'Best College' in the urban region by Mumbai University in 2018-19. It is placed in PLATINUM category by AICTE-CII consistently for years 2018, 2019 and 2020. KJSIT's Institution Innovation Council (IIC) has been recognized as a Top Performing IIC for four consecutive years."
        ],
        "atal_ranking": [
            "KJSIT is placed in the Rank Band 'B', indicating a Rank Between 26-50 among approximately 700 colleges for A.Y. 2020-21."
        ],
        "industry_linkage": [
            "KJSIT is placed in GOLD category by AICTE-CII for years 2016 and 2017 and in PLATINUM category consistently for the years 2018, 2019 and 2020."
        ],
        "iic": [
            "KJSIT runs the Institution's Innovation Council (IIC) under the Ministry of Education's Innovation Cell (MIC) and it has been recognized as the Top Performing IIC for four successive years 2018-19, 2019-20, 2020-21 and 2021-22."
        ],
        
        # Research and Innovation
        "research": [
            "KJSIT provides financial assistance for innovative student and faculty projects through its research funding programs. The institute sanctions research funds to every department, which is utilized for supporting innovative and research project development."
        ],
        "robotics": [
            "KJSIT actively participates in national-level robotics competitions. The ROBOCON team bagged 3rd, 5th, 8th, and 12th All India Ranks in Asia Pacific Broadcasting Union's National Robotic Contest in the last 5 years, competing with India's prestigious institutions including IITs & NITs. The team is ranked top in the Mumbai Region."
        ],
        "e_yantra": [
            "Yes, KJSIT participates in e-Yantra robotic activity coordinated by IIT Bombay. Faculty members from all departments prepare student teams for participating in this activity every year."
        ],
        
        # Placement Information
        "placement": [
            "KJSIT has an approximately 80% placement rate, with the highest CTC offered being ₹13.5 LPA. Companies visiting the campus include top IT firms and multinational corporations."
        ]
    }

    # Map common keywords and variations to main categories
    keyword_mapping = {
        # Basic Information
        "establishment": "established", "founded": "established", "start": "established", "beginning": "established", "history": "established",
        "nickname": "popular_name", "known as": "popular_name", "call": "popular_name", "referred": "popular_name",
        "reach": "location", "address": "location", "where": "location", "situated": "location", "find": "location", "direction": "location",
        "why choose": "why kjsit", "reason": "why kjsit", "advantage": "why kjsit", "benefit": "why kjsit", "special": "why kjsit",
        
        # Admissions
        "eligible": "eligibility", "qualification": "eligibility", "criteria": "eligibility", "requirement": "eligibility",
        "how to apply": "apply", "application": "apply", "registration": "apply", "how to register": "apply",
        "admission": "admission_process", "process": "admission_process", "procedure": "admission_process", "steps": "admission_process",
        "document": "documents", "paper": "documents", "certificate": "documents", "required document": "documents",
        "minority": "minority_seat", "gujarati": "minority_seat", "linguistic": "minority_seat", "51%": "minority_seat",
        "cut off": "cutoff", "cutoffs": "cutoff", "marks": "cutoff", "score": "cutoff", "percentile": "cutoff", "last rank": "cutoff",
        "seat": "seats", "capacity": "seats", "intake": "seats", "vacancy": "seats", "available seat": "seats",
        "branch change": "transfer", "change branch": "transfer", "switch": "transfer", "shift": "transfer",
        "cancel": "cancellation", "refund": "cancellation", "withdraw": "cancellation", "leave": "cancellation",
        "nri": "nri_quota", "foreign": "nri_quota", "overseas": "nri_quota", "abroad": "nri_quota",
        
        # Programs
        "program": "courses", "branch": "courses", "course": "courses", "stream": "courses", "degree": "courses", "specialization": "courses",
        "job": "career_opportunities", "career": "career_opportunities", "opportunity": "career_opportunities", "placement": "career_opportunities",
        
        # Financial
        "fees": "fee", "cost": "fee", "expense": "fee", "tuition": "fee", "payment": "fee", "charge": "fee",
        "concession": "fee_concession", "waiver": "fee_concession", "discount": "fee_concession", "scholarship": "fee_concession",
        "financial help": "financial_aid", "scholarship": "financial_aid", "aid": "financial_aid", "funding": "financial_aid",
        
        # Campus Life
        "hostel": "hostel", "accommodation": "hostel", "stay": "hostel", "residence": "hostel", "dormitory": "hostel",
        "activity": "campus_activities", "event": "campus_activities", "club": "campus_activities", "fest": "campus_activities",
        "facility": "facilities", "amenity": "facilities", "infrastructure": "facilities", "resource": "facilities",
        
        # Achievements
        "autonomous": "autonomous", "self governing": "autonomous", "independence": "autonomous",
        "accreditation": "accreditation", "accredited": "accreditation", "naac": "accreditation", "nba": "accreditation",
        "award": "awards", "recognition": "awards", "achievement": "awards", "honor": "awards", "rank": "awards",
        "atal": "atal_ranking", "aicte ranking": "atal_ranking", "moe ranking": "atal_ranking",
        "industry": "industry_linkage", "corporate": "industry_linkage", "company partnership": "industry_linkage",
        "iic": "iic", "innovation council": "iic", "institution innovation": "iic",
        
        # Research
        "research": "research", "funding": "research", "innovation": "research", "project": "research",
        "robotics": "robotics", "robocon": "robotics", "robot": "robotics", "competition": "robotics",
        "e-yantra": "e_yantra", "eyantra": "e_yantra", "iit bombay": "e_yantra",
        
        # Placement
        "place": "placement", "job": "placement", "recruit": "placement", "salary": "placement", "ctc": "placement", "company": "placement"
    }

    default_responses = [
        "Could you please provide more details about your query?",
        "I'm here to help with admission information. What would you like to know?",
        "Feel free to ask about eligibility, application process, or fee structure.",
        "I didn't understand that. Can you try asking in a different way?"
    ]

    def get_response(query):
        # Direct match first
        for key in bot_responses:
            if key == query:
                return random.choice(bot_responses[key])
        
        # Check for keywords in the query using mapping
        for keyword, mapped_key in keyword_mapping.items():
            if keyword in query:
                return random.choice(bot_responses[mapped_key])
        
        # Check for partial matches in the original keys
        for key in bot_responses:
            if key in query:
                return random.choice(bot_responses[key])
        
        # Otherwise return default
        return random.choice(default_responses)

    response = get_response(query)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
