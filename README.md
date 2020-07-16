# Fellowship Class Profile
Web application that aggregates your GitHub data for the last 12 weeks into pretty statistics to conclude the MLH Fellowship.


## Development Setup:
Docker takes care of the setup for you! `docker-compose` will provision the database and start the web app.
1. Install Docker Desktop https://www.docker.com/get-started

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
        
5. Visit [localhost:8000](localhost:8000) to see the app.
