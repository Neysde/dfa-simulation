#DFA Example
dfa = {
    "states" : ["q0","q1"],
    "alphabet" : ["a","b"],
    "start_state" : "q0",
    "accepting_states" : ["q1"],
    "transitions" : {
        "q0":{"a":"q1",
              "b":"q0"},
        "q1":{"a":"q0",
              "b":"q1"}
    }
}


def simulate_DFA(dfa,word):
   current_state = dfa["start_state"]
   for char in word:
       current_state = dfa["transitions"][current_state][char]
   return current_state in dfa["accepting_states"]


# This function returns a list with all the steps of the given word's process in DFA simulation
def computation_history(dfa,word):
   comp_list=[]
   current_state = dfa["start_state"]
   comp_list.append(f"-{current_state}-{word}") # Initial configuration
   for i in range(len(word)):
       current_state = dfa["transitions"][current_state][word[i]] 
       word_read = word[:i+1] # read word (each char read one by one so we move char by char)
       word_remaining = word[i+1:] # remaining word (each char read one by one so we move char by char)

       comp_list.append(f"{word_read}-{current_state}-{word_remaining}") # It adds each step's result to the list

   return comp_list

# This function returns a dictionary that contains all possible strings up to length n and their corresponding DFA simulation results
def language_exploration(dfa,n):
   lang_dict = {}
   all_strs=all_strings(n) # gets all possible strings using the function defined below
   for c in range(len(all_strs)):
       result = "ACCEPT" if simulate_DFA(dfa,all_strs[c]) else "REJECT" # runs DFA simulation for each string and evaluates the result according its result
       lang_dict[all_strs[c]] = result # append each string as key and result as value in the dictionary


   return lang_dict
  

# This function returns a dictionary that contains visit counts for each state, transition.Also counts accept and reject numbers of the all possible strings up to length n
def language_report(dfa,n):
   all_strs=all_strings(n) # gets all possible strings using the function defined below

   visit_counts,transition_counts,accepted_rejected,final_dict={},{},{"total_accepted":0,"total_rejected":0},{} # dictionaries defined for the count,transition,accept-reject and returned dictionary that holds all of these

   for word in all_strs: # for each word
       from_state, to_state, symbol = "","",""


       current_state = dfa["start_state"]
       visit_counts[f"{current_state}_visit_count"]=visit_counts.get(f"{current_state}_visit_count",0)+1 # makes start state's visit count 1 at the beginning.
       for char in word:
           from_state = current_state
           symbol = char
           current_state = dfa["transitions"][current_state][char]
           to_state = current_state
           visit_counts[f"{current_state}_visit_count"]=visit_counts.get(f"{current_state}_visit_count",0)+1 # Increases visit count by one for the state visited. If this state has not visited before, creates the key value pair
           transition_counts[f"{from_state}_{symbol}_{to_state}_transition_count"]=transition_counts.get(f"{from_state}_{symbol}_{to_state}_transition_count",0)+1 # Increases transition count by one for the states transitioned. If this has not happened before, creates the key value pair
       # After the evaluations this checks whether the current state is one of the accepting states or not. If yes, increases accept count by 1, otherwise increases reject count by 1
       if current_state in dfa["accepting_states"]: 
           accepted_rejected["total_accepted"]+=1
       else:
           accepted_rejected["total_rejected"]+=1

    # With these for loops, we put our evaluated visit, transition and accept-reject count values into one final dictionary
   for k,v in visit_counts.items():
       final_dict[k]=v
   for k,v in transition_counts.items():
       final_dict[k]=v
   for k,v in accepted_rejected.items():
       final_dict[k]=v
  
   return final_dict

# This function returns a list that contains all strings of length 0 to n by using the values for alphabet in dfa
def all_strings(n):
   all_strs=[""] # Holds all possible strings
   tmp_prev=[""] # Holds possible strings only that their length is one less than the strings being generated in the loop below.

    # Runs n times to create all strs' of length 0 to n
   for i in range(n):
       tmp_current=[] # holds strings only generated in current iteration of the loop and adds them to tmp_l2 list to be used from there for the next creation
       for n in range(len(tmp_prev)): # uses only strings created in previous iteration from tmp_l2 and add each possible alphabet values onto each string in tmp_l2 list
           tmp_current.append(tmp_prev[n]+dfa["alphabet"][0]) 
           tmp_current.append(tmp_prev[n]+dfa["alphabet"][1])
       tmp_prev=tmp_current # previous string list is now equal to current string list because loop is moving the next iteration
       all_strs+=tmp_current # adds currently generated strings combinations in the list that holds all possible strings


   return all_strs