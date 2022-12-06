from js import document, console
import json
import pprint
import pyodide
from pyodide.http import pyfetch


# def load_json_file(path):
#     """ no funciona"""
#     with open(path, 'r') as f:
#         return json.load(f)

def read_json():
    json_data = """
[
    {
        "precio": 500,
        "id": 1,
        "title": "Café",
        "thumbnailUrl": "https://picsum.photos/id/0/600"
        },
    {
        "precio": 300,
        "id": 2,
        "title": "Pizza",
        "thumbnailUrl": "https://picsum.photos/id/10/600"
        },
    {
        "precio": 100,
        "id": 3,
        "title": "Agua",
        "thumbnailUrl": "https://picsum.photos/id/20/600"
        },
    {
        "precio": 50,
        "id": 4,
        "title": "Sandía",
        "thumbnailUrl": "https://picsum.photos/id/30/600"
        },
    {
        "precio": 10,
        "id": 5,
        "title": "Mango",
        "thumbnailUrl": "https://picsum.photos/id/40/600"
        },
    {
        "precio": 150,
        "id": 6,
        "title": "Chela",
        "thumbnailUrl": "https://picsum.photos/id/50/600"
    }
]
"""
    return json.loads(json_data)

def fetchData(log=False):
    console.log("\nIngresando a fetchData")
    try:
        # response = load_json_file("./api.json")
        response = read_json()
        data = json.dumps(response, indent=2)
        if log: console.log(data)
        return response
    except Exception as error:
        console.log(error)

def pintarCards(data, log=False):
    console.log("\nIngresando a pintarCards")
    fragment = document.createDocumentFragment()
    for producto in data:
        if log: console.log(str(producto))
        ### IMPORTANTE
        templateCard.querySelector('h5').textContent = producto['title']
        templateCard.querySelector('p').textContent = f"${producto['precio']}"
        templateCard.querySelector('img').setAttribute('src', producto['thumbnailUrl'])
        clone = templateCard.cloneNode(True)
        fragment.appendChild(clone)
        ###


    items.appendChild(fragment)


def main():
    global templateCard, items
    console.log("\nIngresando al main")
    
    data = fetchData()
    templateCard = document.getElementById('template-card').content
    items = document.getElementById('items')

    pintarCards(data)#TODO
    # document.addEventListener("DOMContentLoaded", pyodide.create_proxy(fetchData))


main()
