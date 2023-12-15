Create an EC2 instance in AWS <br>
Connect to EC2 instance using SSH & copy the correpsonding files - requirements.txt & streamlit_app.py <br>
*You can utilize Putty to connect to ec2 instance & winscp to copy the files of leverage visual studio terminal to connect & copy files* <br>
Run the below commands step by step <br>
<ol>
            <li>### Create Virtual Environment <br> python3 -m venv myenv</li>
            <li>### Activate Virtual Environment <br> source myenv/bin/activate</li>
            <li>### Activate Virtual Environment <br> source myenv/bin/activate</li>
            <li>#Run App using <br> streamlit run streamlit_app.py item</li>
</ol> <br>
Once you see the below <br>
![image](https://github.com/palbha/table_transformer/assets/20269788/ce15d35b-d206-4ab1-ac67-17618f749882)

<br>You should update the Security group inbound rules to add port 8501 <br>
![image 2](https://github.com/palbha/table_transformer/assets/20269788/7d23148d-a92d-4ee4-bd07-111d4936e858)

Once done you can click on the link and your app will be up and running . <br>
*PS: Make sure your url is http not https otherwise you will still get "Site can't be reached" or similar error*

