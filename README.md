# jarbas

Jarbas, à seu dispor

__pt_BR__ projeto criado para estudo e depois disponibilizado para as squads 720-II e 720-I

## disclaimer

__pt_BR__ sinta-se livre para usar esse repo como base para o seu proprio bot (handler.py é a classe principal)  
__en_US__ feel free to use this repo as a start point to create your own telegram bot (handler.py is the "main" class)

## setup

this bot needs AWS lambda and api-gateway to work. Serverless framework uses Node.js and needs AWS Cloudformation and S3 to upload the code and deploy it. 
If you don't want to use Serverless, you can deploy a .zip to lambda and configure the api-gateway yourself

you will need:

   * create a telegram bot with [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot) 
   
   * clone this repository (du'h)
 
   * create a virtual env:
   ```console
    $ cd my_project_folder
    $ virtualenv venv
   ```  
   * install dependencies:  
  ```console
    $ pip install -r requirements.txt -t vendored
   ```  
   * download [Node.js](https://nodejs.org/en/) and install Serverless:  
  ```console
    $ npm install -g serverless
   ```  
   * setup some environment vars to deploy the bot:
      * export AWS_ACCESS_KEY_ID=<__your_aws_access_key__>   
      * export AWS_SECRET_ACCESS_KEY=<__your_aws_secret_access_key__>  
      
   * update your serverless.yml with your function name and environment variables (telegram token from botfather, database string connection, and everything your bot will need)
   
   * deploy the code: 
   ```console
    $ serverless deploy
   ```  
   
   * setup a webhook
   ```console
    $ curl https://api.telegram.org/bot<my_bot_token>/setWebhook?url=<api-gateway_url>
   ```  
   
   * test yout bot with /start command 
   
   ## jarbas was build with
   
   * [python 3.7.2](https://www.python.org/)
   * [mongoDB](https://www.mongodb.com/) and [Atlas](https://cloud.mongodb.com)
   * [AWS lambda and api-gateway](https://aws.amazon.com)
   * [serverless framework](https://serverless.com/)
