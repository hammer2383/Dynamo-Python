# Dynamo-Python
Python code that I used in my Dynamo script

A lot of time it quite simple program which boiled down to; take some infomation from some element, do something with it, and put it into some where within those element. Which wouldn't be put here.
Here's the list of the some of the programs and short description of it. (Since some programs name are quite self-explainatory)

AddUserNameToView - add the user name in Revit to the view name, this is to solve the problem when someone batch duplicated view and have to manually rename the view.

ArtInstallationPatternMaker - use to create the Art Wall model for SiamScape building project, here is the link to what it look like; https://twitter.com/hashtag/%E0%B8%AA%E0%B8%A2%E0%B8%B2%E0%B8%A1%E0%B8%AA%E0%B9%80%E0%B8%84%E0%B8%9B.

BatchChangeViewName - as the name suggested it change multiple view name, with some modification it was used for change the name to specific specification.

BatchFamilyExport - While there are some free add-in that could do the job, it's paid one and couldn't meet the our specification.

CreateStructuralConnection - Revit 2019 wouldn't allow creation of steel connection detail all at once(like multiple beams with multiple column) this program solved that problem

DuckPro - Named after floor detergent brand, it's lived up to it name, it'll delete all unused element in project file. It's different from purge funchtion in Revit in that, it'll also delete WIP view too as per my team requested.

EditingSketch - it's expriemental since the API for modifying sketch came after Revit 2022.

JoiningWallandFloor - As the name suggested it will join wall and floor element but in specific order.

MultipleRailRehost - Rehost rail element to the closest stair.

URLchanger - Since our company have to ship the whole model to our contractor (Which is the Design firm at the time of the creation). A lot of family that has a direct link to technical information which usually in pdf file, would be not be usuable since Revit stored directory as absolute address. This program will re-link all of those files by using relative path from the main RVT file (of course if their messed up the folder structure this program wouldn't work).
