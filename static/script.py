from js import document, console
import json
from pyodide import create_proxy
from pyodide.http import pyfetch
from itertools import count

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
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a fetchData")
    try:
        # response = load_json_file("./api.json")
        response = read_json()
        data = json.dumps(response, indent=2)
        if log: console.log(f"\n\tlog_[{next(x)}]\n{data}")
        return response
    except Exception as error:
        console.log(error)

def pintarCards(data, log=False):
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a pintarCards")
    fragment = document.createDocumentFragment()
    for producto in data:
        if log: console.log(f"\n\tlog_[{next(x)}]\n{str(producto)}")
        ### IMPORTANTE
        templateCard.querySelector('h5').textContent = producto['title']
        templateCard.querySelector('p').textContent = f"${producto['precio']}"
        templateCard.querySelector('img').setAttribute('src', producto['thumbnailUrl'])
        templateCard.querySelector('.btn-dark').dataset.id = producto['id']

        clone = templateCard.cloneNode(True)
        fragment.appendChild(clone)
        ###
    items.appendChild(fragment)

def addCarrito(e, log=False):
    global x
    console.log(f"\n\tlog_[{next(x)}]\nIngresando a addCarrito")
    if log: console.log(f"\n\tlog_[{next(x)}]");console.log(e.target)
    
    ### IMPORTANTE
    if e.target.classList.contains('btn-dark'):
        console.log(f"\n\tlog_[{next(x)}]");console.log(e.target.parentElement)
    e.stopPropagation()

class Carrito:
    pass


def setCarrito(objeto):
    """modificar el objeto Carrito"""
    pass




def main():
    global templateCard, items
    global x
    x = count(1)    
    console.log(f"\n\tlog_[{next(x)}]\nIngresando al main")


    data = fetchData()
    templateCard = document.getElementById('template-card').content
    items = document.getElementById('items')
    
    pintarCards(data)

    items.addEventListener('click', create_proxy(addCarrito))
    # document.addEventListener("DOMContentLoaded", pyodide.create_proxy(fetchData))


main()
