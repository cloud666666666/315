from datetime import datetime
from collections import Counter
log_file_path = 'access_log'
with open(log_file_path, 'r', encoding='ISO-8859-1') as file:
    log_lines = file.readlines()
dates = []
bytes_transferred = []
for line in log_lines:
    try:
        status = line.strip().split(' ')[-2]
        date_str = line.split(' ')[3][1:]
        date = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S')
        dates.append(date)
        bytes_str = line.strip().split(' ')[-1]
        if bytes_str.isdigit():
            bytes_transferred.append(int(bytes_str))
        else:
            bytes_transferred.append(0)
    except (IndexError, ValueError):
        dates.append(None)
        bytes_transferred.append(0)
        continue
def answer2():
    dates_only = [date.strftime('%Y-%m-%d') for date in dates if date!=None]
    request_counts_per_day = Counter(dates_only)
    average_requests_per_day = sum(request_counts_per_day.values()) / len(request_counts_per_day)
    print('Q2:'+'%.2f'%average_requests_per_day)
def answer3():
    total_bytes_transferred = sum(bytes_transferred)
    total_megabytes_transferred = total_bytes_transferred / (1000 * 1000)
    print('Q3:'+str('%.2f'%total_megabytes_transferred)+'MB')
def answer4():
    date_bytes_dict = {}
    for date, byte in zip(dates, bytes_transferred):
        if date is not None:
            date_str = date.strftime('%Y-%m-%d')
            if date_str not in date_bytes_dict:
                date_bytes_dict[date_str] = 0
            date_bytes_dict[date_str] += byte
    average_megabytes_per_day = sum(date_bytes_dict.values()) / (len(date_bytes_dict) * 1000 * 1000)
    print('Q4:'+str('%.2f'%average_megabytes_per_day)+'MB/day')
def answer5():
    response_codes = [int(line.strip().split(' ')[-2]) if line.strip().split(' ')[-2].isdigit() else None for line in log_lines]
    response_code_counts = Counter(response_codes)
    total_requests = len(log_lines)
    successful_requests = response_code_counts.get(200, 0)
    not_modified_requests = response_code_counts.get(304, 0)
    found_requests = response_code_counts.get(302, 0)
    unsuccessful_requests = sum(count for code, count in response_code_counts.items() if code is not None and code >= 400)
    response_code_percentages = {
        "Successful": (successful_requests / total_requests) * 100,
        "Not Modified": (not_modified_requests / total_requests) * 100,
        "Found": (found_requests / total_requests) * 100,
        "Unsuccessful": (unsuccessful_requests / total_requests) * 100
    }
    print('Q5:')
    for key,value in response_code_percentages.items():
        print(key,str('%.2f'%value)+'%')
def answer6():
    cilents= [line.split(' ')[0] for line in log_lines if line.strip().split(' ')[-2]=='200']
    local_clients = [cilent for cilent in cilents if cilent==('local')]
    remote_clients = [cilent for cilent in cilents if cilent==('remote')]
    total_requests = len(cilents)
    local_requests_percentage = (len(local_clients) / total_requests) * 100
    remote_requests_percentage = (len(remote_clients) / total_requests) * 100
    print(f"Q6:Local clients made {local_requests_percentage:.2f}% of total requests")
    print(f"   Remote clients made {remote_requests_percentage:.2f}% of total requests")
def answer7():
    local_bytes = []
    remote_bytes = []
    for line in log_lines:
        if line.strip().split()[-2]=='200':
            try:
                client_type = line.split(' ')[0]
                bytes_transferred = int(line.split(' ')[-1])
                if client_type== 'local':
                    local_bytes.append(bytes_transferred)
                elif client_type == 'remote':
                    remote_bytes.append(bytes_transferred)
            except:
                continue
        else:
            continue
    total_bytes_transferred = sum(local_bytes) + sum(remote_bytes)
    local_bytes_percentage = (sum(local_bytes) / total_bytes_transferred) * 100
    remote_bytes_percentage = (sum(remote_bytes) / total_bytes_transferred) * 100

    print(f"Q7:Local clients transferred {local_bytes_percentage:.2f}% of total bytes")
    print(f"   Remote clients transferred {remote_bytes_percentage:.2f}% of total bytes")

answer2()
answer3()
answer4()
answer5()
answer6()
answer7()

