import twint

# Configure
c = twint.Config()
# c.Username = "pielco11"
c.Search = "#amc"
c.limit=10
c.Store_object = True

# Run
print(twint.run.Search(c))

tweets_as_objects = twint.output.tweets_object 
print(tweets_as_objects)