\# Smart Job Tracker with AI Resume Matching



A full-stack job application tracking platform with NLP-based resume analysis and ATS matching.



The application allows users to securely manage job applications, upload resumes, compare resumes against job descriptions, identify skill gaps, monitor application analytics, and export application data.



\## Live Demo



\*\*Live Application:\*\*  

https://ai-resume-analyzer-2g4e.onrender.com/



> The application is hosted on Render's free tier, so the first request may take some time if the service has been inactive.



\---



\## Key Features



\### Authentication \& Security

\- User registration and login

\- JWT-based authentication

\- Secure password hashing

\- User-specific job data

\- Authorization checks for update and delete operations



\### Job Application Tracking

\- Add job applications

\- View saved applications

\- Update application status

\- Delete applications

\- Add job links and notes

\- Track application progress



\### Resume Analysis

\- Upload PDF resumes

\- Extract resume text

\- Extract technical skills using NLP

\- Compare resume skills with job-description skills

\- Identify matched and missing skills



\### ATS Match Scoring

The ATS matching engine combines:



\- TF-IDF vectorization

\- Cosine similarity

\- Explicit skill-overlap analysis



The final ATS score is calculated using:



```text

ATS Score =

(0.70 × Cosine Similarity)

\+

(0.30 × Skill Overlap)

```



The system also provides:



\- ATS match percentage

\- Matched skills

\- Missing skills

\- Resume improvement recommendations

\- Skill recommendations



\### Analytics Dashboard

\- Total job applications

\- Application-status statistics

\- Visual analytics using Chart.js

\- Job application progress tracking



\### CSV Export

Users can export their job-application data as a CSV file.



\---



\## Tech Stack



\### Backend

\- Python

\- Flask

\- Flask-SQLAlchemy

\- Flask-JWT-Extended

\- Flask-Migrate

\- Gunicorn



\### Database

\- PostgreSQL

\- SQLAlchemy ORM

\- Alembic database migrations



\### NLP / Machine Learning

\- spaCy

\- scikit-learn

\- TF-IDF Vectorizer

\- Cosine Similarity

\- Skill extraction



\### Frontend

\- HTML

\- CSS

\- JavaScript

\- Bootstrap

\- Chart.js



\### Testing

\- pytest

\- Flask test client



\### Deployment

\- Render

\- PostgreSQL on Render

\- Gunicorn



\---



\## System Architecture



```text

User

&#x20; |

&#x20; v

Frontend (HTML / CSS / JavaScript)

&#x20; |

&#x20; v

Flask Application

&#x20; |

&#x20; +----------------------+

&#x20; |                      |

&#x20; v                      v

JWT Authentication    Job Management

&#x20; |                      |

&#x20; |                      v

&#x20; |                   PostgreSQL

&#x20; |

&#x20; v

Resume Analysis

&#x20; |

&#x20; +--> PDF Text Extraction

&#x20; |

&#x20; +--> spaCy Skill Extraction

&#x20; |

&#x20; +--> TF-IDF Vectorization

&#x20; |

&#x20; +--> Cosine Similarity

&#x20; |

&#x20; +--> Skill Overlap

&#x20; |

&#x20; v

ATS Score + Skill Gap + Recommendations

```



Detailed architecture diagram:



!\[System Architecture](docs/architecture\_diagram.svg)



\---



\## Database Design



The application primarily uses three entities:



```text

Users

&#x20;  |

&#x20;  | 1 : N

&#x20;  v

Job Applications

&#x20;  |

&#x20;  | 1 : N

&#x20;  v

Resume Analyses

```



Detailed ER diagram:



!\[ER Diagram](docs/er\_diagram.svg)



\---



\## ATS Matching Workflow



```text

Resume PDF

&#x20;   |

&#x20;   v

Text Extraction

&#x20;   |

&#x20;   v

Resume Skill Extraction

&#x20;   |

&#x20;   +----------------------+

&#x20;                          |

Job Description            |

&#x20;   |                      |

&#x20;   v                      |

Skill Extraction           |

&#x20;   |                      |

&#x20;   +----------+-----------+

&#x20;              |

&#x20;              v

&#x20;      TF-IDF Vectorization

&#x20;              |

&#x20;              v

&#x20;       Cosine Similarity

&#x20;              |

&#x20;              +

&#x20;       Skill Overlap

&#x20;              |

&#x20;              v

&#x20;          ATS Score

&#x20;              |

&#x20;       +------+------+

&#x20;       |             |

&#x20;       v             v

&#x20;Matched Skills   Missing Skills

&#x20;                      |

&#x20;                      v

&#x20;               Recommendations

```



\---



\## Security



