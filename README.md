Too Easy Travel bot @Teasy_travel_bot helps to find information and photos from many hotels around the world.
To get project started you need to clone the repository and to install the necessary libraries.

The project consists of a main.py script and a Telegram bot @Teasy_travel_bot. 

The user, using special bot commands, can perform the following actions (get the following information):
1. Find out the top cheapest hotels in the city (command /lowprice).
2. Find out the top most expensive hotels in the city (command /highprice).
3. Find out the top hotels that are most suitable for price and location from the center
(the cheapest and closest to the center) (command /bestdeal).
4. Find out the history of hotels search (command /history).

/lowprice command

After entering the command, the user is asked for:
1. The city where the search will be carried out.
2. The number of hotels to be displayed as a result (no more than the maximum).
3. The need to upload and display photos for each hotel (“Yes / No”):
   - If the answer is yes, the user also enters the number of required photos (no more than the maximum).

/highprice command

After entering the command, the user is asked for:
1. The city where the search will be carried out.
2. The number of hotels to be displayed as a result (no more than the maximum).
3. The need to upload and display photos for each hotel (“Yes / No”):
   - If the answer is yes, the user also enters the number of required photos (no more than the maximum).

/bestdeal command

After entering the command, the user is asked for:
1. The city where the search will be carried out.
2. The price range.
3. The range of the distance at which the hotel is located from the center.
4. The number of hotels to be displayed as a result (no more than the maximum).
5. The need to upload and display photos for each hotel (“Yes / No”):
   - If the answer is yes, the user also enters the number of required photos (no more than the maximum).

/history command

After entering the command, the user get 10 last requests and its results:
1. command used
2. date and time
3. found hotels

The project was developed with Python.
