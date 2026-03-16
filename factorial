import time
def factorial(num):
    if num == 1:
        return 1

    else:   
        return num * factorial(num - 1)

while True:
    try:
        while True:
            x = int(input("Give me a positive integer, and I will tell you the factorial of it: \n"))

            print(f"{factorial(x)}\n")
    except KeyboardInterrupt:
        def long_running_process():
            try:
                print("Performing a long-running process.")
                for i in range(10):
                    time.sleep(1)
                    print(f"Processing step {i + 1}")
            except KeyboardInterrupt:
                print("\nInterrupted! Cleaning up before exiting.")
                # Perform cleanup operations here if needed
            finally:
                print("Exiting the program.")


        # Call the long_running_process function
        long_running_process()
