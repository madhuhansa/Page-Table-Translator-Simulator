# Page Table Translator Simulator  
A simple Python application that simulates how an Operating System converts a **logical address** into a **physical address** using **paging**.  
This tool demonstrates basic virtual memory concepts such as page tables, page numbers, offsets, frames, and page faults.

---

## 🚀 Features
- Select page size: **512 bytes** or **1024 bytes**
- Edit page table entries (Page → Frame mapping)
- Choose number of physical frames (4–6)
- Enter logical address for translation
- See:
  - Page number  
  - Frame number  
  - Offset  
  - Physical address  
  - Page fault message  
- Clean dark-themed GUI  
- Auto explanation box that describes what happened in the backend

---

## 🖥️ Technologies Used
- **Python 3**
- **Tkinter** (GUI)
- **ttk Styles / TreeView**

---

## 📂 Project Structure
```
app.py               # Main application file
README.md            # Project documentation
```

---

## 📘 How It Works
1. User selects the page size (512 or 1024).
2. User edits the page table manually (use -1 for not loaded).
3. User enters a logical address.
4. Program computes:
   - Page number  
   - Offset  
   - Frame number  
   - Physical address  
5. Program displays results in the table.
6. Explanation box shows what happened step by step.

---

## ▶️ Running the Application

### **1. Install Python**
Make sure Python 3 is installed.

### **2. Run the program**
```
python app.py
```

The GUI window will open.

---

## 📸 Screenshots
(Add your screenshots here)

---

## 📚 About This Project
This application was developed as part of the **EEX5564 – Computer Architecture and Operating Systems** Mini Project (Group A: Page Table Translator)  
at the **Open University of Sri Lanka**.

---

## 📎 Appendix
Full project report and documentation available in LMS submission.

GitHub Repo:  
👉 *Add this link after uploading your repo*

