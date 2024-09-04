from PythonLatexSync import PLS

# Credentials
user = 'curie'
write_password = 'supersecretwrite'
read_password = 'supersecretread'
url = 'http://localhost:5000'

# Initialize the PLS class
pls = PLS(user, write_password, read_password, url)

# Use the push method to upload the file
pls.push('example.txt')
pls.push('cat.jpg')

# Use the pull method to download the files
pls.pull('example.txt', 'downloaded_example.txt')
pls.pull('cat.jpg', 'downloaded_cat.jpg')
