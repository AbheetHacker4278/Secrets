import time

def display_loading_screen():
    print("Loading, please wait...")
    bar_length = 30
    for i in range(bar_length + 1):
        loading_bar = '[' + '#' * i + ' ' * (bar_length - i) + ']'
        print(loading_bar, end='\r')
        time.sleep(1)

def main():
    display_loading_screen()

if __name__ == "__main__":
    main()
