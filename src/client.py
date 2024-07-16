import asyncio
import aioconsole
from tkinter import ttk
import tkinter as tk

class client:
    def __init__(self) -> None:
        self.designer = ''
        self.user =''
        self.host = "127.0.0.1"
        self.port = 8888
        self.reader = ''
        self.writer = ''
        
    async def error(self, message):
        print(f"ошибка: {message}")
        
    async def receive_message(self):
        while True:
            message = await self.reader.read(1024)  # Получаем сообщение от сервера
            print(f"{message.decode().strip()}")
            await self.designer.receive_message(message.decode().strip())  
            if "вы отключены от сервера" in message.decode().strip():
                return
            
    async def send_message(self, message):
        if message == "": 
            self.error("вы ничего не ввели")
            return
        self.writer.write(message.encode())
        await self.writer.drain()
        if message == "exit":
            return
    
    async def send_message_to_server(self, writer, message):
        writer.write(message.encode())
        await writer.drain()
           
    async def start_client(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Подключено к серверу")
        
        await self.receive_message()
        self.writer.close()
        
class designer:
    def __init__(self, client):
        self.client = client
        
        self.root = tk.Tk()
        self.root.title("клиент")
        self.root.geometry('620x1000')
        self.root['background'] = "gray"
        self.root. resizable(True, True)
        self.style_frame = ttk.Style()
        self.style_frame.configure("TFrame", background = "white")
        self.style_label = ttk.Style()
        self.style_label.configure("TLabel", font=("Arial", 14), padding = 10, foreground="white", background="gray")
        self.style_input = ttk.Style()
        self.style_input.configure("TEntry", font=("Arial", 14), padding = 10, foreground="black", background="gray")
        self.style_label_message = ttk.Style()
        self.style_label_message.configure("TLabelMessage", font = ("Arial", 14))
        self.style_button = ttk.Style()
        self.style_button.configure("TButton", background="gray", font=("Arial", 14))
        
        
        self.output_frame = ttk.Frame(self.root, style= "TFrame")
        
        self.input_frame = ttk.Frame(self.root, style="TFrame")
        
        self.send_Entry = ttk.Entry(self.input_frame, style="TEntry", width= 78, justify="left")
        self.send_Entry.grid(row=0, column=0)
        
        self.send_button = ttk.Button(self.input_frame, style="TButton", command=self.click, text="отправить")
        self.send_button.grid(row=0, column= 1, sticky="ns")
        
        self.input_frame.pack(fill=tk.X, anchor="s")
        
        self.output_heading = ttk.Label(self.output_frame, state="TLabel", text= "Чат", anchor="center")
        self.output_heading.pack(fill=tk.X)
        
        self.history = list()
        
        self.output_frame.pack(fill=tk.X)
        
    async def update(self, interval = 0.05):
        while True:
            self.root.update()
            await asyncio.sleep(interval)
    def click(self):
        asyncio.create_task(self.send_message())
        
    async def send_message(self):
        message = self.send_Entry.get()
        await self.client.send_message(message)
        
    async def receive_message(self, message):
        new_message = ttk.Label(self.output_frame)
        new_message.configure(foreground="black", font=("Arial", 12), background="grey", text=message)
        new_message.pack(fill=tk.X, anchor="w")
        self.history.append(new_message)
        self.send_Entry.delete(0, "end")
 
async def main():
    my_client = client()
    my_des = designer(my_client)
    my_client.designer = my_des
    tasks = [
        asyncio.create_task(my_client.start_client()),
        asyncio.create_task(my_des.update())
    ]
    
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())
