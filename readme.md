Steps to Deploy the Django Project on Ngrok for Testing
1. Start the Local Server
Run the following command to start the Django development server:


python manage.py runserver
2. Start Ngrok
Open a new command prompt or terminal window and run:

ngrok http 8000
3. Get the Ngrok URL
After running the above command, Ngrok will generate a URL similar to:


Forwarding: https://4be8-2401-4900-3b03-2918-3153-cb84-a4db-7769.ngrok-free.app -> http://localhost:8000
4. Access the Live Server
The generated Ngrok URL (e.g., https://4be8-2401-4900-3b03-2918-3153-cb84-a4db-7769.ngrok-free.app) will act as the public-facing URL for your Django application.

5. Use the Ngrok Link for Testing
Copy and paste the Ngrok URL into your browser.
Test your application as if it were deployed online.
6. Ensure the Local Server is Running
If the local Django server (python manage.py runserver) is not running, Ngrok will not work.
Always ensure the local server is active before using the Ngrok link.
Important Notes:
Every time you restart Ngrok, a new URL will be generated for the free tier
