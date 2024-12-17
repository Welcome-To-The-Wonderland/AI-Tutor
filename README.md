
# AI-Tutor

This is an AI based tutoring system developed to teach individuals how various PC components work and interact with one another.

TODO: add "optimizations" , "Lessons learned" , Updated images

## Explanation

Tech Info:
Python 3
    pillow image processing
    Django REST Framework
    JSON web Token (JWT) Authentication
    pyBKT
React/NextJS

Core Features:

  Question Types:
    - Multiple Choice
    - True/False
    - Short answer
    - Label Images

  Enrichment modules:
    - Uses Bayesian knowledge tracing and data based on the amount of assistance and attempts per question
    - User-specific questions generated based on individual knowledge lapses and weaknesses
  
  AI-based Feedback:
    - Created a chain of thought process to provide contextually relevant and quality responses
    - Image processing of questions enabled for Image based questions to provide scalability


Research backed methods implemented:
- Bayesian Knowledge Tracing
- Dual coding theory
  - "Mental Representations: A dual coding approach" Allen Paivio 
- Constructivist theories of learning
"Evaluating Constructivistic Learning" David H. Jonassen
  

## Demo

#### Main

![demo-1](https://res.cloudinary.com/dotera808/image/upload/v1724405550/Demo-1_tbvd6a.gif)

#### Admin

![demo-2](https://res.cloudinary.com/dotera808/image/upload/v1724405550/Demo-2_keiyxj.gif)

#### Application

![demo-3](https://github.com/user-attachments/assets/7d5450e0-933c-4861-8327-31b64bf232ce)

## Setup

Clone the repo


```

$ git clone https://github.com/kalvincalimag/django-nextjs-jwt-starter.git

```


### Setup Backend (Django)
  

First, create a `.env` file in the root of the backend folder & add your Django secret key:

```

DJ_SECRET_KEY=<your_django_secret_key_here>

```

For generating a key, refer [here](https://www.makeuseof.com/django-secret-key-generate-new/).
  

Enter Directory

```

cd backend

```

  

Install dependencies:

```

pip install -r requirements.txt

```

  

Set up the database:

```

python manage.py makemigrations

python manage.py migrate

```

  

Run server:

```

python manage.py runserver

```

  

### Setup Frontend (NextJS)

  

Enter directory through terminal

  

```

$ cd frontend

```


Install dependencies with 

pnpm install

or 

npm install


```

npm install

```

  

Run the app

  

```

npm run dev

```

  



## License and Credits

[BSD](LICENSE.md) @kalvincalimag

co-contributors for AI-Tutor:
https://github.com/mhoualla
https://github.com/LuffyAI

