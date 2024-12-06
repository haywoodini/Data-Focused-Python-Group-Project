# Data-Focused-Python-Group-Project

Download and Open Instructions

**Preprocess(Important):
Make sure you have downloaded following packages:
os
numpy
pandas
streamlit
selenium
praw
textblob
re
openpyxl
If not, open the terminal and !pip install[package name] first!!**

**Demostration Video Link: 
https://www.youtube.com/watch?v=2d-EXlcowng**

**Github Repository: 
https://github.com/haywoodini/Data-Focused-Python-Group-Project**


1. Firstly Download our zip file and load to a repository that you want, which we name here **'download_repository'**

2. Our product uses 3 datasources for petfood recommendation, providing the customized petfood suggestions from the main shopping websites.
   a. the Amazon top 6 pages shopping data (web scraped)
   b. the Reddit sentimental comments of main Manufactuers (web scraped)
   c. the Manufactuer sales rank data (download from api)

3. To streamline the process, we have already got the raw data and cleaned data processed by our pipelines in the file.
   But if you want to check the validity of our scrape code, you can still run it, but it is gonna take a while.
   The web scraping files are listed below:
   
   ----- Do not Recommend to Run -----
   Web_Crwaler_Amazon_Data.py
   Web_Crwaler_Reddit_Data.py

4. To preprocess of data, we build the pipeline files to transform the data format into our desired formats.
   We also covered our pipeline files here, but still we have cleaned the data for you. If you want to run it that can also be done.

   ----- Do not Recommend to Run -----
   Data_Pipeline_Amazon.py
   Data_Pipeline_Reddit.py

5. After the preparations are done, we have our ui file as the final product output, in the file folder named as prototype_ui.py
   It is also been encapsulated into our main_launcher file.

   ----- Do not Recommend to Run -----
   prototype_ui.py

**6. To open our product, you can access to our main_launcher file, to execute the main product
     a. Lauch the main_launcher.py file in an IDE environment, using Pycharm as an example![82122af0cfc53092b0e1e6e3865a90d](https://github.com/user-attachments/assets/39802205-c86c-4387-b7d6-a3d4be3301ab)
     b. You will be directed to our product page opening in your default web browser![image](https://github.com/user-attachments/assets/3622fc34-5278-430f-ba65-2927ba0bcb91)
     c. The ide enviroment will show your connection ip and status![image](https://github.com/user-attachments/assets/b795834c-a271-4eac-8c87-d8c45bd3f448)**

  **An alternative way to open the product if failed:
    (Make sure you have downloaded the streamlit package locally)
    a. Open your local terminal, change your directory to the file download repository here 'download_repository'![image](https://github.com/user-attachments/assets/cc0e8237-bfaf-4e2f-a28f-0a351cbf5102), press enter
    b. Write stramlit run prototype.ui to run our main file(prototype_ui.py) ![image](https://github.com/user-attachments/assets/f5416449-20b6-4016-96f9-575276477136) press enter
    c. You will be directed to our product page opeining in your default web browser ![image](https://github.com/user-attachments/assets/dbfdc795-46e5-4602-88e4-7bef7e74178e)
    d. The terminal enviroment will show your connection ip and status![image](https://github.com/user-attachments/assets/5f50bd0a-e8e3-43e5-878e-13b66eb5611e)**

   
