def selection_sort(A):
    for i in range(len(A)):
         
        min_idx = i
        for j in range(i+1, len(A)):
            if A[min_idx] == A[j]: #bug => change to >
                min_idx = j
                  
        A[i], A[min_idx] = A[min_idx], A[i]

    return A

# python pipelined.py mid.py testCasesMid testMid
# python pipelined.py selection_sort.py testCasesSel testSel