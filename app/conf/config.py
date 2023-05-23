class Config:
    # User API endpoint
    SIGN_IN = '/api/v1/sign_in'
    SIGN_UP = '/api/v1/sign_up'
    USER_PROFILE = '/api/v1/profile/<string:username>'
    DELETE_ACCOUNT = '/api/v1/delete_account/<string:username>'

    # Movies API endpoint
    FETCH_MOVIES = '/api/v1/fetch_movies/<string:username>'
    ADD_MOVIE = '/api/v1/add_movie/<string:username>'
    DELETE_MOVIE = '/api/v1/delete_movie/<string:title>/<string:username>'

    # Others
    JWT_SECRET_KEY = "admin"
    REGION_NAME = "us-west-2"
    APP_PORT = 8000
