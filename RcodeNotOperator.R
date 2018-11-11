# Store the 5 abbreviations in abbs. (remember that they are character vectors)
abbs <- c("MA", "ME", "MI", "MO", "MU") 

# Use the `which` command and `!` operator to find out which abbreviation are not actually part of the dataset and store in ind
a<-abbs %in% murders$abb
ind<-which(!abbs %in% murders$abb)
# What are the entries of abbs that are not actual abbreviations
abbs[ind]
