from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel, EmailStr
import json
import mysql.connector
import uvicorn
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key=os.environ['OPENAI_API_KEY']

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Apollo200114!",
    database="shop_item"
)
mycursor=mydb.cursor()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/login')
async def login(req : Request):
    new_user_data = await req.json()
    new_name, new_password = new_user_data['name'],  new_user_data['password']
    query = f"SELECT password FROM create_table where name=%s"
    user_field = (new_name,)
    mycursor.execute(query, user_field)
    password = mycursor.fetchall()
    
    if password:
        password = password[0]
        if new_password in password :
            return {"message":"Success"}
        else:
            return {"message":"incorrect password"}
    else: return {"message":"Please register first!"}
   
    
@app.post('/signup')
async def signup(req : Request):
    new_user_data =await req.json()
    new_name, new_password = new_user_data['name'],  new_user_data['password']
    query = f"SELECT name FROM create_table where name=%s"
    user_field = (new_name, )
    # print(query, user_field, new_name, new_password)
    mycursor.execute(query, user_field)
    name=mycursor.fetchall()
    if name: return {"message":"Envailed user name!!"}
    else:
        query = "SELECT name FROM create_table"
        mycursor.execute(query)
        # Fetch all rows
        result = mycursor.fetchall()
        new_user_id=len(result)+1
        # print(new_user_id)
        val=(new_user_id, new_name, new_password)
        sql="INSERT INTO create_table (user_id, name, password) VALUES (%s, %s, %s)"
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted")
        return {"message":"Success"}
    
itemdb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Apollo200114!",
    database="item_price",
)
cursor=itemdb.cursor()

@app.post('/view')
async def initprice(req: Request):
    new_data = await req.json()
    new_item_name=new_data['item_name']
    if new_item_name:
        query = f"SELECT item_price FROM prices where item_name=%s"
        item_field = (new_item_name, )
        cursor.execute(query, item_field)
        price=cursor.fetchall()
        if price:
            price=price[0]
            return {"Price":price}
        else: return {"Price":"No value"}

@app.post('/about')
async def upgrade_items(req:Request):
    new_item_data= await req.json()
    new_item_url=new_item_data["url"]
    new_item_name= new_item_data['item_name']
    new_item_price= new_item_data['price']
    
    query = "SELECT item_name FROM prices"
    cursor.execute(query)
    # Fetch all rows
    result = cursor.fetchall()
    new_item_id=len(result)+1
    val=(new_item_id, new_item_url,new_item_name, new_item_price)
    sql="INSERT INTO prices (item_id, item_url,item_name, item_price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, val)
    # Fetch all rows
    itemdb.commit()
    return {"message":"Updated"}
    

@app.post("/chatroom")
async def get_model_reply(req:Request):
    # combines the new question with a previous context
    data =await req.json()
    # print(data)
    query = data ['chatText']
    context = data ['context']
    print(context)
    context += [query]
    prompt_string='\n\n'.join(context)
    prompt=prompt_string[max(-len(prompt_string), -4096):]
    # print(prompt)
    # given the most recent context (4096 characters)
    # continue the text up to 2048 tokens ~ 8192 charaters
    completion = openai.Completion.create(
        engine='text-davinci-002',
        prompt=prompt,
        max_tokens = 2048,
        temperature = 0.5, # Lower values make responses more deterministic
    )

    # append response to context
    # print(completion)
    response = str(completion['choices'][0]['text'])
    context += [response]

    # list of (user, bot) responses. We will use this format later
    responses = [(u,b) for u,b in zip(context[::2], context[1::2])]
    # print(responses)

    return {"responses": responses, "context":context}

@app.post("/fileupload")
async def get_file(file:Annotated[bytes, File()]):
    # data = req.json()
    return {"file_size":len(file)}


if __name__=="__main__":
    uvicorn.run("main:app", port=8000, reload=True)