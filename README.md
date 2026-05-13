# Installatie + Setup
Volg de onderstaande stappen om de applicatie lokaal te runnen.
1. **Clone de repository:**\
``git clone https://github.com/Rac-Software-Development/wp3-2026-rest-1b6-fox.git``
2.  **Maak een Virtual Environment:**\
``python -m venv .venv``
3. **Activate Virtual Environment:**
- Windows:
``.venv\Scripts\activate``
- macOS/Linux:
``. .venv/bin/activate``
4. **Installeer de requirements.txt:**\
``pip install -r requirements.txt``
5. **Start de applicatie:**\
``python app.py``

# Inloggegevens
### Docent - Dummyaccount
- Email: ``docent@test.nl``
- Password: ``docent123``

### Student - Dummyaccount
- Email: ``student@test.nl``
- Password: ``student123``

# ERD

![img_5.png](img_5.png)

# Screenshots

### Startscherm:

![img_2.png](img_2.png)

### Inlogscherm:

![img.png](img.png)

### Dashboard docent:

![img_1.png](img_1.png)

### Dashboard student:

![img_3.png](img_3.png)

### Resultaten:

![img_4.png](img_4.png)

# **APA bronnen**

Ilias bronnen:
- Programming with Mosh. (2018, April 24). JavaScript Course for Beginners – Your First Step to Web Development [Video]. YouTube. https://www.youtube.com/watch?v=W6NZfCO5SIk
- Programming with Mosh. (2018a, March 30). Object-oriented programming in JavaScript: Made super simple | Mosh [Video]. YouTube. https://www.youtube.com/watch?v=PFmuCDHHpwk
- Lucid Software. (2017, March 6). Entity Relationship Diagram (ERD) Tutorial - Part 1 [Video]. YouTube. https://www.youtube.com/watch?v=QpdhBUYk7Kk
- GeeksforGeeks. (2025, July 23). How to Link JavaScript File to a Separate HTML File? GeeksforGeeks. https://www.geeksforgeeks.org/html/how-to-link-javascript-file-to-a-separate-html-file/
- API — Flask Documentation (3.2.x). (n.d.). https://flask.palletsprojects.com/en/latest/api/#flask.json.jsonify
- W3Schools.com. (n.d.). https://www.w3schools.com/sql/sql_like.asp
- : The HTML Input element - HTML | MDN. (2026, February 13). https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input
- W3Schools.com. (n.d.-b). https://www.w3schools.com/html/html_forms.asp
- W3Schools.com. (n.d.-c). https://www.w3schools.com/html/html_form_input_types.asp
- Buvesa. (2020, June 8). HTML TUTORIAL VOOR BEGINNERS | 👉 Gratis HTML cursus om websites te maken (Nederlands) [Video]. YouTube. https://www.youtube.com/watch?v=gMBUxCgcz1g
- LinkedIn Learning. (2013, January 31). JavaScript Tutorial - What is AJAX? [Video]. YouTube. https://www.youtube.com/watch?v=RDo3hBL1rfA
- LearnWebCode. (2016, October 27). JSON and AJAX tutorial: with real examples [Video]. YouTube. https://www.youtube.com/watch?v=rJesac0_Ftw
- Learning Software. (2025, February 4). Secure and simple role based authorization in python Flask apps with Keycloak [Video]. YouTube. https://www.youtube.com/watch?v=AKTmvERQu20
- Dias, P. (2019, May 16). How do I implement a role Based Permission system on a webpage? Stack Overflow. https://stackoverflow.com/questions/56175371/how-do-i-implement-a-role-based-permission-system-on-a-webpage

Karina bronnen:

- Chart.js. (n.d.). Chart.js – Documentatie. https://www.chartjs.org/docs/latest/
- Bootstrap. (2023). Bootstrap 5.3 – Documentatie. https://getbootstrap.com/docs/5.3/
- Mozilla Developer Network. (n.d.). Fetch API – MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- Mozilla Developer Network. (n.d.). MDN Web Docs (algemeen). https://developer.mozilla.org/
- Nagix. (n.d.). Chart.js Realtime plugin (voor live/scrollende grafieken). https://nagix.github.io/chartjs-plugin-streaming/
- Flask Documentation. (n.d.). Flask – Documentatie. https://flask.palletsprojects.com/
- SQLite. (n.d.). SQLite – Officiële documentatie. https://www.sqlite.org/docs.html
- SQLite. (n.d.). SQLite SQL syntax (SELECT, queries). https://www.sqlite.org/lang.html
- Python Software Foundation. (2024). Python sqlite3 module – DB-API 2.0 interface voor SQLite. https://docs.python.org/3/library/sqlite3.html
- W3Schools.com. (n.d.). W3Schools SQL Tutorial. https://www.w3schools.com/sql/
- JSON.org. (n.d.). JSON – Introductie en structuur. https://www.json.org/json-en.html
- Chart.js. (n.d.). Chart.js Samples (dynamische grafieken). https://www.chartjs.org/docs/latest/samples/
- Mozilla Developer Network. (n.d.). Async JavaScript / Promises / async-await. https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises
- Mozilla Developer Network. (n.d.). Foutafhandeling bij fetch (try/catch voorbeeld). https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#handling_errors


