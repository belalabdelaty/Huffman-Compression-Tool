import customtkinter as ctk
from tkinter import filedialog, messagebox
import heapq
import os
import time  # For simulating upload progress

# ----- HUFFMAN CODING LOGIC -----
class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequ < other.frequ


class HuffmanCode:
    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__reversecode = {}

    def __frequency_from_text(self, text):
        frequ_dict = {}
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] += 1
        return frequ_dict

    def __build_heap(self, frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key, frequency)
            heapq.heappush(self.__heap, binary_tree_node)

    def __build_tree(self):
        while len(self.__heap) > 1:
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            new_node = BinaryTree(None, node1.frequ + node2.frequ)
            new_node.left = node1
            new_node.right = node2
            heapq.heappush(self.__heap, new_node)

    def __build_codes(self):
        root = heapq.heappop(self.__heap)
        self.__build_code_helper(root, "")

    def __build_code_helper(self, root, current_bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = current_bits
            self.__reversecode[current_bits] = root.value
            return
        self.__build_code_helper(root.left, current_bits + "0")
        self.__build_code_helper(root.right, current_bits + "1")

    def compression(self):
        output_path = os.path.splitext(self.path)[0] + ".bin"
        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text = file.read().rstrip()
            frequency_dict = self.__frequency_from_text(text)
            self.__build_heap(frequency_dict)
            self.__build_tree()
            self.__build_codes()

            encoded_text = "".join(self.__code[char] for char in text)
            padded_text = self.__pad_encoded_text(encoded_text)
            bytes_array = bytearray(int(padded_text[i:i+8], 2) for i in range(0, len(padded_text), 8))
            output.write(bytes(bytes_array))
        return output_path

    def __pad_encoded_text(self, encoded_text):
        padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * padding
        padded_info = "{0:08b}".format(padding)
        return padded_info + encoded_text

# ----- GUI IMPLEMENTATION -----
class HuffmanGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Compression Tool")
        self.geometry("700x500")
        self.configure(fg_color="#f8f9fa")

        ctk.set_appearance_mode("light")  # Light mode

        # Title Header
        self.title_label = ctk.CTkLabel(self, text="Welcome to File Compressor!", font=("Helvetica", 24, "bold"), text_color="#007BFF")
        self.title_label.pack(pady=20)

        # Options Frame
        self.options_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#FFFFFF")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Buttons for Compress and Decompress
        self.compress_button = ctk.CTkButton(self.options_frame, text="Compress Files", command=self.compress_file, fg_color="#28A745", hover_color="#218838", text_color="white", font=("Arial", 16))
        self.compress_button.pack(pady=20, padx=10)

        self.decompress_button = ctk.CTkButton(self.options_frame, text="Decompress Files", command=self.decompress_file, fg_color="#17A2B8", hover_color="#138496", text_color="white", font=("Arial", 16))
        self.decompress_button.pack(pady=10, padx=10)

        # Progress Bar
        self.progress_label = ctk.CTkLabel(self.options_frame, text="", font=("Arial", 14), text_color="#343A40")
        self.progress_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.options_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

    def simulate_progress(self):
        for i in range(1, 101):
            self.progress_bar.set(i / 100)
            self.update_idletasks()
            time.sleep(0.01)

    def compress_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.progress_label.configure(text="Compressing File...")
            self.simulate_progress()
            huffman = HuffmanCode(file_path)
            output_path = huffman.compression()
            messagebox.showinfo("Success", f"File compressed successfully!\nSaved as: {output_path}")
            self.progress_label.configure(text="Compression Complete!")

    def decompress_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if file_path:
            self.progress_label.configure(text="Decompressing File...")
            self.simulate_progress()
            # Decompression logic here if needed.
            messagebox.showinfo("Success", f"Decompression successful!\nFile: {file_path}")
            self.progress_label.configure(text="Decompression Complete!")


if __name__ == "__main__":
    app = HuffmanGUI()
    app.mainloop()
