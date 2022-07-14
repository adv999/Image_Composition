Composition Score Calculator

Introduction:

This is a Python Project made to calculate Composition Score of a image. We have take the following characteristics of the image to find the composition score:
1) Rule of Third
2) Diagonal Dominance
3) Visual Balance
4) Object Size and Placement

This project calculates the values of all these factors for a given image and then take average of all these to find final composition score of image.

Main Files:

1) getCompScore.py : Main function

a) Extract prominent line information from getline.py and getlinevalue.py

b) Find salient object information of an input image using opencv image saliency and calculate composition score.

Total composition score is weighted sum of four composition guideline score (Rule of Third, Visual Balance, Diagonal Dominance, Object Size)

2) getLine.py : Extract prominent line's end points from the image.

3) getLineValue.py : Measure the composition score that is related to line information.

4) app.py: Creating flask server to host the score calculator page 

5) templates folder: Containing html pages index.html and score.html

5) static folder: Containing style.css and Upload folder ...Images uploaded will be stored there



How to run:

Step 1) Download the zip folder and extract it and open it in your editor (Vs code, Spyder etc) (Vs Code Recommended)

Step 2) Make a folder named Upload under static folder ( to store the images uploaded ).

Step 3) Install all the dependicies written in dependicies.txt

Step 4) In your terminal, type command "python app.py"

Step 5) Server will start and host a webpage at port 8000.

Step 6) Upload the image whose composition score you want to find and you will get the result