# **AI verantwoording**

Hoe moet ik per leerling zwakke en sterke kernwoord laten zien op het student dashboard (stap voor stap)  
Karina Vargas Flores
0984396
Conversatie: https://chatgpt.com/share/6a04cedf-9fac-8327-b99f-138d1581bcc0
Oplossing: Je moet per kernwoord laten zien of een leerling sterk of zwak is. Dat betekent dat je:
1. Data uit de database ophalen 
2. Scores per kernwoord berekenen.
3. Sterk/zwak bepalen 
4. Naar de template sturen 
5. Visueel tonen in HTML 
Ik heb dit verwerkt in de : app.py en student-dashboard.html
Code regel: app.py 47 t/m 112 en queries in database.py
en html: 6 t/m 38 
student.py: 42 t/m 59
Context: Ik vond het moeilijk om zo uit het niks te beginnen ook vanuit de database, dus ik heb aan Chatgpt gevraagd hoe ik dit stap voor stap moet doen met commits zodat ik hier ook van leer uiteraard.
Git bestand: Rac-Software-Development/wp3-2026-rest-1b6-fox: rac-software-development-2025-2026-wp3-2026-rest-wp3-2026-starter created by GitHub Classroom


Hoe verwerk ik per leerdoel of ik zwak of sterk sta als leerling ? 
Karina Vargas Flores
0984396
Conversatie: https://chatgpt.com/share/6a04d53e-5918-8331-a91b-53c0e4cd4b73
Oplossing:  PER STAP 
Een score per leerdoel berekenen 
Die score visueel duidelijk maken (sterk / gemiddeld / zwak) 
Het begrijpelijk tonen op het dashboard
Ik heb dit verwerkt in de : app.py en html
Code regel: app.py 47 t/m 112 
en html: 55 t/m 71
student.py 1 t/m 40
Context: Ik vond het moeilijk om zo uit het niks te beginnen netzoals met de kernwoorden dus heb ik gevraagd hoe dit moet, het gesprek is lang. Maar het word stap voor stap uitlegd hoe het moet
Git bestand: Rac-Software-Development/wp3-2026-rest-1b6-fox: rac-software-development-2025-2026-wp3-2026-rest-wp3-2026-starter created by GitHub Classroom


Hoe moet ik de database maken ? STAPGEWIJS
Karina Vargas Flores
0984396
Conversatie: https://chatgpt.com/share/6a04d95f-5918-8331-b7ff-a2ad607e60c1
Oplossing:  PER STAP  Wat ik nu zou doen (concreet todo)
Voor jouw situatie, in volgorde:
1.	database.py maken 
2.	 Models schrijven voor alle tabellen 
3.	create_all() draaien 
4.	1 leerling + 1 vak + 1 leerdoel testen 
5.	pas daarna JSON import
Ik heb dit verwerkt in de : database.py
Code regel:  294 t/m 474
Context:  Zoals ook in de conversatie verteld moest ik als eerst een database maken maar dit is allemaal nieuw en moeilijk dus ik heb het zo op de manier gevraagd dat ik er van leer.
Git bestand: Rac-Software-Development/wp3-2026-rest-1b6-fox: rac-software-development-2025-2026-wp3-2026-rest-wp3-2026-starter created by GitHub Classroom


Hoe maak ik een grafiek over tijd in pycharm met AJAX?
Karina Vargas Flores
0984396
Conversatie: https://chatgpt.com/share/6a04dc71-24e8-8330-aee1-749974005877
Oplossing: Laten we dit stapsgewijs aanpakken. Ik geef een voorbeeld met Flask, Chart.js en AJAX.
Ik heb dit verwerkt in de : student-dashboard.html 
Code regel: 87 t/m 131
Context: Vorige conversatie kwijt maar ik had het in deze conversatie geplakt dat is dus de eerste vraag, en daarna hoe ik er ajax in verwerk.
Git bestand: Rac-Software-Development/wp3-2026-rest-1b6-fox: rac-software-development-2025-2026-wp3-2026-rest-wp3-2026-starter created by GitHub Classroom




