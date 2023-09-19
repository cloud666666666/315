from datetime import datetime

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"


    def parse(self, logFile):  # Read each line from the log and process output
        index = 0
        totalrequests=0
        totalbytes=0
        total_successful=0
        first_date_recorded = True
        dict_status={'Successful':0,'Found':0,'Not Modified':0,'Unsuccessful':0}
        dict_address={'remote':0,'local':0}
        dict_bytes={'remote':0,'local':0}
        type_file_dict={'HTML':0,'Images':0,'Sound':0,'Video':0,'Formatted':0,'Dynamic':0,'Others':0}
        byte_file_dict = {'HTML': 0, 'Images': 0, 'Sound': 0, 'Video': 0, 'Formatted': 0, 'Dynamic': 0, 'Others': 0}
        for line in logFile:
            elements = line.split()


            # Skip to the next line if this line has an empty string
            if line == '':continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):continue

            # Corrects a record with a single "-"
            if (len(elements) == 9 and elements[2] != '-'):
                elements.insert(2, '-')

            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5]
            requestFileName = elements[6].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]
            if not responseCode.isdigit():continue
            if replySizeInBytes.isdigit():
                totalbytes+=int(replySizeInBytes)
            else:
                replySizeInBytes=0
            totalrequests += 1
            dict_status[self.checkResCode(responseCode)]+=1
            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 5 onward

            # Prints assigned elements. Please comment print statement.
            # print('{0} , {1} , {2} , {3} , {4} , {5} '.format(sourceAddress,timeStr,requestMethod,requestFileName,responseCode, replySizeInBytes),end="")
            
            # Assigns & prints format type. Please comment print statement.
            fileType = self.getFileType(requestFileName)
            # print(' , {0}'.format(fileType))

            # Q1: Write a condition to identify a start date and an end date.

            if first_date_recorded:
                self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                self.endDate =datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                first_date_recorded = False
            else:
                if datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S") < self.startDate:
                    self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                elif datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S") > self.endDate:
                    self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
            if self.checkResCode(responseCode) == "Successful":
                total_successful+=1
            if self.checkResCode(responseCode)=="Successful":
                dict_address[sourceAddress.lower()]+=1
            if self.checkResCode(responseCode)=="Successful":
                dict_bytes[sourceAddress.lower()]+=int(replySizeInBytes)/1024/1024
            if self.checkResCode(responseCode)=="Successful":
                type_file_dict[fileType]+=1
            if self.checkResCode(responseCode)=="Successful":
                byte_file_dict[fileType]+=int(replySizeInBytes)/1024/1024
        # Outside the for loop, generate statistics output
        totalbytes=totalbytes/1024/1024
        self.numberOfDays = (self.endDate - self.startDate).days+1
        averageRequestsPerDay = totalrequests / self.numberOfDays
        averagetransferbytesperday=totalbytes/self.numberOfDays
        # print(f"Start date: {self.startDate}")
        # print(f"End date: {self.endDate}")
        #print(f"Number of days: {self.numberOfDays}")
        #print(f"Total number of requests: {totalrequests}")
        print(f"Answer2:Average number of requests per day: {'%.2f'%averageRequestsPerDay}")
        print(f"Answer3:Total bytes transferred: {'%.2f'%totalbytes}MB")
        print(f"Answer4:Average bytes per day: {'%.2f' % averagetransferbytesperday}MB/day")
        print(f"Answer5:Successful:{'%.2f'%(dict_status['Successful']/totalrequests*100)}%\nFound:{'%.2f'%(dict_status['Found']/totalrequests*100)}%\nNot Modified:{'%.2f'%(dict_status['Not Modified']*100/totalrequests)}%\nUnsuccessful：{'%.2f'%(dict_status['Unsuccessful']*100/totalrequests)}%")
        print(f"Answer6:remote:{'%.2f'%(dict_address['remote']/total_successful*100)}%\nlocal:{'%.2f'%(dict_address['local']/total_successful*100)}%")
        print(f"Answer7:remote:{'%.2f'%(dict_bytes['remote']/(totalbytes)*100)}%\nlocal:{'%.2f'%(dict_bytes['local']/(totalbytes)*100)}%")
        print(f"Answer8:HTML:{'%.2f'%(type_file_dict['HTML']/total_successful*100)}%\n"
              f"Images:{'%.2f'%(type_file_dict['Images']/total_successful*100)}%\n"
              f"Sound:{'%.2f'%(type_file_dict['Sound']/total_successful*100)}%\n"
              f"Video:{'%.2f'%(type_file_dict['Video']/total_successful*100)}%\n"
              f"Formatted:{'%.2f'%(type_file_dict['Formatted']/total_successful*100)}%\n"
              f"Dynamic:{'%.2f'%(type_file_dict['Dynamic']/total_successful*100)}%\n"
              f"Others:{'%.2f'%(type_file_dict['Others']/total_successful*100)}%\n"
              )
        print(f"Answer9:HTML:{'%.2f'%(byte_file_dict['HTML']/totalbytes*100)}%\n"
              f"Images:{'%.2f'%(byte_file_dict['Images']/totalbytes*100)}%\n"
              f"Sound:{'%.2f'%(byte_file_dict['Sound']/totalbytes*100)}%\n"
              f"Video:{'%.2f'%(byte_file_dict['Video']/totalbytes*100)}%\n"
              f"Formatted:{'%.2f'%(byte_file_dict['Formatted']/totalbytes*100)}%\n"
              f"Dynamic:{'%.2f'%(byte_file_dict['Dynamic']/totalbytes*100)}%\n"
              f"Others:{'%.2f'%(byte_file_dict['Others']/totalbytes*100)}%\n"
              )




    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'
    def checkResCode(self, code):
        if code == '200' :return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'
        else:return 'Unsuccessful'


if __name__ == '__main__':
    logfile = open('access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    logParser

