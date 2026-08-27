
-------------------get_list
curl -X 'GET' \
  'http://127.0.0.1:8000/todos' \
  -H 'accept: application/json'


-------------------Create
curl -X 'POST' \
  'http://127.0.0.1:8000/todos' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Title": "Lam bai tap ve nha",
  "Description": "hoan thanh truoc khi len lop",
  "Priority": 5,
  "Completed": false
}'
---------------------Update
curl -X 'PUT' \
  'http://127.0.0.1:8000/todos/5' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Title": "Nau an",
  "Description": "Nau phai an duoc"
  "Priority": 3,
  "Completed": true
}'

----------------Get_detail 
curl -X 'GET' \
  'http://127.0.0.1:8000/todos/4' \
  -H 'accept: application/json'

----------------Delete 

curl -X 'DELETE' \
  'http://127.0.0.1:8000/todos/3' \
  -H 'accept: application/json'
