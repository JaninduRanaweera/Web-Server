import socket
import time
class Web_server:
    
    def __init__(self, port):
        self.host = 'localhost'   #initiating host,port and dir variables
        self.directory = 'C:/Users/janidu/Desktop/web1/web1'
        self.port = 5050
         
		
 
    def starting_web_server(self):
        """ try to reach socket and launchs the server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        try:
            print ("Launching http server on", self.host,":",self.port)
        except Exception as e:                                          
            print("Warning:Can't reach to the port",self.port,)
            print("Trying Default port")
            users_port = self.port #store users port before trying the default port
            self.port = 8080   #assigning default port number 8080
            
            try:
                print("Launching http server using port :",self.port)
                self.socket.bind((self.host, self.port))
            except Exception as e:
                print("Failed to aqcuire for port",users_port,"and",self.port)
        print("Server is successfully established with the port:", self.port)
        
    def generate_headers(self,code):
        header = ''
	
        if(code == 200):
            header = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            header = 'HTTP/1.1 404 Not Found\n'
			
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: ' + current_date +'\n'
        header += 'Server: Simple-Python-HTTP-Server\n'
        header += 'Connection: close\n\n'
        return header

    def building_connections(self):
        while(True):
            print ("Waiting for a connection")
            self.socket.listen(5)
            
            connection, address = self.socket.accept()
            print("Connection is getting from:", address)
            
            # connection_data variable store the recived data from client and string_data variable decode it and stored
            connection_data = connection.recv(2048)       
            string_data = bytes.decode(connection_data)

            # identifying requested file type GET or HEAD
            request_file_type = string_data.split(" ")[0] 
            print ("Requested File Type: ", request_file_type)
            

            if (request_file_type == 'GET') or (request_file_type == 'HEAD'):

                requested_file = string_data.split(' ') #split on space
                requested_file = requested_file[1] # get the 2nd element
                
                #Check for the URL arguments.
                requested_file = requested_file.split('?')[0]
                if (requested_file == '/'):
                    """ loading the abc.html file in web1 folder"""
                    requested_file = '/abc.html'
                				
            requested_file = self.directory + requested_file
            print ("Serving the web page requested [",requested_file,"]")

        # loading the content of abc.html file
            try:
                file_handler = open(requested_file,'rb')
                    
                if (request_file_type == 'GET'): #reads only GET type files
                    content_of_response = file_handler.read() #reading the file content
                file_handler.close()
                response_headers = self.generate_headers( 200)    
                print("HTTP/1.1 200 OK")
				
				
            except Exception as e:
                print ("Warning, file not found. Serving response code 404\n", e)
                response_headers = self.generate_headers( 404)
                if (request_file_type == 'GET'):
                    content_of_response = b"<html><body><B>Error 404: File not found</B></body></html>"
            server_response =  response_headers.encode()
            if (request_file_type == 'GET'):
                server_response += content_of_response     
                
            connection.send(server_response)
            print("Closing Connection\n")
            connection.close()

        else:
            print("Unknown HTTP requested Type:", request_file_type)

  

s = Web_server(5050)
s.starting_web_server()
s.building_connections()

                     
   


