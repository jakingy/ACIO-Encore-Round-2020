# Potato Pyramid Project

*This paragraph can be skipped, it is pure flavourtext.*
Farmer John had enough of Bessie's incessant demands and disrespect. His loathing and disgust at the inhumane treatment of workers by the cows almost drove him to leave the dairy industry. However, his greed compelled him stay, the dairy industry was a lucrative business after all. Day after day, night after night, John schemed. How could he possibly make as much money elsewhere? Until one day when dining on a *potato* he hatched a grand and devious plan. This was the *Potato Pyramid Project* (PPP): :





Farmer John then formed rules which must be followed for anyone who bought into his PPP.

Suppose person $i$ bought into the PPP, they would ask person $i \times 2$ and $i \times 2 + 1$ "Hey you. Yes you. Would you like $2^{H-d-2}$ potatoes for only \$10" ( $d$ is the depth of person $i$ in the tree. John would be depth 0. ). To which they would respond "That is an absurd price! There must be a catch!"

"Astute observation my friend!" person $i$ would return, fake smile and all.

"You see, you are also selling your s... *cough* buying into the Potato Pyramid Project and must follow these rules... Of course, you can keep a generous proportion of your revenue, I only ask for an $(R \times 100)\%$ cut."

Revenue included the \$10 sale/s they made and $(R \times 100)\%$ of the revenue of whomever they convinced to buy into the PPP.

**The $j$-th person would only accept the deal if $R$ was between $a_j$ and $b_j$ (inclusive, inclusive).**

This process would repeat until no one could convince anyone else to buy into the PPP.

John would be the instigator of the plan. You may assume he has already bought into the PPP.

However, John was a cautious man. He first wanted to simulate his plan.

Given $H$, $a_i$ and $b_i$ for all $i$. Answer $Q$ queries of the form "How much revenue would person $X$ make if the rate was $R$?". 

## Input
The first line of input contains the integer $H$. $2^H-2$ lines follow. The $i$-th line contained the integers $a_{i+1}$ and $b_{i+1}$ (not given for John as he always accepts the deal).
$Q$ is given in the next line. $Q$ lines follow containing two integers $X$ and $R$ representing a query.

## Output
For each query, determine the revenue of person $X$ given the rate $R$. Your output will be accepted if it is within 0.01 of the judge's output.

### Sample Input
```
3
0.0 0.1
0.45 1.0
0.0 0.1
0.2 0.8
0.3 0.7
0.0 0.1
4
1 0.5
4 0.04
1 0.056492
3 0.4
```
### Sample Output
```
30
0
10.56492
10
```

### Explanation
The binary tree in the above diagram corresponds to the sample input. 

For the first query, Farmer John was able to convince both person 2 and 3 to buy into the PPP earning $20 + 50% of their revenue. Person 2 was able to convince person 5 to buy into the PPP, but not person 4 as 0.5 (R) is not within the range 0.0 - 0.1. As person 5 themselves have no revenue, person 2 has a revenue of \$10. Similarly person 3 was able to convince person 6, but not 7, and thus also has a revenue of \$10. Therefore, John has a total revenue of \$20 + \$5 + \$5 = \$30.

For the 2nd, John wasn't able to convince person 2 to buy into the PPP, therefore person 4 could also not buy into the PPP, However, if he could, he would still have a revenue of $0 as he could convince no one else.

For the 3rd query, John convinced person 3 who in turn convinced person 7. This gives John $10 + 0.056492 \times 10 = \$10.56492$. Note: any value between 10.55492 and 10.57492 would also have been accepted.

For the final query, John convinced person 3. Person 3 only convinced person 6. Therefore Person 3 had a revenue of \$10.


## Subtasks and Constraints

For all subtasks:
- $1 \leq H \leq 17$
- $1 \leq Q \leq 10^5$
- $1 \leq A \leq 2^D-1$
- $0 \leq R \leq 1$
- $0 \leq a_i \leq b_i \leq 1$ for all $i$
    
For specific subtasks:

- Subtask 1 (*10 points*), $R$ is the same for all queries.
- Subtask 2 (*28 points*), $H > 1$ and $A$ is at a depth of $H-2$ for all queries. 
- Subtask 3 (*19 points*), $a_i = 0$ for all $i$ and if $i \lt j, b_i \gt b_j$.
- Subtask 4 (*12 points*), $a_i = 0$ for all $i$.
- Subtask 5 (*31 points*), No further constraints
