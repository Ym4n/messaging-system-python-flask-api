# messaging-system-python-flask-api

rest API backend system that responsible of handling messages between users and group of users.
using Flask , sqlalchemy , postgresql.

<b>features :</b>
<br />
1. Authentication by flask-login - user can read/delete only related message. <br />
2. many-to-many - user can send message to group or single user.
3. join/add/leave groups

DB models inspired from :
<br/>
https://vertabelo.com/blog/database-model-for-a-messaging-system/


app at heroku ,quick exmple :
https://messaging-system-flask-api.herokuapp.com/

API function | Method | URL | notes 
--- | --- | --- | --- 
add user | POST | /signup | json with username and password |
login | POST | /login | json with username and password |
add_group | POST | /add_group | json with name |
join_group | POST | /join_group/<string:group name> |  |
leave_group | POST | /leave_group/<string:group name> |  |
my_groups | GET | /my_groups |  |
--- | --- | --- | --- 
write new message | POST | /api/send_msg | json with message |
get sent messages | GET | /api/sent | A short version message |
get inbox messages | GET | api/inbox | A short version message |
get unread messages | GET | /api/unread | A short version message |
Read one msg from inbox | GET | /api/inbox/read/{{msg_id}} | msg_id= the id of specific msg , full version message |
Read one msg from sent | GET | /api/sent/read/{{msg_id}}   | msg_id= the id of specific msg , full version message |
delete sent msg | DELETE | /api/delet_sent_msg/{{msg_id}} | msg_id= the id of specific msg |
delete inbox msg | DELETE | /api/delet_inbox_msg/{{msg_id}} | msg_id= the id of specific msg |

