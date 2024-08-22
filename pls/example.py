from PythonLatexSync import PLS

# Credentials
user = 'curie'
write_password = 'supersecretwrite'
read_password = 'supersecretread'

# Initialize the PLS class
pls = PLS(user, write_password, read_password)

# Use the push method to upload the file
pls.push('example.txt')
pls.push('cat.jpg')

