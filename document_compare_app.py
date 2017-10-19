import json
import os
import Tkinter as tk
import tkFileDialog
import tkFont

import requests


def get_file(doc):
    dir_options = {'initialdir': os.environ["HOME"] + '\\', 'title': 'Please select a file'}
    result = tkFileDialog.askopenfile(**dir_options)
    doc.delete(1.0, tk.END)
    doc.insert(tk.END, result.read())


def setup_file_selector(root, doc1, doc2):
    buttons_frame = tk.Frame(root, pady=5)
    buttons_frame.pack(side='top')

    doc1_button = tk.Button(buttons_frame, text='Select document 1', padx=5, width=20, command=lambda: get_file(doc1))
    doc2_button = tk.Button(buttons_frame, text='Select document 2', padx=5, width=20, command=lambda: get_file(doc2))

    doc1_button.pack(side='left')
    doc2_button.pack(side='left')


def showresults(root, doc1, doc2, result_slider):
    doc1_payload = doc1.get("1.0", tk.END)
    doc2_payload = doc2.get("1.0", tk.END)

    response = get_comparison_result(doc1_payload, doc2_payload)

    if response.status_code == 200:  # OK
        result_json = json.loads(response.text)
        result_slider.set(result_json['cosineSimilarity'] * 100)


def get_comparison_result(doc1_payload, doc2_payload):
    base_url = "http://api.cortical.io:80"
    final_url = "%s/rest/compare?retina_name=en_associative" % base_url
    payload = [{"text": doc1_payload}, {"text": doc2_payload}]
    response = requests.post(final_url, json=payload)
    return response


def setup_result_section(root, doc1, doc2):
    result_frame = tk.Frame(root, padx=10)

    result_slider = tk.Scale(result_frame, from_=0, to=100, orient=tk.HORIZONTAL, width=15, length=600)
    result_button = tk.Button(root, text='Compare', padx=5, width=20,
                              command=lambda: showresults(root, doc1, doc2, result_slider))
    result_button.pack(pady=20)

    result_frame.pack()
    left_label = tk.Label(result_frame, text="Not Similar", padx=10, pady=20).pack(side='left')
    result_slider.pack(side='left')
    right_label = tk.Label(result_frame, text="Very Similar", padx=10, pady=20).pack(side='left')


def center_window(root, width=300, height=200):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def setup_app():
    root = tk.Tk()
    root.title("Document comparison using cortical-api - developed by Vishnu")
    h1 = tkFont.Font(root, family='Helvetica', size=24, weight=tkFont.BOLD)

    title = tk.Label(root, pady=10, text="Document Comparison", font=h1)
    title.pack()

    doc_outer_frame, doc1_frame, doc1, doc2_frame, doc2 = setup_doc_variables(root)

    setup_file_selector(root, doc1, doc2)

    setup_documents(doc_outer_frame, doc1_frame, doc1, doc2_frame, doc2)

    setup_result_section(root, doc1, doc2)

    info_label = tk.Label(root, text="Result calculated using cortical api and cosine similarity.").pack()

    center_window(root, 1000, 750)

    root.mainloop()


def setup_doc_variables(root):
    doc_outer_frame = tk.Frame(root, padx=5)
    doc1_frame = tk.Frame(doc_outer_frame, padx=0)
    doc2_frame = tk.Frame(doc_outer_frame, padx=0)
    doc1 = tk.Text(doc1_frame, height=30, width=50, relief='sunken', bd=1)
    doc2 = tk.Text(doc2_frame, height=30, width=50, relief='sunken', bd=1)

    return doc_outer_frame, doc1_frame, doc1, doc2_frame, doc2


def setup_documents(doc_outer_frame, doc1_frame, doc1, doc2_frame, doc2):
    doc_outer_frame.pack()
    doc1_frame.pack(side='left')
    doc2_frame.pack(side='left')

    doc1_scrollbar = tk.Scrollbar(doc1_frame)
    doc1_scrollbar.pack(side='right', fill='y')
    doc1.pack(side='left', fill='y')
    doc1_scrollbar.config(command=doc1.yview)
    doc1.config(yscrollcommand=doc1_scrollbar.set)

    doc2_scrollbar = tk.Scrollbar(doc2_frame)
    doc2_scrollbar.pack(side='right', fill='y')
    doc2.pack(side='left', fill='y')
    doc2_scrollbar.config(command=doc2.yview)
    doc2.config(yscrollcommand=doc2_scrollbar.set)


setup_app()
