# Assign the state abbreviation when the state name is longer than 8 characters 
new_names<-ifelse(nchar(murders$state)>8,substr(murders$state, start = 1, stop = 2),murders$state)


