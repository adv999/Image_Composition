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

2) getLine.m : Extract prominent line's end points from the image.

3) getLineValue.m : Measure the composition score that is related to line information.



