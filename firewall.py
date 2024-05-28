import tkinter as tk
from tkinter import scrolledtext
from scapy.all import sniff, IP, TCP, UDP
import platform
import threading

# Function to play beep sound
def play_beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms
    else:
        print("\a")  # ASCII Bell

# Define lists for allowed and blocked IPs
allowed_ips = ['192.168.1.100']
blocked_ips = ['192.168.1.101']

# Function to process each packet
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        packet_info = f"[!] Packet: {src_ip} -> {dst_ip}\n"

        if src_ip in blocked_ips or dst_ip in blocked_ips:
            packet_info += f"    [!] Blocked Packet: {src_ip} -> {dst_ip}\n"
            play_beep()  # Play beep for blocked packet
        elif src_ip in allowed_ips or dst_ip in allowed_ips:
            packet_info += f"    [!] Allowed Packet: {src_ip} -> {dst_ip}\n"
            if packet.haslayer(TCP):
                tcp_layer = packet.getlayer(TCP)
                packet_info += f"        [TCP] Sport: {tcp_layer.sport} Dport: {tcp_layer.dport}\n"
            elif packet.haslayer(UDP):
                udp_layer = packet.getlayer(UDP)
                packet_info += f"        [UDP] Sport: {udp_layer.sport} Dport: {udp_layer.dport}\n"
        else:
            packet_info += f"    [!] Unclassified Packet: {src_ip} -> {dst_ip}\n"

        # Insert packet info into the text box
        gui_text_box.insert(tk.END, packet_info)
        gui_text_box.see(tk.END)  # Scroll to the end

        # Animate packet transfer
        animate_packet_transfer(src_ip, dst_ip)

# Function to start packet sniffing
def start_sniffing():
    sniff(prn=packet_callback, store=0)

# Function to animate packet transfer
def animate_packet_transfer(src_ip, dst_ip):
    packet = canvas.create_oval(90, 190, 110, 210, fill='blue')
    canvas.update()

    if src_ip in allowed_ips or dst_ip in allowed_ips:
        target_x = 300
    else:
        target_x = 500

    for x in range(100, target_x, 5):
        canvas.move(packet, 5, 0)
        canvas.update()
        canvas.after(10)  # Decrease the delay to speed up the animation

    canvas.delete(packet)

# Create the main window
root = tk.Tk()
root.title("Packet Sniffer and Firewall")

# Create a ScrolledText widget
gui_text_box = scrolledtext.ScrolledText(root, width=100, height=20)
gui_text_box.pack()

# Create a Canvas for animation
canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.pack()

# Draw the computers
canvas.create_rectangle(50, 150, 150, 250, fill='lightgrey')
canvas.create_text(100, 130, text='Source Computer')
canvas.create_rectangle(250, 150, 350, 250, fill='lightgreen')
canvas.create_text(300, 130, text='Allowed Destination')
canvas.create_rectangle(450, 150, 550, 250, fill='lightcoral')
canvas.create_text(500, 130, text='Blocked Destination')

# Start sniffing in a separate thread
thread = threading.Thread(target=start_sniffing, daemon=True)
thread.start()

# Start the Tkinter event loop
root.mainloop()