The application includes several security measures:



\- Passwords are stored using secure password hashing rather than plaintext.

\- Protected API routes require JWT authentication.

\- Job operations are scoped to the authenticated user.

\- Sensitive configuration is stored using environment variables.

\- `.env` files and uploaded resumes are excluded from version control.



\---



\## Automated Testing



The project contains automated tests covering authentication, job-management APIs, authorization, analytics, CSV export, and ATS/NLP logic.



Current test suite:



```text

33 tests passing

```



Example:



```bash

pytest -v

```



Tests cover scenarios including:



\- Registration

\- Duplicate users

\- Login

\- Invalid credentials

\- Password hashing

\- JWT-protected endpoints

\- Adding jobs

\- Updating jobs

\- Deleting jobs

\- User ownership isolation

\- Analytics

\- CSV export

\- Perfect resume/job matches

\- Partial matches

\- No-match scenarios

\- Empty input

\- Case-insensitive skill matching

\- Missing-skill detection

\- ATS recommendations



\---



\## Project Structure



```text

Smart\_Job\_Tracker\_with\_AI\_Resume\_Matching/

|

├── backend/

│   ├── database/

│   ├── models/

│   ├── routes/

│   └── utils/

|

├── nlp/

│   ├── matcher.py

│   ├── parser.py

│   └── skills.csv

|

├── migrations/

│   └── versions/

|

├── static/

│   ├── css/

│   └── js/

|

├── templates/

|

├── tests/

|

├── docs/

│   ├── architecture\_diagram.svg

│   └── er\_diagram.svg

|

├── app.py

├── config.py

├── Procfile

├── pytest.ini

├── requirements.txt

└── requirements-dev.txt

```



\---



\## Local Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Ankit-tech175/Smart\_Job\_Tracker\_with\_AI\_Resume\_Matching.git

cd Smart\_Job\_Tracker\_with\_AI\_Resume\_Matching

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the environment



Windows:



```bash

venv\\Scripts\\activate

```



Linux/macOS:



```bash

source venv/bin/activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\### 5. Install the spaCy English model



```bash

python -m spacy download en\_core\_web\_sm

```



\### 6. Configure environment variables



Create a `.env` file with the required configuration, including:



```text

DATABASE\_URL

SECRET\_KEY

JWT\_SECRET\_KEY

```



Do not commit `.env` to Git.



\### 7. Apply database migrations



```bash

flask db upgrade

```



\### 8. Run the application



```bash

python app.py

```



\---



\## Deployment



The production application is deployed using:



```text

GitHub

&#x20;  |

&#x20;  v

Render Web Service

&#x20;  |

&#x20;  +--> Gunicorn

&#x20;  |

&#x20;  +--> Flask Application

&#x20;  |

&#x20;  +--> PostgreSQL

```



Production dependencies and the spaCy language model are installed during the Render build process.



Database schema changes are managed through Flask-Migrate/Alembic migrations.



\---



\## Limitations



The current ATS system is primarily based on textual similarity and explicit skill matching.



Current limitations include:



\- It does not reproduce the proprietary scoring algorithms used by commercial ATS platforms.

\- TF-IDF does not capture deep contextual meaning as effectively as transformer-based embeddings.

\- Resume parsing currently focuses on PDF input.

\- Skill extraction depends partly on the available skill vocabulary.

\- Resume formatting quality is not deeply evaluated.

\- The application is currently designed primarily as a single-service academic/portfolio project.



\---



\## Future Scope



Potential improvements include:



\- Transformer/Sentence-BERT based semantic matching

\- DOCX resume support

\- More advanced resume section extraction

\- Job-description keyword weighting

\- Resume formatting analysis

\- Email/application reminders

\- Interview scheduling

\- Improved recommendation ranking

\- Cloud object storage for uploaded files

\- CI/CD automation

\- Docker containerization

\- Expanded integration and end-to-end testing



\---



\## What I Learned



This project provided practical experience with:



\- REST API development

\- Flask application architecture

\- JWT authentication

\- Authorization and user-data isolation

\- PostgreSQL

\- SQLAlchemy ORM

\- Database migrations

\- NLP preprocessing

\- TF-IDF

\- Cosine similarity

\- Skill-gap analysis

\- Automated testing

\- Production deployment

\- Environment-variable management



\---



\## Disclaimer



This project implements an NLP-based resume/job matching system for educational and portfolio purposes. The generated ATS score should not be interpreted as the score produced by any specific commercial Applicant Tracking System.



\---



\## Author



\*\*Ankit Chauhan\*\*



B.Tech — Computer Science \& Engineering  

Specialization: Artificial Intelligence \& Machine Learning

