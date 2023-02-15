import concurrent.futures
import time, requests

def main():
    ...
    
#important functions   
def parallel(function, lists):
    """This parallel function uses multithreading to simulteanously run a request for a large list
    Args:
        ``function`` (_type_): The function you'd like to use, your function must
                            contain an asteriks(*)for unpacking values
        ``lists`` (_type_): the list, must be a list 
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if isinstance(lists[0], (list, tuple)):
                results = {executor.submit(function, *arguments)  for arguments in lists}
            else:
                results = {executor.submit(function, arguments)  for arguments in lists}
            total = [future.result() for future in concurrent.futures.as_completed(results)]
        return total
    except TypeError as error:
        return (error)
        
def odd(number):
    if number % 2 == 0:
        return "even"
    else:
        return "odd"     
        
if __name__ == "__main__":
    main()