# TwitterAggregateSolution
Yun Ho Jung - HackSMU2019

Problem:
As of right now, the training model is seperated from 12499 to 25000, this causes
data under 25000 to be predicted only using the positive data.
    
Solution: 
Seperate the training data into two, and predict the same data twice using two seperate sets
