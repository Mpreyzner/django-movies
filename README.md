# Movies app


## API requirements

## movies API
##### GET /movies: 
Should return all the movies. 
Can include additional filtering, sorting.
##### ​POST /movies:
Request body should only contain movie title which will be validated.
Given movie title movie info that will be fetched from some API should be saved in DB.
Should return full movie object.


## comments API
##### GET /comments: 
Should return all the comments present in DB.
Allows for filtering by movie id.
##### POST /comments:
Request should contain movie id and given it should be validated for presence in DB and comment body.
Comment should be save.
Should return whole comment in response.    
     
## top API
##### GET /top: 
Should return movie ranking for given time range (required).
Movie ranking should be based on number of comments for given time period.
Movies with the same number of comments should have the same position in ranking.
Should return: movie id, rank position and total number of comments (for specified date range).
