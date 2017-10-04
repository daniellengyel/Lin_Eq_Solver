# Markov_Chain_Probability_Solver
A specific system of linear equations solver

# Summary
Given a square matrix, every row corresponds to a state, and the ith entry in a row corresponds to how often we expect to reach the ith state, given that we are in the current state. A row with no entries indicates a state which never leaves its state. (It may be easier to think of it as being analogous to a markov chain, where the matrix is a transition matrix). The program will then find all the exact probabilities of reaching a terminal state starting in the first state (row 0). The result will be returned by representing all probabilities as fractions, where every numerator is scaled such that every probability has the same denominator. The returned result will then be in an array where the last element is the common denominator and the ith element is the numerator of the ith terminals states probability.

Sample Input:

[[1, 2, 3, 22],
 [4, 2, 10, 12], 
 [0, 0, 0, 0], <- Terminal state
 [0, 0, 0, 0]] <- Terminal state
 
 Sample output:
  [49, 298, 347]
  where 49/347 is probability of reaching first terminal state before the second one
  and 298/347 is probability of reaching second terminal state before first
