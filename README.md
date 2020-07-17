# Fellowship Class Profile <img src="https://github.com/chrisngyn/fellowship-class-profile/blob/master/readme_imgs/Hi.gif" width="40px">

<p align="center"><img src="https://github.com/chrisngyn/fellowship-class-profile/blob/master/readme_imgs/ss1.png" width="80%"></p>

## Motivation
[View our project here!](https://fellowship-class-profile.herokuapp.com/)  
  
Seeing your *progress overtime* is vital to developers as we can see how much we have learned and grown across a given timespan. It can be hard to remember everything you worked on and who you worked with off the top of your head, therefore the **Fellowship Class Profile** is a web application that aggregates your [GitHub data](https://docs.github.com/en/graphql) from the last 12 weeks and turns it into statistics and visualiations to conclude the MLH Fellowship, with the goal of showcasing your work and accolades.  

<p align="center"><img src="https://github.com/chrisngyn/fellowship-class-profile/blob/master/readme_imgs/ss2.png" width="40%"> <img src="https://github.com/chrisngyn/fellowship-class-profile/blob/master/readme_imgs/ss3.png" width="40%"></p>

## Setup:
Docker takes care of the setup for you! `docker-compose` will provision the database and start the web application.
1. Install Docker Desktop: https://www.docker.com/get-started

2. Setup a `.env.dev` file with the required environment variables. 

        FLASK_APP=web:app
        DATABASE_URL=postgresql://coderman:codermanpassword123@postgres:5432/fellowship-class-profile
        GITHUB_CLIENT_ID=fc7c0f9b52387b87d52d
        GITHUB_CLIENT_SECRET=REPLACE_ME
        GITHUB_API_TOKEN=REPLACE_ME_WITH_YOUR_TOKEN
        
3. Use `docker-compose`: 

       $ docker-compose up --build

4. Create the database. Execute the `manage.py` script in the container. 

       $ docker-compose exec web python -m web.manage create_db
        
5. Visit [localhost:8000](localhost:8000) to see the application.
