# IOT Assignment 2

## Scenario
Your team has been contacted by a medical office in Melbourne to advise them on an office automation project to automate the medical appointments process known as **MAPS** _(medical appointment system)_, usually handled by medical receptionists.

<br>

You have been tasked create a website for three types of users: patients, doctors and medical clerks and a series of inter-connected IoT devices in the doctor's office and the front desk. (Please make use of Flask, Jinja2 templating and Bootstrap to build your web interface).

<br>

For this assignment, you will be making extensive use of the Google Calendar API, and Google Assistant SDK for devices to work with your Raspberry Pi. You can watch this YouTube video about the SDK. These links are also outlined as below, just in case if the actual links do not work in this PDF document:

<br>


[Google Calendar API][https://developers.google.com/calendar/v3/reference/] 
[Google Assistant SDK for devices][https://developers.google.com/assistant/sdk/]
[YouTube about the SDK][https://www.youtube.com/watch?v=FBXRwu6hgy8]

All of data is now saved in **cloud database(s).**
##### Important
You must adhere to the following requirements:
a. Only Raspberry Pi model 3 should be used
b. You must use Python 3.5 or >3.5 to complete the tasks. Older versions must not be used.
c. You must use a version control system of some sorts such as GitHub, Bitbucket, etc. A private repository is to be used ONLY.
d. You must stick to the standard style guide for your Python code: (https://www.python.org/dev/peps/pep-0008/)
e. You must attend a 25 minutes demo session to get the assignment 1 marked during week 6 (Oct 08- 12, 2018). A schedule and a booking document will be published soon. You must submit the assignment prior to demo. No submissionNo demoNo marks.

Tasks
Note: This time the tasks are divided into four parts: A, B, C and D:
Part A - Web Interface using Flask [30 marks]
Your team will need to
i. (20 marks) create at least three separate web pages for doctors, patients and medical clerks. Each of the user will have a different URL to access their page. You need not implement complete login features for these users.
A patient can make and delete an appointment for a doctor using MAPS.
Doctor will use MAPS to pull up patient history, add patient notes and diagnoses.
Medical clerk can add, delete appointments on behalf of patients. They are also responsible for keeping an eye on doctor appointments.
The pages must be professionally styled using Bootstrap. You will be marked on the design, professional look & appeal and user friendly of these pages.
Please note that no actual implementation of booking is required for this part. You are setting up the web pages for the further parts.
ii. (5 marks) Your team are expected to set up private github/bitbucket repositories and work on separate branches individually. Everyone will have to explain what they have done in each branch during the demonstration.
iii. (5 marks) Complete documentation of the project using PyDoc and Sphinx. You can read an excellent tutorial at
https://projects.raspberrypi.org/en/projects/documenting-your-code/

Part B – APIs (Patient and Doctor) [30 marks]
You will now implement
iv. (5 marks) The patient registration and booking feature. All the data must be saved to Cloud.
v. (5 marks) all of the Doctor’s page(s): pulling up patient data, making notes and diagnoses during the appointment. All the data must be saved to Cloud.
vi. (10 marks) Create separate API(s) to interact with the cloud. The patient and doctor pages should not directly talk to the Cloud.
vii. (5 marks) Since the interface is web, all the user inputs must be validated
viii. (5 marks) Complete documentation using PyDoc and Sphinx
*It is your responsibilities to make sure that you do not exceed the free tier limit on the Google Cloud Platform.
Part C – API (Medical Clerk) [10 marks]
You will now implement
ix. (4 marks) All of the medical clerk features: add/delete appointment and list of the doctor appointments. Once again use an API to talk to cloud.
x. (3 marks) Add an extra feature where the clerk can generate a visual representation of the doctors appointment(s) (number of patients seen) week wise.
xi. (3 marks) Complete documentation using PyDoc and Sphinx
Part D - Advanced Implementation [30 marks]
xii. (10 marks) Your team will be tasked to create custom actions and traits on Google Assistant SDK to interact with the doctors and patients. This involves
a. implementing the interaction between Reception and Advisor Rapsberry Pi s
b. Doctor dictating medical notes to Advisor Pi
xiii. (15 marks) Your team will choose ONE advanced implementation. Some of the suggestions are (you may come up with your own implementation):
facial recognition, deep learning for scheduling, Integration with Arduino, etc. YOU WILL NEED TO GET THIS approved by the lecturer or the head tutor (not your
tutors) to receive marks in this section.
xiv. (5 marks) Complete documentation using PyDoc and Sphinx